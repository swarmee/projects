FROM docker.elastic.co/logstash/logstash-oss:6.1.0

RUN logstash-plugin install logstash-filter-rest

RUN mkdir -p /usr/share/logstash/config

COPY logstash.conf /usr/share/logstash/config

COPY mapping.json /usr/share/logstash/config

USER root
# install wget and unzip
RUN yum install -y wget gzip curl

# create logstash data directory
RUN mkdir -p /tmp/icij/data/

# give everybody access
RUN chmod -R 777 /tmp/icij/*

# Download data
RUN wget -c --output-document=/tmp/icij/data/data.csv.gz "https://www.dropbox.com/s/bcnckrkf6k5msm3/offshore_leaks.nodes.address.csv.gz?dl=0"

RUN gunzip /tmp/icij/data/data.csv.gz 

RUN chmod -R 777 /tmp/icij/*

USER logstash 

CMD ["-f", "/usr/share/logstash/config/logstash.conf"]
