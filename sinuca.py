from src import graphics as gf
from src.balls import *
from src.table import *
from src.team import *
from src.radio import *
import time
import random
        

def play_music():
    playlist = ['music/pool_music_1.wav', 'music/pool_music_3.wav']

    random.shuffle(playlist)
    play_sequence(playlist)


def get_lowest_ball(table_balls, team):
        team_balls = list(filter(lambda ball: ball.ball_type == team.target_ball_type, table_balls))
        lowest_ball = min(team_balls, key = lambda ball: int(ball.number.getText()))
        return lowest_ball


window_size = 1000
win = gf.GraphWin('bar do patrick', window_size * 1.2, window_size)
# play_music()
pocketed_balls = []
ball_radius = 15
cue_element = gf.Polygon(gf.Point(0,0))
cue = Cue(cue_element)

walls, holes = generate_table(win)

table_balls = generate_balls(350, [700, 500], ball_radius, win)


#inputs para os nomes dos times e dos jogadores
input_label = gf.Text(gf.Point(600, 100), '')
input_label.draw(win)
nome_input = gf.Entry(gf.Point(600, 150), 10)
nome_input.setFill("white")
nome_input.setSize(25)
nome_input.draw(win)

teams = []

# Adicionando os times
teams.append(generate_team("primeiro", input_label, nome_input, win))
teams.append(generate_team("segundo", input_label, nome_input, win))
input_label.undraw()
nome_input.undraw()

current_player_text = gf.Text(gf.Point(600, 160), "")
current_player_text.setSize(14)
current_player_text.draw(win)

first_ball_pocketed_type = "" # vai definir qual tipo de bola cada time deve encaçapar

##################
### Sorteio para ver qual time começa
##################
team_start = random.randint(1, 2)
if team_start == 1:
    current_player = teams[0].nextToPlay()
else:
    current_player = teams[1].nextToPlay()

turn = 1

while True:

    if current_player in teams[0].players:
        team = teams[0]
        other_team = teams[1]
    else:
        team = teams[1]
        other_team = teams[0]
    
    display_text = f"É a vez de {current_player}."

    if team.target_ball_type != "":
        if team.target_ball_type == "low_ball":
            display_text += "\nVocê deve encaçapar as menores."
        else:
            display_text += "\nVocê deve encaçapar as maiores."
    else:
        display_text += "\nVocê pode encaçapar qualquer bola!"

    current_player_text.setText(display_text)

    first_ball_type = "" # primeira bola acertada pela branca
    current_ball_hit = "" # última bola que foi acertada pela branca
    
    current_pocketed_balls = [] # bolas encaçapadas durante uma tacada

    change_player = True # vai definir se o jogador terá que passar o taco para outra pessoa ou se ele deverá jogar de novo

    use_cue(cue, table_balls, win) # aguarda até que o jogador mova o taco

# loop em que ocorre a física
    while balls_still_moving(table_balls):
        for ball in table_balls:
            ball.move()
        for i, ball1 in enumerate(table_balls):
            if (i + 1 == len(table_balls)):
                break
            for j, ball2 in enumerate(table_balls[i + 1:]):
                current_ball_hit = BallCollision(ball1, ball2, first_ball_pocketed_type)
                
                # atribui a primeira bola que foi acertada na rodada à variável first_ball_type
                if current_ball_hit and first_ball_type == "":
                    first_ball_type = current_ball_hit.ball_type
            
        for wall in walls:
            for ball in table_balls:
                Ball_Wall_Collision(ball, wall, win)

        for hole in holes:
            for ball in table_balls:
                current_pocketed_ball = Ball_Hole_Collision(table_balls, first_ball_pocketed_type, ball, hole, current_player, teams, win)
                if current_pocketed_ball:
                    current_pocketed_balls.append(current_pocketed_ball)
                    # define o primeiro tipo de bola que foi encaçapado no jogo (maior ou menor)
                    if first_ball_pocketed_type == "" and (current_pocketed_ball.ball_type == "high_ball" or current_pocketed_ball.ball_type == "low_ball"):
                        first_ball_pocketed_type = current_pocketed_ball.ball_type

        time.sleep(0.001)


    print(f"first ball hit: {first_ball_type}\nteam target ball: {team.target_ball_type}\n")

    # verifica se o jogador não acertou uma bola correspondente ao seu time 
    if first_ball_type != team.target_ball_type and team.target_ball_type != "":
        print('errou afude\n')

        ball_to_pocket = get_lowest_ball(table_balls, other_team)

        ball_to_pocket.undraw()
        table_balls.remove(ball_to_pocket)
    else:
        print('acertou')


    # define qual tipo de bola cada time deve encaçapar. Importante que aconteça depois da verificação da jogada ^
    if team.target_ball_type == "":
        if first_ball_pocketed_type == "low_ball":
            team.target_ball_type = "low_ball"
            other_team.target_ball_type = "high_ball"

        elif first_ball_pocketed_type == "high_ball":
            team.target_ball_type = "high_ball"
            other_team.target_ball_type = "low_ball"


    # verificaçoes para cada bola que foi encaçapada na jogada
    for ball in current_pocketed_balls:
        if ball.ball_type == 'cue_ball':

            # tira uma bola do outro time
            ball_to_pocket = get_lowest_ball(table_balls, other_team)
            ball_to_pocket.undraw()
            table_balls.remove(ball_to_pocket)

            # respawna a bola branca
            change_player = True
            table_balls.insert(0, spawn_cue_ball(350, 500, ball_radius, win))

            # move a bola caso ela spawne em cima de outra (nao é o melhor jeito, interessante mexer nisso depois)
            for i, ball1 in enumerate(table_balls):
                if (i + 1 == len(table_balls)):
                    break
                for j, ball2 in enumerate(table_balls[i + 1:]):
                    BallCollision(ball1, ball2, first_ball_pocketed_type)
            break

        elif ball.ball_type == other_team.target_ball_type:
            change_player = True
            break
        else:
            change_player = False
    
    if change_player:
        turn += 1

        if turn % 2 == 1:
            if team_start == 1:
                current_player = teams[0].nextToPlay()
            else:
                current_player = teams[1].nextToPlay()
        else:
            if team_start == 1:
                current_player = teams[1].nextToPlay()
            else:
                current_player = teams[0].nextToPlay()


    
# win.close()
