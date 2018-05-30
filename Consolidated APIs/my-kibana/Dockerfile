FROM docker.elastic.co/kibana/kibana-oss:6.2.4

COPY ./kibana.yml /usr/share/kibana/config/kibana.yml

USER root
RUN mkdir -p /var/log/kibana && chmod 777 /var/log/kibana
USER kibana

