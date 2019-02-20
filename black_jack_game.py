# Black Jack game logic
#
#Will need Globals:
# -Deck
# -Player with given credit
# -amount of bet
#
# Logic:
# 0. Player places bets
# 1. Dealer deals
# 2. Player hits or stays (while loop)
#     - Check for blackjack or bust
# 3. Once Player stays, it's the Dealer's turn
# 4. Dealer hits until they beat the Player or the Dealer busts (while loop)
#     - Check conditions for game end in every round (over Players sum, blackjack or bust)
# 5. Players credit modified based on bet
# 6. Replay?

from black_jack import Card, Player, deal, Deck, show_cards, place_bet, check_game_end
import time

deck = Deck()
player = Player('Player', 100)
dealer = Player('Dealer', 300)
players = [dealer, player]

game_on = True
while (game_on == True):
    deck.full_new()
    deck.shuffle()
    print(len(deck))
    bet = place_bet(player)
    deal(players, deck)
    players_turn = True
    player_busted = False
    while players_turn:
        choice = input('Hit or Stay? Press H or S and then Enter.\n')
        if choice.lower() == 'h':
            player.hit(deck)
            show_cards(players, deck)
        else:
            players_turn = False
        sum = player.add_up()
        if  sum > 21:
            print('BUSTED!')
            time.sleep(1.5)
            player_busted = True
            players_turn = False
        elif sum == 21:
            print('Black Jack!')
            time.sleep(1.5)
            players_turn = False

    dealer.pile.cards[-1].turn_card()
    show_cards(players, deck)

    if(player_busted == False) and (players_turn == False): # dealer can only hit if player did not bust - otherwise the round is over
        dealer.add_up()
        time.sleep(2)
        while (dealer.sum < 21) and (dealer.sum < player.sum):
            dealer.hit(deck)
            print('Dealer hits...')
            time.sleep(1)
            show_cards(players, deck)
            if dealer.add_up() == 21:
                print('Dealer got a Black Jack!')
            time.sleep(1.5)

    check_game_end(players, bet) # check outcome and modify credits

    print(f'{player.name}\'s credit: {player.credit}')
    print(f'{dealer.name}\'s credit: {dealer.credit}')

    # check whether the player and the bank has enough credit to play again
    if (player.credit <= 0):
        print('You lost all your credit. Time to go home.')
        game_on = False
    elif (dealer.credit <= 0):
        print('The bank is out of money. You are rich. Go home.')
        game_on = False
    else: # if they both have enough credit, ask the player for replay
        replay = ''
        while True:
            replay = input('Do you want to play again? Y/N?\n')
            if replay.lower() == 'n':
                game_on = False
                break
            elif replay.lower() == 'y':
                game_on = True
                break
            else:
                print('Invalid input.')
