FROM docker.elastic.co/elasticsearch/elasticsearch-oss:6.2.3

RUN bin/elasticsearch-plugin install https://github.com/spinscale/elasticsearch-ingest-opennlp/releases/download/6.2.3.1/ingest-opennlp-6.2.3.1.zip

COPY ./en-ner-organization.bin /usr/share/elasticsearch/config/ingest-opennlp 

