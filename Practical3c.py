#!/usr/bin/env python
# coding: utf-8

# Import Pandas and NumPy
print('in')
import pandas as pd
import numpy as np


# Dask imports
from dask import dataframe as dd
from dask_jobqueue import SLURMCluster
from dask.distributed import Client

# Other imports
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import warnings
warnings.filterwarnings("ignore")
import time
import sys

# if __name__ == '__main__':
start = time.time()
cluster = SLURMCluster(cores=36,
                       processes=72,
                       name='plotgen',
                       memory='256GB',
                       queue='standard',
                       header_skip=['--mem'],
                       job_extra=['--qos="standard"','--exclusive'],
                       python='srun python',
                       project='m22oc-staff',
                       walltime="00:10:00",
                       shebang="#!/bin/bash --login",
                       local_directory='$PWD',
                       interface='ib0',
                       env_extra=['source /mnt/lustre/indy2lfs/work/m22oc/m22oc/dmckayk/.bashrc_node','conda activate'])
cluster.scale(jobs=8)
print('Cluster initiated')
client = Client(cluster)
print('Client initiated')
stop = time.time()
print("Dask setup time ",stop - start,"seconds")
from dask.distributed import get_client

print(client.scheduler_info())
print(client)
# a list of the columns we are interested in - we'll look at the air temperature and the soil temperature closest to the surface
cols = ['DATE_TIME','SITE_ID','TA','TDT1_TSOIL','TDT2_TSOIL'] # list of columns we're interested in
dtypes = {'DATE_TIME':object,'SITE_ID':str,'TA':np.float64,'TDT1_TSOIL':np.float64,'TDT2_TSOIL':np.float64} # datatypes dictionary
print(cols,dtypes)
divisions = tuple(pd.date_range(start='2015', end='2020', freq='1d'))
# print(divisions)
start = time.time()
##
df = dd.read_csv('/work/m22oc/m22oc/shared/DAwHPC/practicals_data/P3/*2019.csv', usecols=cols, dtype=dtypes, parse_dates=['DATE_TIME']).replace(-9999,np.nan).set_index('DATE_TIME',divisions=divisions)

df['SOIL_TEMP'] = df[['TDT1_TSOIL','TDT2_TSOIL']].mean(axis=1)
df = df.drop(columns=['TDT1_TSOIL','TDT2_TSOIL'])

df = df[:].resample('1d').mean().compute()
#print(df.head())
ax = df.plot()
#futures = client.map(gen_plot,cols,dtypes,divisions)
#ax = client.gather(futures)
stop = time.time()
print("Plot generation took ",stop - start," seconds.")
plt.savefig('test.png')