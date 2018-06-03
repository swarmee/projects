## Upgrading To a Current Version of Elasticsearch from Version 1.X

### Background
One of my friends Ben (hey Ben) has been running elasticserch for the past 4 years, he originally started off using it as a search engine feed by his mysql database (source of truth). However like most people with an elastic cluster it has graduately be leveraged to meet logging and analytic purposes over the past few years. Basically his elastic cluster is a core part of his business. 

The only issue is that his elastic cluster is stuck back on version 1.7.5. This has not really been an issue at all until recently, as elasticsearch 1.X is a pretty feature rich and stable product. 

However more recently Ben has been looking enviously at some of the newer features in elasticsearch. Specifically;
- Improved search speed, 
- More feature rich aggregrations (particualry in relation to geo-spatical analysis). 
- Storage savings - i.e. being able to compress source documents and taking advantage of the space savings associate with sparsely populated.

I should also note that his elasticsearch cloud provider had let him know that elasticsearch 1.X was a legacy product for them as well - so he probably better start thinking about an upgrade.  

## Standard Migration Approach

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
      "match_all": {}
    }
  },
  "dest": {
    "index": "my-index"
  }
} 



I should also mention to go with this option your elasticsearch infrastructure provider needs to allow you to set the 'reindex.remote.whitelist' parameters in the elasticsearch.yml on your V6.X cluster (nothing is required to be configured on your V1.X cluster). You can check to see if this paramater has been applied successfully by submitting the below in kibana dev_tools 'GET /_cluster/settings?pretty&include_defaults&filter_path=defaults.reindex'

## Alternative Migration Approach

However if you are a user of elasticsearch its highly likely that you are  been using elasticsearch f

> _Elasticsearch provides backwards compatibility support that enables indices from the previous major version to be upgraded to the current major version. Skipping a major version means that you must resolve any backward compatibility issues yourself._



 

The approach that Ben and I have taken


## Test Environment 

Before you start your 

POST _reindex
{
  "source": {
    "remote": {
      "host": "http://elasticsearch9:9200"
    },
    "index": "source",
    "query": {
      "match_all": {}
    }
  },
  "dest": {
    "index": "source"
  }
}










But most importantly as his business has grown his data holdings have also grown which has made his monthly hosting charged grow. 

ability to compress _source_ documents in elasticsearch 2.0



but also storage savings (paricualary for his main search index which has lots of small nested documents. 


- and during. During that time it has been working for him very well as a search engine.

Originally it was just providing him a search engine, however over time he has started to use it for logging as business analytics. 


The only problem was that His only problem is that 




### Key Learnings

Obviously, you need to run a test for yourself but in this scenario the storage savings were greater than 40% which translated into a similar reducation in the required monthly software as a service costs. 

upgrade more than paid for itself in two months of storage savings. 
by the upgrade to version 6.0 your milage may vary as a result of differences in data however
