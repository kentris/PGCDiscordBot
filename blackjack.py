import random


class Card:
    def __init__(self, rank, suite):
        self.rank = rank
        self.suite = suite
        self.values = {
            'A': 11,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 10,
            'Q': 10,
            'K': 10
        }

    def __str__(self):
        return f"{self.rank}-{self.suite}"

    def get_value(self):
        return self.values[self.rank]


class Deck:
    def __init__(self):
        self.suit = ["Hearts", "Clubs", "Spades", "Diamonds"]
        self.rank = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        # self.rank = ["A"]
        self.deck = [Card(r, s) for r in self.rank for s in self.suit]
        random.shuffle(self.deck)

    def shuffle(self):
        self.deck = [Card(r, s) for r in self.rank for s in self.suit]
        random.shuffle(self.deck)

    def deal_card(self):
        if len(self.deck) == 0: self.shuffle()
        return self.deck.pop(0)


class Player:
    def __init__(self):
        self.cards = []
        self.total = 0

    def reset(self):
        self.cards = []
        self.total = 0

    def take_card(self, card):
        self.cards.append(card)
        self.total = sum([c.get_value() for c in self.cards])
        ace_count = sum([1 for card in self.cards if card.rank == "A"])
        # Do check for an Ace
        while self.total > 21 and ace_count:
            self.total -= 10
            ace_count -= 1

    def is_bust(self):
        return self.total > 21


class Blackjack:
    def __init__(self):
        self.dealer = Player()
        self.player = Player()
        self.deck = Deck()
        self.is_player_turn = True

    def __str__(self):
        return '\n'.join([
            f"Dealer: Total={self.dealer.total}, ({', '.join([str(c) for c in self.dealer.cards])})",
            f"Player: Total={self.player.total}, ({', '.join([str(c) for c in self.player.cards])})\n"
        ])

    def start_game(self):
        # Reset game state
        self.dealer.reset()
        self.player.reset()
        self.deck.shuffle()
        self.is_player_turn = True
        # Deal initial cards
        self.hit(self.player)
        self.hit(self.dealer)
        self.hit(self.player)
        self.hit(self.dealer)

    def hit(self, player):
        player.take_card(self.deck.deal_card())

    def get_dealer_total(self):
        return sum([c.get_value() for c in self.dealer.cards])

    def print_player(self):
        print(f"Player: {', '.join([c for c in self.player.cards])}")
        print(f"Player Total: {sum([c.get_value() for c in self.player.cards])}\n")

    def print_dealer(self):
        print(f"Dealer: {', '.join([c for c in self.dealer.cards])}")
        print(f"Dealer Total: {sum([c.get_value() for c in self.dealer.cards])}\n")

    def is_game_over(self):
        return self.player.is_bust() or self.dealer.is_bust() or self.dealer.total > 16
