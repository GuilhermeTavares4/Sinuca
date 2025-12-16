from . import graphics as gf
import math
import time
import random


# win = gf.GraphWin('bar do patrick', 1000, 1000)

class Ball:
    def __init__(self, element, ball_text_circle, text, ball_type): # ball_text_circle e text são instâncias de Circle e Text do gf
        self.element = element
        self.radius = element.getRadius()
        self.text_circle = ball_text_circle
        self.number = text
        self.ball_type = ball_type
        self.velocity_x = 0
        self.velocity_y = 0
        self.drag = 0.7

    def __repr__(self):
        return self.number.getText()

    def move(self):
        self.element.move(self.velocity_x, self.velocity_y)
        if self.text_circle != None: # and self.number != None  // No caso da bola branca
            center = self.element.getCenter()
            X = center.getX()
            Y = center.getY()
            text_circle_pos = self.text_circle.getCenter()
            text_pos = self.number.getAnchor()
            self.text_circle.move(X - text_circle_pos.getX(), Y - text_circle_pos.getY())
            self.number.move(X - text_pos.getX(), Y - text_pos.getY())

        if abs(self.velocity_x) <= 0.15 and abs(self.velocity_y) <= 0.15:
            self.velocity_x = 0
            self.velocity_y = 0

        self.velocity_x -= self.velocity_x * self.drag * 0.016
        self.velocity_y -= self.velocity_y * self.drag * 0.016

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
    
    def undraw(self):
        self.element.undraw()
        if self.text_circle != None:
            self.text_circle.undraw()
            self.number.undraw()


def BallScramble():
    positions = []
    numbers = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]
    # numbers = [1, 2, 3, 9, 10, 11] # apenas para testes

    chosen8 = random.randint(1, 9) # Sorteia a posição da bola 8 | 33.33%

    while len(numbers) != 0:
        chosen = random.choice(numbers)      
        if (chosen8 <= 3 and len(positions) == 4) or (chosen8 > 3 and chosen8 <= 6 and len(positions) == 7) or (chosen8 > 6 and chosen8 <= 9 and len(positions) == 8):
            chosen = 8

        if chosen != 8:
            numbers.pop(numbers.index(chosen))
            
        positions.append(chosen)
        # print(f"\n>>{chosen} |  {positions}")

    return positions


def generate_balls(whiteBallCoordX: int, triangleCoords: list, radius, win):
    colors = [[1, 9, "Yellow"], [2, 10, "Blue"], [3, 11, "Red"], [4, 12, "Purple"], [5, 13, "Orange"], [6, 14, "Green"], [7, 15, "Brown"], [8, "Black"]]
    # colors = [[1, 9, "Yellow"], [2, 10, "Blue"], [3, 11, "Red"], [8, "Black"]] # apenas para testes
    triangleCoords.append(triangleCoords[1]) # Salvando o valor original de y
    balls_postions = BallScramble()
    table_balls = []
    
    colN = [0, 2]

    if whiteBallCoordX > triangleCoords[0] - 2*radius:
        print(f"\n>>> Erro! \nA bola branca está em x = {whiteBallCoordX} mas a bola do triângulo está em x = {triangleCoords[0]}, \nHavendo sobreposição já que o raio é {radius} (diâmetro = {2*radius})\n")
        return

    ###################
    ### Bola Branca
    ###################
    table_balls.append(spawn_cue_ball(whiteBallCoordX, triangleCoords[1], radius, win))

    for i, ball_number in enumerate(balls_postions):
        
        if ball_number <= 8: # Círculo interno e texto ficam diferentes
            text_color = "Black"
            center_circle_color = "White"
            ball_type = "low_ball"
            if ball_number == 8:
                ball_type = "8_ball"
        else:
            text_color = "White"
            center_circle_color = "Black"
            ball_type = "high_ball"

        ###################
        ### Criando a bola
        ###################
        ball = gf.Circle(gf.Point(triangleCoords[0], triangleCoords[1]), radius)
        for color_info in colors:
            if ball_number in color_info:
                color = color_info[-1]
                break
        ball.setFill(color)
        ball.draw(win)
        
        ###################
        ### Criando o círculo para o texto da bola
        ###################
        text_circle = gf.Circle(gf.Point(triangleCoords[0], triangleCoords[1]), radius/1.9)
        text_circle.setFill(center_circle_color)
        text_circle.draw(win)

        ###################
        ### Criando o texto da bola
        ###################
        text = gf.Text(gf.Point(triangleCoords[0], triangleCoords[1]), str(ball_number))
        text.setFill(text_color)
        text.setSize(round(radius*0.5))
        text.draw(win)
        
        table_balls.append(Ball(ball, text_circle, text, ball_type))        

        if i == colN[0]:
            triangleCoords[0] += 2*radius # Coordenada X
            colN[0] += colN[1]
            colN[1] += 1
            triangleCoords[1] = triangleCoords[2] - (colN[1] * radius) # Coordenadas Y, e Y0
        triangleCoords[1] += 2*radius + 1 # Coordenada Y

    return table_balls


