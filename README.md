INFORMATION
In the folder "Players" our bots will be pushed to. They need to be -.py files that contains a class Player(). This class needs to contain a function MyTurn() that accepts MyTurn(self, num_of_players, actions, diff, hand, table=0) as parametres but we can remove or add information. 
- num_of_players is a scalar
- actions is a dictionary where every players action this round is saved. Example is {'Benny': [3, 10, 10], 'Lisa': [3, 10, 'Fold'], where every element is what the champ raised with or called, i. e. Lisa lost 13 units before folding.
- diff is what is between your sum in the pot and what you need to match - in summary, what will be added if you call
- hand is your hand: for example [('H', 9), ('S', 10)]
- table will be added if there are cards on the table. They will look just as above, example is preflop [('H', 9), ('S', 10), ('D', 2)]

Every MyTurn() function needs to return either 'Fold' or 'Call' or a value which is what you would like to raise with ("on top" of calling)
You can name your players whatever you'd like. Try the play.py file and see how it can look like when Benny and Lisa plays.



(other information):

deck.py contains the deck class. It can be drawn from and reshuffled and used for dealing.
 - returns preflop as a dictionary {'player_1': [('S', 14), ('S', 3)], 'player_2': [('H', 11), ('C', 2)]}
 - returns each card with two elements; color and valor, sorted in an array: [('S', 12), ('S', 10), ('S', 4), ('H', 2), ('D', 4)]


check.py contains the class Check() made for interpretting the result of the game according to the rules of Texas Hold'Em
Check.Total() returns a matrix and or announces hands
- This can be used for interpreting hands and hand values! Check.Total() returns an array (in an array sadly so Check.Total()[0] is the array) with information about the cards you have on your hands 
- Check.Winner() returns winner indexes as an array of size one (winner) or larger (split pot)
- prints results as it checks but this can be manuevered
- bugs might be found... but it works well
