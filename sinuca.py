import graphics as gf
import time
import math
import simplesound as sd


class Ball:
    def __init__(self, element): #number e number_color são instâncias de Text e Circle gf
        self.element = element
        self.radius = element.getRadius()

        # self.color = color
        # self.number = number
        # self.number_color = number_color
        
        self.velocity_x = 0
        self.velocity_y = 0
        self.drag = 0.8
        self.acc_x = 0
        self.acc_y = 0

    def move(self):
        self.element.move(self.velocity_x, self.velocity_y)
        if abs(self.velocity_x) <= 0.08 and abs(self.velocity_y) <= 0.08:
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
    def __init__(self, element, wall_type):
        self.element = element
        self.wall_type = wall_type
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
    
    def getType(self):
        return self.wall_type
    

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
        if wall.getType() == 'vertical':
            used_side = ball_x
            if ball_x < wall.getLeft():
                used_side = wall.getLeft()
            else:
                if ball_x > wall.getRight(): 
                    used_side = wall.getRight()
            distance = abs(ball_x - used_side)
            
        else:
            used_side = ball_y
            if ball_y < wall.getTop():
                used_side = wall.getTop()
            else:
                if ball_y > wall.getBottom():
                    used_side = wall.getBottom()
            distance = abs(ball_y - used_side)

        if distance <= ball.getRadius():
            if wall.getType() == 'vertical':
                ball.setVelocity_x(ball.getVelocity_x() * -1)
            else:
                ball.setVelocity_y(ball.getVelocity_y() * -1)


def generate_table():
    x_pos = 150
    top_walls_height = 100
    wall_thickness = 50
    wall_length = 300
    gap = 50
    corner_gap = 15
    
    walls_info = [
        {
            #parede cima-esquerda
            'p1': gf.Point(x_pos - corner_gap, top_walls_height),
            'p2': gf.Point(x_pos + wall_length, top_walls_height + wall_thickness),
            'type': 'horizontal'
        },
        {   
            #parede cima-direita
            'p1': gf.Point(x_pos + wall_length + gap, top_walls_height),
            'p2': gf.Point(x_pos + wall_length * 2 + gap + corner_gap, top_walls_height + wall_thickness),
            'type': 'horizontal'
        },
        {
            #parede baixo-esquerda
            'p1': gf.Point(x_pos - corner_gap, top_walls_height + wall_thickness + gap * 2 + wall_length),
            'p2': gf.Point(x_pos + wall_length, top_walls_height + wall_thickness * 2 + gap * 2 + wall_length),
            'type': 'horizontal'
        },
        {
            #parede baixo-direita
            'p1': gf.Point(x_pos + wall_length + gap, top_walls_height + wall_thickness + gap * 2 + wall_length),
            'p2': gf.Point(x_pos + wall_length * 2 + gap + corner_gap, top_walls_height + wall_thickness * 2 + gap * 2 + wall_length),
            'type': 'horizontal'
        },
        {
            #parede esquerda
            'p1': gf.Point(x_pos - gap - wall_thickness, top_walls_height + wall_thickness + gap - corner_gap),
            'p2': gf.Point(x_pos - gap, top_walls_height + wall_thickness + gap + wall_length + corner_gap),
            'type': 'vertical'
        },
        {
            #parede direita
            'p1': gf.Point(x_pos + wall_length * 2 + gap * 2, top_walls_height + wall_thickness + gap - corner_gap),
            'p2': gf.Point(x_pos + wall_length * 2 + gap * 2 + wall_thickness, top_walls_height + wall_thickness + gap + wall_length + corner_gap),
            'type': 'vertical'
        },
    ]

    for wall in walls_info:
        wall_element = gf.Rectangle(wall['p1'], wall['p2'])
        wall_element.draw(win)
        wall_obj = Wall(wall_element, wall['type'])
        walls.append(wall_obj)

    
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
        



# sd.play('pool_music_1.wav')
window_size = 1000
win = gf.GraphWin('bar do patrick', window_size, window_size)

b1 = gf.Circle(gf.Point(150,298), 10)
b1.draw(win)
ball1 = Ball(b1)

table_balls = []
pocketed_balls = []
walls = []

b2 = gf.Circle(gf.Point(500,305), 10)
b2.draw(win)
ball2 = Ball(b2)

generate_table()
ball1.setVelocity_x(8)

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