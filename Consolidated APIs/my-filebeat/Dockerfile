FROM docker.elastic.co/beats/filebeat:6.2.4

COPY ./filebeat.yml /usr/share/filebeat/filebeat.yml
USER root
RUN chmod go-w /usr/share/filebeat/filebeat.yml
RUN chown filebeat /usr/share/filebeat/filebeat.yml
USER filebeat
