FROM alpine:3.7

WORKDIR /tmp
RUN apk add --no-cache --virtual .build-deps build-base python3-dev \
      && apk add --no-cache libev python3 py3-pip \
      && pip3 install --no-cache-dir gevent pedis \
      && apk del .build-deps
EXPOSE 63790
VOLUME /var/lib/pedis
ENTRYPOINT ["pedis.py", "-l", "/var/lib/pedis/server.log", "-H", "0.0.0.0"]