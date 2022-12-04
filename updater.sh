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
	diff <(shasum fuzzer.py | awk '{print $1}') <(shasum $var/fuzzer.py | awk '{print $1}')
	if [ $? -eq 1]
	then
		mv $var "CRASH_STATION_DIR"
	else
		rm -rf $var
	fi
fi
