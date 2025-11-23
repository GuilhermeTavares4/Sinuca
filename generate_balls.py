import graphics as gf


win = gf.GraphWin('bar do patrick', 1000, 1000)

class Ball:
    def __init__(self, element, color, number, number_color): #number e number_color são instâncias de Text e Circle gf
        self.element = element
        self.radius = element.getRadius()

        self.color = color
        self.number = number
        self.number_color = number_color
        
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

table_balls = []

def generate_balls(radius):
    colors = ["Yellow", "Blue", "Red", "Purple", "Orange", "Green", "Brown", "Black"]
    text_color = "Black"
    center_circle_color = "White"
    cx = 100 #Valor arbitrário
    cy = 100 #Valor arbitrário


    table_balls.append(gf.Circle(gf.Point(radius, radius), radius)) # Bola branca

    color_picker = 0
    for i in range(1, 15):
        
        if color_picker == 8: # Recomeça na lista de cores depois da preta, que nunca é alcançada 2 vezes
            color_picker = 0

        if i > 8: # Círculo interno e texto ficam diferentes
            text_color = "White"
            center_circle_color = "Black"

        #(self, element, color, number, number_color) #number e number_color são instâncias de Text e Circle gf
        table_balls.append(
            Ball(gf.Circle(gf.Point(cx, cy), radius).draw(win),
            colors[color_picker], 
            gf.Text(gf.Point(cx, cy), str(i)).setFill(text_color), # Número da bola e sua cor
            gf.Circle(gf.Point(cx, cy), radius).setFill(center_circle_color))) # Cículo do texto da bola e sua cor

        # Ball(gf.Circle(gf.Point(cx, cy), radius).draw(win),
        #     colors[color_picker], 
        #     gf.Text(gf.Point(cx, cy), str(i)).setFill(text_color), # Número da bola e sua cor
        #     gf.Circle(gf.Point(cx, cy), radius).setFill(center_circle_color)) # Cículo do texto da bola e sua cor
        
        # gf.Circle(gf.Point(cx, cy), radius).draw(win)
        # test = gf.Circle(gf.Point(cx, cy), radius)
        # test.draw(win)

        color_picker += 1

        # Por agora só forma uma linha em diagonal
        cx += radius
        cy += radius

generate_balls(20)

print(table_balls)
win.getMouse()
win.close()