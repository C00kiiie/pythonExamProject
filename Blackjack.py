import random
import copy

# Variables to keep track of a players money to play for (bettings)
# and two variables (dealer_score & player_score) that keep track of the overall score between the player and the dealer. 
# These will increment every time a game is over.
bettings = 100
dealer_score = 0
player_score = 0

# Suits, Ranks and Values are all variables that hold multiple values. These are used in Card, Deck, Hand class.
suits = ('♥', '♦', '♠', '♣')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

# Creating Card class.
# This class is used to create cards.
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + self.suit

# Creating Deck class 
# This class is used to shuffle the deck, and dealing cards out of the deck.
class Deck:
    def __init__(self):
        self.deck = []  # Create an empty list, and fill it out with suits and ranks, from the Card class.
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    # A function that uses the Random library to shuffle a deck.        
    def shuffle(self):
        random.shuffle(self.deck)
        
    # A function that deal cards, and then uses .pop(), to 'eliminate' the cards from the deck.    
    def deal(self):
        single_card = self.deck.pop()
        return single_card

# Creating Hand class. 
# This class is later used as a way to deal- and keep track of a player/dealer hand.
# The Hand class keeps track of cards and the totalt value of them. Also keeps track of aces.
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value, so that we can add to it later.
        self.aces = 0    # add an attribute to keep track of aces

        # adds variables that stores cards and their rank. Used if a split should ocour.
        self.rankin = ''
        self.rankin2 = ''

    # add_card(), is used for the actual dealing of cards to a players hand.
    def add_card(self,card):
        self.cards.append(card)
        if len(self.cards) > 0 and len(self.cards) <= 1: # adds the first drawn card to rankin
            self.rankin = card.rank
        elif len(self.cards) > 1 and len(self.cards) <= 2: # adds the second drawn card to rankin2
            self.rankin2 = card.rank
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
# A function to check a hand for aces, if a hands value eceets 21.
def aceChecker(hand):
    while hand.value > 21 and hand.aces > 0:
        hand.value -= 10
        hand.aces -= 1


### Below functions (regularPlay, splitPlay and play_game) are the main part of this Blackjack game ###
### play_game() includes the dealing of cards and betting, etc. ###
### From play_game(), other functions are called, such as regularPlay and splitPlay ###

# regularPlay is if the player isn't dealt to of the same cards in the beginning of the game.
# this function goes through a normal game of Blackjack, without any further gameplay-elements.
def regularPlay(dealer_cards, player_cards, currentBet, deck):
    global bettings, player_score, dealer_score
    
    # Sum of the Player cards
    while player_cards.value < 21:
        action_taken = str(input("Do you want to stay or hit? (type hit / stay)"))
        if action_taken == "hit":
            player_cards.add_card(deck.deal())
            if player_cards.value > 21:
                aceChecker(player_cards)
            print("\nYou now have a total of", player_cards.value,"from these cards ", *player_cards.cards)
        elif action_taken == "stay":
            print("\nYou have a total of", player_cards.value,"with", *player_cards.cards)
            print("The dealer has a total of", dealer_cards.value," with ", *dealer_cards.cards)
            while dealer_cards.value < 17:
                dealer_cards.add_card(deck.deal())
                if dealer_cards.value > 21:
                    aceChecker(dealer_cards)
                print("Dealer is going for another card.","\n","He drew a: ", dealer_cards.cards[-1])
                print("The dealer has a total of ", dealer_cards.value," with ", *dealer_cards.cards)
            if dealer_cards.value > 21:
                 # 2) Add 1 for player
                player_score += 1
                bettings = bettings + currentBet
                aceChecker(dealer_cards)
                print("Dealer BUSTED!")
                break
            elif dealer_cards.value >= player_cards.value:
                # 2) Add 1 for dealer
                dealer_score += 1
                bettings = bettings - currentBet
                print("Dealer wins!")
                break
            elif dealer_cards.value == 21:
                # 2) Add 1 for dealer
                dealer_score += 1
                bettings = bettings - currentBet
                print("Dealer has 21 and wins!")
                break
            else:
                # 2) Add 1 for player
                player_score += 1
                bettings = bettings + currentBet
                print("You win!")
                break

    if player_cards.value > 21:
        # 2) Add 1 for dealer
        dealer_score += 1
        bettings = bettings - currentBet
        print("You BUSTED! Dealer wins.")
    elif player_cards.value == 21:
        # 2) Add 1 for player
        player_score += 1
        bettings = bettings + currentBet
        print("You have BLACKJACK! You Win!! 21")

    # Text to inform the player of the status of the game and iterate over the total_games
    print("\n----Current scores----\n")
    print("Dealer: " + str(dealer_score) + " games" + " - to - You: " + str(player_score) + " games")

