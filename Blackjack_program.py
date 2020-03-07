import random

# Global variables
ranks = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')
suits = ('Spades', 'Hearts', 'Clubs', 'Diamonds')
values = {'Ace':11, 'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10}

playing = True


# Classes
class Card:  
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:   
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        printed_deck = ''
        for card in self.deck:
            printed_deck += '\n' + card.__str__()
        return 'The deck has:' + printed_deck

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()        

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
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Chips:   
    def __init__(self, total):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


# Functions definition
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Enter your bet amount: $"))
        except:
            print("Invalid value entered. Please enter bet amount in numbers")
        else:
            if chips.bet <= chips.total:
                print(f"Your bet amount: ${chips.bet}")
                break
            else:
                print(f"Not enough funds left to bet ${chips.bet} \nYou have: ${chips.total}")

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    while True: 
        decision = input("\nHit or Stand (H/S): ")
        if decision[0].upper() == 'H':
            hit(deck,hand)
        elif decision[0].upper() == 'S':
            playing = False
            print("Player stands. Dealer turn")
        else:
            continue
        break
    
def show_some(player,dealer):
    # Display Dealer hand with 1st card hidden
    print('\n---------------------')
    print('-----DEALER HAND-----')
    print('---------------------')
    print('[]')
    print(dealer.cards[1])
    
    print('\n')
    # Display Player hand
    print('\n---------------------')
    print('-----PLAYER HAND-----')
    print('---------------------')
    for card in player.cards:
        print(card)
    print(f'\nTotal value: {player.value}')
    
def show_all(player,dealer):
    # Display full Dealer hand
    print('\n---------------------')
    print('-----DEALER HAND-----')
    print('---------------------')
    for card in dealer.cards:
        print(card)
    print(f'\nTotal value: {dealer.value}')
    
    print('\n')
    # Display full Player hand
    print('\n---------------------')
    print('-----PLAYER HAND-----')
    print('---------------------')
    for card in player.cards:
        print(card)
    print(f'\nTotal value: {player.value}')


def player_busts(player, dealer, chips):
    print('Player BUST')
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print('Player WIN')
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print('Dealer BUST. Player WIN')
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print('Dealer WIN')
    chips.lose_bet()
    
def push(player, dealer):
    print("Dealer and Player tie. PUSH!")


# Run main program

# Print an opening statement
print("\n======================================")
print("-----Welcome to my Blackjack game-----")
print("======================================")

# Set up the Player's chips
total = 0
while total == 0:
    total = int(input("\nEnter amount of chips for buy-in: $"))
    player_chips = Chips(total)
    while True:
        # Create & shuffle the deck
        play_deck = Deck()    # Create deck object
        play_deck.shuffle()   # Shuffle deck
        
        # Deal two cards to each player
        player_hand = Hand()       # Create player hand object
        dealer_hand = Hand()       # Create dealer hand object
        for count in range(0,2): 
            player_hand.add_card(play_deck.deal())
            dealer_hand.add_card(play_deck.deal())
            
        # Prompt the Player for their bet
        take_bet(player_chips)
        
        # Show cards (but keep one dealer card hidden)
        print('\n'*50)
        show_some(player_hand, dealer_hand)
        
        while playing:  # recall this variable from our hit_or_stand function
            
            # Prompt for Player to Hit or Stand
            hit_or_stand(play_deck, player_hand)
            
            # Show cards (but keep one dealer card hidden)
            print('\n'*50)
            show_some(player_hand, dealer_hand)
            
            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player_hand.value > 21:
                print('\nResult:')
                player_busts(player_hand, dealer_hand, player_chips)
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(play_deck, dealer_hand)
                    
            # Show all cards
            print('\n'*50)
            show_all(player_hand, dealer_hand)
        
            # Run different winning scenarios
            print('\nResult:')
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            elif player_hand.value > dealer_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)
            else:
                push(player_hand, dealer_hand)
        
        # Inform Player of their chips total 
        print(f"\nPlayer chip total: ${player_chips.total}")
        # Ask to play again
        play_again = input("Do you want to play again? (Y/N): ")
        print('\n')
        if play_again[0].upper() == 'Y':
            # When player chips finished, prompt for buy in again
            if player_chips.total == 0:
                total = 0
                break
            else:
                playing = True
                continue
        elif play_again[0].upper() == 'N':
            playing = False
            break
        else:
            continue
        
        
