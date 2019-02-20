# Black Jack module

#Will need:
#-Card object
# -Player object
import random
from colorama import init, Fore, Back
init(autoreset=True)

class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face
        self.turned = False
        self.value = 0
        self.set_value()

    def set_value(self):
        if (self.face == 'A' or self.face =='J' or self.face =='Q' or self.face =='K'):
            self.value = 10
        else:
            self.value = int(self.face)

    def turn_card(self):
        self.turned = True

    def __str__(self):
        if self.turned:
            if self.suit == 'hearts':
                return Back.WHITE + Fore.RED +'\u2665 '+ self.face + '\u2665 '
            elif self.suit == 'tiles':
                return Back.WHITE + Fore.RED +'\u2666 ' + self.face + '\u2666 '
            elif self.suit == 'clovers':
                return Back.WHITE + Fore.BLACK +'\u2663 ' + self.face + '\u2663 '
            elif self.suit == 'pikes':
                return Back.WHITE + Fore.BLACK +'\u2660 '+ self.face + '\u2660 '
        else:
            if self.suit == 'hearts' or self.suit == 'tiles':
                return Back.WHITE + Fore.RED + '|   |'
            else:
                return Back.WHITE + Fore.BLACK + '|   |'

class Deck:
    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        deck_string = ''
        for card in self.cards:
            deck_string = deck_string + Back.RESET + ' ' + str(card)
        return deck_string

    def full_new(self):
        faces = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suits = ['hearts', 'tiles', 'clovers', 'pikes']
        self.cards = []
        for suit in suits:
            for face in faces:
                self.cards.append(Card(suit, face))

    def shuffle(self):
        random.shuffle(self.cards)

class Player:
    def __init__(self, name, credit):
        self.credit = credit
        self.name = name
        self.pile = Deck()
        self.sum = 0

    def add_up(self):
        sum = 0
        for cards in self.pile.cards:
            sum += cards.value
        if sum > 21:
            if 'A' in [card.face for card in self.pile.cards]:
                ace_counter = 0
                for card in self.pile.cards:
                    if card.face == 'A':
                        ace_counter += 1
                while (sum > 21) and (ace_counter > 0):
                    ace_counter -= 1
                    sum -= 9
        print('{} has a sum of {}'.format(self.name, sum))
        self.sum = sum
        return sum

    def hit(self, deck):
        self.pile.cards.append(deck.cards[-1])
        self.pile.cards[-1].turn_card()
        deck.cards.pop()

def show_cards(players, deck):
    print('\n'*100)
    print(f' {players[0].name}\n{players[0].pile}')
    print(f'\n\n {players[1].name}\n{players[1].pile}')

def deal(players, deck):
    for player in players:
        player.pile.cards = []
        for dealt_card in [0,1]:
            player.pile.cards.append(deck.cards[-1])
            deck.cards.pop()
        if player.name == 'Dealer':
            player.pile.cards[0].turn_card()
        else:
            player.pile.cards[0].turn_card()
            player.pile.cards[1].turn_card()

        show_cards(players, deck)

def place_bet(player):
    while True:
        bet_str = input('Please place your bet: ')
        try:
            bet = int(bet_str)
        except:
            print('Looks like you did not add a valid, whole number.\nTry again!')
        else:
            if bet == 0:
                print('Bet value must be greater than 0.')
            elif bet <= player.credit:
                print(f'Bet value of {bet} accepted.')
                break
            else:
                print(f'You do not have enough credit. Your credit: {player.credit}')
    return bet

def check_game_end(players, bet):
    if (players[1].sum > 21): #player busted, player loses, dealer wins
        print('Dealer Won!')
        players[1].credit -= bet
        players[0].credit += bet
    elif (players[0].sum > 21):
        print('Dealer Busted - PLAYER WON!') # dealer busted, player wins
        players[0].credit -= bet
        players[1].credit += bet
    elif (players[0].sum > players[1].sum): #dealer has a higher sum, player loses
        print('Dealer Won!')
        players[1].credit -= bet
        players[0].credit += bet
    elif (players[0].sum == players[1].sum): #draw - credit remains the same
        print('It\'s a draw!')
