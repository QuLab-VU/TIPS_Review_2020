#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 15:55:25 2019

@author: meyerct6
"""

import os, sys

import pandas as pd
import numpy as np
import pickle

import matplotlib.pyplot as plt

#os.environ["CUDA_VISIBLE_DEVICES"]="0" #specify GPU 
import keras as K
import tensorflow as tf
from keras import backend
from keras.backend.tensorflow_backend import set_session
from keras.models import Sequential
from keras.layers import Dense, Dropout

np.random.seed(1) #For reproducibility


hyperparameter_file = 'hyperparameters' # textfile which contains the hyperparameters of the model
data_file = 'data_test_fold0_tanh.p' # pickle file which contains the data (produced with normalize.ipynb)


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


exec(open(hyperparameter_file).read()) 

file = open(data_file, 'rb')
X_tr, X_val, X_train, X_test, y_tr, y_val, y_train, y_test = pickle.load(file)
file.close()

config = tf.ConfigProto(
         allow_soft_placement=True,
         gpu_options = tf.GPUOptions(allow_growth=True))
set_session(tf.Session(config=config))


model = Sequential()
for i in range(len(layers)):
    if i==0:
        model.add(Dense(layers[i], input_shape=(X_tr.shape[1],), activation=act_func, 
                        kernel_initializer='he_normal'))
        model.add(Dropout(float(input_dropout)))
    elif i==len(layers)-1:
        model.add(Dense(layers[i], activation='linear', kernel_initializer="he_normal"))
    else:
        model.add(Dense(layers[i], activation=act_func, kernel_initializer="he_normal"))
        model.add(Dropout(float(dropout)))
    model.compile(loss='mean_squared_error', optimizer=K.optimizers.SGD(lr=float(eta), momentum=0.5))
    
    
hist = model.fit(X_tr, y_tr, epochs=epochs, shuffle=True, batch_size=64, validation_data=(X_val, y_val))
val_loss = hist.history['val_loss']
#Save the results
with open('train_hist.p','wb') as f:
    pickle.dump(hist,f)
with open('train_model.p','wb') as f:
    pickle.dump(model,f)
    
model.reset_states()

average_over = int(epochs/(200/3)) #Equal to 15 if epochs = 1000
mov_av = moving_average(np.array(val_loss), average_over)
smooth_val_loss = np.pad(mov_av, int(average_over/2), mode='edge')

epo = np.argmin(smooth_val_loss)

hist = model.fit(X_train, y_train, epochs=epo, shuffle=True, batch_size=64, validation_data=(X_test, y_test))
test_loss = hist.history['val_loss']


fig, ax = plt.subplots(figsize=(16,8))
ax.plot(val_loss, label='validation loss')
ax.plot(smooth_val_loss, label='smooth validation loss')
ax.plot(test_loss, label='test loss')
ax.legend()
plt.savefig('fit_loss.png')

#Save the results
with open('test_hist.p','wb') as f:
    pickle.dump(hist,f)
with open('test_model.p','wb') as f:
    pickle.dump(model,f)

    

