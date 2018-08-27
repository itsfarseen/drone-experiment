import math
import random
import cairo
import operator
from gi.repository import Gtk


def generate_random_points(n, max_xy):
    x, y = max_xy
    return [(random.randint(0, x), random.randint(0, y)) for i in range(0, n)]


def distance(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)


def vec_sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def vec_mod(p):
    return math.sqrt(p[0]**2+p[1]**2)


def distance_from_line(point, lineA, lineB):
    # lineA, lineB forms the line segment
    vec_AP = vec_sub(point, lineA)
    vec_AB = vec_sub(lineB, lineA)
    cross_prod = vec_AP[0]*vec_AB[1] - vec_AB[0]*vec_AP[1]
    dist = cross_prod/vec_mod(vec_AB)
    return abs(dist)


def distance_from_line_approx(point, lineA, lineB):
    # lineA, lineB forms the line segment
    return distance(point, lineA) + distance(point, lineB)


def distance_from_lineA_parallel(point, lineA, lineB):
    # lineA, lineB forms the line segment
    vec_AP = vec_sub(point, lineA)
    vec_AB = vec_sub(lineB, lineA)
    dot_prod = vec_AP[0]*vec_AB[0] + vec_AB[1]*vec_AP[1]
    dist = dot_prod/vec_mod(vec_AB)
    return dist


def com(points):
    com_unnorm = sum(x for x, y in points), sum(y for x, y in points)
    return (com_unnorm[0]/len(points), com_unnorm[1]/len(points))


def snakefy(points):
    x_c, y_c = com(points)
    print(points)
    points.sort(key=lambda p: math.atan2(p[1]-y_c, p[0]-x_c))
    print(points)
    return points


def tuple_add(p, q):
    return tuple(map(operator.add, p, q))


def tuple_sub(p, q):
    return tuple(map(operator.sub, p, q))


def tuple_dot(p, q):
    return tuple(map(operator.mul, p, q))


def draw_snake(ctx, points, base_color=(1, 1, 1)):
    p = points.pop(0)
    ctx.move_to(*p)
    ctx.set_source_rgb(*tuple_dot((0.8, 0.6, 0.6), base_color))
    ctx.arc(*p, 2, 0, 2*math.pi)
    ctx.stroke()
    ctx.move_to(*p)
    for p in points:
        ctx.set_source_rgb(*tuple_dot((0.6, 0.8, 0.6), base_color))
        ctx.line_to(*p)
        ctx.stroke()
        ctx.set_source_rgb(*tuple_dot((0.8, 0.6, 0.6), base_color))
        ctx.arc(*p, 2, 0, 2*math.pi)
        ctx.stroke()
        ctx.move_to(*p)
    p = com(points)
    ctx.move_to(*p)
    ctx.set_source_rgb(*tuple_dot((0.6, 0.6, 0.6), base_color))
    ctx.arc(*p, 2, 0, 2*math.pi)
    ctx.stroke()


def draw_path(ctx, src, dest):
    pass
    # ctx.set_source_rgb(0.1, 0.1, 0.1)
    # pair_iter = zip(src, dest):
    # for i in range(0, len(pair_iter)-1):


# ----------- MAIN LOGIC --------------------------------
# Note, resizing the window will redraw using a different
# random set of points
def draw(da, ctx):
    n = 10
    max_xy = (640, 480)
    src = generate_random_points(n, max_xy)
    # snakefy: permute the points so that it forms a snake of shortest length
    src = snakefy(src)
    dest = generate_random_points(n, max_xy)
    dest = snakefy(dest)

    # Calculate the C.O.M of src snake,
    # Move it so that it coincides with the C.O.M of dest snake.
    # This operation is trivial, move everything by same distance,
    # so it is not drawn.
    src_com = com(src)
    dest_com = com(dest)
    diff_com = tuple_sub(dest_com, src_com)

    # I have a slight feeling that this might simplify the problem,
    # Not rigorously sure though.
    # Comments appreciated.

    src_new = [tuple_add(p, diff_com) for p in src]

    draw_snake(ctx, src_new.copy(), (1, 0.5, 0.5))
    draw_snake(ctx, dest.copy(), (0.5, 1, 0.5))
    draw_path(ctx, src_new, dest)


# main ---------------------------------
win = Gtk.Window()
win.set_type_hint(1)  # 1 = DIALOG
win.connect('destroy', lambda w: Gtk.main_quit())
win.set_default_size(640, 480)

drawing_area = Gtk.DrawingArea()
win.add(drawing_area)
drawing_area.connect('draw', draw)

win.show_all()
Gtk.main()
