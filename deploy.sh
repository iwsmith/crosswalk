#!/bin/bash

set -e

if [[ -z $1 ]]; then
    echo "Usage: $(basename $0) <host>" >&2
    exit 1
fi

DEPLOY_HOST="$1"
DEPLOY_USER="${DEPLOY_USER:-pi}"

echo "Copying code to ${DEPLOY_HOST}"
rsync -rz --progress *.py config.yml static templates xwalk "${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/crosswalk"

echo "Synchronizing deployed code"
ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "sudo rsync -r /tmp/crosswalk/ /srv/crosswalk/code/"

echo "Restarting crosswalk service"
ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "sudo systemctl restart crosswalk"
