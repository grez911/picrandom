FROM python:alpine
RUN adduser -S user
COPY . /home/user
WORKDIR /home/user/tests
RUN /bin/tar xzvf data.tar.gz
RUN /bin/chown user:users -R data
USER user
WORKDIR /home/user
