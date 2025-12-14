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
        gf.update(60)

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
    
    time.sleep(0.5)

    # verifica se o jogador não acertou uma bola correspondente ao seu time 
    if first_ball_type != team.target_ball_type and team.target_ball_type != "":

        if len(get_team_balls(table_balls, other_team)) > 0:
            ball_to_pocket = get_lowest_ball(table_balls, other_team)
            ball_to_pocket.undraw()
            table_balls.remove(ball_to_pocket)

    # define qual tipo de bola cada time deve encaçapar. Importante que aconteça depois da verificação da jogada ^
    if team.target_ball_type == "":
        if first_ball_pocketed_type == "low_ball":
            team.target_ball_type = "low_ball"
            other_team.target_ball_type = "high_ball"

        elif first_ball_pocketed_type == "high_ball":
            team.target_ball_type = "high_ball"
            other_team.target_ball_type = "low_ball"

    # aplica as regras gerais do jogo caso alguma bola tenha sido encaçapada
    if len(current_pocketed_balls) > 0:
        cue_ball_pocketed = check_if_ball_pocketed(current_pocketed_balls, 'cue_ball')
        ball_8_pocketed = check_if_ball_pocketed(current_pocketed_balls, '8_ball')

        if ball_8_pocketed:
            # encaçapar a bola 8 só acaba o jogo se já tiver sido encaçapada alguma outra bola
            if team.target_ball_type != "":
                if len(get_team_balls(table_balls, team)) > 0:
                    print(f'{other_team.name} won!')
                else:
                    if not cue_ball_pocketed:
                        print(f'{team.name} won!')
                    else:
                        print(f'{other_team.name} won!')
                break
        
        if cue_ball_pocketed: 
            # tira uma bola do outro time se ainda tiver alguma
            if len(get_team_balls(table_balls, other_team)) > 0:
                ball_to_pocket = get_lowest_ball(table_balls, other_team)
                ball_to_pocket.undraw()
                table_balls.remove(ball_to_pocket)

            # respawna a bola branca    
            table_balls.insert(0, spawn_cue_ball(350, 500, ball_radius, win))

            # move a bola caso ela spawne em cima de outra (nao é o melhor jeito, interessante mexer nisso depois)
            for i, ball1 in enumerate(table_balls):
                if (i + 1 == len(table_balls)):
                    break
                for j, ball2 in enumerate(table_balls[i + 1:]):
                    BallCollision(ball1, ball2, first_ball_pocketed_type)
        
            change_player = True

        else:
            if team.target_ball_type != "":
                if check_if_ball_pocketed(current_pocketed_balls, team.target_ball_type) and not check_if_ball_pocketed(current_pocketed_balls, other_team.target_ball_type):
                    change_player = False
                else:
                    change_player = True

    print(f'{get_team_balls(table_balls, team)}, {len(get_team_balls(table_balls, team))}\n')        
    print(f'{get_team_balls(table_balls, other_team)}, {len(get_team_balls(table_balls, other_team))}\n\n')
    
    # caso a bola preta tenha sido encaçapada de primeira...
    if team.target_ball_type != "":
        if len(get_team_balls(table_balls, team)) == 0:
            print(f'{team.name} won!')
            break
        if len(get_team_balls(table_balls, other_team)) == 0:
            print(f'{other_team.name} won!')
            break
    
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