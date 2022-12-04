#!/bin/bash


file="fuzzer.py"
if test -f file ;
then
	echo "File not there"
	echo "Downloading the script"
	git clone https://github.com/Helsingxx/CRASH-STATION.git CRASH_STATION_DIR
else
	var=$(echo $RANDOM | shasum | awk '{print $1}')
	git clone https://github.com/Helsingxx/CRASH-STATION.git $var
	var2=$(diff <(shasum fuzzer.py | awk '{print $1}') <(shasum $var/fuzzer.py | awk '{print $1}'))
	if [var2 -eq 1]
	then
		mv $var "CRASH_STATION_DIR"
	fi
fi
