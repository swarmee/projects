## Upgrading Elasticsearch from Version 1.X to Version 6.X

### Background
Recently I have been helping out a number of organisations upgrading from elasticsearch V1.X to V6.X. The story is uncannily similar at each organisation. They have been running elasticsearch for the past 4+ years, they originally started off using elasticsearch as a search engine feed by an application database (mostly mysql, but sometimes postgres or Mongo) that is their source of truth. Since then elasticsearch has gradually been leveraged to meet logging and analytic purposes. To a point now where elastic cluster is a core part of the service they provide.  

The only issue is that there elastic cluster is stuck back on V1.X. This has not really been an issue, as elasticsearch 1.X is a pretty feature rich and stable product and cloud providers have been happily provisioning them for years. 

However more recently these organisations all seem to be coming to the same conculusion that its time to upgrade these older V1.X clusters. From what I can see its mainly non functional improvements in the core elastic product that are driving the upgrades. Specifically customers want to take advantage of improvements in search speed and savings in relation to storage requirements. Obviously there are lots of functional enhancements that will be able to be taken advantage of after the upgrade, but the rational for the upgrade is generally related to reduced cloud infrastructure requirements (i.e. OPEX savings). 




And cloud elasticsearch provides are activity telling customers that elasticsearch 1.X is a legacy  legacy - so he probably better start thinking about an upgrade.  


### Upgrade Summary

To perform any elasticsearch upgrade there are three main tasks;
1. Review and update of cluster settings. 
2. Review and update of index settings, including \_mappings, \_settings and any custom \_analysis.
3. Migration of data / Cutover to new cluster

Most concern is directed towards the migration of data and the cutover to the new cluster. However this ends up being pretty easy. Most of the effort is required to review and update index settings as lots has changed in this area. 


### 1. Migration of Cluster Settings

Reviewing old cluster settings is probably the most important step in the upgrade. Its ideal to go back to the vanilla settings in your V6.X cluser then just change things as needed. Carrying over old settings from V1.X is likely not going to be ideal for the new cluster as pretty much everything has changed. I would recommend that you run some tests with vanilla V6.X settings before jumping in an change node or cluster settings.

Obviously there are a couple of important settings that need to be set in the new cluster including snapshot data path directories and the breaker settings. I strongly recommend tight breaker settings for any elasticsearch cluster with business Kibana users - cause they can't help themselves from making dashboards with 20 visulidations. 

### 2. Migration of Index Settings

