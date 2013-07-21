#!/bin/sh

DATA_ROOT=data
touch history
[[ -d "$DATA_ROOT" ]] || mkdir "$DATA_ROOT"

tail -n 200 -f history  | while read line
do
	result=$(echo $line | grep 'method=Playlog.add')
  	if [[ "$result" != "" ]]
	then
	    #echo $line
	    file=$(echo $line | sed -ne 's/.*id=\([0-9]*\).*time=\([0-9]*\).*/\2-\1/p')
	    #echo $file
	    touch "$DATA_ROOT"/"$file"
	fi
done
