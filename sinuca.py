import graphics as gf
import time
import math
import radio as sd
import random
import generate_balls


class Ball: # REMOVER?  ==========================
    def __init__(self, element): #number e number_color são instâncias de Text e Circle gf
        self.element = element
        self.radius = element.getRadius()

        # self.color = color
        # self.number = number
        # self.number_color = number_color
        
        self.velocity_x = 0
        self.velocity_y = 0
        self.drag = 0.65
        self.acc_x = 0
        self.acc_y = 0

    def move(self):
        self.element.move(self.velocity_x, self.velocity_y)
        if abs(self.velocity_x) <= 0.1 and abs(self.velocity_y) <= 0.1:
            self.velocity_x = 0
            self.velocity_y = 0

        self.acc_x = -self.velocity_x * self.drag
        self.acc_y = -self.velocity_y * self.drag
        self.velocity_x += self.acc_x * 0.01
        self.velocity_y += self.acc_y * 0.01

    def getX(self):
        return self.element.getCenter().getX()
        
    def getY(self):
        return self.element.getCenter().getY()

    def getRadius(self):
        return self.radius

    def setVelocity_x(self, velocity):
        self.velocity_x = velocity

    def setVelocity_y(self, velocity):
        self.velocity_y = velocity

    def getVelocity_x(self):
        return self.velocity_x

    def getVelocity_y(self):
        return self.velocity_y


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


class Cue:
    def __init__(self, element):
        self.element = element
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
        self.redraw(points)        
    
    def get_center(self):
        points = self.element.getPoints()
        sum_x = sum(p.getX() for p in points)
        sum_y = sum(p.getY() for p in points)
        return gf.Point(sum_x / len(points), sum_y / len(points))

    def redraw(self, points):
        self.element.undraw()
        self.element = gf.Polygon(points)
        self.element.setFill(gf.color_rgb(154, 69, 21))
        self.element.draw(win)

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
            
        self.redraw(new_points)

    def move_towards_target(self, target):
        target_x = target.getX()
        target_y = target.getY()
        dx = self.last_mouse_pos.getX() - target_x
        dy = self.last_mouse_pos.getY() - target_y
        distance = math.sqrt(dx * dx + dy * dy)
        nx = dx / distance
        ny = dy / distance
        velocity = distance / 20
        if velocity > 15:
            velocity = 15
        while distance > target.getRadius():
            self.element.move(nx * velocity * -1, ny * velocity * -1)
            dx += nx * velocity * -1
            dy += ny * velocity * -1
            distance = math.sqrt(dx * dx + dy * dy)
            time.sleep(0.01)
        target.setVelocity_x(nx * velocity * -1)
        target.setVelocity_y(ny * velocity * -1)



        
def BallCollision(ball1, ball2):
    dx = ball1.getX() - ball2.getX()
    dy = ball1.getY() - ball2.getY()
    distance = math.sqrt(dx * dx  + dy * dy)
    nx = dx / distance
    ny = dy / distance

    #verifica se as bolas estão colidindo
    if distance <= (ball1.getRadius() + ball2.getRadius()):
        displacement = (distance - ball1.getRadius() - ball2.getRadius()) / 2

        #impede que uma bola sobreponha a outra
        ball1.element.move((displacement * dx / distance) * -1, (displacement * dy / distance) * -1)
        ball2.element.move(displacement * dx / distance, displacement * dy / distance)

        rel_vx = ball1.getVelocity_x() - ball2.getVelocity_x()
        rel_vy = ball1.getVelocity_y() - ball2.getVelocity_y()

        dot_product = (rel_vx * nx) + (rel_vy * ny)

        ball1.setVelocity_x(ball1.getVelocity_x() - dot_product * nx)
        ball1.setVelocity_y(ball1.getVelocity_y() - dot_product * ny)        
        
        ball2.setVelocity_x(ball2.getVelocity_x() + dot_product * nx)
        ball2.setVelocity_y(ball2.getVelocity_y() + dot_product * ny)


def Ball_Wall_Collision(ball, wall):
    ball_x = ball.getX()
    ball_y = ball.getY()
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


