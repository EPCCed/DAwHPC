#!/usr/bin/env python
# coding: utf-8

# # Data Analytics with High Performance Computing - Practical 2
# ## Data Cleaning

# ### Learning outcomes

# Practice some common techniques for data cleaning with Python, using functionality of the Pandas library.
# *  Part 1 - (Practical2a.ipynb) reading data, data exploration, data typing, coercion.
# *  Part 2 - (Practical2b.ipynb) dealing with unstructured data, pattern matching, regular expressions, handling missing data, more typing and coercion, standardisation.

# ### 1. Reading and cleaning data

# Import Pandas and NumPy

# In[ ]:


import pandas as pd
import numpy as np

# Ignore DeprecationWarnings emitted by Numpy
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


# Use pd.read_csv() to read in a CSV file containing some data.

# In[ ]:


pd.read_csv('DatasetsForPracticals/DataCleaning/somedata.csv')


# The CSV file didn't contain a header row!

# In[ ]:


pd.read_csv('DatasetsForPracticals/DataCleaning/somedata.csv',header=None)


# You have a bit of information - the file contains ages and heights of people.<br/>
# Read it in again, but this time pass a list of column names.

# In[ ]:


pd.read_csv('DatasetsForPracticals/DataCleaning/somedata.csv',header=None,names=['age','height'])


# Store that data in memory as a Pandas DataFrame object.

# In[ ]:


person = pd.read_csv('DatasetsForPracticals/DataCleaning/somedata.csv',header=None,names=['age','height'])
person


# The data isn't clean yet - use DataFrame.info() to have a look.

# In[ ]:


person.info()


# 'age' is an integer object, which makes sense, but 'height' is a generic 'object'. Also, we are told both columns contain 4 "non-null" values, but there is a 'NA' entry.<br/>
# Let's attempt to set the datatypes of 'age' and 'height' values to NumPy int and float values respectively.

# In[ ]:


person = pd.read_csv('DatasetsForPracticals/DataCleaning/somedata.csv',header=None,names=['age','height'],dtype={'age':np.int,'height':np.float})


# The values '5.7*' is causing a ValueError to be raised.<br/>
# Let's put the pd.read_csv() call inside a try...except statement to get a more readable error message:

# In[ ]:


try:
    person = pd.read_csv('DatasetsForPracticals/DataCleaning/somedata.csv',header=None,names=['age','height'],dtype={'age':np.int,'height':np.float})
except ValueError as e:
    print(e)


# We cannot apply datatypes to data before cleaning!
# Instead, read in the data as before, then use coercion.

# In[ ]:


person = pd.read_csv('DatasetsForPracticals/DataCleaning/somedata.csv',header=None,names=['age','height'])
person


# In[ ]:


person.info() # as before


# Now convert the 'height' column to numerical data with "errors='coerce'". This means if any values cannot be converted to numerical, they are replace with NaN (not a number) values.

# In[ ]:


person['height'] = pd.to_numeric(person['height'],errors='coerce')
person


# In[ ]:


person.info()


# Finally, we see all values are of the correct datatypes and values that were inconsistent with these datatypes are NaN values. DataFrame.info() now reports 2 of the 4 entries in the 'height' column are non-null.

# __Now move on to Practical2b.ipynb__

# In[ ]:




