FROM docker.elastic.co/logstash/logstash-oss:6.2.4 

RUN mkdir -p /usr/share/logstash/config

COPY logstash.conf /usr/share/logstash/config

COPY mapping.json /usr/share/logstash/config/

CMD ["-f", "/usr/share/logstash/config/logstash.conf"]

USER root
# install wget and unzip
RUN yum install -y wget unzip

# create logstash data directory
RUN mkdir -p /tmp/geonames/data/

# give everybody access
RUN chmod -R 777 /tmp/geonames/*

# Download data
RUN wget -c --output-document=/tmp/geonames/data/cities1000.zip   "http://download.geonames.org/export/dump/cities1000.zip" && unzip /tmp/geonames/data/cities1000.zip -d /tmp/geonames/data/ && chmod -R 777 /tmp/geonames/*

USER logstash 


