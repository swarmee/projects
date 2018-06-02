## Upgrading To a Current Version of Elasticsearch from Version 1.X

### Background
One of my friends Ben (hey Ben) has been running elasticserch for the past 4 years, he originally started off using it as a search engine feed by his mysql database (source of truth). However like most people with an elastic cluster it has graduately be leveraged to meet logging and analytic purposes over the past few years. Basically his elastic cluster is a core part of his business. 

The only issue is that his elastic cluster is stuck back on version 1.7.5. This has not really been an issue at all until recently, as elasticsearch 1.X is a pretty feature rich and stable product. 

However more recently Ben has been looking enviously at some of the newer features in elasticsearch. Specifically;
- Improved search speed, 
- More feature rich aggregrations (particualry in relation to geo-spatical analysis). 
- Storage savings - i.e. being able to compress source documents and taking advantage of the space savings associate with sparsely populated.

I should also note that his elasticsearch cloud provider had let him know that elasticsearch 1.X was a legacy product for them as well - so he probably better start thinking about an upgrade.  

## Migration Approach

Elastic recommends two migration paths for moving between V1.X to V6.X. They are described here --> https://www.elastic.co/guide/en/elasticsearch/reference/current/reindex-upgrade.html.

1. Upgrade to 2.4 reindex --> upgrade to 5.6 and reindex --> upgrade to 6.X and reindex. 

2. Create a new 6.x cluster and reindex from remote to import indices directly from the 1.x cluster.

I can not imagine anybody with any significant volume of data in elasticsearch that had reasonably high SLAs would go with option 1. Assuming you setup a secondary cluster and restored your indexes in to it to perform the upgrade, the secondary cluster would need to have enough storage for two versions of all your indexes while you performed the two reindexing processes ($$$). And there would not be a easy way to pull over the new data to the V6.X cluster that had arrived in the V1.X cluster during the migration processes. So this is not really an option for a elastic cluster that is supporting critical business processes. 

Option 2. Sounds much better as you only need to hold one version of the data in your V1.X production cluster and one version in your new V6.X cluster. And it provides a easy easy way to pull over any incremental changes to the V1.X cluster to the V6.X cluster - by running a subsequent reindex of all new things that have happended after the big migration (basically you can drive the reindex process based on a search). 

The only thing is that when moving from 

you would need to hold two versions of the data

for the upgrade you would nAs it would be impossible to migrate the majority of the data in one hit and then move 


.The second option sounds pretty good. 

The approach that Ben and I have taken











But most importantly as his business has grown his data holdings have also grown which has made his monthly hosting charged grow. 

ability to compress _source_ documents in elasticsearch 2.0



but also storage savings (paricualary for his main search index which has lots of small nested documents. 


- and during. During that time it has been working for him very well as a search engine.

Originally it was just providing him a search engine, however over time he has started to use it for logging as business analytics. 


The only problem was that His only problem is that 




###
