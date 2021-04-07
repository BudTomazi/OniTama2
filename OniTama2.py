# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 23:27:35 2021

@author: budto
"""

import random as r
from Bots import *

class Move:
    def __init__(self, squares, name):
        self.squares = squares
        self.name = name
    def __str__(self):
        output = self.name + "\n"
        grid = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        grid[2][2]="@"
        count = 1
        for place in self.squares:
            grid[2-place[1]][2+place[0]] = count
            count += 1
        for i in range(5):
            s = "|" + str(grid[i][0]) + " " + str(grid[i][1]) + " " + str(grid[i][2]) + " " + str(grid[i][3]) + " " + str(grid[i][4]) + "|"
            output += (s + "\n")
        return output
    
cards = []
cards.append(Move([(-2,0),(-1,1),(1,-1)],"Frog"))
cards.append(Move([(-2,1),(-1,-1),(1,-1),(2,1,1)],"Dragon"))
cards.append(Move([(1,0),(-1,1),(-1,-1)],"Eel"))
cards.append(Move([(-1,1),(1,1),(0,-1)],"Mantis"))
cards.append(Move([(-1,-1),(1,1),(2,0)],"Rabbit"))
cards.append(Move([(-2,0),(0,1),(2,0)],"Crab"))
cards.append(Move([(0,1),(1,0),(0,-1)],"Ox"))
cards.append(Move([(-1,1),(1,1),(1,-1),(-1,-1)],"Monkey"))
cards.append(Move([(-1,0),(0,1),(1,0)],"Boar"))
cards.append(Move([(-1,0),(1,1),(1,-1)],"Cobra"))
cards.append(Move([(-1,-1),(0,1),(1,-1)],"Crane"))
cards.append(Move([(-1,-1),(-1,0),(1,0),(1,1)],"Rooster"))
cards.append(Move([(0,-1),(0,2)],"Tiger"))
cards.append(Move([(-1,0),(0,1,1),(0,-1)],"Horse"))
cards.append(Move([(-1,1),(-1,0),(1,0),(1,-1)],"Goose"))
cards.append(Move([(-1,0),(-1,1),(1,0),(1,1)],"Elephant"))

class Game_State:
    def __init__(self, blue_pieces, red_pieces, blue_cards, red_cards, middle_card, bk, rk):
        self.blue_pieces = blue_pieces
        self.blue_cards = blue_cards
        self.red_cards = red_cards
        self.red_pieces = red_pieces
        self.middle_card = middle_card
        self.bk = bk
        self.rk = rk
        
    def game_over(self, game_state):
        g = game_state
        if g.bk not in g.blue_pieces:
            print("Red Wins Capture")
            return True
        elif g.rk == (2,0):
            print("Red Wins Temple")
            return True
        if g.rk not in g.red_pieces:
            print("Blue Wins Capture")
            return True
        elif g.bk == (2,4):
            print("Blue Wins Temple")
            return True
        return False
    def game_over2(self, game_state):
        g = game_state
        if g.bk not in g.blue_pieces:
            return -100
        elif g.rk == (2,0):
            return -100
        if g.rk not in g.red_pieces:
            return 100
        elif g.bk == (2,4):
            return 100
        return False
        
        
    def next_state(self, action):
        copies = [self.blue_pieces[:], self.blue_cards[:], self.red_cards[:], self.red_pieces[:], self.middle_card, self.bk, self.rk]
        if action[0] in self.blue_pieces:
            if(action[0] == copies[5]):
                copies[5] = action[1]
            copies[0].remove(action[0])
            copies[0].append(action[1])
            if action[1] in self.red_pieces:
                copies[3].remove(action[1])
            copies[1].remove(action[2])
            copies[1].append(self.middle_card)
            copies[4] = action[2]
        else:
            if(action[0] == copies[6]):
                copies[6] = action[1]
            copies[3].remove(action[0])
            copies[3].append(action[1])
            if action[1] in self.blue_pieces:
                copies[0].remove(action[1])
            copies[2].remove(action[2])
            copies[2].append(self.middle_card)
            copies[4] = action[2]

        return Game_State(copies[0], copies[3], copies[1], copies[2], copies[4], copies[5], copies[6])
    
    def get_actions(self, blue):
        actions = []
        temp = (0,0)
        if blue:
            for card in self.blue_cards:
                for piece in self.blue_pieces:
                    for move in card.squares:
                        temp = (piece[0] + move[0], piece[1] + move[1])
                        if temp not in self.blue_pieces and temp[0] in range(0,5) and temp[1] in range(0,5):
                            actions.append((piece, temp, card))
        else:
            for card in self.red_cards:
                for piece in self.red_pieces:
                    for move in card.squares:
                        temp = (piece[0] - move[0], piece[1] - move[1])
                        if temp not in self.red_pieces and temp[0] in range(0,5) and temp[1] in range(0,5):
                            actions.append((piece, temp, card))
        return actions
        
    def print_actions(self, actions):
        i = 0
        for a in actions:
            print(i, ": ", a[0:2], a[2].name)
            i+=1
    
    def board(self):
        grid = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        for unit in self.blue_pieces:
            if unit == self.bk:
                grid[4-unit[1]][unit[0]] = "B"
            else:
                grid[4-unit[1]][unit[0]] = "b"
        for unit in self.red_pieces:
            if unit == self.rk:
                grid[4-unit[1]][unit[0]] = "R"
            else:
                grid[4-unit[1]][unit[0]] = "r"
        output = '\n'
        for i in range(5):
            s = "|" + str(grid[i][0]) + " " + str(grid[i][1]) + " " + str(grid[i][2]) + " " + str(grid[i][3]) + " " + str(grid[i][4]) + "|"
            output += (s + "\n")
        return output



def manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def eval_function(game_state, blue):
    g = game_state
    # if blue:
    #     return len(game_state.blue_pieces)
    # return len(game_state.red_pieces)
    a = b = 0
    # if(len(game_state.blue_pieces) + len(game_state.red_pieces) < 5):
    #     a = manhattan_distance(g.bk, (2,4))
    #     b = manhattan_distance(g.rk, (2,0))
    if(g.game_over2(game_state)):
        return g.game_over2(game_state)
    if g.bk == (2,4):
        a = 5
    if g.rk == (2,0):
        b = 5
    return len(game_state.blue_pieces) + 20 * (g.bk in g.blue_pieces) + a - len(game_state.red_pieces) - 20 * (g.rk in g.red_pieces) - b

draw = r.sample(cards, 5)
# draw = [cards[1],cards[12],cards[10],cards[15],cards[5]]
g = Game_State([(0,0),(1,0),(2,0),(3,0),(4,0)],[(0,4),(1,4),(2,4),(3,4),(4,4)],[draw[0],draw[1]],[draw[2],draw[3]],draw[4],(2,0),(2,4))
# g = Game_State([(0,1),(1,1),(2,1),(2,0),(4,1)],[(0,3),(1,3),(2,3),(3,3),(2,4)],[draw[0],draw[1]],[draw[2],draw[3]],draw[4],(2,0),(2,4))

print(g.blue_cards[0].name,g.blue_cards[1].name)
print(g.red_cards[0].name,g.red_cards[1].name)
print(g.middle_card.name)

bot = minimax_bot(eval_function)
bot2 = minimax_bot2(eval_function)
bot3 = minimax_bot3(eval_function)
turn = True
print(g.board())
for i in range(60):
    if turn == False:
        action = bot3.play(g, not turn, 6)
        print(action[0:2], action[2].name)
        # print(g.red_pieces, g.rk)
        g = g.next_state(action)
        
        #Human Player
        # actions = g.get_actions(turn)
        # g.print_actions(actions)
        # a = input("Which Move")
        # g = g.next_state(actions[int(a)])
        
        
        print(g.board())
    else:
        #Random Player
        # actions = g.get_actions(turn)
        # c = actions[r.randint(0,len(actions)-1)]
        # print(c[0:2], c[2].name)
        # g = g.next_state(c)
        
        #Human Player
        # actions = g.get_actions(turn)
        # g.print_actions(actions)
        # a = input("Which Move")
        # g = g.next_state(actions[int(a)])
        
        #Minimax Robot Player
        action = bot3.play(g, not turn, 3)
        print(action[0:2], action[2].name)
        # print(g.red_pieces, g.rk)
        g = g.next_state(action)
        
        print(g.board())
    if g.game_over(g):
        break;
    print("-----------------------------")
    turn = not turn
