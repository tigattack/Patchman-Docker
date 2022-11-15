FROM python:3.9-alpine

ARG BUILD_DATE
# Branch name or tag like "tags/v2.0.3"
ARG BRANCH="master"
ENV APPDIR="/app"
ARG EXTRA_PY_DEPS="celery==5.2.7 \
  django-environ==0.9.0 \
  gunicorn==20.1.0 \
  mysqlclient==2.1.1 \
  redis==4.3.4 \
  psycopg[binary]==3.1.4 \
  whitenoise==3.3.1"

LABEL org.opencontainers.image.authors="tigattack"
LABEL org.opencontainers.image.title="Patchman"
LABEL org.opencontainers.image.description="Alpine-based Patchman container image."
LABEL org.opencontainers.image.url="https://github.com/furlongm/patchman"
LABEL org.opencontainers.image.documentation="https://github.com/tigattack/Patchman-Docker/blob/main/README.md"
LABEL org.opencontainers.image.source="https://github.com/tigattack/Patchman-Docker"
LABEL org.opencontainers.image.version=$BRANCH
LABEL org.opencontainers.image.created=$BUILD_DATE

RUN \
  # Required deps
  apk --no-cache add \
    git \
    libmagic \
    libxslt-dev \
    mariadb-connector-c-dev &&\
  # Clone repo & checkout version
  git clone https://github.com/furlongm/patchman.git "$APPDIR" && \
  git --git-dir "${APPDIR}/.git" checkout $BRANCH -b execbranch

ADD configs/ /

WORKDIR "$APPDIR"

RUN \
  # Build deps
  apk add --no-cache --virtual .build-deps build-base &&\
  # Py deps
  pip install --no-cache-dir --no-warn-script-location \
    $EXTRA_PY_DEPS -r "${APPDIR}/requirements.txt" &&\
  # Remove build deps
  apk del --purge .build-deps

ADD entry.sh /entry.sh
RUN chmod 755 /entry.sh

EXPOSE 80

ENTRYPOINT ["/entry.sh"]
