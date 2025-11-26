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

    def getName():
        return self.name
    
    def getPocketedBalls():
        return self.pocketed_balls

    def getPlayers():
        return self.players

    def getPlayerPocketeds():
        return self.player_pocketeds

# test = Team(["Ana", "Bianca", "Carol"])
# print(vars(test))

# test.player_pocketed("Bianca", 8)
# print(vars(test))

def generate_team(order):
    name = input(f"\n> Insira um nome para o {order} time: ")
    n = int(input(f">> Número de jogadores do time {name}: "))
    players = []
    for i in range(n):
        players.append(input(f">>> Insira o nome do player {i + 1}: "))
    team = Team(name, players)
    return team