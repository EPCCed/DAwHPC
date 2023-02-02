#!/usr/bin/env python
# coding: utf-8

# # Data Analytics with High Performance Computing - Practical 2
# ## Data Cleaning

# ### 2. Unstructured data - "Dalton Brothers"

# In[ ]:


import pandas as pd
import numpy as np

# Ignore DeprecationWarnings emitted by Numpy
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Start by reading the file to determine its basic structure.

# This time we'll keep the path in a `string` variable to make our code neater.

# In[ ]:


daltons_path = "DatasetsForPracticals/DataCleaning/daltons.txt"


# We use the `with open` statement to create a file object, then use the readlines() function to produce a list where each entry is a line of the file.

# In[ ]:


with open (daltons_path, "r") as daltons_file:
    daltons_lines = daltons_file.readlines()
daltons_lines


# Note '\n' newline characters.

# We can loop over the lines of the files and use the str.strip() function to remove leading white space and new line characters.

# In[ ]:


with open (daltons_path, "r") as daltons_file:
    daltons_lines = []
    for line in daltons_file.readlines():
        daltons_lines.append(line.strip())
daltons_lines


# We can see that the data lines are in a comma-separated value (CSV) form, with comment lines starting with '%' symbols. There is no obvious header row.<br/>
# Using a Python "list comprehension", we can coerce the data into sublists (`str.split(',')`) and ignore comments (`if not x.startswith('%')`).<br/>
# This one line can be though of as a compact version of:
# ```
# daltons_data = []
# for x in daltons_lines:
#     if not x.startswith('%'):
#         daltons_data.append(x.split(','))
# ```

# In[ ]:


daltons_data = [x.split(',') for x in daltons_lines if not x.startswith("%")]
daltons_data


# We can now create a Pandas DataFrame from our list.

# In[ ]:


daltons_df = pd.DataFrame(daltons_data)
daltons_df


# We have a dataframe, but it's a mess. There are no column names and some of the data in rows is in the wrong order.
# 
# First, let's fix the column names.

# In[ ]:


daltons_df = pd.DataFrame(daltons_data,columns=['Name','DOB','DOD'])
daltons_df


# It's clear now that the data in rows is not in a consistent order.
# Start by ensuring names are in the correct column.

# In[ ]:


#object to hold a piece of data to move
misplaced_datum = None
#loop over rows of the DataFrame - each row is a Pandas Series object.
for i,row in daltons_df.iterrows():
    print(row) # row is a view of the row, not the row itself
    #'Name' is the only column that contains a word, orthers contain numbers, so just use str.isalpha() - returns True is the string only contains letter characters.
    #Note we have not coerced any data yet, so all data are strings. None is Python's null object.
    
    #if the 'Name' entry does not only contain letters, then the actual name must be in the DOB or the DOD column.
    if not row['Name'].isalpha():
        print(i,row['Name'])
        if row['DOB'].isalpha():
            #Name is in DOB column
            print(i,row['DOB'])
            misplaced_datum = row['Name'] # take a copy of whatever is in the 'Name' column
            row['Name'] = row['DOB'] # set the 'Name' entry to the 'DOB' entry
            row['DOB'] = misplaced_datum # set the 'DOB' entry to the value that was in the 'Name' column
        elif row['DOD'].isalpha():
            print(i,row['DOD'])
            misplaced_datum = row['Name']
            row['Name'] = row['DOD']
            row['DOD'] = misplaced_datum
        daltons_df.iloc[i] = row # replace the row in daltons_df with the row object we've just modified
    print(row)


# In[ ]:


daltons_df


# Now convert numerical data to numerical dtypes.

# In[ ]:


daltons_df['DOB'] = pd.to_numeric(daltons_df['DOB'],errors='coerce')
daltons_df['DOD'] = pd.to_numeric(daltons_df['DOD'],errors='coerce')
daltons_df


# We are told all Dalton brothers with born before 1890 and all died after 1890.<br/>
# Use this information to check 'DOB' and 'DOD' entries.

# In[ ]:


