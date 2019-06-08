import random

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
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

def regularPlay(dealer_cards, player_cards, currentBet):
    global bettings, player_score, dealer_score
    # Sum of the Dealer cards
    if sum(dealer_cards) == 21:
        # 2) Add 1 for dealer
        dealer_score += 1
        bettings = bettings - currentBet
        print("Dealer has 21 and wins!")
    elif sum(dealer_cards) > 21:
        # 2) Add 1 for player
        player_score += 1
        bettings = bettings + currentBet
        print("Dealer has busted!")

    # Sum of the Player cards
    while sum(player_cards) < 21:
        action_taken = str(input("Do you want to stay or hit?  "))
        if action_taken == "hit":
            player_cards.append(random.randint(1, 11))
            print("You now have a total of " + str(sum(player_cards)) + " from these cards ", player_cards)
        elif action_taken == "stay":
            print("You have a total of " + str(sum(player_cards)) + " with ", player_cards)
            print("The dealer has a total of " + str(sum(dealer_cards)) + " with ", dealer_cards)
            while sum(dealer_cards) < 17:
                dealer_cards.append(random.randint(1,11))
                print("Dealer is going for another card.","\n","He drew a: ", dealer_cards[-1])
                print("The dealer has a total of " + str(sum(dealer_cards)) + " with ", dealer_cards)
            if sum(dealer_cards) > 21:
                 # 2) Add 1 for player
                player_score += 1
                bettings = bettings + currentBet
                print("Dealer BUSTED!")
                break
            elif sum(dealer_cards) >= sum(player_cards):
                # 2) Add 1 for dealer
                dealer_score += 1
                bettings = bettings - currentBet
                print("Dealer wins!")
                break
            else:
                # 2) Add 1 for player
                player_score += 1
                bettings = bettings + currentBet
                print("You win!")
                break

    if sum(player_cards) > 21:
        # 2) Add 1 for dealer
        dealer_score += 1
        bettings = bettings - currentBet
        print("You BUSTED! Dealer wins.")
    elif sum(player_cards) == 21:
        # 2) Add 1 for player
        player_score += 1
        bettings = bettings + currentBet
        print("You have BLACKJACK! You Win!! 21")

    # Text to inform the player of the status of the game and iterate over the total_games
    print("Current scores: ")
    print("Dealer: " + str(dealer_score) + " games" + " - to - You: " + str(player_score) + " games")

def splitPlay(dealer_cards, dealer_cards2, player_cards, player_cards2, currentBet):
    global bettings, player_score, dealer_score
    leftHand = True
    rightHand = True
    print("You have a bet of: " + str(currentBet) + "for both of your hands")
    while leftHand and rightHand:
        #Left hand gameplay
        while leftHand and sum(player_cards) < 21:
            action_taken = str(input("Do you want to stay or hit?  "))
            if action_taken == "hit":
                player_cards.append(random.randint(1, 11))
                print("You now have a total of " + str(sum(player_cards)) + " from these cards ", player_cards)
            elif action_taken == "stay":
                print("You have a total of " + str(sum(player_cards)) + " with ", player_cards)
                print("The dealer has a total of " + str(sum(dealer_cards)) + " with ", dealer_cards)
                while sum(dealer_cards) < 17:
                    dealer_cards.append(random.randint(1,11))
                    print("Dealer is going for another card.","\n","He drew a: ", dealer_cards[-1])
                    print("The dealer has a total of " + str(sum(dealer_cards)) + " with ", dealer_cards)
                if sum(dealer_cards) > 21:
                    # 2) Add 1 for player
                    player_score += 1
                    bettings = bettings + currentBet
                    print("Dealer BUSTED!")
                    leftHand = False
                    
                elif sum(dealer_cards) >= sum(player_cards):
                    # 2) Add 1 for dealer
                    dealer_score += 1
                    bettings = bettings - currentBet
                    print("Dealer wins!")
                    leftHand = False
                    
                else:
                    # 2) Add 1 for player
                    player_score += 1
                    bettings = bettings + currentBet
                    print("You win!")
                    leftHand = False
                    
        # Ends gameplay if a player hits 21 or above        
        if sum(player_cards) > 21:
                print("Player has a total of: ",str(sum(player_cards)),"That means the player busted! Dealer wins")
                leftHand = False
                dealer_score += 1
                bettings = bettings - currentBet
        elif sum(player_cards) == 21:
                print("Player has 21! THATS A BLACKJACK! Player wins!!!")
                leftHand = False
                player_score += 1
                bettings = bettings + currentBet
        
        #Right hand gameplay
        print("Time to play the right hand")
        print("The dealer has: X &", dealer_cards2[1])
        while rightHand and sum(player_cards2) < 21: 
            action_taken = str(input("Do you want to stay or hit?  "))
            if action_taken == "hit":
                player_cards2.append(random.randint(1, 11))
                print("You now have a total of " + str(sum(player_cards2)) + " from these cards ", player_cards2)
            elif action_taken == "stay":
                print("You have a total of " + str(sum(player_cards2)) + " with ", player_cards2)
                print("The dealer has a total of " + str(sum(dealer_cards2)) + " with ", dealer_cards2)
                while sum(dealer_cards2) < 17:
                    dealer_cards2.append(random.randint(1,11))
                    print("Dealer is going for another card.","\n","He drew a: ", dealer_cards2[-1])
                    print("The dealer has a total of " + str(sum(dealer_cards2)) + " with ", dealer_cards2)
                if sum(dealer_cards2) > 21:
                    # 2) Add 1 for player
                    player_score += 1
                    bettings = bettings + currentBet
                    print("Dealer BUSTED!")
                    rightHand = False
                    
                elif sum(dealer_cards2) >= sum(player_cards2):
                    # 2) Add 1 for dealer
                    dealer_score += 1
                    bettings = bettings - currentBet
                    print("Dealer wins!")
                    rightHand = False
                    
                else:
                    # 2) Add 1 for player
                    player_score += 1
                    bettings = bettings + currentBet
                    print("You win!")
                    rightHand = False
                    

        # Ends gameplay if a player hits 21 or above        
        if sum(player_cards2) > 21:
                print("Player has a total of: ",str(sum(player_cards2)),"That means the player busted! Dealer wins")
                rightHand = False
                dealer_score += 1
                bettings = bettings - currentBet
        elif sum(player_cards2) == 21:
                print("Player has 21! THATS A BLACKJACK! Player wins!!!")
                rightHand = False
                player_score += 1
                bettings = bettings + currentBet

    if leftHand == False and rightHand == False:
        print("Current scores: ")
        print("Dealer: " + str(dealer_score) + " games" + " - to - You: " + str(player_score) + " games")

