import numpy as np
from deck import Deck
from check import Check

deck = Deck()

num_of_players = 6

players = deck.PreFlop(num_of_players)

flop = deck.Flop()

turn = deck.Turn(flop)

river = deck.River(turn)

print("PreFlop:")
print(players)
print("River")
print(river)


check_river = Check(players, river)

check_river.Winner(Announce=True)

