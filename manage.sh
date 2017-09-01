#!/bin/bash

PACKAGED=false

# Check if this file is a symlink, if so, read real base dir
BASE_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
if [ $? -eq 0 ] && [ "$BASE_DIR" != $(pwd)  ]; then
	PACKAGED=true
fi

COMMAND="python $@"

if [ $PACKAGED == true ]; then
	if [ "$(id -u)" != "0" ]; then
		echo "This script must be run as root" 1>&2
		exit 1
	fi
	/bin/su -s /bin/bash -c "cd $BASE_DIR && source env/bin/activate && $COMMAND && deactivate" pyazo 
else
	cd $BASE_DIR
	source env/bin/activate
	$COMMAND
	deactivate
fi

