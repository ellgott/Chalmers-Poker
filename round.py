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
                p += 1
                continue

            bank = self.player_bank[player]
            hand = self.players_hands[player]


            if p == 0 and first_round==True: # If nothing happened before, first round
                blind = self.small_blind
                self.actions[player] = [blind]
                self.player_bank[player] = bank - blind
                self.pot += blind
                print(f"{player} has the small blind.")
            if p == 1 and first_round==True: # Second player to the left gets big
                blind = self.big_blind
                self.actions[player] = [blind]
                self.player_bank[player] = bank - blind
                self.pot += blind
                print(f"{player} has the big blind.")

            if p > 1 or first_round==False:

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

                if move == "Call":
                    self.actions[player].append(diff)
                    self.player_bank[player] = bank - diff
                    self.pot += diff
                    print(f"{player} calls.")

                if isinstance(move, float):
                    self.actions[player].append(diff+move)
                    self.player_bank[player] = bank - diff - move
                    self.pot += diff + move
                    print(f"{player} raises with {move}!")

            
            p += 1


    def PreFlop(self):

        print("PreFlop!")
        print(f"Order of players: {self.order_of_players}")

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

        print(f'Pot size: {self.pot}')

        if len(self.relevant_players) == 1: 
            self.player_bank[self.relevant_players[0]] += self.pot
            print(str(self.relevant_players[0]) + " wins due to the others folding.")

    
    def FlopRound(self):

        if len(self.relevant_players) < 2:
            return(str(self.relevant_players[0]) + " has won.")

        self.table = self._deck.Flop() # Flop on the table

        print("Flop!")
        print(self.table)

        self.Round()

        print(f'Pot size: {self.pot}')

        if len(self.relevant_players) == 1: 
            bank = self.player_bank[self.relevant_players[0]]
            self.player_bank[self.relevant_players[0]] += self.pot
            print(str(self.relevant_players[0]) + " wins due to the others folding.")
            return self.relevant_players[0]

    def TurnRound(self):
        if len(self.relevant_players) < 2:
            return(str(self.relevant_players[0]) + " has won.")

        self.table = self._deck.Turn(self.table) # Flop on the table

        print("Turn!")
        print(self.table)

        self.Round()

        print(f'Pot size: {self.pot}')

        if len(self.relevant_players) == 1: 
            bank = self.player_bank[self.relevant_players[0]]
            self.player_bank[self.relevant_players[0]] += self.pot
            print(str(self.relevant_players[0]) + " wins due to the others folding.")
            return self.relevant_players[0]


    def RiverRound(self):
        if len(self.relevant_players) < 2:
            return(str(self.relevant_players[0]) + " has won.")

        self.table = self._deck.River(self.table) # Flop on the table

        print("River!")
        print(self.table)

        self.Round()

        print(f'Pot size: {self.pot}')

        if len(self.relevant_players) == 1: 
            self.player_bank[self.relevant_players[0]] += self.pot
            print(str(self.relevant_players[0]) + " wins due to the others folding.")
            return self.relevant_players[0]
        
        else:
            hands = self._hands.copy()
            names = self.order_of_players.copy()

            for player, hand in zip(self.order_of_players, self._hands.keys()):
                if player not in self.relevant_players:
                    del hands[hand]
                    names.remove(player)

            key_list = list(hands.keys())
            
            for i in range(len(hands)):
                hands[f'player_{i+1}'] = hands.pop(key_list[i])
                    
            print('Showing cards...')
            for name,hand in zip(names, hands.keys()):
                print(f"{name} has cards {hands[hand]}!")
        
            check = Check(hands, self.table)
            winner_index, rank = check.Winner(Announce=True, player_names=names)

            if len(winner_index) == 1:
                winner = names[winner_index[0]]
                self.player_bank[winner] += self.pot
                print(f"The winner is {winner} due to {rank}!")

            else:
                winners = []
                for index in winner_index:
                    player = self.order_of_players[index]
                    winners.append(player)
                    self.player_bank[player] += self.pot/len(winner_index)
                print(f"The pot is split between {winners} due to {rank}!")

    def NewRound(self):

        self.order_of_players = self.order_of_players[-1:] + self.order_of_players[:-1]
        print(f"Players' bank:")
        print(f"{self.player_bank}")
        print(f"Next Round")

    def CompleteRound(self):
        self.PreFlop()
        self.FlopRound()
        self.TurnRound()
        self.RiverRound()
        self.NewRound()








        



    
        
#Benny/Lisa vinner, fel prioritetsorning


# Split pot - om pengarna tar slut
# har ännu ej nått river
# Inget lägsta värde för banken



        


    
        
    

    














