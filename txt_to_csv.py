#!/usr/bin/env python
# coding: utf-8

# # CONVERT TXT TO CSV

# In[19]:


import csv
import pandas as pd


# In[ ]:


with open('4.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split("|") for line in stripped if line)
    with open('output-4.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)


# In[21]:


df=pd.read_csv("output-4.csv")


# In[22]:


df.head()


# In[ ]:




