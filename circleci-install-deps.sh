#!/usr/bin/env bash

set -e

sudo add-apt-repository ppa:beineri/opt-qt542-trusty -y
sudo apt-get update -y; true

sudo apt-get clean

CHECKSUM="$(sha256sum $0)"

CACHE_DIR=pkgcache
CHECKSUM_FILE=$CACHE_DIR/installer-checksum.txt

if [[ -s $CHECKSUM_FILE ]] && [[ "CHECKSUM" -eq "$(cat $CHECKSUM_FILE)" ]]; then
    echo "Package cache up to date, no need to download."
else
    echo "Downloading packages..."

    sudo aptitude --download-only install -y qt54webkit libwebkit-dev libgstreamer0.10-dev
    sudo aptitude --download-only install -y arduino arduino-mk

    mkdir -p $CACHE_DIR
    cp /var/cache/apt/archives/*.deb $CACHE_DIR

    echo "$CHECKSUM" > $CHECKSUM_FILE
fi

echo "installing packages..."
sudo dpkg -i $CACHE_DIR/*.deb

echo "/opt/qt54/bin/qt54-env.sh" >> ~/.circlerc
