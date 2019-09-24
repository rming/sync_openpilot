#!/usr/bin/env bash

while true; do
    ms=`date +%M%S`
    if [[ "${ms}" == "0000" ]] || [[ "${ms}" == "3000" ]]; then
        dateTime=`date  +"%Y-%m-%d %H:%M:%S"`
        echo "run command at ${dateTime}"
        /usr/bin/python /root/git/sync_openpilot/SyncOpenpilot.py > /root/git/sync_openpilot/syncopenpilot.log 2>&1
    fi
    sleep 1
done
