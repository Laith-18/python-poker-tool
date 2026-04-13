def get_card_image_from_file(card):

    #Mapping for cards
    ranks = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10', 'j': 'jack', 'q': 'queen', 'k': 'king', 'a': 'ace'}
    suits = {'c': 'clubs', 'd': 'diamonds', 'h': 'hearts', 's': 'spades'}

    rank = card[0]
    suit = card[1]

    return f"{ranks[rank]}_of_{suits[suit]}.png" #Load the image
