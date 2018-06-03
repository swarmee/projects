## Upgrading Elasticsearch from Version 1.X to Version 6.X

### Background
Recently I have been helping out a number of organisations upgrading from elasticsearch V1.X to V6.X. The story is uncannily similar at each organisation. They have been running elasticsearch for the past 4+ years, they originally started off using elasticsearch as a search engine feed by an application database (mostly mysql, but sometimes postgres or Mongo) that is their source of truth. Since then elasticsearch has gradually been leveraged to meet logging and analytic purposes. To a point now where elastic cluster is a core part of the service they provide.  

The only issue is that his elastic cluster is stuck back on V1.X. This has not really been an issue, as elasticsearch 1.X is a pretty feature rich and stable product and cloud providers have been happily provisioning the years. However more recently they have been looking enviously at some of the newer features in elasticsearch. Specifically;
- Improved search speed (everybodies data volumes have increased expotentially over the last 4 years), 
- More feature rich aggregrations (particualry in relation to geo-spatical analysis). 
- Storage savings - i.e. being able to compress source documents and taking advantage of the space savings associate with new lucene data structures.

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

The biggest in index settings to get your head around between V1.X and V6.X relates to text fields (this particuar change actually occured in V5.X). The direct mapping between the data types between the versions is:
- `Analysed strings` in old cluster becomes `text` in new cluster, and
- `Non analysed strings` inold cluster becomes `keywords` in new cluster. 

Lots more is explained in the related elasticsearch [blog](https://www.elastic.co/blog/strings-are-dead-long-live-strings)



### 3. Data Migration Approach

#### 3a. Standard Approach
Elastic recommends two migration paths for moving between V1.X to V6.X. They are described here --> https://www.elastic.co/guide/en/elasticsearch/reference/current/reindex-upgrade.html.

1. Upgrade to 2.4 reindex --> upgrade to 5.6 and reindex --> upgrade to 6.X and reindex. 

2. Create a new 6.x cluster and reindex from remote to import indices directly from the 1.x cluster.

I can not imagine anybody with any significant volume of data in elasticsearch that had reasonably high SLAs would go with option 1. Assuming you setup a secondary cluster and restored your indexes in to it to perform the upgrade, the secondary cluster would need to have enough storage for two versions of all your indexes while you performed the two reindexing processes ($$$). And there would not be a easy way to pull over the new data to the V6.X cluster that had arrived in the V1.X cluster during the migration processes. So this is not really an option for a elastic cluster that is supporting critical business processes. 

Option 2. Sounds much better as you only need to hold one version of the data in your V1.X production cluster and one version in your new V6.X cluster. And it provides a easy easy way to pull over any incremental changes to the V1.X cluster to the V6.X cluster - by running a subsequent reindex of all new things that have happended after the big migration (basically you can drive the reindex process based on a search on the V1.X cluster). 

However there is a little gotta, which is the data you are streaming out of your es V1.X cluster may not be compatible with elasticsearch 6.X. Basically there have been lots of breaking changes between V1.X and V6.X. These include;
- Single mapping `_type` per index. Explained in detail here -->  https://www.elastic.co/guide/en/elasticsearch/reference/master/removal-of-types.html
- Some changes in restrictions in relation to fieldnames. 
- Tighter restrictions on datatypes. 

Many of these issues can be easily worked around using ingest pipeline [processors](https://www.elastic.co/guide/en/elasticsearch/reference/master/ingest-processors.html) to perform actions such as renaming fields, change destination index names (for source indexes with mulitple types) and standarise data types. 

As a quick start to this process I have provided a docker-compose configuration in the folder named `elasticserach-esV1.7.5-and-esV6.2.4`. All you need to do is clone the repo, `cd` into that direction and then run `docker-compose up` (I'm assuming you have docker and docker-compose installed already --> if you don't do a google search for get docker). This will bring up 
- elasticsearch V1.7.4 (http://localhost:9201)
- kibana 4.2 with sense installed (http://localhost:5602/app/sense). 
- elasticsearch V6.2.4 (http://localhost:9200)
- kibana 6.4.2 (http://localhost:5601). 

Once you have booted up these containers its pretty easy to POST some data into the V1.7.5 cluster using the Sense frontend.Then submit a re-indexing request for that data from your V6 cluster using the V6 kibana dev_tools tab. 

Here is an example of POST'ing some data into the V1.X cluster using sense (V4.X kibana). 

_POST /my-index/my-type/1

{
  "report.first": 1,
  "report.last": 1000
}_

Here is a example of a re-indexing request for the data POST'ed in above in dev_tools (V6.X kibana).  


_POST \reindex

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
}_


I should also mention to go with this option your elasticsearch infrastructure provider needs to allow you to set the 'reindex.remote.whitelist' parameters in the elasticsearch.yml on your V6.X cluster (nothing is required to be configured on your V1.X cluster). You can check to see if this paramater has been applied successfully by submitting the below in kibana dev_tools 'GET /_cluster/settings?pretty&include_defaults&filter_path=defaults.reindex'

#### 3b. Alternative Data Migration Approach

However if you are a user of elasticsearch its highly likely that you are  been using elasticsearch f

> _Elasticsearch provides backwards compatibility support that enables indices from the previous major version to be upgraded to the current major version. Skipping a major version means that you must resolve any backward compatibility issues yourself._


### Key Learnings

Obviously, you need to run a test for yourself but in this scenario the storage savings were greater than 40% which translated into a similar reducation in the required monthly software as a service costs. 

upgrade more than paid for itself in two months of storage savings. 
by the upgrade to version 6.0 your milage may vary as a result of differences in data however
