#!/bin/sh

nohup ./sniff-packet.sh > history 2>&1 &

nohup ./raw-data-parser.sh > /dev/null 2>&1 &

#nohup python ./lastfm-scrobler.py > syslog 2>&1 & 
python ./lastfm-scrobler.py
