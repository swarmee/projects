FROM logstash:2.0

RUN mkdir -p /data/logstash/config

COPY logstash.conf /data/logstash/config

CMD ["-f", "/data/logstash/config/logstash.conf"]
