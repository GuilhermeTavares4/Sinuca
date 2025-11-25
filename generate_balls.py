import graphics as gf
import time
import random


# win = gf.GraphWin('bar do patrick', 1000, 1000)

class Ball:
    def __init__(self, element, ball_text_circle, text): # ball_text_circle e text são instâncias de Circle e Text do gf
        self.element = element
        self.radius = element.getRadius()
        self.text_circle = ball_text_circle
        self.number = text
        
        self.velocity_x = 0
        self.velocity_y = 0
        self.drag = 1.1

    def move(self):
        self.element.move(self.velocity_x, self.velocity_y)
        if self.text_circle != None and self.number != None: # No caso da bola branca
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

        self.velocity_x -= self.velocity_x * self.drag * 0.01
        self.velocity_y -= self.velocity_y * self.drag * 0.01

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


def BallScramble():
    positions = []
    numbers = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]

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
    ball = gf.Circle(gf.Point(whiteBallCoordX, triangleCoords[1]), radius)
    ball.setFill("White")
    ball.draw(win)
    table_balls.append(Ball(ball, None, None))

    for i, ball_number in enumerate(balls_postions):
        
        if ball_number <= 8: # Círculo interno e texto ficam diferentes
            text_color = "Black"
            center_circle_color = "White"
        else:
            text_color = "White"
            center_circle_color = "Black"

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
        
        table_balls.append(Ball(ball, text_circle, text))        

        if i == colN[0]:
            triangleCoords[0] += 2*radius # Coordenada X
            colN[0] += colN[1]
            colN[1] += 1
            triangleCoords[1] = triangleCoords[2] - (colN[1] * radius) # Coordenadas Y, e Y0
        triangleCoords[1] += 2*radius + 1 # Coordenada Y

    return table_balls

# table_balls = generate_balls(190, [250, 250], 30)

# for bola in table_balls:
#     bola.setVelocity_x(4)

# while True:
#     for bola in table_balls:
#         bola.move()
#     time.sleep(0.01)


# win.getMouse()
# win.close()

