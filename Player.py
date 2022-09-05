class Player:
    def __init__(self):
        self.n_dices = 6
        self.dices = []
        self.forwarded = []
        if not hasattr(self, "health"):
            self.health = 15
        if not hasattr(self, "tokens"):
            self.tokens = 0
        if not hasattr(self, "favors"):
            self.favors = []

#######################################################

    def set_dices(self, dices):
        self.dices = dices

    def set_forwarded(self, forwarded):
        self.forwarded = self.forwarded+forwarded
        self.forward_n_dices(len(forwarded))

    def set_n_dices(self, n_dices):
        self.n_dices = n_dices

    def forward_n_dices(self, len_forwarded):
        self.n_dices -= len_forwarded

    def set_health(self, health):
        self.health = health

    def set_tokens(self, tokens):
        self.tokens = tokens

    def set_favors(self, new_favor):
        self.favors.append(new_favor)

#######################################################

    def get_dices(self):
        return self.dices

    def get_forwarded(self):
        return self.forwarded

    def get_n_dices(self):
        return self.n_dices

    def get_health(self):
        return self.health

    def get_tokens(self):
        return self.tokens

    def get_favors(self):
        return self.favors
