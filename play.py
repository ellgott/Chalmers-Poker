import numpy as np
from deck import Deck
from check import Check
from round import Game

game = Game()
print("A New Game of Poker!")
print(f"Players: {game.names_of_players}")

game.CompleteRound()

