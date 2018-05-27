FROM docker.elastic.co/logstash/logstash-oss:6.2.4 

RUN mkdir -p /usr/share/logstash/config

COPY logstash.conf /usr/share/logstash/config

COPY mapping.json /usr/share/logstash/config/

CMD ["-f", "/usr/share/logstash/config/logstash.conf"]