def spawn_cue_ball(spawn_x, spawn_y, radius, win):
    cue_ball = gf.Circle(gf.Point(spawn_x, spawn_y), radius)
    cue_ball.setFill("White")
    cue_ball.draw(win)
    return Ball(cue_ball, None, None, 'cue_ball')


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
        if ball1.text_circle != None:
            ball1.text_circle.move((displacement * dx / distance) * -1, (displacement * dy / distance) * -1)
            ball1.number.move((displacement * dx / distance) * -1, (displacement * dy / distance) * -1)

        ball2.element.move(displacement * dx / distance, displacement * dy / distance)
        if ball2.text_circle != None:
            ball2.text_circle.move(displacement * dx / distance, displacement * dy / distance)
            ball2.number.move(displacement * dx / distance, displacement * dy / distance)
        

        rel_vx = ball1.getVelocity_x() - ball2.getVelocity_x()
        rel_vy = ball1.getVelocity_y() - ball2.getVelocity_y()

        dot_product = (rel_vx * nx) + (rel_vy * ny)

        ball1.setVelocity_x((ball1.getVelocity_x() - dot_product * nx) * 0.95)
        ball1.setVelocity_y((ball1.getVelocity_y() - dot_product * ny) * 0.95)        
        
        ball2.setVelocity_x((ball2.getVelocity_x() + dot_product * nx) * 0.95)
        ball2.setVelocity_y((ball2.getVelocity_y() + dot_product * ny) * 0.95)

        # retorna a bola que a branca acertou
        if ball1.ball_type == "cue_ball":
            return ball2
    return None


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
        displacement = distance - ball.getRadius()
        if distance < 1:
            distance = 1
        if abs(dy) < abs(dx):
            ball.element.move((displacement * dx / distance) * -1, 0)
            ball.setVelocity_x(ball.getVelocity_x() * -0.9)
        else:
            ball.element.move(0, (displacement * dy / distance) * -1)
            ball.setVelocity_y(ball.getVelocity_y() * -0.9)
        
    
def Ball_Hole_Collision(table_balls, ball, hole, player, teams):
    ball_center = ball.element.getCenter()
    hole_center = hole.element.getCenter()
    dx = ball_center.getX() - hole_center.getX()
    dy = ball_center.getY() - hole_center.getY()
    distance = math.sqrt(dx * dx  + dy * dy)

    #verifica se as bola e o buraco estão colidindo :)
    if distance < (ball.element.getRadius() * 0.5 + hole.element.getRadius()):
        if player in teams[0].players:
            team = teams[0]
            other_team = teams[1]
        else:
            team = teams[1]
            other_team = teams[0]

        team.player_pocketed(player, ball)
        table_balls.remove(ball)
        ball.undraw()

        return ball
    
    return None


#verifica se ainda tem alguma bola se mexendo na mesa
def balls_still_moving(table_balls):
    for ball in table_balls:
        if ball.getVelocity_x() != 0 or ball.getVelocity_y() != 0:
            return True            
    return False


def get_lowest_ball(table_balls, team):
        team_balls = list(filter(lambda ball: ball.ball_type == team.target_ball_type, table_balls))
        if len(team_balls) > 0:
            lowest_ball = min(team_balls, key = lambda ball: int(ball.number.getText()))
            return lowest_ball
        return None


def get_team_balls(table_balls, team):
        team_balls = list(filter(lambda ball: ball.ball_type == team.target_ball_type, table_balls))
        return team_balls


def check_if_ball_pocketed(pocketed_balls, ball_type):
    for ball in pocketed_balls:
        if ball.ball_type == ball_type:
            return True
    return False


def check_if_ball_on_table(table_balls, ball_type):
    for ball in table_balls:
        if ball.ball_type == ball_type:
            return True
    return False