#!/usr/bin/env python
# coding: utf-8

# Import Pandas and NumPy

import pandas as pd
import numpy as np


# Import Dask dataframe


from dask import dataframe as dd


# Other imports
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import warnings
warnings.filterwarnings("ignore")
import time
import sys

from dask.distributed import Client

# def gen_plot(cols,dtypes,divisions):
#     df = dd.read_csv('/work/m22oc/m22oc/shared/DAwHPC/practicals_data/P3/*2019.csv', usecols=cols, dtype=dtypes, parse_dates=['DATE_TIME']).replace(-9999,np.nan).set_index('DATE_TIME',divisions=divisions)
#     print(df.head())
#     df['SOIL_TEMP'] = df[['TDT1_TSOIL','TDT2_TSOIL']].mean(axis=1)
#     df = df.drop(columns=['TDT1_TSOIL','TDT2_TSOIL']).compute().persist()

#     df = df[:].resample('1d').mean().compute()

#     ax = df.plot()
#     return ax

if __name__ == '__main__':
    start = time.time()
    client = Client(n_workers=36,threads_per_worker=2,memory_limit="7GB")
    stop = time.time()
    print("Dask setup time ",stop - start,"seconds")

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
    df = df.drop(columns=['TDT1_TSOIL','TDT2_TSOIL']).compute()

    df = df[:].resample('1d').mean()
    print(df.head())
    ax = df.plot()
    #futures = client.map(gen_plot,cols,dtypes,divisions)
    #ax = client.gather(futures)
    stop = time.time()
    print("Plot generation took ",stop - start," seconds.")
    plt.savefig('test.png')