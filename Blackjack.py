import random
import copy

bettings = 100
dealer_score = 0
player_score = 0

suits = ('♥', '♦', '♠', '♣')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

#creating card class#
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + self.suit

#creating Deck, shuffle function and single dealing#
class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list#
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_comp = '' #strating competition deck empty#
        for card in self.deck:
            deck_comp += '\n' + card.__str__() #add each card object;s strin#
        return 'The deck has' + deck_comp
            
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card

#creating Hand
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
        # need the rank if a split should ocour
        self.rankin = ''
        self.rankin2 = ''

    def add_card(self,card):
        self.cards.append(card)
        if len(self.cards) > 0 and len(self.cards) <= 1:
            self.rankin = card.rank
        elif len(self.cards) > 1 and len(self.cards) <= 2:
            self.rankin2 = card.rank
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    

def aceChecker(hand):
    while hand.value > 21 and hand.aces > 0:
        hand.value -= 10
        hand.aces -= 1

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

def splitPlay(dealer_cards, dealer_cards2, player_cards, player_cards2, currentBet, deck):
    global bettings, player_score, dealer_score
    leftHand = True
    rightHand = True
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
            print("You have", bettings, "to play for")

        bet_input = input("How much do you wonna bet?")
        currentBet = int(bet_input)
        
        # Checking if bet is valid
        if currentBet > bettings:
            print("You dont have that amount to gamble for!")
        else:
            print("\n----Dealing the cards----")
            # Dealer Cards
            while len(dealer_hand.cards) != 2:
                dealer_hand.add_card(deck.deal())
                if len(dealer_hand.cards) == 2:
                    print("\nDealer has X &", dealer_hand.cards[1])

            # Player Cards
            while len(player_hand.cards) != 2:
                player_hand.add_card(deck.deal())
                if len(player_hand.cards) == 2:
                    print("You have ", *player_hand.cards, ". Thats a total of:", player_hand.value, "\n" )

            # Splitting Pairs
            if player_hand.rankin == player_hand.rankin2:
                split_action = input("Player has a pair. Do you want to plit? (type Y/N)")
                if currentBet + currentBet > bettings:
                    print("You dont have enough money to play split" + "\n" + "Continueing with regular play")
                elif split_action == "Y" and currentBet + currentBet < bettings:
                    player_hand2.cards.append(player_hand.cards[1])
                    player_hand.cards.remove(player_hand.cards[1])
                    print("Players left hand is now:", *player_hand.cards, "and their right hand is:", *player_hand2.cards)
                    while len(dealer_hand2.cards) != 2:
                        dealer_hand2.add_card(deck.deal())
            # Double Down
            if player_hand.value in (9,10,11):
                double_input = input("Do you want to double down? (Y/N)") 
                if double_input == "Y" and (currentBet+currentBet) <= bettings:
                    currentBet += currentBet
                elif double_input == "Y" and (currentBet+currentBet) > bettings:
                    print("You dont have the money to double down! \n Continueing regular play")
                else:
                    print("You have rejected to doubledown")

            print("\n----Your turn----\n")

            # if the dealer starts with 2 aces
            aceChecker(dealer_hand)
            
            # regularPlay function called
            if not player_hand2.cards:
                regularPlay(dealer_hand, player_hand, currentBet, deck)

            # splitPlay function called
            if player_hand2.cards:
                splitPlay(dealer_hand, dealer_hand2, player_hand, player_hand2, currentBet, deck)

            # If user has no more money on balance
            if bettings <= 0:
                    print("You have no more money to play for... GOODBYE!") 
        
def main():
    play_game()

if __name__ == "__main__":
    main()



    
