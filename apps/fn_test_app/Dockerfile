# Generated with resilient-sdk v51.0.7.2.16540
# docker build -t fn_test_app:1.2.0 .
ARG BASE_IMAGE_REPO=quay.io
# BASE_IMAGE_TAG options: latest, python-311, python-312. See https://quay.io/repository/ibmresilient/soarapps-base-docker-image?tab=tags for all options
# use --build-arg BASE_IMAGE_TAG=<tag> to set base image to be built from
ARG BASE_IMAGE_TAG=latest

FROM ${BASE_IMAGE_REPO}/ibmresilient/soarapps-base-docker-image:${BASE_IMAGE_TAG}

ARG APPLICATION=fn_test_app

COPY ./dist /tmp/packages
USER 0
RUN yum -y update && yum clean all
RUN set -eux; \
    ls -l /tmp/packages/${APPLICATION}-*.tar.gz; \
    /usr/bin/python3.12 -m pip --python /opt/app-root/bin/python3 install /tmp/packages/${APPLICATION}-*.tar.gz
USER 1001
