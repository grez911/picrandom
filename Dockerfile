FROM python:alpine

RUN apk --update upgrade \
  && apk --no-cache --no-progress add py-pip \
  && pip3 install pytest

RUN adduser -S user
COPY . /home/user
WORKDIR /home/user/tests
RUN /bin/tar xzf data.tar.gz
RUN /bin/chown user:users -R data
USER user
WORKDIR /home/user

CMD pytest tests/test_all.py -v --ignore=tests/data/
