import graphics as gf
import time
import math
import radio
import random
from generate_balls import *
from generate_team import *


class Wall:
    def __init__(self, element):
        self.element = element
        self.left = element.getP1().getX()
        self.right = element.getP2().getX()
        self.bottom = element.getP2().getY()
        self.top = element.getP1().getY()

    def getLeft(self):
        return self.left
    
    def getRight(self):
        return self.right
    
    def getTop(self):
        return self.top
    
    def getBottom(self):
        return self.bottom


class Hole:
    def __init__(self, element):
        self.element = element
    
    def getRadius(self):
        return self.element.getRadius()
    
    def getCenter(self):
        return self.element.getCenter()


class Cue:
    def __init__(self, element):
        self.element = element
        self.assist_line = gf.Line(gf.Point(0,0), gf.Point(0,0))
        self.width = 50
        self.height = 250
        self.last_mouse_pos = gf.Point(0,0)

    def move_cue_to_mouse_pos(self, mouse_pos):
        self.last_mouse_pos = gf.Point(mouse_pos.getX(), mouse_pos.getY())
        points = [gf.Point(mouse_pos.getX() - self.height * 0.5, mouse_pos.getY() - self.width * 0.5), 
                  gf.Point(mouse_pos.getX() + self.height * 0.5, mouse_pos.getY() - self.width * 0.5), 
                  gf.Point(mouse_pos.getX() + self.height * 0.5, mouse_pos.getY() + self.width * 0.5), 
                  gf.Point(mouse_pos.getX() - self.height * 0.5, mouse_pos.getY() + self.width * 0.5)
                  ]
        self.element = gf.Polygon(points)        
    
    def get_center(self):
        points = self.element.getPoints()
        sum_x = sum(p.getX() for p in points)
        sum_y = sum(p.getY() for p in points)
        return gf.Point(sum_x / len(points), sum_y / len(points))


    def rotate_polygon_to_angle(self, angle_rad):
        center = self.get_center()
        r = 8
        points = self.element.getPoints()
        base_coords = [(self.height, -r), (0, -r + 5), (0, r - 5), (self.height, r)]
        #base_coords = [(+200, -r + 5), (0, -r), (0, r), (+200, r - 5 )] #taco invertido (braian)
        new_points = []
        for x, y in base_coords:
            rotated_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            rotated_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            
            final_p = gf.Point(rotated_x + center.getX(), rotated_y + center.getY())
            new_points.append(final_p)
        
        self.element = gf.Polygon(new_points)
        self.element.setFill(gf.color_rgb(154, 69, 21))
        self.element.draw(win)

    def move_towards_target(self, target):
        target_x = target.getX()
        target_y = target.getY()
        dx = self.last_mouse_pos.getX() - target_x
        dy = self.last_mouse_pos.getY() - target_y
        distance = math.sqrt(dx * dx + dy * dy)
        nx = dx / distance
        ny = dy / distance
        velocity = distance / 10
        if velocity > 23:
            velocity = 23
        while distance > target.getRadius():
            self.element.move(nx * velocity * -1, ny * velocity * -1)
            dx += nx * velocity * -1
            dy += ny * velocity * -1
            distance = math.sqrt(dx * dx + dy * dy)
            time.sleep(0.01)
        target.setVelocity_x(nx * velocity * -1)
        target.setVelocity_y(ny * velocity * -1)

    def draw_assist_line(self, dx, dy, spawn_pos):
        spawn_x = spawn_pos.getX()
        spawn_y = spawn_pos.getY()
        distance = math.sqrt(dx * dx + dy * dy)
        self.assist_line = gf.Line(gf.Point(spawn_x, spawn_y), gf.Point(spawn_x + dx / distance * -70, spawn_y + dy / distance * -70))
        self.assist_line.setArrow('last')
        self.assist_line.draw(win)
        

    def undraw(self):
        self.assist_line.undraw()
        self.element.undraw()


        
