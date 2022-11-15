#!/bin/sh

mode=$(cat /tmp/container-mode)
if [ "$mode" = "server" ]; then
    exec curl --fail --silent --write-out 'HTTP CODE : %{http_code}\n' --output /dev/null http://127.0.0.1:80/
elif [ "$mode" = "worker" ]; then
    exec celery -b redis://${CELERY_REDIS_HOST}:${CELERY_REDIS_PORT}/0 inspect ping -j
fi
