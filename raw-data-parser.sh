#!/bin/sh

DATA_ROOT=data
FAV_ROOT=fav
touch history
[[ -d "$DATA_ROOT" ]] || mkdir "$DATA_ROOT"
[[ -d "$FAV_ROOT" ]] || mkdir "$FAV_ROOT"

tail -n 200 -f history  | while read line
do
	result=$(echo $line | grep 'method=Playlog.add')
    file=$(echo $line | sed -ne 's/.*id=\([0-9]*\).*time=\([0-9]*\).*/\2-\1/p')

  	if [[ "$result" != "" ]]
	then
	    touch "$DATA_ROOT"/"$file"
	fi

done
