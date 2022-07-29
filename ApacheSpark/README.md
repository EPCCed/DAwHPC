# Spark on Cirrus

## Prerequisites

Create a directory within the Cirrus `/work` directory tree to hold Apache Spark and the scripts.
We will call this directory `$WORK_DIR` in the following.

## Download Spark

Choose a Spark version here: https://spark.apache.org/downloads.html, download it to `$WORK_DIR` and untar it.

For example:
```
cd $WORK_DIR
wget https://dlcdn.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz
tar xzf spark-3.3.0-bin-hadoop3.tgz
```

## Install the scripts

Clone the DAwHPC git repo.

* Copy the slurm script [`spark_cluster.slurm`](spark_cluster.slurm) to `$WORK_DIR`.
* Copy the worker start script [`bin/run_worker.sh`](bin/run_worker.sh) to `$WORK_DIR/bin`.
* Copy [`conf/spark-defaults.conf`](conf/spark-defaults.conf) to the Spark configuration directory, e.g. `$WORK_DIR/spark-3.3.0-bin-hadoop3/conf`.

## Start a Spark cluster

Modify the slurm job submission script `spark_cluster.slurm`: add the correct account code to `#SBATCH --account=` and define the correct location for `$WORK_DIR`. Choose the size of your cluster by specifying the number of nodes `#SBATCH --nodes=<N>`. The cluster created by the script will have one master node and `N-1` worker nodes. Adjust other slurm parameters such as time, partition and qos as required.

Then submit the job:
```
sbatch $WORK_DIR/spark_cluster.slurm
```
The log file is going to show the paths of the Spark worker and master log files. You can watch those to see that the cluster is starting up correctly and that the worker nodes register with the master.

A worker node should report something similar to the following:
```
INFO Worker: Successfully registered with master spark://r1i5n2.ib0.icexa.epcc.ed.ac.uk:7077
```
where `r1i5n2` is the name of the master node and this depends on the nodes that were allocated for your job. Make a note of the master node name - you'll need it later.

If the cluster started up correctly you can also find the name of the master node in the file `$WORK_DIR/logs/master.log`. For example:
```
$ cat $WORK_DIR/logs/master.log 
r1i5n2
```

The job submission script also starts the Spark history server.

## Submit a test job to the Spark cluster

Spark comes with a number of examples that run out of the box. For example, to run [SparkPi](https://github.com/apache/spark/blob/master/examples/src/main/scala/org/apache/spark/examples/SparkPi.scala):
```
$WORK_DIR/spark-3.3.0-bin-hadoop3/bin/spark-submit --deploy-mode client \
    --master spark://r1i0n22:7077 \
    --class org.apache.spark.examples.SparkPi \
    $WORK_DIR/spark-3.3.0-bin-hadoop3/examples/jars/spark-examples_2.12-3.3.0.jar
```
where you replace `spark-3.3.0-bin-hadoop3` and `spark-examples_2.12-3.3.0.jar` with the Spark version and examples jar that you downloaded.

## View the Spark GUI and the history server

(Linux/MacOS only)

Log in to Cirrus again mapping the ports:
```
ssh <username>@login.cirrus.ac.uk -L8080:r1i5n2:8080 -L18080:r1i5n2:18080 
```
where `r1i5n2` is the master node discovered above.

Now you can open [http://localhost:8080](http://localhost:8080) to view the Apache Spark web UI and [http://localhost:18080](http://localhost:18080) for the history server.
