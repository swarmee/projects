FROM docker.elastic.co/elasticsearch/elasticsearch-oss:6.3.0

COPY ./elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

COPY ./jvm.options /usr/share/elasticsearch/config/jvm.options

#RUN bin/elasticsearch-plugin install ingest-geoip

#RUN bin/elasticsearch-plugin install ingest-user-agent
