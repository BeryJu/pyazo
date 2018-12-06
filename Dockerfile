FROM python:3.6-alpine
ARG REQUIREMENTS=requirements.txt
LABEL version="1.8.8"

COPY ${REQUIREMENTS} /
RUN apk update && \
    apk add --no-cache openssl-dev libffi-dev libmagic libffi-dev build-base py2-pip python2-dev jpeg libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev && \
    pip install -r /${REQUIREMENTS} && \
    apk del openssl-dev libffi-dev libffi-dev build-base py2-pip python2-dev libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl jpeg-dev zlib-dev freetype-dev lcms2-dev tk-dev tcl-dev && \
    adduser -S pyazo

USER pyazo

COPY ./allauth_supervisr/ /app/allauth_supervisr/
COPY ./pyazo/ /app/pyazo
COPY ./static/ /app/static
COPY ./manage.py /app/
WORKDIR /app/
