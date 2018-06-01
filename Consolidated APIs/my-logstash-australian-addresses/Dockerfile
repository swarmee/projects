FROM docker.elastic.co/logstash/logstash-oss:6.2.4 

RUN mkdir -p /usr/share/logstash/config

COPY logstash.conf /usr/share/logstash/config

COPY mapping.json /usr/share/logstash/config/

CMD ["-f", "/usr/share/logstash/config/logstash.conf"]


USER root

# install wget and unzip
RUN yum install -y wget unzip 

# create logstash data directory
RUN mkdir -p /tmp/openaddresses/data/


# give everybody access
RUN chmod -R 777 /tmp/openaddresses/*



RUN wget --no-check-certificate -c --output-document=/tmp/openaddresses/data/countrywide.zip "https://s3.amazonaws.com/data.openaddresses.io/runs/418554/au/countrywide.zip" 

RUN unzip /tmp/openaddresses/data/countrywide.zip -d /tmp/openaddresses/data/

RUN chmod -R 777 /tmp/openaddresses/*

USER logstash


