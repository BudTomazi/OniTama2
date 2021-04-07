# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:32:09 2021

@author: budto
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten


class network():
    def __init__(self):
        self.inputs = np.array([[0 for i in range(250)]])
        self.outputs = np.array([[0]])
        
        
        # input_shape = (25, 9, 1)
        # self.model = keras.Sequential([
        #     keras.layers.Conv2D(64,3,activation="relu", input_shape=input_shape[1:],kernel_initializer=initializers.RandomNormal(stddev=0.01)),
        #     keras.layers.Conv2D(32,3,activation="relu",kernel_initializer=initializers.RandomNormal(stddev=0.01)),
        #     keras.layers.Conv2D(16,3,activation="relu",kernel_initializer=initializers.RandomNormal(stddev=0.01)),
        #     keras.layers.Flatten(),
        #     keras.layers.Dense(1, activation = "relu",kernel_initializer=initializers.RandomNormal(stddev=0.01)),
        #     ])
        
        #create model
        self.model = keras.Sequential()
        #add model layers
        self.model.add(Conv2D(16, kernel_size=3, activation='relu', input_shape=(25,10,1)))
        self.model.add(Conv2D(16, kernel_size=3, activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(1))
        
        # self.model = keras.models.load_model("current_model")
        self.model.compile(optimizer = "adam", loss = "mean_squared_error", metrics = ["accuracy"])
        
    def predict(self, inputs):
        return self.model.predict(inputs).sum()
    
    def add_input(self, inputs):
        self.inputs = np.append(self.inputs, inputs, axis=0)
        
    def update_ouputs(self, result):
        div = len(self.inputs) - len(self.outputs)
        factor = result/50 - 1
        j = 0
        for i in range(len(self.inputs)):
            if i > len(self.outputs)-1:
                j += 1
                # self.outputs = np.append(self.outputs, [[50 + (factor * 50/(div)) * j]])
                self.outputs = np.append(self.outputs, [[result/100]])
    
    def save_model(self):
        self.model.save("model_checkpoint")
        np.save("inputs_checkpoint", self.inputs)
        np.save("inputs_checkpoint", self.outputs)
    
    def clear_training_set(self):
        self.inputs = np.array([[0 for i in range(30)]])
        self.outputs = np.array([[0]])
        
    def train(self):
        self.model.fit(np.reshape(self.inputs,(len(self.inputs),25,10,1)), self.outputs, epochs=8)