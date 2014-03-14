#!/bin/sh

nohup ./sniff-packet.sh > history 2>&1 &
nohup ./sniff-packet-fav.sh >> history 2>&1 &

nohup ./raw-data-parser.sh > /dev/null 2>&1 &
#nohup python ./lastfm-scrobler.py > syslog 2>&1 & 

python ./lastfm-scrobler.py

ps aux | grep raw-data-parse.sh | grep -v grep | awk '{print $2}' | xargs kill -9
ps aux | grep "python ./lastfm-scrobler.py"  | grep -v grep | awk '{print $2}' | xargs kill -9
ps aux | grep "tail -n 200 -f history"  | grep -v grep | awk '{print $2}' | xargs kill -9
ps aux | grep "ngrep -l -M -q -d en0 -Wbyline method=Playlog.add" | grep -v "grep ngrep -l -M -q -d en0 -Wbyline method=Playlog.add" | awk '{print $2}' | xargs kill -9
ps aux | grep "ngrep -l -M -q -d en1 -Wbyline method=Playlog.add" | grep -v "grep ngrep -l -M -q -d en1 -Wbyline method=Playlog.add" | awk '{print $2}' | xargs kill -9

ps aux | grep "ngrep -l -M -q -d en0 -Wbyline method=Library.addSong" | grep -v "grep ngrep -l -M -q -d en0 -Wbyline method=Library.addSong" | awk '{print $2}' | xargs kill -9
ps aux | grep "ngrep -l -M -q -d en1 -Wbyline method=Library.addSong" | grep -v "grep ngrep -l -M -q -d en1 -Wbyline method=Library.addSong" | awk '{print $2}' | xargs kill -9

echo "Scrobbler shutdown."
