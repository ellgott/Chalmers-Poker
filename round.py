import numpy as np
from deck import Deck
from check import Check
import os
import importlib.util
import random
import copy


class Game():

    def __init__(self, buyin=100, small_blind=3, big_blind=6):

        self.small_blind = small_blind
        self.big_blind = big_blind

        HOME = os.getcwd()
        PLAYERS = file_path = os.path.join(HOME, "Players")

        self.player_classes = {} # Gather classes of players from modules in dictionary

        for filename in os.listdir(PLAYERS):
            if "player" in filename:
                module_name = filename[:-3] # Name of file (-.py)

                file_path = os.path.join(PLAYERS, filename)

                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                PlayerClass = module.Player
                self.player_classes[module_name] = PlayerClass()


        self.num_of_players = len(self.player_classes.keys()) # How many players participate?
        self.names_of_players = self.player_classes.keys() # Gathered player names
        self.order_of_players = random.sample(self.names_of_players, k=len(self.names_of_players)) # Randomize the order

        self.player_bank = {}

        for key in self.names_of_players:
            self.player_bank[key] = buyin # Define the buy-in


    def CheckingIn(self): # Peaking at the hands
        check = Check(self._hands, self.table)
        check.Total(Announce=True)


    def Round(self):

        p = 0 # Will decide index of player
        m = 0 # Will break loop

        while m == 0: # Start a while loop, if FIRST ROUND - a bit different rules

            i = p % (self.num_of_players) # Iterating between 0 and num_of_players, i enumerates
            player = self.order_of_players[i] # Choosing the correct player

            if self.actions[player] == []:
                first_round = True
            else:
                first_round = False

            if "Fold" in self.actions[player]:
                #print("One too many loops")
                continue

            bank = self.player_bank[player]
            hand = self.players_hands[player]

            if first_round == True:

                if p == 0: # If nothing happened before, first round
                    blind = self.small_blind
                    self.actions[player] = [blind]
                    self.player_bank[player] = bank - blind
                    self.pot += blind
                    print(f"{player} has the small blind.")

                if p == 1: # Second player to the left gets big
                    blind = self.big_blind
                    self.actions[player] = [blind]
                    self.player_bank[player] = bank - blind
                    self.pot += blind
                    print(f"{player} has the big blind.")

            else:

                bet = 0

                for plp in self.relevant_players:
                    if "Fold" not in self.actions[plp]:
                        if np.sum(self.actions[plp]) > bet:
                            bet = np.sum(self.actions[plp])
                            max_player = plp

                bet = sum(self.actions[max_player])
                diff = bet - sum(self.actions[player])

                if diff == 0 and p > self.num_of_players: # If the checking has gone a full circle

                    break
                    m +=1
                print("Betting...")
                # Here is where the actual decision making happens
                move = self.player_classes[player].MyTurn(self.num_of_players, self.actions, diff, hand, self.table)

                if move == "Fold":
                    self.actions[player].append("Fold")
                    print(f"{player} folds!")

                    if player in self.relevant_players:
                        self.relevant_players.remove(player)

                if move == "Check":
                    self.actions[player].append(diff)
                    self.player_bank[player] = bank - diff
                    self.pot += diff
                    print(f"{player} checks.")

                if isinstance(move, float):
                    self.actions[player].append(diff+move)
                    self.player_bank[player] = bank - diff - move
                    self.pot += diff + move
                    print(f"{player} raises with {move}!")

            
            p += 1


    def FirstRound(self):

        self._deck = Deck()
        self._hands = self._deck.PreFlop(self.num_of_players)
        self.table = 0

        self.players_hands = {}
        self.relevant_players = self.order_of_players.copy()

        for player, hand in zip(self.order_of_players, self._hands.keys()):
            self.players_hands[player] = self._hands[hand] # Creating hands of this round

        self.actions = {}
        for key in self.order_of_players:
            self.actions[key] = []

        self.pot = 0 # POT STARTS AT 0

        self.Round()

        if len(self.relevant_players) == 1: 
            self.player_bank[self.relevant_players[0]] += self.pot
            print(str(self.relevant_players[0]) + " wins due to the others folding.")

    
    def FlopRound(self):

        if len(self.relevant_players) < 2:
            return(str(self.relevant_players[0]) + " has already won.")

        self.table = self._deck.Flop() # Flop on the table

        self.Round()

        if len(self.relevant_players) == 1: 
            bank = self.player_bank[self.relevant_players[0]]
            self.player_bank[self.relevant_players[0]] = bank + 1
            print(str(self.relevant_players[0]) + " wins due to the others folding.")

        
game = Game()
print(game.order_of_players)
game.FirstRound()
game.FlopRound()
game.CheckingIn()
print("Bank:")
print(game.player_bank)



        



    
        



# Split pot - om pengarna tar slut
# har ännu ej nått river
# Inget lägsta värde för banken



        


    
        
    

    














