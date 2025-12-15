import numpy as np
import copy

class Deck():
    # All constants needed; deck, potential hands, colors, values

    def __init__(self):

        self.colors = ['S', 'H', 'D', 'C']
        self.values = np.arange(2,15)
        self.deck = {k: self.values.copy() for k in self.colors}
        self.rank = ['Fifth Highest Card','Fourth Highest Card','Third Highest Card', 'Second Highest Card', 'Highest Card','Pairs', 'Two Pairs', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush']
        self.value_names = [2,3,4,5,6,7,8,9,10,'Knight', 'Queen', 'King', 'Ace']

    def Shuffle(self):
        self.deck = {k: self.values.copy() for k in self.colors}


    def Draw(self, n=1): # definiera antal kort man drar
        
        cards = []

        for iteration in range(n): 
           
            new_deck = self.deck # assign deck

            col = self.colors[np.random.randint(4)] # random color and val, "shuffling"-process
            val_ind = np.random.randint(13)

            m=0

            while m == 0:

               if new_deck[col][val_ind] != 0: # Choose card
                   val = new_deck[col][val_ind]
                   new_deck[col][val_ind] = 0 # Remove from deck
                   m += 1


               else:
                   val_ind = np.random.randint(13) # Already taken - try again
                   col = self.colors[np.random.randint(4)]

            card = col,val
            self.deck = new_deck
            cards.append(card)

        return cards
    
    def PreFlop(self, num_of_players):
        players = {} 

        for i in range(num_of_players):
            hand = self.Draw(2)
            players[f'player_{i+1}'] = hand # Create dic of players w different hands
    
        return players

    def Flop(self):
        flop = self.Draw(3) 
        return flop
    
    def Turn(self, table):
        table = table.copy()
        table.extend(self.Draw(1))
        return table
    
    def River(self, table):
        table = table.copy()
        table.extend(self.Draw(1))
        return table