#object to hold a piece of data to move
misplaced_datum = None
#loop over rows of the DataFrame - each row is a Pandas Series object.
for i,row in daltons_df.iterrows():
    #If the value in the 'DOB' column is after 1890, swap the 'DOB' and 'DOD' entries
    if row['DOB'] > 1890:
        print(i,row['DOB'])
        misplaced_datum = row['DOB']
        row['DOB'] = row['DOD']
        row['DOD'] = misplaced_datum
        print(i,row['DOB'])
        daltons_df.iloc[i] = row
    print(row)


# Now have another look at the DataFrame.<br/>
# 

# In[ ]:


daltons_df.info()


# In[ ]:


daltons_df


# __Correct types__ - Can we convert years from `float` to `int` object?

# In[ ]:


#Create a "type dictionary" of column names and dtypes and pass to pd.DataFrame.astype()
dtypes = {'Name': str, 'DOB': int, 'DOD': int}
daltons_df = daltons_df.astype(dtypes,errors='ignore')
daltons_df.info()


# DOD values have changed to integers, but DOB values are still floats. Maybe you noticed this happened to the 'height' column in Part 2a of this practical!<br/>
# What has gone wrong? Let's change `errors='ignore'` to `errors='raise'` to check.

# In[ ]:


daltons_df = daltons_df.astype(dtypes,errors='raise') # intentionally causes an error!
daltons_df


# This error tells us that the `NaN` cannot be converted to a Python integer, `int`.<br/>
# But, as Pandas 0.24.4 (January 2019), there is a <a href='https://pandas.pydata.org/pandas-docs/version/0.24/whatsnew/v0.24.0.html#optional-integer-na-supporthttps://pandas.pydata.org/pandas-docs/version/0.24/whatsnew/v0.24.0.html#optional-integer-na-support'>solution</a> to this!<br/>
# Pandas dtype `Int64` (note the capital 'I') offers "optional NA integer support". Pandas will use its own dtypes if the name of the dtype is given as a string.

# In[ ]:


dtypes = {'Name': 'str', 'DOB': 'Int64', 'DOD': 'Int64'}
daltons_df = daltons_df.astype(dtypes,errors='raise')
daltons_df


# __Standardisation__

# Finally, we wish to use the above code in a repeatable manner. To to this, we should save it as a Python script (`.py`) and make some changes.<br/>
# Run the cell below to convert this IPython Notebook to a Python script.

# In[ ]:


get_ipython().system("jupyter nbconvert --to script 'Practical2b.ipynb'")


# Now open Practical2b.py from the navigation pane - it will open as a new tab, but refer back here for instructions.

# __Python script editing__

# The first thing to note is Markdown cells and input markers (e.g., `# In[1]:`) are given as comments (leading `#`).<br>
# The Markdown lines are useful - leave them in. But the input markers are not required, so delete these lines.

# Next, lines that are intended for interaction with the IPython system should be dealt with. These are where we simply have a variable name or some output call on a line, such as "`daltons_lines`", "`daltons_df`" or "`daltons_df.info()`". These can either be removed completely, or, if you fine the output useful, should be put into Python `print()` function calls, e.g., `print(daltons_df)`. Perhaps the last of these lines could be printed so the user sees the form of the final DataFrame on standard output. Also remove the two IPython shell commands (the `!jupyter` and `!python` lines)

# Now, in a step that wouldn't normally be required, we need to remove erroneous lines. Remember we converted types incorrectly? Remove the lines between "# \_\_Correct types\_\_ - Can we convert years...?" and "# Pandas dtype `Int64`..." to leave only the _correct_ `dtypes` dictionary declaration and `astype` call.

# Optionally, since some Python documentation generators, such as `sphinx`, can interpret Markdown comments in so-called doctstrings, the `#` characters could be removed from Markdown lines and replaced with triple quotes `""" ... """` (over single or multiple lines). This makes documentation much quicker!

# Finally, try running the script by running the cell below.<br/>
# Also, try running in a terminal tab (hit the <kbd>+</kbd> button above to open a Launcher tab and choose Other - Terminal). Then, navigate to the folder containing your Practical2b.py file and type `python Practical2b.py`

# In[ ]:


get_ipython().system('python Practical2b.py')


# In[ ]: