## Upgrading Elasticsearch from Version 1.X to Version 6.X

### Background
Recently I have been helping out a number of small organisations upgrading from elasticsearch V1.X to V6.X. The story is uncannily similar at each organisation. They have been running elasticsearch for the past 4+ years, they originally started off using elasticsearch as a search engine feed by an application database (mostly mysql, but sometimes postgres) that is their source of truth. Since then elasticsearch has gradually been leveraged to meet logging and analytic purposes. To a point where elastic cluster is a core part of the service they provide and is the master of some data within the organisation - particularly data used for analytics.  

The only issue is that their elastic cluster is stuck back on V1.X. This has not really been an issue, as elasticsearch 1.X is a pretty feature rich, stable and cloud providers have got pretty good and managing them over the years.  

However more recently these organisations all seem to be coming to the same conculusion that its time to upgrade these older V1.X clusters. From what I can see its mainly non functional improvements in the core elastic product that are driving the upgrades. Specifically customers want to take advantage of improvements in search speed and savings in relation to storage requirements. Obviously there are lots of functional enhancements that will be able to be taken advantage of after the upgrade, but the rational for the upgrade is generally related to reduced cloud infrastructure requirements (i.e. OPEX savings). As their elastic clusters hold unique data the upgrade requires a data migration. 


### Data Migration Approach

Historically due to infrastructure constraints all organisations pretty much always performed in place upgrades to production systems. However now that (I would say) all small to medium organisations are working in the cloud running up a similar scale production cluster is fast and cheap. For these types of upgrades where we are impacting the primary revenue stream of the organisation the only approach I recommend is running up a concurrent cluster, getting it humming and then cutting over production applications over to it. 

#### Standard Data Migration Approaches
Elastic [recommends](https://www.elastic.co/guide/en/elasticsearch/reference/current/reindex-upgrade.html) two migration paths for moving between V1.X to V6.X.

##### Option 1. Upgrade to 2.4 --> reindex --> upgrade to 5.6 --> reindex --> upgrade to 6.X --> reindex. 

##### Option 2. Create a new 6.x cluster and [reindex](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html) from remote to import indices directly from the 1.x cluster.

Option 1. would involve restoring a backup of the production V1.X cluster into a new V1.X cluster then running through the required upgrades and reindexes. This secondary cluster would need to have double the storage of the original cluster during the two reindexing processes. The biggest issue with this approach is that there is no easy way to pull across the records that are added or updated in the production cluster after the migration started but before the new cluster takes over the role of production. And seeing there are three reindexes as part of this process the amount of time between when the migration started and when it finished could be days.  

Option 2. Sounds much better as you only need to hold one version of the data in your V1.X production cluster and one version in your new V6.X cluster. And it provides an easy way to pull over any incremental changes to the V1.X cluster to the V6.X cluster after the initial migration - by running a subsequent reindex of all new things that have happened after the big migration (basically you can drive the reindex process based on a search on the V1.X cluster). 

However there is a little gotta, which is, the data you are streaming out of your V1.X cluster may not be compatible with elasticsearch 6.X. Basically there have been some breaking changes between V1.X and V6.X. These include;
- Single mapping `_type` per index. Explained in detail [here](https://www.elastic.co/guide/en/elasticsearch/reference/master/removal-of-types.html).  
- Some changes in restrictions in relation to field names. 
- Tighter restrictions on datatypes. 

Many of these issues can be easily worked around using ingest pipeline [processors](https://www.elastic.co/guide/en/elasticsearch/reference/master/ingest-processors.html) to perform actions such as renaming fields, change destination index names (for source indexes with mulitple types) and standarising data types. 

Its important to understand that all the reindexing is doing is moving the data from the old cluster to the new cluster. None of the index settings or mappings are being brought across with the data. So you will need to manually set these before commencing the reindexing process. 

As a kick start to this process I have provided a docker-compose configuration in the folder named `elasticsearch-esV1.7.5-and-esV6.2.4`. All you need to do is clone the repo, `cd` into that direction and then run `docker-compose up` (I'm assuming you have docker and docker-compose installed already --> if you don't do a google search for `get docker`). This will bring up 
- Elasticsearch V1.7.5 (http://localhost:9201)
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

I should also mention that this option requires your elasticsearch provider to allow you to set the 'reindex.remote.whitelist' parameters in the elasticsearch.yml on your V6.X cluster (nothing is required to be configured on your V1.X cluster). 
You can check to see if this parameter has been applied successfully by submitting the below in kibana dev_tools 'GET /_cluster/settings?pretty&include_defaults&filter_path=defaults.reindex'


#### Alternative Data Migration Approach

Reindexing is the prefered approach when the data being migrated does not require any complex transformations. However if more complex transformations (e.g. IF THEN ELSE style transformations) then I have always fallen back to logstash to migrate the data from the old cluster to the new cluster. 

The benefit of using logstash is that it can be packaged up with a template that includes the index \_settings and \_mappings in a container that starts up, applies the template and moves the data across. 

I have provided a sample docker-compose configuration in the folder named `sample-logstash-migrator` which demonstrates this idea. 

I normally create a container for each index to be migrated. You can see that within the repo there is a docker-compose.yml file which builds the logstash container and applies the environment variables to the image (e.g. password, username, source and target elastic urls, etc).  The environment variables are stored in a .env which is generally not stored in git however I have included it for completeness.  

Underneath that there is a sub folder called my-logstash which includes: 
- The dockerfile --> `Dockerfile` - which specifies the version of logstash to use (and any plugins to be installed).
- The logstash configuration --> `logstash.conf` - which has three parts 
	- input  - configuration to pull data from the V1.7 cluster 
    - filter - which performs any required transformations. 
    - output - configuration to push data into the elastic 6.X cluster.
- The elasticsearch index template to be applied --> `mapping.json` . This has the \_mappings as well as the \_settings for the index being created.


### Migration of Cluster Settings

It's often the case of nobody knowing why certain settings have been set for your old V1.X cluster. Rather than trying to work out those historical reasons I highly recommend just going with the vanilla settings in your V6.X cluster and then change things based on testing in the V6.X cluster. Carrying over old settings from V1.X is likely not going to be ideal for the new cluster.

Obviously there are a couple of customer specific settings that need to be set in the new cluster including snapshot data path directories and the breaker settings. I strongly recommend tight breaker settings for any elasticsearch cluster with business Kibana users - cause they can't help themselves from making dashboards with 20 visualizations.

### Migration of Index Settings

The biggest change in index settings to get your head around between V1.X and V6.X relates to text fields (this particular change actually occured in V5.X). The direct mapping between the data types between the versions is:
- `Analysed strings` in old cluster becomes `text` in new cluster, and
- `Non analysed strings` in old cluster becomes `keywords` in new cluster. 

Further details can be found in the related elasticsearch [blog](https://www.elastic.co/blog/strings-are-dead-long-live-strings)

A related change is that fielddata is turned off by default in elasticsearch V5.X+. The only use case where I have found where fielddata to be required in a elasticsearch V6.X cluster was for generating word clouds based on large text fields, in all other cases I have found keyword fields sufficient to meet business requirements. If you can avoid turning fielddata on you should as it will save you JVM heap for other purposes.

### Key Learnings

Here are my key takeaways from what I have learnt performing these migrations: 

- ****Don't**** perform a inplace upgrade on your production cluster. I guarantee that there will be unforeseen impacts as a result of this upgrade. The migration assistant is helpful however don't expect it to identify all possible issues. 

- Storage savings are big between elastic V1.X and V6.X - on each one of the clusters I have migrated I have seen storage savings between 20%-50%. This alone should provide financial justification for the upgrade.  

- If you are using an elasticsearch client library (e.g. elasticsearch-php) ensure you review the compatibility matrix before upgrading. I know it sounds stupid in retrospect. 

- Most of your effort as part of the upgrade is going to be spent reviewing your \_mappings, ensuring you have all your data typed correctly.
