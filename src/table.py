from . import graphics as gf
import math
import time

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

    def rotate_polygon_to_angle(self, angle_rad, win):
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
        cue_velocity = distance / 9
        ball_velocity = distance / 10
        if ball_velocity > 23:
            ball_velocity = 23
            cue_velocity = 23
        while distance > target.getRadius():
            self.element.move(nx * cue_velocity * -1, ny * cue_velocity * -1)
            dx += nx * cue_velocity * -1
            dy += ny * cue_velocity * -1
            distance = math.sqrt(dx * dx + dy * dy)
            time.sleep(0.01)
        target.setVelocity_x(nx * ball_velocity * -1)
        target.setVelocity_y(ny * ball_velocity * -1)


    def draw_assist_line(self, dx, dy, spawn_pos, win):
        spawn_x = spawn_pos.getX()
        spawn_y = spawn_pos.getY()
        distance = math.sqrt(dx * dx + dy * dy)
        self.assist_line = gf.Line(gf.Point(spawn_x, spawn_y), gf.Point(spawn_x + dx / distance * -70, spawn_y + dy / distance * -70))
        self.assist_line.setArrow('last')
        self.assist_line.draw(win)
        

    def undraw(self):
        self.assist_line.undraw()
        self.element.undraw()


def use_cue(cue, table_balls, win):
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
            cue.rotate_polygon_to_angle(angle_rad, win)
            cue.draw_assist_line(dx, dy, table_balls[0].element.getCenter(), win)

        key = win.checkKey()
        if pos and key == 'space':
            break
    cue.move_towards_target(table_balls[0])
    cue.undraw()


def generate_table(win):
    x_start_pos = 420
    walls = []
    holes = []
    top_walls_height = 250
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

    return walls, holes