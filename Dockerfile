FROM python:3.14-alpine

# renovate: datasource=github-tags depName=furlongm/patchman
ARG PATCHMAN_VERSION="v4.0.7"

ENV APPDIR="/app"
ENV CELERY_REDIS_HOST="redis"
ENV CELERY_REDIS_PORT="6379"
ENV CELERY_LOG_LEVEL="INFO"
ENV GUNICORN_WORKERS="2"

WORKDIR "$APPDIR"

COPY requirements.txt /requirements-source.txt

RUN \
  # Required deps
  apk --no-cache add \
    curl \
    git \
    libmagic \
    libxslt-dev \
    mariadb-connector-c-dev &&\
  # Clone repo, checkout version, and enter directory
  git clone https://github.com/furlongm/patchman.git . && \
  git checkout tags/$PATCHMAN_VERSION -b execbranch &&\
  # Build deps
  apk add --no-cache --virtual .build-deps build-base &&\
  mv /requirements-source.txt ./ &&\
  # Py deps
  pip install \
    --no-cache-dir \
    --no-warn-script-location \
    -r requirements-source.txt \
    -r requirements.txt &&\
  # Install Patchman
  ./setup.py install &&\
  # Remove build deps
  apk del --purge .build-deps

COPY configs/ /

EXPOSE 80
HEALTHCHECK \
  --interval=20s \
  --timeout=10s \
  --start-period=60s \
  --retries=5 \
  CMD [ "/healthcheck.sh" ]

ENTRYPOINT ["/entry.sh"]
