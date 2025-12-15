
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

    def MyTurn(self, num_of_players, actions, diff, hand, table=0):

        me = {'player_1': hand}

        control = Control(me, table)

        rank = control.Total(Announce=False)

        if diff > 0:
            answer = self.Fold()
        else:
            answer = self.Call(diff)

        return answer