def BallCollision(ball1, ball2):
    ball1_center = ball1.element.getCenter()
    ball2_center = ball2.element.getCenter()
    dx = ball1_center.getX() - ball2_center.getX()
    dy = ball1_center.getY() - ball2_center.getY()
    distance = math.sqrt(dx * dx  + dy * dy)
    #verifica se as bolas estão colidindo
    if distance < (ball1.element.getRadius() + ball2.element.getRadius()):
        nx = dx / distance
        ny = dy / distance
        displacement = (distance - ball1.getRadius() - ball2.getRadius()) * 0.5

        #impede que uma bola sobreponha a outra
        ball1.element.move((displacement * dx / distance) * -1, (displacement * dy / distance) * -1)
        ball2.element.move(displacement * dx / distance, displacement * dy / distance)

        rel_vx = ball1.getVelocity_x() - ball2.getVelocity_x()
        rel_vy = ball1.getVelocity_y() - ball2.getVelocity_y()

        dot_product = (rel_vx * nx) + (rel_vy * ny)

        ball1.setVelocity_x((ball1.getVelocity_x() - dot_product * nx) * 0.9)
        ball1.setVelocity_y((ball1.getVelocity_y() - dot_product * ny) * 0.9)        
        
        ball2.setVelocity_x((ball2.getVelocity_x() + dot_product * nx) * 0.9)
        ball2.setVelocity_y((ball2.getVelocity_y() + dot_product * ny) * 0.9)


def Ball_Wall_Collision(ball, wall):
    ball_center = ball.element.getCenter()
    ball_x = ball_center.getX()
    ball_y = ball_center.getY()
    horizontal_side = ball_x
    vertical_side = ball_y
    if ball_x < wall.getLeft():
        horizontal_side = wall.getLeft()
    else:
        if ball_x > wall.getRight(): 
            horizontal_side = wall.getRight()
    
    if ball_y < wall.getTop():
        vertical_side = wall.getTop()
    else:
        if ball_y > wall.getBottom():
            vertical_side = wall.getBottom()

    dx = ball_x - horizontal_side
    dy = ball_y - vertical_side
    distance = math.sqrt(dx * dx + dy * dy)
    if distance <= ball.getRadius():
        displacement = distance - ball1.getRadius()
        if distance < 1:
            distance = 1
        if abs(dy) < abs(dx):
            ball.element.move((displacement * dx / distance) * -1, 0)
            ball.setVelocity_x(ball.getVelocity_x() * -0.9)
        else:
            ball.element.move(0, (displacement * dy / distance) * -1)
            ball.setVelocity_y(ball.getVelocity_y() * -0.9)
        
    
def Ball_Hole_Collision(ball, hole, player, teams):
    ball_center = ball.element.getCenter()
    hole_center = hole.element.getCenter()
    dx = ball_center.getX() - hole_center.getX()
    dy = ball_center.getY() - hole_center.getY()
    distance = math.sqrt(dx * dx  + dy * dy)

    #verifica se as bola e o buraco estão colidindo :)
    if distance < (ball.element.getRadius() * 0.5 + hole.element.getRadius()):
        if player in teams[0].players:
            print(f"{player} está no time {teams[0].name} com players: {teams[0].players}")
            ### if ball not in player.pocketeds adicionar abaixo, se não ignorar
            teams[0].player_pocketed(player, ball.number.getText())
            print(teams[0].player_pocketeds)
        else:
            print(f"{player} está no time {teams[1].name} com players: {teams[1].players}")
            teams[1].player_pocketed(player, ball.number.getText())
            print(teams[1].player_pocketeds)
        ball.undraw() # por enquanto só torna a bola invisível
        

