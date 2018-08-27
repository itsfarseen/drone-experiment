import math
import random
import cairo
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


def snakefy(points):
    frame_i = 0
    snake = [points.pop(), points.pop()]
    for p in points:
        WIDTH, HEIGHT = 640, 480
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        ctx = cairo.Context(surface)
        ctx.rectangle(0, 0, 640, 480)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()

        draw_snake(ctx, snake.copy())
        surface.write_to_png("frame{}.png".format(frame_i))
        frame_i += 1
        # nls: nearest line segment
        nls_i = -1
        nls_cost = distance(p, snake[0])
        for i in range(0, len(snake)-1):
            dist = distance_from_line_approx(p, snake[i], snake[i+1])
            ls_length = distance(snake[i], snake[i+1])
            cost = dist - ls_length
            if (nls_i is None or cost < nls_cost):
                nls_i = i
                nls_cost = cost
        dist_end = distance(p, snake[len(snake)-1])
        if dist_end < nls_cost:
            nls_i = len(snake) - 1
            nls_cost = dist_end
        snake.insert(nls_i + 1, p)
    return snake


def draw_snake(ctx, points):
    p = points.pop(0)
    ctx.move_to(*p)
    ctx.set_source_rgb(1, 0, 0)
    ctx.arc(*p, 2, 0, 2*math.pi)
    ctx.stroke()
    ctx.move_to(*p)
    for p in points:
        ctx.set_source_rgb(0, 1, 0)
        ctx.line_to(*p)
        ctx.stroke()
        ctx.set_source_rgb(1, 0, 0)
        ctx.arc(*p, 2, 0, 2*math.pi)
        ctx.stroke()
        ctx.move_to(*p)


def draw(da, ctx):
    n = 10
    max_xy = (640, 480)
    src = generate_random_points(n, max_xy)
    src = snakefy(src)
    draw_snake(ctx, src)


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
