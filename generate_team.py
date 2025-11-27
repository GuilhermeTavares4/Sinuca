class Team:
    def __init__(self, name, players: list):
        self.name = name
        self.pocketed_balls = []
        self.players = players
        self.player_pocketeds = {}
        for player in players:
            self.player_pocketeds[player] = []

    def player_pocketed(self, player, ball):
        self.pocketed_balls.append(ball)
        self.player_pocketeds[player].append(ball)

    def getName(self):
        return self.name
    
    def getPocketedBalls(self):
        return self.pocketed_balls

    def getPlayers(self):
        return self.players

    def getPlayerPocketeds(self):
        return self.player_pocketeds

# test = Team(["Ana", "Bianca", "Carol"])
# print(vars(test))

# test.player_pocketed("Bianca", 8)
# print(vars(test))

def generate_team(order, input_label, entry, win):
    input_label.setText(f'Digite o nome do {order} time')
    team_name = get_text_input(entry, win)
    input_label.setText(f'Digite o número de jogadores do time {team_name}')
    n = int(get_text_input(entry, win))
    players = []
    for i in range(n):
        input_label.setText(f'Digite o nome do jogador {i + 1}')
        players.append(get_text_input(entry, win))
    team = Team(team_name, players)
    return team
                

def get_text_input(entry, win): 
    while True:
        key = win.getKey()
        if key == 'Return' and entry.getText() != '':
            text = entry.getText()
            entry.setText('')
            break
    return text

