#!/usr/bin/env python
# coding: utf-8

# Import Pandas and NumPy

import pandas as pd
import numpy as np


# Dask imports
import dask
from dask import dataframe as dd
from dask_jobqueue import SLURMCluster
from dask.distributed import Client, performance_report
dask.config.set({"distributed.comm.timeouts.tcp": "50s"})
# Other imports
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import warnings
warnings.filterwarnings("ignore")
import time
import sys

all_start = time.time()

number_of_nodes = 1

if __name__ == '__main__':
    start = time.time()
    cluster = SLURMCluster(cores=2,
                           processes=36,
                           job_cpu=36,
                           name='plotgen',
                           memory='256GB',
                           queue='standard',
                           header_skip=['--mem'],
                           job_extra=['--qos="standard"','--exclusive'],
                           python='time srun python',
                           account='m22oc-staff',
                           walltime="00:10:00",
                           shebang="#!/bin/bash --login",
                           local_directory='$PWD',
                           interface='ib0',
                           log_directory='sched_logs',
                           env_extra=['source /mnt/lustre/indy2lfs/work/m22oc/m22oc/dmckayk/.bashrc_node','conda activate'])
    cluster.scale(jobs=number_of_nodes)
    print('Cluster initiated')
    client = Client(cluster)
    print('Client initiated')
    stop = time.time()
    print("Dask setup time: ",stop - start,"seconds")
    from dask.distributed import get_client

    # print(client.scheduler_info())
    # print(client)
    # a list of the columns we are interested in - we'll look at the air temperature and the soil temperature closest to the surface
    cols = ['DATE_TIME','SITE_ID','TA','TDT1_TSOIL','TDT2_TSOIL'] # list of columns we're interested in
    dtypes = {'DATE_TIME':object,'SITE_ID':str,'TA':np.float64,'TDT1_TSOIL':np.float64,'TDT2_TSOIL':np.float64} # datatypes dictionary
    # print(cols,dtypes)
    with performance_report(filename='Practical3c_performance.html'):
        start = time.time()
        ##
        df = dd.read_csv('/work/m22oc/m22oc/shared/DAwHPC/practicals_data/P3/*2019.csv', usecols=cols, dtype=dtypes, parse_dates=['DATE_TIME'])
        start = time.time()
        df = df.replace(-9999,np.nan).set_index('DATE_TIME',npartitions=72)


        df['SOIL_TEMP'] = df[['TDT1_TSOIL','TDT2_TSOIL']].mean(axis=1)
        df = df.drop(columns=['TDT1_TSOIL','TDT2_TSOIL']).compute()

        df = df[:].resample('1d').mean()
        stop = time.time()
        print('Data cleaning time: ',stop-start)
        start = time.time()
        ax = df.plot()
        stop = time.time()
        print("Plot generation time: ",stop - start," seconds.")
    plt.savefig('Practical3c_plot.png')
    
    all_stop = time.time()
    
    print("Total time: ",all_stop-all_start," seconds.")
    
    sys.exit()