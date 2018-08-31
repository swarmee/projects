FROM docker.elastic.co/elasticsearch/elasticsearch-oss:6.4.0

COPY ./elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

COPY ./jvm.options /usr/share/elasticsearch/config/jvm.options

#COPY ./log4j2.properties /usr/share/elasticsearch/config/log4j2.properties
#RUN bin/elasticsearch-plugin install ingest-geoip
#RUN bin/elasticsearch-plugin install ingest-user-agent
