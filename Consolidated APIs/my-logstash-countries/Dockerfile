FROM docker.elastic.co/logstash/logstash-oss:6.2.4 

RUN mkdir -p /usr/share/logstash/config

COPY logstash.conf /usr/share/logstash/config

COPY mapping.json /usr/share/logstash/config/

USER root
# install wget and unzip
RUN yum install -y bash 

#wget 

#RUN mkdir -p     /tmp/restcountries/data/
#RUN mkdir -p 777 /tmp/restcountries/*
#RUN wget --no-check-certificate -c --output-document=/tmp/restcountries/data/countries.json "https://restcountries.eu/rest/v2/all"


#RUN wget --no-check-certificate -c --output-document=/usr/share/jq "https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64"  

#RUN chmod +x /usr/share/jq
#USER logstash

CMD ["-f", "/usr/share/logstash/config/logstash.conf"]
