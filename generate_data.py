#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 10:10:11 2020

@author: hanbo
"""

'''Creating mock timeseries data'''

#from 1.1.2019 to 31.12.2020, daily, 30 minute increments, randomly
import pandas as pd
import random
from pathlib import Path

def create_data(times, mask, fraction=0.7):
    '''
    

    Parameters
    ----------
    times : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    fraction : TYPE, optional
        DESCRIPTION. The default is 0.7.

    Returns
    -------
    temp : TYPE
        DESCRIPTION.

    '''
    
    my_data = generate_pomodoros(times=times, mask=mask, fraction=fraction)
    temp = pd.DataFrame(my_data, columns=['pomodoros'])
    topics = ['coding', 'reading', 'chores', 'email']
    topics_col = []
    for i in range(len(temp)):
        topic = random.choices(topics, weights = [10, 5, 4, 3])[0]
        topics_col.append(topic)
    temp['task'] = topics_col
    temp.loc[temp['pomodoros'] == 0, 'task'] = '0'
    return temp

def generate_pomodoros(times, mask, fraction=0.7):
    '''
    

    Parameters
    ----------
    times : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    fraction : TYPE, optional
        DESCRIPTION. The default is 0.7.

    Returns
    -------
    my_data : TYPE
        DESCRIPTION.

    '''
    my_data = times[mask]
    my_data = pd.Series(index=(my_data))
    my_data = my_data.sample(frac=fraction, random_state=(42))
    my_data.sort_index(inplace=True)
    my_data.fillna(value=1, inplace=True)
    my_data = my_data.resample('30min').asfreq(0)
    #add data points from midnight?
    return my_data
    
 
if __name__ == "__main__":
    #create and save synthetic data for pomodash
    times = pd.date_range(start='1/1/2019', end='31/12/2019', freq='30min')
    mask_night_owl = (((times.hour < 5) | (times.hour > 15)) & (times.weekday != 6) )
    mask_broad = (times.hour >= 6) & (times.weekday != 6) & (times.weekday != 5)
    mask_narrow = ((times.hour >= 9) & (times.hour <= 16)) & (times.weekday != 6)\
        & (times.weekday != 5)
    
    night_owl_dense  = create_data(times, mask_night_owl)
    night_owl_sparse = create_data(times, mask_night_owl, 0.5)
    broad_dense = create_data(times, mask_broad)
    broad_sparse = create_data(times, mask_broad, 0.5)
    narrow_dense = create_data(times, mask_narrow)
    narrow_sparse = create_data(times, mask_narrow, 0.5)
    
    my_dfs = [night_owl_dense, night_owl_sparse, broad_dense, broad_sparse,\
              narrow_dense, narrow_sparse]
    i = 0
    for df in my_dfs:
        path = Path('data/data_' + str(i) +'.txt')
        df.to_csv(path)
        i+=1
        