# splitPlay is if the player should receive two of the same cards in the beginning of the game. 
# if the player then chooses to 'split' his hand, the gameplay will continue inside the splitPlay() function.
def splitPlay(dealer_cards, dealer_cards2, player_cards, player_cards2, currentBet, deck):
    global bettings, player_score, dealer_score
    leftHand = True # Used to check if user is done with left hand game
    rightHand = True # Used to check if user is done with right hand game
    print("You have a bet of: " + str(currentBet) + "for both of your hands")
    while leftHand and rightHand:
        #Left hand gameplay
        while leftHand and player_cards.value < 21:
            action_taken = str(input("Do you want to stay or hit? (type hit / stay)"))
            if action_taken == "hit":
                player_cards.add_card(deck.deal())
                if player_cards.value > 21:
                    aceChecker(player_cards)
                print("You now have a total of ", player_cards.value," from these cards ", *player_cards.cards)
            elif action_taken == "stay":
                print("You now have a total of ", player_cards.value," from these cards ", *player_cards.cards)
                print("The dealer has a total of ", dealer_cards.value," from these cards ", *dealer_cards.cards)
                while dealer_cards.value < 17:
                    dealer_cards.add_card(deck.deal())
                    if dealer_cards.value > 21:
                        aceChecker(dealer_cards)
                    print("Dealer is going for another card.","\n","He drew a: ", dealer_cards.cards[-1])
                    print("The dealer has a total of ", dealer_cards.value," from these cards ", *dealer_cards.cards)
                if dealer_cards.value > 21:
                    # 2) Add 1 for player
                    player_score += 1
                    bettings = bettings + currentBet
                    print("Dealer BUSTED!")
                    leftHand = False
                    break
                elif dealer_cards.value >= player_cards.value:
                    # 2) Add 1 for dealer
                    dealer_score += 1
                    bettings = bettings - currentBet
                    print("Dealer wins!")
                    leftHand = False
                    break
                else:
                    # 2) Add 1 for player
                    player_score += 1
                    bettings = bettings + currentBet
                    print("You win!")
                    leftHand = False
                    break
        # Ends gameplay if a player hits 21 or above        
        if player_cards.value > 21:
                print("Player has a total of: ",player_cards.value,"That means the player busted! Dealer wins")
                leftHand = False
                dealer_score += 1
                bettings = bettings - currentBet
        elif player_cards.value == 21:
                print("Player has 21! THATS A BLACKJACK! Player wins!!!")
                leftHand = False
                player_score += 1
                bettings = bettings + currentBet
        
        #Right hand gameplay
        print("Time to play the right hand")
        print("The dealer has: X &", dealer_cards2.cards[1])
        while rightHand and player_cards2.value < 21:
            action_taken = str(input("Do you want to stay or hit? (type hit / stay)"))
            if action_taken == "hit":
                player_cards2.add_card(deck.deal())
                if player_cards2.value > 21:
                    aceChecker(player_cards2)
                print("You now have a total of ", player_cards2.value," from these cards ", *player_cards2.cards)
            elif action_taken == "stay":
                print("You now have a total of ", player_cards2.value," from these cards ", *player_cards2.cards)
                print("The dealer has a total of ", dealer_cards2.value," from these cards ", *dealer_cards2.cards)
                while dealer_cards2.value < 17:
                    dealer_cards2.add_card(deck.deal())
                    if dealer_cards2.value > 21:
                        aceChecker(dealer_cards2)
                    print("Dealer is going for another card.","\n","He drew a: ", dealer_cards2.cards[-1])
                    print("The dealer has a total of ", dealer_cards2.value," from these cards ", *dealer_cards2.cards)
                if dealer_cards2.value > 21:
                    # 2) Add 1 for player
                    player_score += 1
                    bettings = bettings + currentBet
                    print("Dealer BUSTED!")
                    leftHand = False
                    break
                elif dealer_cards2.value >= player_cards2.value:
                    # 2) Add 1 for dealer
                    dealer_score += 1
                    bettings = bettings - currentBet
                    print("Dealer wins!")
                    leftHand = False
                    break
                else:
                    # 2) Add 1 for player
                    player_score += 1
                    bettings = bettings + currentBet
                    print("You win!")
                    leftHand = False
                    break
        # Ends gameplay if a player hits 21 or above        
        if player_cards2.value > 21:
                print("Player has a total of: ",player_cards2.value,"That means the player busted! Dealer wins")
                leftHand = False
                dealer_score += 1
                bettings = bettings - currentBet
        elif player_cards2.value == 21:
                print("Player has 21! THATS A BLACKJACK! Player wins!!!")
                leftHand = False
                player_score += 1
                bettings = bettings + currentBet

    if leftHand == False and rightHand == False:
        print("Current scores: ")
        print("Dealer: " + str(dealer_score) + " games" + " - to - You: " + str(player_score) + " games")