def generate_table():
    x_start_pos = 270
    top_walls_height = 100
    wall_thickness = 35
    wall_length = 300
    gap = 60
    corner_inverse_gap = 22 #valor maior reduz o gap das bordas da mesa
    
    walls_info = [
        {
            #parede cima-esquerda
            'p1': gf.Point(x_start_pos - corner_inverse_gap, top_walls_height),
            'p2': gf.Point(x_start_pos + wall_length, top_walls_height + wall_thickness),
        },
        {   
            #parede cima-direita
            'p1': gf.Point(x_start_pos + wall_length + gap, top_walls_height),
            'p2': gf.Point(x_start_pos + wall_length * 2 + gap + corner_inverse_gap, top_walls_height + wall_thickness),
        },
        {
            #parede baixo-esquerda
            'p1': gf.Point(x_start_pos - corner_inverse_gap, top_walls_height + wall_thickness + gap * 2 + wall_length),
            'p2': gf.Point(x_start_pos + wall_length, top_walls_height + wall_thickness * 2 + gap * 2 + wall_length),
        },
        {
            #parede baixo-direita
            'p1': gf.Point(x_start_pos + wall_length + gap, top_walls_height + wall_thickness + gap * 2 + wall_length),
            'p2': gf.Point(x_start_pos + wall_length * 2 + gap + corner_inverse_gap, top_walls_height + wall_thickness * 2 + gap * 2 + wall_length),
        },
        {
            #parede esquerda
            'p1': gf.Point(x_start_pos - gap - wall_thickness, top_walls_height + wall_thickness + gap - corner_inverse_gap),
            'p2': gf.Point(x_start_pos - gap, top_walls_height + wall_thickness + gap + wall_length + corner_inverse_gap),
        },
        {
            #parede direita
            'p1': gf.Point(x_start_pos + wall_length * 2 + gap * 2, top_walls_height + wall_thickness + gap - corner_inverse_gap),
            'p2': gf.Point(x_start_pos + wall_length * 2 + gap * 2 + wall_thickness, top_walls_height + wall_thickness + gap + wall_length + corner_inverse_gap),
        },
    ]
    #outline para todos os elementos da mesa
    outline_color = gf.color_rgb(60, 60, 60)

    #borda de madeira da mesa
    border = gf.Rectangle(gf.Point(x_start_pos - gap - wall_thickness * 2, top_walls_height - wall_thickness), 
                          gf.Point(x_start_pos + wall_length * 2 + gap * 2 + wall_thickness * 2, top_walls_height + wall_thickness * 3 + gap * 2 + wall_length))
    border.setFill(gf.color_rgb(123, 67, 42))
    border.draw(win)

    #pinta a mesa antes das paredes
    table_carpet = gf.Rectangle(gf.Point(x_start_pos - gap - wall_thickness, top_walls_height), 
                                gf.Point(x_start_pos + wall_length * 2 + gap * 2 + wall_thickness, top_walls_height + wall_thickness * 2 + gap * 2 + wall_length))
    table_carpet.setFill(gf.color_rgb(4, 141, 124))
    table_carpet.setOutline(outline_color)
    table_carpet.draw(win)

    #desenha todas as paredes visíveis
    for wall in walls_info:
        wall_element = gf.Rectangle(wall['p1'], wall['p2'])
        wall_element.setFill(gf.color_rgb(0, 101, 83))
        wall_element.setOutline(outline_color)
        wall_element.draw(win)
    
    #aumenta o tamanho das paredes para gerar as invisíveis que são usadas para colisão (fisica funciona melhor assim)
    walls_info[0]['p1'] = gf.Point(x_start_pos - corner_inverse_gap, top_walls_height - gap * 3)
    walls_info[1]['p1'] = gf.Point(x_start_pos + wall_length + gap, top_walls_height - gap * 3)
    walls_info[2]['p2'] = gf.Point(x_start_pos + wall_length, top_walls_height + wall_thickness * 2 + gap * 5 + wall_length)
    walls_info[3]['p2'] = gf.Point(x_start_pos + wall_length * 2 + gap + corner_inverse_gap, top_walls_height + wall_thickness * 2 + gap * 5 + wall_length)
    walls_info[4]['p1'] = gf.Point(x_start_pos - gap * 4 - wall_thickness, top_walls_height + wall_thickness + gap - corner_inverse_gap)
    walls_info[5]['p2'] = gf.Point(x_start_pos + wall_length * 2 + gap * 5 + wall_thickness, top_walls_height + wall_thickness + gap + wall_length + corner_inverse_gap)

    for wall in walls_info:
        wall_element = gf.Rectangle(wall['p1'], wall['p2'])
        wall_obj = Wall(wall_element)
        walls.append(wall_obj)

    #agora gera as regiões dos buracos da mesa (invisíveis)
    small_radius = gap * 0.5
    radius = gap * 0.7

    holes_info = [
        {
            #buraco cima-esquerda
            'center': gf.Point(x_start_pos - gap - wall_thickness / 2, top_walls_height + wall_thickness / 2),
            'radius': radius
        },
        {
            #buraco cima
            'center': gf.Point(x_start_pos + wall_length + small_radius, top_walls_height),
            'radius': small_radius
        },
        {
            #buraco direita
            'center': gf.Point(x_start_pos + wall_length * 2 + gap * 2 + wall_thickness / 2, top_walls_height + wall_thickness / 2),
            'radius': radius
        },
        {
            #buraco baixo-esquerda
            'center': gf.Point(x_start_pos - gap - wall_thickness / 2, top_walls_height + wall_thickness * 3 / 2 + gap * 2 + wall_length),
            'radius': radius
        },
        {
            #buraco baixo
            'center': gf.Point(x_start_pos + wall_length + small_radius, top_walls_height + wall_thickness * 2 + gap * 2 + wall_length),
            'radius': small_radius
        },
        {
            #buraco baixo-direita
            'center': gf.Point(x_start_pos + wall_length * 2 + gap * 2 + wall_thickness / 2, top_walls_height + wall_thickness * 3 / 2 + gap * 2 + wall_length),
            'radius': radius
        },
    ]

    # buracos para encaçapar as bolas
    for hole in holes_info:
        hole_element = gf.Circle(hole['center'], hole['radius'])
        hole_element.setFill(gf.color_rgb(193, 189, 175))
        hole_element.setOutline(outline_color)
        hole_element.draw(win)
        hole_obj = Hole(hole_element)
        holes.append(hole_obj)