def play_game():
    # New variables 
    global bettings, player_score, dealer_score

    # New text for the game
    print("Welcome to Blackjack. \nAfter each game you can see have many games you've won or lost")

    while bettings > 0:
        # Dealer cards
        dealer_cards = []
        dealer_cards2 = []
        # Player cards
        player_cards = []
        player_cards2 = []

        # Placing bets
        if not player_cards:
            print("\nYou have", bettings, "to play for")

        bet_input = input("How much do you wonna bet?")
        currentBet = int(bet_input)
        
        # Checking if bet is valid
        if currentBet > bettings:
            print("You dont have that amount to gamble for!")
        else:
            print("Dealing the cards")
            # Dealer Cards
            while len(dealer_cards) != 2:
                dealer_cards.append(random.randint(1,11))
                if len(dealer_cards) == 2:
                    print("Dealer has X &", dealer_cards[1])

            # Player Cards
            while len(player_cards) != 2:
                player_cards.append(random.randint(4,6))
                if len(player_cards) == 2:
                    print("You have ", player_cards)

            # Splitting Pairs
            if player_cards[0] == player_cards[1]:
                split_action = input("Player has a pair. Do you want to plit? (type Y/N)")
                if currentBet + currentBet > bettings:
                    print("You dont have enough money to play split" + "\n" + "Continueing with regular play")
                elif split_action == "Y" and currentBet + currentBet < bettings:
                    player_cards2.append(player_cards[1])
                    player_cards.remove(player_cards[1])
                    print("Players left hand is now:", player_cards, "and their right hand is:", player_cards2)
                    while len(dealer_cards2) != 2:
                        dealer_cards2.append(random.randint(1,11))
            # Double Down
            if sum(player_cards) in (9,10,11):
                double_input = input("Do you want to double down? (Y/N)") 
                if double_input == "Y" and (currentBet+currentBet) <= bettings:
                    currentBet += currentBet
                elif double_input == "Y" and (currentBet+currentBet) > bettings:
                    print("You dont have the money to double down! \n Continueing regular play")
                else:
                    print("You have rejected to doubledown")

            # regularPlay function called
            if not player_cards2:
                regularPlay(dealer_cards, player_cards, currentBet)

            # splitPlay function called
            if player_cards2:
                splitPlay(dealer_cards, dealer_cards2, player_cards, player_cards2, currentBet)

            # If user has no more money on balance
            if bettings <= 0:
                    print("You have no more money to play for... GOODBYE!") 
        
def main():
    play_game()

if __name__ == "__main__":
    main()



    
