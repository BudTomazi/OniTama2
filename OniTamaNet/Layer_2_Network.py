# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 23:11:22 2021

@author: budto
"""


import numpy as np
np.random.seed(1)

def relu(x):
    return (x > 0) * x

def relu2deriv(output):
    return output > 0

class network():
    def __init__(self, alpha, hidden_size):
        self.alpha = alpha                                        #alpha = 0.2
        self.hidden_size = hidden_size                    #currently arbitrary
        self.weights_0_1 = 2 * np.random.random((30,hidden_size)) - 1
        self.weights_1_2 = 2 * np.random.random((hidden_size,1)) - 1
        # self.weights_0_1 = np.load("0_1_weights2.npy")
        # self.weights_1_2 = np.load("1_2_weights2.npy")
        self.temperature = 10
        
        self.inputs = np.array([[0 for i in range(30)]])
        self.outputs = np.array([[0]])

        #example inputs and outputs
        # streetlights = np.array([[1,0,1],[0,1,1],[0,0,1],[1,1,1]])
        
        # walk_vs_stop = np.array([[1,1,0,0]]).T

    def predict(self, inputs):
        layer_0 = inputs
        layer_1 = relu(np.dot(layer_0, self.weights_0_1))
        layer_2 = np.dot(layer_1, self.weights_1_2)
        
        # self.inputs = np.append(self.inputs, inputs, axis=0)
        return np.sum(layer_2)
    
    def add_input(self, inputs):
        self.inputs = np.append(self.inputs, inputs, axis=0)
    
    def update_ouputs(self, result):
        div = len(self.inputs) - len(self.outputs)
        factor = result/50 - 1
        j = 0
        for i in range(len(self.inputs)):
            if i > len(self.outputs)-1:
                j += 1
                self.outputs = np.append(self.outputs, [[50 + (factor * 50/(div)) * j]])
                
    def heat(self, amount=10):
        self.temperature += amount
                
    def clear_training_set(self):
        self.inputs = np.array([[0 for i in range(30)]])
        self.outputs = np.array([[0]])
    
    def train(self):
        for i in range(self.temperature):
            layer_2_error = 0
            for j in range(len(self.inputs)):
                layer_0 = self.inputs[j:j+1]
                layer_1 = relu(np.dot(layer_0, self.weights_0_1))
                layer_2 = np.dot(layer_1, self.weights_1_2)
                
                layer_2_error += np.sum((layer_2 - self.outputs[j:j+1]) ** 2)
                
                layer_2_delta = self.outputs[j:j+1] - layer_2
                # print(layer_2)
                # print(layer_2, self.outputs[j:j+1], layer_2_delta)
                layer_1_delta = layer_2_delta.dot(self.weights_1_2.T) * relu2deriv(layer_1)
                
                self.weights_1_2 += self.alpha * layer_1.T.dot(layer_2_delta)
                self.weights_0_1 += self.alpha * layer_0.T.dot(layer_1_delta)

