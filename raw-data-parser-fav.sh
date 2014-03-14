#!/bin/sh

DATA_ROOT=data
FAV_ROOT=fav
touch history
[[ -d "$DATA_ROOT" ]] || mkdir "$DATA_ROOT"
[[ -d "$FAV_ROOT" ]] || mkdir "$FAV_ROOT"

tail -n 200 -f history2  | while read line
do
	resultfav=$(echo $line | grep 'method=Library.addSong')

	file=$(echo $line | sed -ne 's/.*id=\([0-9]*\).*/\1/p')
	if [[ "$resultfav" != "" ]]
	then
	    touch "$FAV_ROOT"/"$file"
	fi
done
