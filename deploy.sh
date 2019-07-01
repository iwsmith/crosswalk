#!/bin/bash

set -e

if [[ -z $1 ]]; then
    echo "Usage: $(basename $0) <host> [--media]" >&2
    exit 1
fi

DEPLOY_HOST="$1"
DEPLOY_USER="${DEPLOY_USER:-pi}"

ssh_sudo() {
    ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "sudo $@"
}

echo "Copying code to ${DEPLOY_HOST}"
rsync -rz --progress --delete xwalk templates config.yml run.py button.py "${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/crosswalk"

if [[ $1 = --media ]]; then
    echo "Copying media to ${DEPLOY_HOST}"
    rsync -rz --progress --delete static "${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/crosswalk"
fi

echo "Synchronizing deployed code"
ssh_sudo rsync -r /tmp/crosswalk/ /srv/crosswalk/code/
ssh_sudo chown -R crosswalk:crosswalk /srv/crosswalk/code

echo "Restarting crosswalk and button service"
ssh_sudo systemctl restart button
ssh_sudo systemctl restart crosswalk
