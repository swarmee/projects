FROM alpine:3.6

RUN apk add --update bash && \
    rm -rf /var/cache/apk/*

RUN apk add --update curl && \
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/usr/bin/curl"]
