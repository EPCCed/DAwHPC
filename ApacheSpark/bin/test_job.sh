#!/bin/bash

# replace this with your setup
WORK_DIR=/work/<project>/<project>/<username>/
SPARK_VERSION=3.3.0
SPARK_HOME=$WORK_DIR/spark-$SPARK_VERSION-bin-hadoop3

if [ $# -eq 0 ]
then
        echo "Usage $0 <master_node_id>"
        exit 1
fi

$SPARK_HOME/bin/spark-submit --deploy-mode client \
    --master spark://$1:7077 \
    --class org.apache.spark.examples.SparkPi \
    $SPARK_HOME/examples/jars/spark-examples_2.12-$SPARK_VERSION.jar
