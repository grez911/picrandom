FROM alpine:latest

ENV HOME /root

RUN apk --update upgrade \
  && apk --no-cache --no-progress add python \
  && rm -rf /var/cache/apk/* /tmp/* /var/tmp/*

COPY . /root
WORKDIR /root

CMD python picrandom1.py
