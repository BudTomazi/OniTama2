# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 09:44:57 2021

@author: budto
"""

import random as r

class minimax_bot3():
    def __init__(self, eval_function):
        self.eval_function = eval_function
    
    def play(self, game_state, red, limit):
        self.count = 0
        self.limit = limit
        if(not red):
            a, b = self.max_value(game_state, -5000, 5000, 0)
            print(self.count, a)
            return b
        else:
            a, b = self.min_value(game_state, -5000, 5000, 0)
            print(self.count, a)
            return b
    
    def max_value(self, game_state, alpha, beta, depth):
        if game_state.game_over2(game_state):
            return (game_state.game_over2(game_state), None)
        if depth == self.limit:
            self.count += 1
            return (self.eval_function(game_state, True), None)
        
        v = -500000
        move = None
        actions = game_state.get_actions(True)
        for a in actions:
            v2, a2 = self.min_value(game_state.next_state(a), alpha, beta, depth + 1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return (v, move)
        return (v, move)
            
    def min_value(self, game_state, alpha, beta, depth):
        if game_state.game_over2(game_state):
            return (game_state.game_over2(game_state), None)
        if depth == self.limit:
            self.count += 1
            return (self.eval_function(game_state, True), None)
        
        v = 500000
        move = None
        actions = game_state.get_actions(False)
        for a in actions:
            v2, a2 = self.max_value(game_state.next_state(a), alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return (v, move)
        return (v, move)
    
    
class minimax_bot4():
    def __init__(self, network):
        # self.eval_function = eval_function
        self.network = network
    
    def play(self, game_state, red, limit):
        self.count = 0
        self.limit = limit
        if(not red):
            a, b = self.max_value(game_state, -5000, 5000, 0)
            print(self.count, a)
            return b
        else:
            a, b = self.min_value(game_state, -5000, 5000, 0)
            print(self.count, a)
            return b
    
    def max_value(self, game_state, alpha, beta, depth):
        if game_state.game_over2(game_state):
            return (game_state.game_over2(game_state), None)
            # return (self.network.predict(game_state.to_representation2(False)), None)
        if depth == self.limit:
            self.count += 1
            return (self.network.predict(game_state.to_representation2(False)), None)
        
        v = -500000
        move = None
        actions = game_state.get_actions(True)
        for a in actions:
            v2, a2 = self.min_value(game_state.next_state(a), alpha, beta, depth + 1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return (v, move)
        return (v, move)
            
    def min_value(self, game_state, alpha, beta, depth):
        if game_state.game_over2(game_state):
            return (game_state.game_over2(game_state), None)
            # return (self.network.predict(game_state.to_representation2(True)), None)
        if depth == self.limit:
            self.count += 1
            return (self.network.predict(game_state.to_representation2(True)), None)
        
        v = 500000
        move = None
        actions = game_state.get_actions(False)
        for a in actions:
            v2, a2 = self.max_value(game_state.next_state(a), alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return (v, move)
        return (v, move)
    
def play_100_games(game_state, turn):
    r_wins = 0
    b_wins = 0
    for j in range(100):
        g = game_state
        for i in range(60):
            if turn == False:
                #Random Player
                actions = g.get_actions(turn)
                c = actions[r.randint(0,len(actions)-1)]
                g = g.next_state(c)

            else:
                #Random Player
                actions = g.get_actions(turn)
                c = actions[r.randint(0,len(actions)-1)]
                g = g.next_state(c)

            if g.game_over2(g):
                if g.game_over2(g) < 0:
                    r_wins += 1
                else:
                    b_wins += 1
                break;
            # print("-----------------------------")
            turn = not turn
    if turn:
        return b_wins/100
    else:
        return r_wins/100