def generate_table():
    x_start_pos = 270
    top_walls_height = 100
    wall_thickness = 35
    wall_length = 300
    gap = 50
    corner_gap = 20
    
    walls_info = [
        {
            #parede cima-esquerda
            'p1': gf.Point(x_start_pos - corner_gap, top_walls_height),
            'p2': gf.Point(x_start_pos + wall_length, top_walls_height + wall_thickness),
        },
        {   
            #parede cima-direita
            'p1': gf.Point(x_start_pos + wall_length + gap, top_walls_height),
            'p2': gf.Point(x_start_pos + wall_length * 2 + gap + corner_gap, top_walls_height + wall_thickness),
        },
        {
            #parede baixo-esquerda
            'p1': gf.Point(x_start_pos - corner_gap, top_walls_height + wall_thickness + gap * 2 + wall_length),
            'p2': gf.Point(x_start_pos + wall_length, top_walls_height + wall_thickness * 2 + gap * 2 + wall_length),
        },
        {
            #parede baixo-direita
            'p1': gf.Point(x_start_pos + wall_length + gap, top_walls_height + wall_thickness + gap * 2 + wall_length),
            'p2': gf.Point(x_start_pos + wall_length * 2 + gap + corner_gap, top_walls_height + wall_thickness * 2 + gap * 2 + wall_length),
        },
        {
            #parede esquerda
            'p1': gf.Point(x_start_pos - gap - wall_thickness, top_walls_height + wall_thickness + gap - corner_gap),
            'p2': gf.Point(x_start_pos - gap, top_walls_height + wall_thickness + gap + wall_length + corner_gap),
        },
        {
            #parede direita
            'p1': gf.Point(x_start_pos + wall_length * 2 + gap * 2, top_walls_height + wall_thickness + gap - corner_gap),
            'p2': gf.Point(x_start_pos + wall_length * 2 + gap * 2 + wall_thickness, top_walls_height + wall_thickness + gap + wall_length + corner_gap),
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
    walls_info[0]['p1'] = gf.Point(x_start_pos - corner_gap, top_walls_height - gap * 2)
    walls_info[1]['p1'] = gf.Point(x_start_pos + wall_length + gap, top_walls_height - gap * 2)
    walls_info[2]['p2'] = gf.Point(x_start_pos + wall_length, top_walls_height + wall_thickness * 2 + gap * 4 + wall_length)
    walls_info[3]['p2'] = gf.Point(x_start_pos + wall_length * 2 + gap + corner_gap, top_walls_height + wall_thickness * 2 + gap * 4 + wall_length)
    walls_info[4]['p1'] = gf.Point(x_start_pos - gap * 3 - wall_thickness, top_walls_height + wall_thickness + gap - corner_gap)
    walls_info[5]['p2'] = gf.Point(x_start_pos + wall_length * 2 + gap * 4 + wall_thickness, top_walls_height + wall_thickness + gap + wall_length + corner_gap)

    for wall in walls_info:
        wall_element = gf.Rectangle(wall['p1'], wall['p2'])
        wall_obj = Wall(wall_element)
        walls.append(wall_obj)

    #agora gera as regiões dos buracos da mesa (invisíveis)
    small_radius = gap * 0.5
    radius = wall_thickness
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

    for hole in holes_info:
        hole_element = gf.Circle(hole['center'], hole['radius'])
        hole_element.setFill(gf.color_rgb(193, 189, 175))
        hole_element.setOutline(outline_color)
        hole_element.draw(win)
        #holes.append(wall_obj)

    
# def generate_balls(radius):
#     colors = ["Yellow", "Blue", "Red", "Purple", "Orange", "Green", "Brown"] # Pensar na black
#     cx = 100 #Valor arbitrário
#     cy = 100 #Valor arbitrário

#     # (self, element, color, number, number_color)

#     table_balls.append(gf.Circle(100, 100), radius) # Bola branca

#     color_picker = 0
#     for i in range(1, 15):
        
#         if color_picker < 7:
#             table_balls.append(Ball(gf.Circle(gf.Point(cx, cy), radius), colors[color_picker], i, ))
#             color_picker += 1
#         else: # No caso de ser a bola 8

#         # Por agora só forma uma linha em diagonal
#         cx += radius
#         cy += radius
        


playlist = ['music/pool_music_1.wav', 'music/pool_music_3.wav']

random.shuffle(playlist)
# sd.play_sequence(playlist)
window_size = 1000
win = gf.GraphWin('bar do patrick', window_size * 1.2, window_size)

table_balls = []
pocketed_balls = []
walls = []

cue_element = gf.Polygon(gf.Point(0,0))
cue = Cue(cue_element)

generate_table()

b1 = gf.Circle(gf.Point(400,298), 12)
b1.draw(win)
b1.setFill('white')
ball1 = Ball(b1)

b2 = gf.Circle(gf.Point(600,305), 12)
b2.draw(win)
ball2 = Ball(b2)

a = win.getMouse()
cue.move_cue_to_mouse_pos(gf.Point(a.getX(), a.getY()))

dy = a.getY() - ball1.getY()
dx = a.getX() - ball1.getX()

angle_rad = math.atan2(dy, dx)
cue.rotate_polygon_to_angle(angle_rad)
key = win.getKey()
if key == 'space':
    cue.move_towards_target(ball1)
#loop em que ocorre a física

while True:
    ball1.move()
    ball2.move()
    BallCollision(ball1, ball2)
    for wall in walls:
        Ball_Wall_Collision(ball1, wall)
        Ball_Wall_Collision(ball2, wall)

    time.sleep(0.01)

win.close()



# char = input("Digite um tijolo")
# altura = int(input("Digite a altura"))
# i = 0
# piramide = ""
# while i < altura:
#     j = 0
#     while j < altura - i:
#         piramide += " "
#         j += 1
#     j = 0
#     while j < 1 + i * 2:
#         piramide += char
#         j += 1
#     piramide += "\n"
#     i += 1
# print(piramide)