#!/bin/sh

ngrep -l -M -q -d en1 -Wbyline method=Playlog.add 
ngrep -l -M -q -d en0 -Wbyline method=Playlog.add 


