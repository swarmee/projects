FROM elasticsearch:1.7.4
#FROM alpine:latest
#RUN apk add --no-cache openjdk8 curl tar

#FROM openjdk:8

#RUN apt-get update && apt-get install -y curl tar

#RUN apk --no-cache add curl tar

#RUN apk --no-cache add curl tar default-jre

#RUN mkdir /app10

#WORKDIR /app10

#RUN curl -L -O https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.4.tar.gz
#RUN mkdir -p /opt
#RUN tar -xvf elasticsearch-1.7.4.tar.gz -C /opt

#RUN chmod +x /opt/elasticsearch-1.7.4/bin/elasticsearch

#CMD ["/opt/elasticsearch-1.7.4/bin/elasticsearch --cluster.name swarmee --node.name swarmee1"]

#ENTRYPOINT ["./elasticsearch-1.7.4/bin"]
#RUN chmod 777 /app10/elasticsearch-1.7.4/bin/elasticsearch
#USER root

# configure
#ADD supervisord.conf /etc/supervisor/conf.d/elasticsearch.conf

# startup
#ADD elasticsearch.sh /start.d/10-elasticsearch
