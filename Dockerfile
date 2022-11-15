FROM python:3.9-alpine

ARG BUILD_DATE
# Branch name or tag like "tags/v2.0.3"
ARG BRANCH="master"
ARG EXTRA_PY_DEPS="celery==5.2.7 \
  django-environ==0.9.0 \
  gunicorn==20.1.0 \
  mysqlclient==2.1.1 \
  redis==4.3.4 \
  psycopg[binary]==3.1.4 \
  whitenoise==3.3.1"

ENV APPDIR="/app"
ENV CELERY_REDIS_HOST="redis"
ENV CELERY_REDIS_PORT="6379"
ENV CELERY_LOG_LEVEL="INFO"
ENV GUNICORN_WORKERS="2"

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
    curl \
    git \
    libmagic \
    libxslt-dev \
    mariadb-connector-c-dev &&\
  # Build deps
  apk add --no-cache --virtual .build-deps build-base &&\
  # Clone repo & checkout version
  git clone https://github.com/furlongm/patchman.git "$APPDIR" && \
  git --git-dir "${APPDIR}/.git" checkout $BRANCH -b execbranch &&\
  # Py deps
  pip install --no-cache-dir --no-warn-script-location \
    $EXTRA_PY_DEPS -r "${APPDIR}/requirements.txt" &&\
  # Install Patchman
  ${APPDIR}/setup.py install &&\
  ${APPDIR}/manage.py collectstatic --noinput &&\
  # Remove build deps
  apk del --purge .build-deps

COPY configs/ /
WORKDIR "$APPDIR"

EXPOSE 80
HEALTHCHECK CMD [ "/healthcheck.sh" ] \
  --interval=30s \
  --timeout=10s \
  --start-period=60s \
  --retries=3

ENTRYPOINT ["/entry.sh"]
