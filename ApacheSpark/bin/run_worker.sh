#!/bin/bash

# replace this with your setup
WORK_DIR=/work/<project>/<project>/<username>/
SPARK_HOME=$WORK_DIR/spark-3.3.0-bin-hadoop3

cd $SPARK_HOME
myhostname=`hostname`

# don't start a worker on the master node
if [ $myhostname = $1 ]
  then echo "Master node: not starting a worker here"; exit 0
fi

echo Starting worker on $myhostname and reporting to master spark://$1:$2
$SPARK_HOME/sbin/start-worker.sh spark://$1:$2

sleep 24h
