from dask_jobqueue import SLURMCluster
cluster = SLURMCluster(cores=36, 
                       processes=36,
                       memory='256GB',
                       queue='standard',
                       header_skip=['--mem'],
                       job_extra=['--qos="standard"'],
                       python='srun python',
                       project='m22oc-staff',
                       walltime="00:10:00",
                       shebang="#!/bin/bash --login",
                       local_directory='$PWD',
                       interface='ib0',
                       env_extra=['source /mnt/lustre/indy2lfs/work/m22oc/m22oc/dmckayk/.bashrc_node','conda activate'])


cluster.scale(jobs=2)    # Deploy two single-node jobs

from dask.distributed import Client
client = Client(cluster)  # Connect this local process to remote workers

from dask.distributed import get_client

print(client.scheduler_info())
print(client)

import dask.array as da
x = da.random.random((10000, 10000), chunks=(1000, 1000))
mean = x.mean().compute()
print(mean)
print(client)