# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 09:44:57 2021

@author: budto
"""

import random as r

class minimax_bot():
    def __init__(self, eval_function):
        self.eval_function = eval_function
    
    def play(self, game_state, red, limit):
        self.count = 0
        def recursive(game_state, depth, side, minormax, limit):
            #If state is game over, dont continue the analysis
            if game_state.game_over2(game_state):
                return game_state.game_over2(game_state)
            
            #initialize variables
            values = []
            choices = []
            nex = not minormax
            actions = game_state.get_actions(side)
            
            #special case for bottom
            if(depth == limit):
                for a in actions:
                    self.count += 1
                    values.append(self.eval_function(game_state.next_state(a), True))
                if minormax:
                    return min(values, default=0)
                return max(values, default=0)
            
            #evaluating branches
            for a in actions:
                values.append(recursive(game_state.next_state(a), depth + 1, not side, nex, limit))
                choices.append(a)
                
            #if top return actions
            if(depth == 0):
                if minormax:
                    return choices[values.index(min(values))]
                return choices[values.index(max(values))]
            
            #if no special case, return what we'd expect
            if minormax:
                return min(values, default=0)
            return max(values, default=0)

        #final return
        output = recursive(game_state, 0, not red, red, limit)
        print(self.count)
        return output

class minimax_bot2():
    def __init__(self, eval_function):
        self.eval_function = eval_function
    
    def play(self, game_state, red, limit):
        self.count = 0
        def recursive(game_state, depth, side, minormax, limit, alpha):
            #If state is game over, dont continue the analysis
            if game_state.game_over2(game_state):
                return game_state.game_over2(game_state)
            
            #initialize variables
            layer_alpha = alpha
            values = []
            choices = []
            nex = not minormax
            actions = game_state.get_actions(side)
            
            #special case for bottom
            if(depth == limit):
                for a in actions:
                    self.count += 1
                    current = self.eval_function(game_state.next_state(a), True)
                    values.append(current)
                    if alpha != None:
                        if minormax and current < alpha:
                            break;
                        if not minormax and current > alpha:
                            break;
                if minormax:
                    return min(values, default=0)
                return max(values, default=0)
            
            #evaluating branches
            for a in actions:
                current = recursive(game_state.next_state(a), depth + 1, not side, nex, limit, layer_alpha)
                values.append(current)
                choices.append(a)
                if layer_alpha == None:
                    layer_alpha = current
                elif minormax:
                    if current < layer_alpha:
                        layer_alpha = current
                elif not minormax:
                    if current > layer_alpha:
                        layer_alpha = current
                
            #if top return actions
            if(depth == 0):
                if minormax:
                    return choices[values.index(min(values))]
                return choices[values.index(max(values))]
            
            #if no special case, return what we'd expect
            if minormax:
                return min(values, default=0)
            return max(values, default=0)

        #final return
        output = recursive(game_state, 0, not red, red, limit, None)
        print(self.count)
        return output
    
class monte_carlo_bot():
    def __init__(self):
        self.exists = True
    
    def play(game_state, red, limit):
        actions = game_state.get_actions(not red)
        values = []
    
        next_states = []
        for a in actions:
            next_states.append(game_state.next_state(a))
            
        for state in next_states:
            values.append(play_100_games(state, red))
            

        return actions[values.index(max(values))]


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
        
        v = -5000
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
        
        v = 5000
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

