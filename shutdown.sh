#!/bin/sh


ps aux | grep raw-data-parse.sh | grep -v grep | awk '{print $2}' | xargs kill -9
ps aux | grep "python ./lastfm-scrobler.py"  | grep -v grep | awk '{print $2}' | xargs kill -9
ps aux | grep "ngrep -l -M -q -d en1 -Wbyline method=Playlog.add"  | grep -v grep | awk '{print $2}' | xargs kill -9
ps aux | grep "ngrep -l -M -q -d en0 -Wbyline method=Playlog.add"  | grep -v grep | awk '{print $2}' | xargs kill -9
ps aux | grep "tail -n 200 -f history"  | grep -v grep | awk '{print $2}' | xargs kill -9


