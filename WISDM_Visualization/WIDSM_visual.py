# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 21:56:23 2020
# REFERENCE: https://www.kaggle.com/adamlouly/exploratory-data-analysis-on-wisdm
@author: mrjok
"""
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import re
###matplotlib inline

sns.set(style='whitegrid', palette='muted', font_scale=1)

plt.rcParams["figure.figsize"] = (20,10)

RANDOM_SEED = 42

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

### The column headins
columns = ['user','activity','timestamp', 'x-axis', 'y-axis', 'z-axis']
### Read file
df = pd.read_csv('WISDM_ar_v1.1_raw.txt', header = None, names = columns)

### Removes all null values or na
df=df.dropna()

### Print out the first 5 rows
df.head()

df.info()

df['z-axis'] = df['z-axis'].map(lambda x: str(re.findall("\d+\.\d+", str(x))))
df['z-axis'] = df['z-axis'].map(lambda x: x[2:-2])
df['z-axis'] = pd.to_numeric(df['z-axis'],errors='coerce')

### Prints information based on the type of dataframe
df.info()

### Plot total iteration of each activity
df['activity'].value_counts().plot(kind='bar', title='Number of Activites',color=['b','r','g','y','k','r']);

### Plot graph of activity per user
df['user'].value_counts().plot(kind='bar', title='Activities Per User',color=['r','y','g','b']);

def plot_activity(activity, df):
    data = df[df['activity'] == activity][['x-axis', 'y-axis', 'z-axis']][:200]
    axis = data["x-axis"].plot(subplots=True, 
                     title=activity,color="b")
    axis = data["y-axis"].plot(subplots=True, 
                 title=activity,color="r")
    axis = data["z-axis"].plot(subplots=True, 
             title=activity,color="g")
    for ax in axis:
        ax.legend(loc='lower left', bbox_to_anchor=(1.0, 0.5))
        
plot_activity("Sitting", df)

plot_activity("Standing", df)

plot_activity("Walking", df)

plot_activity("Jogging", df)

plot_activity("Upstairs", df)

plot_activity("Downstairs", df)

plt.rcParams["figure.figsize"] = (15,7)

### Plot heat map of walking and 
def plot_corr(activity, df):
    corr = df[df["activity"]==activity].corr()
    corr = corr[["x-axis","y-axis","z-axis"]][2:5]
    ax = sns.heatmap(
        corr, 
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=100)    )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right'
    );
plot_corr("Walking",df)

plot_corr("Jogging",df)

plot_corr("Sitting",df)

plot_corr("Standing",df)

plot_corr("Upstairs", df)

plot_corr("Downstairs", df)
