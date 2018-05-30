FROM alpine:3.6

# install wget and unzip
RUN apk update && apk add bash wget unzip && rm -rf /var/cache/apk/*

# create logstash data directory
RUN mkdir -p /tmp/geonames/data/
RUN mkdir -p /tmp/openaddresses/data/

# give everybody access
RUN chmod -R 777 /tmp/geonames/*
RUN chmod -R 777 /tmp/openaddresses/*

# Download data
RUN wget -c --output-document=/tmp/geonames/data/cities1000.zip   "http://download.geonames.org/export/dump/cities1000.zip" && unzip /tmp/geonames/data/cities1000.zip -d /tmp/geonames/data/ && chmod -R 777 /tmp/geonames/*

RUN wget --no-check-certificate -c --output-document=/tmp/openaddresses/data/countrywide.zip "https://s3.amazonaws.com/data.openaddresses.io/runs/418554/au/countrywide.zip" && unzip /tmp/openaddresses/data/countrywide.zip

# unzip data - why this does work I don't understand
#RUN unzip /tmp/geonames/data/cities1000.zip -d /tmp/geonames/data/

# give everybody access
#RUN chmod -R 777 /tmp/geonames/*

# use this to keep a temporary container alive for trouble shooting
#ENTRYPOINT ["tail", "-f", "/dev/null"]
