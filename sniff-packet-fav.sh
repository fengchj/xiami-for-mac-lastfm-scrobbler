#!/bin/sh

ngrep -l -M -q -d en1 -Wbyline method=Library.addSong
ngrep -l -M -q -d en0 -Wbyline method=Library.addSong
