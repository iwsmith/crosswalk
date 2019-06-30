#!/bin/bash

set -e

if [[ -z $1 ]]; then
    echo "Usage: $(basename $0) <host>" >&2
    exit 1
fi

DEPLOY_HOST="$1"
DEPLOY_USER="${DEPLOY_USER:-pi}"

ssh_sudo() {
    ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "sudo $@"
}

echo "Copying code to ${DEPLOY_HOST}"
rsync -rz --progress *.py config.yml static templates xwalk "${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/crosswalk"

echo "Synchronizing deployed code"
ssh_sudo rsync -r /tmp/crosswalk/ /srv/crosswalk/code/

echo "Restarting crosswalk and button service"
ssh_sudo systemctl restart button
ssh_sudo systemctl restart crosswalk
