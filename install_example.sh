#!/usr/bin/env bash

set -x

function install_config() {
    rm -f "$2"
    ln -s "$1" "$2"
}

install_config "${PWD}/bauchan.config.example.json" ~/.bauchan.config.json
NATIVE_MESSAGING_HOSTS_DIR="~/Library/Application\ Support/Mozilla/NativeMessagingHosts"
if [[ ! -d "${NATIVE_MESSAGING_HOSTS_DIR}" ]]
then
    mkdir "${NATIVE_MESSAGING_HOSTS_DIR}"
fi
cp -f "${PWD}/bauchan.json" "${NATIVE_MESSAGING_HOSTS_DIR}/bauchan.json"
