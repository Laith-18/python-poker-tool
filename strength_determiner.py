#This module evaluates a poker hand's strength by combining the player's hand and community cards.
#Returns a strength value from 0 (high card) to 9 (straight flush) based on standard poker rankings.
from collections import Counter # Importing Counter from collections module to count occurrences of elements in a list

def eval_hand(hand1,com_cards): # Function to evaluate the strength of a poker hand
    #Evaluates the strength of a poker hand.

    #Parameters:
    #    hand1 (list): List of two card tuples for the player (e.g., [('a', 's'), ('k', 'h')]).
    #    com_cards (list): List of five community card tuples.

    #Returns:
    #    int: An integer from 0 to 9 representing the hand strength.

    # Combine the player's hand and community cards
    hand1 = hand1 + com_cards 
    
    # Convert card ranks to values and extract suits
    ranks1 = [rank_to_value(card[0]) for card in hand1] # Convert card ranks to numerical values
    suits1 = [card[1] for card in hand1] # Extract suits from the cards

    # Count the occurrences of each rank and suit
    rank_counts1 = Counter(ranks1) # Count the occurrences of each rank
    counts1 = rank_counts1.values() # Convert the counts to a list
    suits_counts1 = Counter(suits1) # Count the occurrences of each suit

    # Determine if there is a flush (5 or more cards of the same suit)
    flush1 = max(suits_counts1.values()) >= 5

    # Determine if there is a straight (5 consecutive cards)
    rank_set1 = set(ranks1) # Convert the list of ranks to a set to remove duplicates
    rank_list1 = sorted(rank_set1, reverse=True) # Sort the ranks in descending order
    straight1 = any(rank_list1[i:i+5] == list(range(rank_list1[i], rank_list1[i]-5, -1)) for i in range(len(rank_list1) - 4))
    #any function returns true if any element in the iterable statement is true, otherwise it returns false
    #for i in range(len(rank_list1)-4) iterates through rank_list1, and the -4 ensures that there is not a index error, as there are 5 cards
    #rank_list[i:i+5] checks elements to see if they form a straight, starting at index i.
    #list(range(rank_list1[i], rank_)list[i]-5, -1), gens a decending list of numbers, pattern for a straight
    #checks if the 5 cards array pattern matches the pattern of the decending list, if so it is a straight   

    # Determine the strength of the hand
    if straight1 and flush1:
        strength = 9
    elif 4 in counts1:
        strength = 8
    elif 3 in counts1 and 2 in counts1:
        strength = 7
    elif flush1:
        strength = 6
    elif straight1:
        strength = 5 
    elif 3 in counts1:
        strength = 4
    elif list(counts1).count(2) == 2:
        strength = 3
    elif 2 in counts1:
        strength = 2
    else:
        strength = 0
    return strength
    # Output: strength value from 0 to 9
    # The strength value is based on standard poker rankings:

def rank_to_value(rank):
    # Convert card rank to numerical value
    if rank == 'a':
        return 14
    elif rank == 'k':
        return 13
    elif rank == 'q':
        return 12
    elif rank == 'j':
        return 11
    else:
        return int(rank)
    
    


