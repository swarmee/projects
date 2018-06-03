FROM kibana:4.2.1

USER kibana

COPY ./kibana.yml /opt/kibana/config/kibana.yml

RUN /opt/kibana/bin/kibana plugin --install elastic/sense

USER root

#RUN chmod 777 -R /opt/kibana/

#USER kibana


