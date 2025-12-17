import numpy as np
from check import Check as Control

class Player():

    def __init__(self):
        self.bank = 100
        self.confidence = 1

    def Raise(self, value):
        self.bank = self.bank - self._diff - value
        return value
    
    def Call(self):
        self.bank = self.bank - self._diff
        return "Call"
    
    def Fold(self):
        return "Fold"

    def MyTurn(self, num_of_players, actions, diff, hand, table=0): # These are the variables (actions are raises, calls, and folds)

        self._diff = diff
        me = {'player_1': hand}

        border = 1

        control = Control(me, table)

        self.rank = control.Total(Announce=False)[0]

        self.confidence = 0

        if table == 0: # PreFlop Judgement

            self._vals = hand[0][1], hand[1][1]
            self._colors = hand[0][0], hand[1][0]

            for val in range(10,15):
                if val in self._vals:
                    self.confidence += val # If high cards, close to each other: Very nice position (altough different color subtraction)
                    
            if self._colors[0] == self._colors[1]:
                self.confidence += 5 # same color bonus

            if self._vals[0] == self._vals[1]:
                self.confidence += self._vals[0]*2 + 10 # pair bonus, example two twos gives 4 in value and 
            
            if self.confidence > 30 and diff < 33: # Don't raise too aggressively at the PreFlop, wants bots to join
                return self.Raise(self.bank/3 - diff)
        
            if self.confidence <= 30 and self.confidence > 10: # Joins with high hopes
                if diff < 15:
                    return self.Call()
                else:
                    return self.Fold()
            
            if self.confidence <= 10:
                if diff > 0:
                    return self.Fold()
                else:
                    return self.Call()
                
                
        if table != 0:

            for index in range(len(control.rank)):
                val = self.rank[len(control.rank)-1-index]
                if val != 0 and index<5:
                    self.confidence += (8-index)*10
                if val != 0 and index>5 and index <7:
                    self.confidence += val*(7-index)+5

            if self.confidence >= 40:
                border = int(self.bank)
            if self.confidence >= 30 and self.confidence < 40:
                border = 50
            if self.confidence < 30 and self.confidence >= 15:
                border= 15
            if self.confidence < 15:
                border = 0

            if diff > border:
                return self.Fold()
            if diff == border:
                return self.Call()
            if diff < border:
                return int(border)-diff

        
