#!/bin/bash
mongorun=$(ps aux | grep mongod | grep $USER | wc -l)
echo $mongorun
if [ $mongorun -eq 1 ]; then
	mongod --fork --logpath ./db/mongolog --dbpath ./db --port 27018
fi
export FLASK_APP=server.py
python3 -m flask run --host=0.0.0.0 -p 7777
