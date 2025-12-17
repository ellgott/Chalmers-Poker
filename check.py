import numpy as np
from deck import *

class Check():

    def __init__(self, players, table=0):
        self.colors = ['S', 'H', 'D', 'C']
        self.values = np.arange(2,15)
        self.deck = {k: self.values.copy() for k in self.colors}
        self.rank = ['Fifth Highest Card','Fourth Highest Card','Third Highest Card', 'Second Highest Card', 'Highest Card','Pairs', 'Two Pairs', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush']
        self.value_names = [2,3,4,5,6,7,8,9,10,'Knight', 'Queen', 'King', 'Ace']
        self.players = players
        self.table = table


    def Pairs(self, Announce=True, player_names=0):

        players = self.players
        table = self.table

        players_ranks = np.zeros((len(players),len(self.rank)))

        for i in range(len(players)):

            rank_list = np.zeros(len(self.rank)) # Here results will be added througout the code

            hand = [players[f'player_{i+1}'][0][1], players[f'player_{i+1}'][1][1]]

            if table != 0:
                for j in range(len(table)):
                    hand.append(table[j][1])
            
            duplicates = [c for c in set(hand) if hand.count(c) == 2]

            if duplicates:
            
                if len(duplicates) >= 2:
                    two_pair_value, single_pair_value = np.unique(duplicates)[-1], np.unique(duplicates)[-2]
                    rank_list[6] = two_pair_value
                    rank_list[5] = single_pair_value # In case of two pair, second highest is put as single pair
                    
                    if Announce:
                        if player_names == 0:
                            print(f'Player {i+1:.0f} has Two Pairs in {self.value_names[two_pair_value-2]}s and {self.value_names[single_pair_value-2]}s')
                        else:
                            print(f'{player_names[i]} has Two Pairs in {self.value_names[two_pair_value-2]}s and {self.value_names[single_pair_value-2]}s')
                else:
                    pair_value = np.max(duplicates)
                    rank_list[5] = pair_value # add pair

                    if Announce:
                        if player_names==0:
                            print(f'Player {i+1:.0f} has Pairs in {self.value_names[pair_value-2]}s')
                        else:
                            print(f'{player_names[i]} has Pairs in {self.value_names[pair_value-2]}s')


            players_ranks[i] = rank_list

        return players_ranks


    def Three(self, Announce=True, player_names=0):

        players = self.players
        table = self.table

        players_ranks = np.zeros((len(players),len(self.rank)))

        for i in range(len(players)):
            rank_list = np.zeros(len(self.rank)) # High card and pair check

            hand = [players[f'player_{i+1}'][0][1], players[f'player_{i+1}'][1][1]]

            if table != 0:
                for j in range(len(table)):
                    hand.append(table[j][1])
            
            triples = [c for c in set(hand) if hand.count(c) == 3]

            if triples:
                triple_val = np.max(triples)
                rank_list[7] = triple_val # add pair
                
                if Announce:
                    if player_names==0:
                        print(f'Player {i+1:.0f} has Three of a Kind in {self.value_names[triple_val-2]}s')
                    else:
                        print(f'{player_names[i]} has Three of a Kind in {self.value_names[triple_val-2]}s')


            players_ranks[i] = rank_list

        return players_ranks
    

    def Straight(self, Announce=True, player_names=0):

        players = self.players
        table = self.table

        players_ranks = np.zeros((len(players),len(self.rank)))

        for i in range(len(players)):

            straight = 0

            rank_list = np.zeros(len(self.rank))
            hand = [players[f'player_{i+1}'][0][1], players[f'player_{i+1}'][1][1]]

            if table != 0:
                for j in range(len(table)):
                    hand.append(table[j][1])


            for c in hand:
                latter = np.arange(int(c), int(c)+5)
                m = 0
                test_hand = np.unique(hand)

                for val in test_hand:
                    if val in latter:
                        m += 1

                if m == 5:
                    straight = np.max(latter)
                    if Announce:
                        if player_names==0:
                            print(f'Player {i+1:.0f} has Straight up to {np.max(latter)}!')
                        else:
                            print(f'{player_names[i]} has Straight up to {np.max(latter)}!')
                        break

            rank_list[8] = straight
            players_ranks[i] = rank_list

        return players_ranks
    

    def Flush(self, Announce=True, player_names=0):

        players = self.players
        table = self.table

        players_ranks = np.zeros((len(players),len(self.rank)))

        for i in range(len(players)):

            flush = 0
            rank_list = np.zeros(len(self.rank))

            hand_colors = [players[f'player_{i+1}'][0][0], players[f'player_{i+1}'][1][0]]

            if table != 0:
                for j in range(len(table)):
                    hand_colors.append(table[j][0])

            for c in set(hand_colors):
                if hand_colors.count(c) > 4:
                    flush = 1

                    if Announce:
                        if player_names==0:
                            print(f'Player {i+1:.0f} has Flush in {c}!')
                        else:
                            print(f'{player_names[i]} has Flush in {c}!')

            rank_list[9] = flush

            players_ranks[i] = rank_list

        return players_ranks
    

    def FullHouse(self, Announce=True, player_names=0):

        players = self.players
        table = self.table

        players_ranks = np.zeros((len(players),len(self.rank)))

        for i in range(len(players)):

            rank_list = np.zeros(len(self.rank))
            hand = [players[f'player_{i+1}'][0][1], players[f'player_{i+1}'][1][1]]
            if table != 0:
                for j in range(len(table)):
                    hand.append(table[j][1])
            thrice = [c for c in set(hand) if hand.count(c) == 3]

            if thrice:
                thrice = np.max(thrice)
                pair = [c for c in set(hand) if hand.count(c) > 1]
                pair = [c for c in set(pair) if c != thrice]

                if pair:
                    pair = np.max(pair)
                    rank_list[10] = thrice

                    if Announce:
                        if player_names==0:
                            print(f'Player {i+1:.0f} has Full House in {self.value_names[np.max(thrice)-2]}s and {self.value_names[np.max(pair)-2]}')
                        else:
                            print(f'{player_names[i]} has Full House in {self.value_names[np.max(thrice)-2]}s and {self.value_names[np.max(pair)-2]}')

            players_ranks[i] = rank_list

        return players_ranks
    

    def Four(self, Announce=True, player_names=0):

        players = self.players
        table = self.table

        players_ranks = np.zeros((len(players),len(self.rank)))

        for i in range(len(players)):
            rank_list = np.zeros(len(self.rank))
            hand = [players[f'player_{i+1}'][0][1], players[f'player_{i+1}'][1][1]]

            if table != 0:
                for j in range(len(table)):
                    hand.append(table[j][1])

            four = [c for c in set(hand) if hand.count(c) == 4]

            if four:
                rank_list[11] = np.max(four)
                val = np.max(four)

                if Announce:
                    if player_names==0:
                        print(f'Player {i+1:.0f} has Four of a kind in {self.value_names[val-2]}s')
                    else:
                        print(f'{player_names[i]} has Four of a kind in {self.value_names[val-2]}s')

            players_ranks[i] = rank_list

        return players_ranks


    def StraightFlush(self, Announce=True, player_names=0):

        players = self.players
        table = self.table
        
        players_ranks = np.zeros((len(players),len(self.rank)))

        for i in range(len(players)):

            straight = 0
            flush = 0

            rank_list = np.zeros(len(self.rank))
            hand = [players[f'player_{i+1}'][0][1], players[f'player_{i+1}'][1][1]]

            if table != 0:
                for j in range(len(table)):
                    hand.append(table[j][1])

            hand_colors = [players[f'player_{i+1}'][0][0], players[f'player_{i+1}'][1][0]]

            if table != 0:
                for j in range(len(table)):
                    hand_colors.append(table[j][0])

            for value in hand:
                latter = np.arange(int(value), int(value)+5)
                m = 0
                test_hand = np.unique(hand)

                for val in test_hand:
                    if val in latter:
                        m += 1

                if m >= 5:
                    straight = value+4

            if straight != 0:
                colors = []


                for vals, color in zip(hand, hand_colors):
                    latter = np.arange(straight-4, straight+1)

                    if vals in np.arange(straight-4, straight+1):
                        colors.append(color)


                for color in set(colors):
                    if colors.count(color) > 4:
                        flush = 1
                        flush_color = color

                if flush != 0:
                    rank_list[12] = straight
                    if Announce:
                        if player_names == 0:
                            print(f'{player_names[i]} has Straight Flush in {flush_color} up to {np.max(latter)}!')
                        else:
                            print(f'{player_names[i]} has Straight Flush in {flush_color} up to {np.max(latter)}!')

            players_ranks[i] = rank_list

        return players_ranks
    
    def Highest(self, Announce=True, player_names=0):
            
        players = self.players
        table = self.table
        players_ranks = np.zeros((len(players),len(self.rank)))
            
        for i in range(len(players)):

            rank_list = np.zeros(len(self.rank))

            hand = [players[f'player_{i+1}'][0][1], players[f'player_{i+1}'][1][1]]

            if table != 0:
                for j in range(len(table)):
                    hand.append(table[j][1])
            
            single_cards = [c for c in set(hand) if hand.count(c) == 1]
            high_cards = np.unique(single_cards)
            if len(high_cards) > 5:
                high_cards = high_cards[-5:]

            for j in range(len(high_cards)):
               rank_list[4-j] = high_cards[len(high_cards)-1-j]
            
            players_ranks[i] = rank_list

        return players_ranks
                    


    def Total(self, Announce=True, player_names=0):
        
        players_ranks = self.Pairs(Announce, player_names)
        players_ranks += self.Three(Announce, player_names)
        players_ranks += self.FullHouse(Announce, player_names)
        players_ranks += self.Flush(Announce, player_names)
        players_ranks += self.Straight(Announce, player_names)
        players_ranks += self.Four(Announce, player_names)
        players_ranks += self.StraightFlush(Announce, player_names)
        players_ranks += self.Highest(Announce, player_names)

        return players_ranks


    def Winner(self, Announce=True, player_names=0):

        players_ranks = self.Total(Announce=Announce, player_names=player_names)
        possible_hands = players_ranks.shape[1]
        num_of_players = players_ranks.shape[0]

        player_names = np.arange(1,num_of_players+1)[:, None]
        relevant_players = np.hstack([player_names, players_ranks]) # Name the players

        hc = 5 # Removing possible hands from the bottom, depending how many cards are involved in the hands

        for i in range(possible_hands):
            column = relevant_players[:,-(i+1)] # Goes from last row to second first
            winning_hands = []

            if all(val == 0 for val in column):
                continue

            highest = np.max(column)
            indexes = [i for i, val in enumerate(column) if val == highest]

            if len(indexes) == 1:
                #print(player_names)
                #print(f'The winner is player {relevant_players[indexes][0][0]:.0f} due to {self.rank[-(i+1)]}!')
                return indexes, self.rank[-(i+1)]

            else:
                relevant_players = relevant_players[indexes, :]

                if i in (0,3,4):
                    #print(f'Split pot between players due to {self.rank[-(i+1)]}') 
                    return indexes, self.rank[-(i+1)]

            if i == possible_hands-5: # We've reached card value comparison

                row = relevant_players[0,:]

                for j in range(len(row)): # Take one relevant player

                    val = row[len(row)-1-j]

                    if val != 0:
                        if j in [1, 6]: # If four of a kind, twopairs
                            hc = 1 # check this many
                            break
                        if j in [5]: # if three of a kind
                            hc = 2 # check this many
                            break
                        if j in [7]: # if pairs
                            hc = 3 # check this many
                            break

            if i == possible_hands - 6 + hc:
                #print(f'Split pot between players due to {self.rank[-(i+1)]}')
                return indexes, self.rank[-(i+1)]
                break
            
            if i == possible_hands-1:
                print(hc)
                #print(f'Split pot between players due to {self.rank[-(i+1)]}')
                return indexes, self.rank[-(i+1)]
                break


            
#players = {'player_1':  [('D', 8), ('D', 6)]}
    
#check = Check(players, table=[('C', 2), ('H', 6), ('C', 13)])
#print(check.Total())