The biggest change in index settings to get your head around between V1.X and V6.X relates to text fields (this particuar change actually occured in V5.X). The direct mapping between the data types between the versions is:
- `Analysed strings` in old cluster becomes `text` in new cluster, and
- `Non analysed strings` in old cluster becomes `keywords` in new cluster. 
Lots more is explained in the related elasticsearch [blog](https://www.elastic.co/blog/strings-are-dead-long-live-strings)
A related change is that fielddata is turned off by default in elasticsearch V5.X+. The only use case where I have found fielddata to be required in a elasticsearch V6.X cluster was for generating word clouds based on large text fields, in all other cases I have found keyword fields sufficient to meet business requirements. Similar if you can avoid turning fielddata on you should as it will save you JVM heap for other purposes.  


### 3. Data Migration Approach

#### 3a. Standard Approach
Elastic recommends two migration paths for moving between V1.X to V6.X. They are described here --> https://www.elastic.co/guide/en/elasticsearch/reference/current/reindex-upgrade.html.

1. Upgrade to 2.4 reindex --> upgrade to 5.6 and reindex --> upgrade to 6.X and reindex. 

2. Create a new 6.x cluster and [reindex](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html) from remote to import indices directly from the 1.x cluster.

I can not imagine anybody with any significant volume of data in elasticsearch that had reasonably high SLAs would go with option 1. Assuming you setup a secondary cluster and restored your indexes in to it to perform the upgrade, the secondary cluster would need to have enough storage for two versions of all your indexes while you performed the two reindexing processes ($$$). And there would not be a easy way to pull over the new data to the V6.X cluster that had arrived in the V1.X cluster during the migration processes. So this is not really an option for a elastic cluster that is supporting critical business processes. 

Option 2. Sounds much better as you only need to hold one version of the data in your V1.X production cluster and one version in your new V6.X cluster. And it provides a easy easy way to pull over any incremental changes to the V1.X cluster to the V6.X cluster - by running a subsequent reindex of all new things that have happended after the big migration (basically you can drive the reindex process based on a search on the V1.X cluster). 

However there is a little gotta, which is the data you are streaming out of your es V1.X cluster may not be compatible with elasticsearch 6.X. Basically there have been lots of breaking changes between V1.X and V6.X. These include;
- Single mapping `_type` per index. Explained in detail here -->  https://www.elastic.co/guide/en/elasticsearch/reference/master/removal-of-types.html
- Some changes in restrictions in relation to fieldnames. 
- Tighter restrictions on datatypes. 

Many of these issues can be easily worked around using ingest pipeline [processors](https://www.elastic.co/guide/en/elasticsearch/reference/master/ingest-processors.html) to perform actions such as renaming fields, change destination index names (for source indexes with mulitple types) and standarise data types. 

Its important to understand that all the reindexing is doing is moving the data from the old cluster to the new cluster. None of the index settings or mappings are being brought across with the data. So you will need to manually set these before commencing the reindexing process. 

As a quick start to this process I have provided a docker-compose configuration in the folder named `elasticsearch-esV1.7.5-and-esV6.2.4`. All you need to do is clone the repo, `cd` into that direction and then run `docker-compose up` (I'm assuming you have docker and docker-compose installed already --> if you don't do a google search for get docker). This will bring up 
- Elasticsearch V1.7.4 (http://localhost:9201)
- Kibana 4.2 with sense installed (http://localhost:5602/app/sense). 
- Elasticsearch V6.2.4 (http://localhost:9200)
- Kibana 6.4.2 (http://localhost:5601). 

Once you have booted up these containers its pretty easy to POST some data into the V1.7.5 cluster using the Sense frontend.Then submit a re-indexing request for that data from your V6 cluster using the V6 kibana dev_tools tab. 

Here is an example of POST'ing some data into the V1.X cluster using sense (V4.X kibana). 

POST /my-index/my-type/1

{
  "report.first": 1,
  "report.last": 1000
}

Here is a example of a re-indexing request for the data POST'ed in above in dev_tools (V6.X kibana).  


POST \_reindex

{
  "source": {
    "remote": {
      "host": "http://elasticsearchv1.7.5:9200"
    },
    "index": "my-index",
    "query": {
      "matchall": {}
    }
  },
  "dest": {
    "index": "my-index"
  }
}

I should also mention to go with this option your elasticsearch infrastructure provider needs to allow you to set the 'reindex.remote.whitelist' parameters in the elasticsearch.yml on your V6.X cluster (nothing is required to be configured on your V1.X cluster). 
You can check to see if this paramater has been applied successfully by submitting the below in kibana dev_tools 'GET /_cluster/settings?pretty&include_defaults&filter_path=defaults.reindex'

#### 3b. Alternative Data Migration Approach

Reindexing is the prefered approach when the data being migrated does not require any complex transformations. However if more complex transformations (e.g. IF THEN ELSE style transformations) then I have always fallen back to logstash to migrate the data from the old cluster to the new cluster. 

The benefit of using logstash is that it can be packaged up with a template that includes the index \_settings and \_mappings in a container that starts up applies the template and moves the data across. 

I have provided a sample docker-compose configuration in the folder named `sample-logstash-migrator` which demonstrates this idea. 

I normally create a container for each index to be migrated. You can see that within the repo there is a docker-compose.yml file which does nothing apart from build the docker logstash image and apply the environment variables to the image (e.g. password, username, source and target elastic urls, etc). You could do the same with a long docker run command. 

The environment variables are stored in a .env which is generally not stored in git however I have included it for completeness of understanding. 

Underneath that there is a sub folder called my-logstash which includes: 
- The dockerfile - which specifies the version of logstash to use (and any plugins to be installed).
- The logstash configuration - which has three parts A. input - configuration to pull data from the V1.7 cluster B. filter - which performs any required transformations. C. output - configuration to push data into the elastic 6.X cluster.
- The elasticsearch index template to be applied. This has the \_mappings as well as the \_settings for the index being created.


### Key Learnings

Obviously, you need to run a test for yourself but in this scenario the storage savings were greater than 40% which translated into a similar reducation in the required monthly software as a service costs. 

upgrade more than paid for itself in two months of storage savings. 
by the upgrade to version 6.0 your milage may vary as a result of differences in data however

will be provided as part of the upgrade but being able to reduce your storage footprint by greater than 30% 

its a combination of new features in 

more recently they have been looking enviously at some of the newer features in elasticsearch. Specifically;
- Improved search speed (everybodies data volumes have increased exponentially over the last 4 years), 
- More feature rich aggregations (particularly in relation to geospatial analysis). 
- Storage savings - i.e. being able to compress source documents and taking advantage of the space savings associate with new lucene data structures.