def use_cue():
    pos = None
    while True:
        click = win.checkMouse()
        if click:
            pos = gf.Point(click.getX(), click.getY())
            cue.undraw()
            cue.move_cue_to_mouse_pos(pos)
            dy = pos.getY() - table_balls[0].getY()
            dx = pos.getX() - table_balls[0].getX()
            angle_rad = math.atan2(dy, dx)
            cue.rotate_polygon_to_angle(angle_rad)
            cue.draw_assist_line(dx, dy, table_balls[0].element.getCenter())

        key = win.checkKey()
        if pos and key == 'space':
            break
    cue.move_towards_target(table_balls[0])
    cue.undraw()


def balls_still_moving():
    for ball in table_balls:
        if ball.getVelocity_x() != 0 or ball.getVelocity_y() != 0:
            return True            
    return False
        

playlist = ['music/pool_music_1.wav', 'music/pool_music_3.wav']

random.shuffle(playlist)
# radio.play_sequence(playlist) # descomente para ouvir a trilha sonora :)
window_size = 1000
win = gf.GraphWin('bar do patrick', window_size * 1.2, window_size)

pocketed_balls = []
walls = []
holes = []

cue_element = gf.Polygon(gf.Point(0,0))
cue = Cue(cue_element)

generate_table()

table_balls = generate_balls(350, [700, 325], 15, win)

teams = []
teams = [Team("ab", ["a", "b"]), Team("cde", ["c", "d", "e"])] # Definição direta
print(teams[0].players, teams[1].players)

# Adicionando os times

# teams.append(generate_team("Primeiro"))
# teams.append(generate_team("Segundo"))

player_order = [] # Ordem dos jogadores
luck = random.randint(1, 2) # Sorteio para ver qual time começa

if luck == 1:
    first = teams[0].players.copy()
    second = teams[1].players.copy()
else:
    first = teams[1].players.copy()
    second = teams[0].players.copy()

while len(first) != 0 or len(second) != 0:
    if len(first) != 0:
        player_order.append(first[0])
        first.pop(0)
    if len(second) != 0:
        player_order.append(second[0])
        second.pop(0)

current_player = 0 

while True:

    if current_player == len(player_order):
        current_player = 0

    use_cue() #aguarda até que o jogador mova o taco

# loop em que ocorre a física
    while balls_still_moving():
        for ball in table_balls:
            ball.move()
        for i, ball1 in enumerate(table_balls):
            if (i + 1 == len(table_balls)):
                break
            for j, ball2 in enumerate(table_balls[i + 1:]):
                BallCollision(ball1, ball2)
            
        for wall in walls:
            for ball in table_balls:
                Ball_Wall_Collision(ball, wall)

        for hole in holes:
            for ball in table_balls:
                Ball_Hole_Collision(ball, hole, player_order[current_player], teams)

        time.sleep(0.001)

    current_player += 1
        

# win.close()
