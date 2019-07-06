#!/bin/bash

set -e

if [[ -z $1 ]]; then
    echo "Usage: $(basename $0) <host> [--config] [--code] [--media]" >&2
    exit 1
fi

DEPLOY_HOST="$1"
DEPLOY_USER="${DEPLOY_USER:-pi}"
DEPLOY_DIR=/srv/crosswalk/code

DEPLOY_DEST="${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_DIR}"

ssh_sudo() {
    ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "sudo $@"
}

echo "Switching permissions during deploy..."
ssh_sudo chown -R $DEPLOY_USER $DEPLOY_DIR

shift
if [[ $# -eq 0 ]]; then
    SYNC_CONFIG=1
    SYNC_CODE=1
    SYNC_MEDIA=1
else
    for opt in $@; do
        case $opt in
            --config) SYNC_CONFIG=1 ;;
            --code)   SYNC_CODE=1   ;;
            --media)  SYNC_MEDIA=1  ;;
            *)
                echo "Unknown option: $opt" >&2
                exit 1
        esac
    done
fi

if [[ $SYNC_CONFIG ]]; then
    echo "Copying config to ${DEPLOY_HOST}"
    scp config.yml $DEPLOY_DEST/config.yml
fi

if [[ $SYNC_CODE ]]; then
    echo "Copying code to ${DEPLOY_HOST}"
    rsync -rz --delete xwalk templates config.yml run.py button.py $DEPLOY_DEST
fi

if [[ $SYNC_MEDIA ]]; then
    echo "Copying media to ${DEPLOY_HOST}"
    rsync -rz --progress --delete static/ $DEPLOY_DEST/static/
fi

echo "Resetting permissions..."
ssh_sudo chown -R crosswalk:crosswalk $DEPLOY_DIR

echo "Restarting crosswalk and button service"
ssh_sudo systemctl restart button
ssh_sudo systemctl restart crosswalk
