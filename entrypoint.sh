#!/bin/bash

cd /tmp/src

target="${districts}"
if [ -n "$target" ]; then
  python postgis2epanet.py -d $database -H $db_host -p $db_port -u $db_user -w $db_password -l $target
else
  python postgis2epanet.py -d $database -H $db_host -p $db_port -u $db_user -w $db_password
fi
