deck.py contains the deck class. It can be drawn from and reshuffled and used for dealing.
 - returns preflop as a dictionary {'player_1': [('S', 14), ('S', 3)], 'player_2': [('H', 11), ('C', 2)]}
 - returns each card with two elements; color and valor, sorted in an array: [('S', 12), ('S', 10), ('S', 4), ('H', 2), ('D', 4)]


check.py contains the class Check() made for interpretting the result of the game according to the rules of Texas Hold'Em
- returns winner indexes as an array of size one (winner) or larger (split pot)
- prints results as it checks but this can be manuevered
- bugs might be found...

Check.Winner() returns scalar or array with the index of the player who has won
