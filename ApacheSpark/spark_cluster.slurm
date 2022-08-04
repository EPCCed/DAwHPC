#!/bin/bash

#SBATCH --job-name=Spark
#SBATCH --time=0:20:0
#SBATCH --exclusive
#SBATCH --nodes=4
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=36
#SBATCH --distribution=block:block
#SBATCH --account=<YOUR_ACCOUNT_HERE>
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --hint=nomultithread

module load java

# replace this with your setup
WORK_DIR=/work/<project>/<project>/<username>/
SPARK_HOME=$WORK_DIR/spark-3.3.0-bin-hadoop3

cd $WORK_DIR

mkdir -p tmp
mkdir -p logs
rm logs/*

scontrol show hostnames $SLURM_JOB_NODELIST > logs/nodes_list.log
mastername=$(head -n 1 logs/nodes_list.log)
echo $mastername > logs/master.log
echo Spark master is $mastername

nodes=$(cat logs/nodes_list.log |tr "\n" " ")
echo "Nodes:" ${nodes[*]}

# start Spark master
$SPARK_HOME/sbin/start-master.sh
echo "Started the master" $mastername

# give the master time to start up
sleep 20
# start the workers
srun $WORK_DIR/bin/run_worker.sh $mastername 7077 &

# start history server on the master node
$SPARK_HOME/sbin/start-history-server.sh
echo "Started the history server"

# now wait until the job ends
sleep 24h
