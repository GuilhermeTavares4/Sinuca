import graphics as gf
import time
import radio
import random
from balls import *
from table import *
from team import *
        

def play_music():
    playlist = ['music/pool_music_1.wav', 'music/pool_music_3.wav']

    random.shuffle(playlist)
    radio.play_sequence(playlist)


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

current_player_text = gf.Text(gf.Point(600, 180), "")
current_player_text.draw(win)

first_ball_pocketed = "" # vai definir qual tipo de bola cada time deve encaçapar

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
    
    display_text = f"É a vez de {current_player}"

    if team.target_ball_type != "":
        if team.target_ball_type == "low_ball":
            display_text += "\nVocê deve encaçapar as menores."
        else:
            display_text += "\nVocê deve encaçapar as maiores."
    else:
        display_text += "\nVocê pode encaçapar qualquer bola!"

    current_player_text.setText(display_text)

    first_ball_hit = ""

    use_cue(cue, table_balls, win) #aguarda até que o jogador mova o taco

# loop em que ocorre a física
    while balls_still_moving(table_balls):
        for ball in table_balls:
            ball.move()
        for i, ball1 in enumerate(table_balls):
            if (i + 1 == len(table_balls)):
                break
            for j, ball2 in enumerate(table_balls[i + 1:]):
                BallCollision(ball1, ball2, first_ball_hit, first_ball_pocketed, win)
            
        for wall in walls:
            for ball in table_balls:
                Ball_Wall_Collision(ball, wall, win)

        for hole in holes:
            for ball in table_balls:
                Ball_Hole_Collision(table_balls, first_ball_pocketed, ball, hole, current_player, teams, win)

        time.sleep(0.001)



    print(f"first ball hit: {first_ball_hit}\nteam target ball: {team.target_ball_type}")
    if first_ball_hit != team.target_ball_type and team.target_ball_type != "":
        print('errou afude')
        #aqui vai o codigo pra encaçapar automaticamente uma bola do time oponente caso o jogador tenha feito uma jogada considerada errada


    #define qual tipo de bola cada time deve encaçapar. Importante que aconteça depois da verificação da jogada ^
    if team.target_ball_type == "":
        if first_ball_pocketed == "low_ball":
            team.target_ball_type = "low_ball"
            other_team.target_ball_type = "high_ball"

        elif first_ball_pocketed == "high_ball":
            team.target_ball_type = "high_ball"
            other_team.target_ball_type = "low_ball"

    #respawna a bola branca caso ela tenha sido encaçapada
    if "cue_ball" not in map(lambda ball: ball.ball_type, table_balls):
        table_balls.insert(0, spawn_cue_ball(350, 500, ball_radius, win))

        # move a bola caso ela spawne em cima de outra (nao é o melhor jeito, interessante mexer nisso depois)
        for i, ball1 in enumerate(table_balls):
            if (i + 1 == len(table_balls)):
                break
            for j, ball2 in enumerate(table_balls[i + 1:]):
                BallCollision(ball1, ball2, first_ball_hit, first_ball_pocketed, win)

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
