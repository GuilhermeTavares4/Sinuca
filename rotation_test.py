import math
from graphics import *

def get_center(polygon):
    """Calculates the center point of a polygon."""
    points = polygon.getPoints()
    sum_x = sum(p.getX() for p in points)
    sum_y = sum(p.getY() for p in points)
    return Point(sum_x / len(points), sum_y / len(points))


def rotate_polygon_to_angle(polygon, angle_rad):
    """
    Rotates a polygon around its OWN center to a specific absolute angle.
    Returns a NEW polygon (does not modify the old one).
    """
    center = get_center(polygon)
    r = 8
    points = polygon.getPoints()
    base_coords = [(+200, -r), (0, -r + 5), (0, r - 5), (+200, r)]
    #base_coords = [(-200, -r), (0, -r + 5), (0, r - 5), (-200, r)] #taco invertido (braian)
    
    
    new_points = []
    for x, y in base_coords:
        rotated_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        rotated_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        
        final_p = Point(rotated_x + center.getX(), rotated_y + center.getY())
        new_points.append(final_p)
        
    new_poly = Polygon(new_points)
    new_poly.setFill(polygon.config['fill'])
    new_poly.setOutline(polygon.config['outline'])
    return new_poly


def move_polygon_to_point(polygon, click):
        polygon.undraw()
        points = [Point(click.getX() - 100, click.getY() - 25), Point(click.getX() + 100, click.getY() - 25), Point(click.getX() + 100, click.getY() + 25), Point(click.getX() - 100, click.getY() + 25)]
        new_polygon = Polygon(points)
        return new_polygon


def main():
    win = GraphWin("Look At Target", 700, 700)
    win.setBackground("white")

    cx, cy = 350, 350
    ball = Circle(Point(cx,cy), 5)
    ball.draw(win)

    player = Polygon(Point(225, 225), Point(275, 225), Point(278, 275), Point(222, 275))
    player.setFill("skyblue")
    player.setOutline("black")
    player.draw(win)


    
    message = Text(Point(250, 50), "Move mouse to rotate square").draw(win)

    while True:

        target = win.getMouse()
        moved_player = move_polygon_to_point(player, Point(target.getX(), target.getY()))
        
        dy = target.getY() - cy
        dx = target.getX() - cx
        
        angle_rad = math.atan2(dy, dx)

        new_player = rotate_polygon_to_angle(moved_player, angle_rad)
        


        player.undraw() 

        
        player = new_player

        
        player.draw(win)

    win.close()

main()