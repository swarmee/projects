## Upgrading To the Current Version of Elasticsearch from Version 1.X


One of my friends Ben (hey Ben) has been running elasticserch for the past 4 years, he originally started off using it as a search engine feed by his mysql database (source of truth). However like most people with an elastic cluster it has graduately be leveraged to meet logging and analytic purposes over the past few years. Basically his elastic cluster is a core part of his business. 

The only issue is that his elastic cluster is stuck back on version 1.7.5. This has not really been an issue, as elasticsearch 1.X is a pretty feature rich and stable product. 

However more recently he has been looking evisious at some of the newer features in elasticsearch. Specifically;
- Better geo-spatical aggregrations. 
- Pipeline aggregations
- 

But most importantly as his business has grown his data holdings have also grown which has made his monthly hosting charged grow. 



but also storage savings (paricualary for his main search index which has lots of small nested documents. 


- and during. During that time it has been working for him very well as a search engine.

Originally it was just providing him a search engine, however over time he has started to use it for logging as business analytics. 


The only problem was that His only problem is that 




###

Migration Approach 

Elastic recommends two migration paths for moving between V1.X to V6.X. They are;
https://www.elastic.co/guide/en/elasticsearch/reference/current/reindex-upgrade.html.

1. Upgrade to 2.4 reindex --> upgrade to 5.6 and reindex --> upgrade to 6.X and reindex. 

2. Create a new 6.x cluster and reindex from remote to import indices directly from the 1.x cluster.

I can imagine anybody anywhere with any significant volume of data in elasticsearch would go with option 1. as the outage period would just be to long leaving aside what would happen if you had an issue part way through this migration (assumming you changed your application code to work with elasticsearch version 6 only).The second option sounds pretty good. 

The approach that Ben and I have taken







