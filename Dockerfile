FROM alpine:3.7
MAINTAINER Nicholas Willhite (willnx84@gmail.com)

RUN apk update && apk upgrade
RUN apk add python3 python3-dev openssl openssl-dev gcc \
            linux-headers libc-dev libffi-dev pcre pcre-dev
COPY dist/*.whl /tmp

RUN pip3 install /tmp/*.whl && rm /tmp/*.whl
RUN apk del gcc
WORKDIR /usr/lib/python3.6/site-packages/vlab_inventory_api
CMD uwsgi --ini ./app.ini
