# country-api

This is a simple python flask api to server up country geo location data based on a supplied country code. Its a standalone app with an in memory data structure it can be started with --> gunicorn3 -b <server ip:port> country-api:app

This type of API can be used in conjunction with the below logstash filter plugin to emblish events with reference data.
https://github.com/lucashenning/logstash-filter-rest

It basically allows you some more flexibility than the tranlate filter (https://github.com/logstash-plugins/logstash-filter-translate)
