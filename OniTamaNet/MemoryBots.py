# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 13:09:28 2021

@author: budto
"""

import numpy as np

class memory_bot():
    def __init__(self):
        self.memory = {}
        
    def similarity(self, input1, input2):
        total = 0
        for i in range(len(input1)):
            if input1[i] == input2[i]:
                total += 1
        return total
    
    def add_memory(self, memory, importance, outcome):
        self.memory[memory] = (importance, outcome)
        
    def evalutate_training(self, position):
        if position in self.memory:
            a, b = self.memory[position]
            return a * b
        
        highest_similarity = 0
        chosen_value = 0
        chosen_key = None
        for key in self.memory:
            sim = self.similarity(key, position)
            if sim > highest_similarity:
                highest_similarity = sim
                a, b = self.memory[key]
                chosen_value = a * b
                chosen_key = key
        scores = self.memory[chosen_key]
        self.memory[chosen_key] = (scores[0]+0.05, scores[1])
        return chosen_value
        