# play_game() is the only function called in main(). play_game() is where a game starts, and ends. 
# Here shuffeling, betting, splitting and double down is handled. Resolving in other function being called.
def play_game():
    # New variables 
    global bettings, player_score, dealer_score

    # New text for the game
    print("\nWelcome to Blackjack. \nAfter each game you can see have many games you've won or lost")

    while bettings > 0:
        # Dealer cards
        dealer_hand = Hand()
        dealer_hand2 = Hand()
        # Player cards
        player_hand = Hand()
        player_hand2 = Hand()
        # Making & shufling deck
        deck = Deck()
        deck.shuffle()

        # Placing bets
        if not player_hand.cards:
            print("\n----New game----\n")
            print("You have", str(bettings) + "$ to play for")

        while True:
            try:
                bet_input = input("How much do you wonna bet?")
                currentBet = int(bet_input)
                break
            except ValueError:
                print("No valid integer! Please try again...")

        # Checking if bet is valid
        if currentBet > bettings:
            print("You dont have that amount to gamble for!")
        else:
            print("\n----Dealing the cards----")

            # Dealer cards dealt, and not showing the first.
            while len(dealer_hand.cards) != 2:
                dealer_hand.add_card(deck.deal())
                if len(dealer_hand.cards) == 2:
                    print("\nDealer has X &", dealer_hand.cards[1])

            # Player cards dealt, and then shown.
            while len(player_hand.cards) != 2:
                player_hand.add_card(deck.deal())
                if len(player_hand.cards) == 2:
                    print("You have ", *player_hand.cards, ". Thats a total of:", player_hand.value, "\n" )

            # Splitting Pairs. If a player should receive two cards of the same rank, the option to split will be given.
            if player_hand.rankin == player_hand.rankin2:
                split_action = input("Player has a pair. Do you want to plit? (type Y/N)")
                if currentBet + currentBet > bettings:
                    print("You dont have enough money to play split" + "\n" + "Continueing with regular play")
                elif split_action == "Y" and currentBet + currentBet < bettings:
                    player_hand2.cards.append(player_hand.cards[1]) # Appending card to a second hand.
                    player_hand.cards.remove(player_hand.cards[1]) # Removing card from the first hand.
                    print("Players left hand is now:", *player_hand.cards, "and their right hand is:", *player_hand2.cards)
                    while len(dealer_hand2.cards) != 2: # Dealing 2 cards to the dealer. So that he also has two hands.
                        dealer_hand2.add_card(deck.deal())

            # Double Down. If the value of a hand should be between 9 and 11, give the player the option to double down.
            if player_hand.value in (9,10,11): 
                double_input = input("Do you want to double down? (Y/N)") 
                if double_input == "Y" and (currentBet+currentBet) <= bettings: # If the player is able to perform action
                    currentBet += currentBet
                elif double_input == "Y" and (currentBet+currentBet) > bettings: # If the player does not have the enough money to perform action
                    print("You dont have the money to double down! \nContinueing regular play")
                else:
                    print("You have rejected to doubledown") 

            print("\n----Your turn----\n")

            # if the dealer starts with 2 aces. 
            # This needs to be done, so that the dealer dosn't automaticly loose when it is his turn (11+11).
            aceChecker(dealer_hand)
            
            # regularPlay function called. If player_hand2 is an empty list.
            if not player_hand2.cards:
                regularPlay(dealer_hand, player_hand, currentBet, deck)

            # splitPlay function called. If player_hand2 is NOT an empty list.
            if player_hand2.cards:
                splitPlay(dealer_hand, dealer_hand2, player_hand, player_hand2, currentBet, deck)
    
            # If user has no more money on balance
            if bettings <= 0:
                print("You have no more money to play for... GOODBYE!") 

        # When a game is over, give the user a option to replay or leave the game.
        replay_input = input("\nWonna replay? (Y/N)")
        if(replay_input == "Y"):
            if(bettings == 0):
                print("Nice try! You dont have anything left to play for... GET OUT'a HERE!!!\n")
            pass
        else:
            print("Thanks for playing! Your leaving the table, with a sum of: " + str(bettings) + "$\n")
            break
     

def main():
    play_game()

if __name__ == "__main__":
    main()



    
