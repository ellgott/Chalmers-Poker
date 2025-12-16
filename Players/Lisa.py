import numpy as np
from check import Check as Control


class Player():

    def __init__(self):
        self.bank = 100

    def Raise(self, diff, value):
        self.bank = self.bank - diff - value
        return value
    
    def Call(self, diff):
        self.bank = self.bank - diff
        return "Call"
    
    def Fold(self):
        return "Fold"

    def MyTurn(self, num_of_players, actions, diff, hand, table=0): # These are the variables (actions are raises, calls, and folds)

        me = {'player_1': hand}

        control = Control(me, table)

        rank = control.Total(Announce=False)

        return self.Call(diff) # Return "Fold", "Call" or value ("Raise") and then raise is what you add on top of the Call
