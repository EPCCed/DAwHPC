#!/usr/bin/env python
# coding: utf-8

# Import Pandas and NumPy

import pandas as pd
import numpy as np


# Import Dask dataframe

import dask
from dask import dataframe as dd
from tornado.iostream import StreamClosedError
from distributed.comm.core import CommClosedError
dask.config.set({"distributed.comm.timeouts.tcp": "50s"})
# Other imports
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import warnings
warnings.filterwarnings("ignore")
import time
import sys

from dask.distributed import Client, performance_report

all_start = time.time()

if __name__ == '__main__':
    start = time.time()
    client = Client(n_workers=36,threads_per_worker=2,memory_limit="{}GB".format(256//36))
    stop = time.time()
    print("Dask setup time: ",stop - start,"seconds")
    from dask.distributed import get_client

    # a list of the columns we are interested in - we'll look at the air temperature and the soil temperature closest to the surface
    cols = ['DATE_TIME','SITE_ID','TA','TDT1_TSOIL','TDT2_TSOIL'] # list of columns we're interested in
    dtypes = {'DATE_TIME':object,'SITE_ID':str,'TA':np.float64,'TDT1_TSOIL':np.float64,'TDT2_TSOIL':np.float64} # datatypes dictionary
    # print(cols,dtypes)
    with performance_report(filename='Practical3b_performance.html'):
        start = time.time()

        ##
        df = dd.read_csv('/work/m22oc/m22oc/shared/DAwHPC/practicals_data/P3/*2019.csv', usecols=cols, dtype=dtypes, parse_dates=['DATE_TIME'])
        start = time.time()
        df = df.replace(-9999,np.nan).set_index('DATE_TIME',npartitions=72)

        df['SOIL_TEMP'] = df[['TDT1_TSOIL','TDT2_TSOIL']].mean(axis=1)
        df = df.drop(columns=['TDT1_TSOIL','TDT2_TSOIL']).compute()

        df = df[:].resample('1d').mean()
        stop = time.time()
        print('Data cleaning time: ',stop-start,' seconds.')
        start = time.time()
        ax = df.plot()
        stop = time.time()
        print("Plot generation time: ",stop - start," seconds.")
    plt.savefig('Practical3b_plot.png')

    all_stop = time.time()

    print("Total run time: ",all_stop-all_start," seconds.")

    # sys.exit() required inside __main__ to prevent Dask -> tornado communication attempts after the tornado client has closed (causing StreamClosedError)
    sys.exit()