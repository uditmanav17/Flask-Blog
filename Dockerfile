# FROM alpine:3.12.3
FROM python:3.8-alpine

LABEL maintainer="uditmanav17@gmail.com"

COPY . /src

WORKDIR /src


RUN apk update \
    && apk add py3-pip \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip3 install --no-cache --upgrade pip setuptools \
    && pip3 install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && apk add --update musl-dev gcc libffi-dev \
    && apk update \
    && apk add build-base libzmq musl-dev python3 python3-dev zeromq-dev \
    && pip install Pillow \
    && apk del build-deps

# RUN apk add python3

# RUN apk add py3-pip

# COPY . /src

# WORKDIR /src

# RUN pip3 install --no-cache --upgrade pip setuptools

# needed for bcrypt
# RUN apk add --update musl-dev gcc libffi-dev

# for pyzmq
# RUN apk update && apk add build-base libzmq musl-dev python3 python3-dev zeromq-dev

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["run.py"]


