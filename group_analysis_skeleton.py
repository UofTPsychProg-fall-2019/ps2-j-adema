#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#
testingrooms = ['A','B','C']
for room in testingrooms:
    filepath = os.path.join(('testingroom'+room), 'experiment_data.csv') #defining origin filepath
    filename = 'experiment_data_'+room+'.csv' #new filename
    newpath = os.path.join('rawdata', filename) #new filepath to rawdata
    shutil.copyfile(filepath,newpath) #copying files with new name to rawdata


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5)) #creating an empty array to put five columns of data into
for room in testingrooms:
    filename = 'experiment_data_'+room+'.csv' #create new filenames for each room
    pathname = os.path.join('rawdata', filename) #had to put this here to make vstack work
    tmp = sp.loadtxt(pathname,delimiter=',') #load the data as text, comma-separated
    data = np.vstack([data,tmp]) #stack that data into an array!!!


#%%
# calculate overall average accuracy and average median RT
#
subj = [data[:, 0]] #made all of these because it wasn't happening in the calcs;
stim = [data[:, 1]] #indexed data based on its columns
pair = [data[:, 2]]
acc = [data[:, 3]]
med_rt = [data[:, 4]]
acc_avg = np.average(acc) # 91.48%
mrt_avg = np.average(med_rt)  # 477.3ms


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an
# if statement. (i.e., loop through the data to make a sum for each condition,
# then divide by the number of data points going into the sum)
#

stim1_acc_sum = 0 #made these empty variables in order to add to them for every
# iteration of the loop
stim1_mrt_sum = 0
stim1_n = 0
stim2_acc_sum = 0
stim2_mrt_sum = 0
stim2_n = 0
for sbj in data: #for every row in the data...
    if sbj[1] ==1: #if the value in column 1 = 1 (i.e., if this data is for words)
        stim1_acc_sum += sbj[3] #add this row's accuracy to the variable
        stim1_mrt_sum += sbj[4] #add this row's med rt to the variable
        stim1_n += 1 #add 1 for n, for later calcs
    elif sbj[1] ==2: #if the value in column 1 = 2 (i.e., if this data is for faces)
        stim2_acc_sum += sbj[3] #see above
        stim2_mrt_sum += sbj[4] #see above
        stim2_n+=1 #see above
stim1_acc_avg = (stim1_acc_sum/stim1_n) #average accuracy for words
stim1_mrt_avg = (stim1_mrt_sum/stim1_n) #average median RT for words
stim2_acc_avg = (stim2_acc_sum/stim2_n) #average accuracy for faces
stim2_mrt_avg = (stim2_mrt_sum/stim2_n) #average median RT for faces


# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms


#%%
# calculate averages (accuracy & RT) split by congruency using indexing,
# slicing, and numpy's mean function
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#
acc_wp = np.average(data[data[:,2]==1,3])  # 94.0%; sliced data based on the
# value for column 2. Calculates the average accuracy for values of 1 in column 2.
# This is the same command used for every other variable in this block.
acc_bp = np.average(data[data[:,2]==2,3])  # 88.9%; column 2 = 2 average accuracy
mrt_wp = np.average(data[data[:,2]==1,4])  # 469.6ms; column 2 = 1 average median rt
mrt_bp = np.average(data[data[:,2]==2,4])  # 485.1ms; column 2 = 2 average median rt


#%%
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#
stim1 = data[data[:,1]==1,:] #the slice for words, where column 1 =1
stim2 = data[data[:,1]==2,:] #the slices for faces, where column 1 = 2

w_wp_mrt = np.average(stim1[stim1[:,2]==1,4]) #WP (column 2 = 1) word median RT
f_wp_mrt = np.average(stim2[stim2[:,2]==1,4]) #WP face median RT
w_bp_mrt = np.average(stim1[stim1[:,2]==2,4]) #BP (column 2 =2) word median RT
f_bp_mrt = np.average(stim2[stim2[:,2]==2,4]) #BP face median RT

# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%
# compare pairing conditions' effect on RT within stimulus using scipy's
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats
words_t = scipy.stats.ttest_rel(stim1[stim1[:,2]==1,4], stim1[stim1[:,2]==2,4], axis=0)
faces_t = scipy.stats.ttest_rel(stim2[stim2[:,2]==1,4], stim2[stim2[:,2]==2,4], axis=0)

# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))
print('\nWORD CONDITION: average accuracy: {:.2f}%, average median RT: {:.1f} ms' .format(100*stim1_acc_avg,stim1_mrt_avg))
print('\nFACE CONDITION: average accuracy: {:.2f}%, average median RT: {:.1f} ms' .format(100*stim2_acc_avg,stim2_mrt_avg))
print('\nWHITE/PLEASANT CONDITION: average accuracy:{:.2f}%, average median RT:{:.1f} ms' .format(100*acc_wp,mrt_wp))
print('\nBLACK/PLEASANT CONDITION: average accuracy:{:.2f}%, average median RT:{:.1f} ms' .format(100*acc_bp,mrt_bp))
print('\nMEDIAN RTs for WHITE/PLEASANT: WORDS:{:.1f} ms, FACES:{:.1f} ms'.format(w_wp_mrt,f_wp_mrt))
print('\nMEDIAN RTs for BLACK/PLEASANT: WORDS:{:.1f} ms, FACES:{:.1f} ms'.format(w_bp_mrt,f_bp_mrt))
t1 = words_t[0]
p1 = words_t[1]
print('\nCOMPARING PAIRING CONDITIONS FOR WORD RT: t = {:.2f}, p = {:.5f}'.format(t1,p1))
t2 = faces_t[0]
p2 = faces_t[1]
print('\nCOMPARING PAIRING CONDITIONS FOR FACE RT: t = {:.2f}, p = {:.5f}'.format(t2,p2))
print('\nThe results suggest that people are generally biased towards "white/pleasant" pairings.')
