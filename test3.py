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
    ctx.set_source_rgb(0.1, 0.1, 0.1)
    pair_iter = zip(src, dest)
    for s, p in pair_iter:
        ctx.set_source_rgb(1, 0, 0)
        ctx.move_to(*s)
        ctx.arc(*s, 2, 0, 2*math.pi)
        ctx.stroke()

        ctx.set_source_rgb(0, 1, 0)
        ctx.move_to(*p)
        ctx.arc(*p, 2, 0, 2*math.pi)
        ctx.stroke()

        ctx.set_source_rgb(0, 0, 1)
        ctx.move_to(*s)
        ctx.line_to(*p)
        ctx.stroke()


def determinant(m):
    return m[0][0]*m[1][1] - m[0][1]*m[1][0]


def will_collide(s1, d1, s2, d2):
    a1 = s1[1]-d1[1]
    b1 = -(s1[0]-d1[0])
    c1 = s1[0]*a1 + d1[0]*b1
    a2 = s2[1]-d2[1]
    b2 = -(s2[0]-d2[0])
    c2 = s2[0]*a2 + d2[0]*b2

    denominator = determinant([[a1, b1], [a2, b2]])
    if denominator == 0:
        return c1 == c2*a1/a2

    x = determinant([[c1, b1], [c2, b2]])/denominator
    return x >= min(s1[0], d1[0]) and x <= max(s1[0], d1[0])


def swap_items(l, n, m):
    temp = l[n]
    l[n] = l[m]
    l[m] = temp


# ----------- MAIN LOGIC --------------------------------
# Note, resizing the window will redraw using a different
# random set of points
def draw(da, ctx):
    n = 3
    max_xy = (640, 480)
    src = generate_random_points(n, max_xy)
    dest = generate_random_points(n, max_xy)

    print(len(src))
    print(len(dest))

    frame_i = 0
    WIDTH, HEIGHT = 640, 480

    any_collisions = True
    while any_collisions:

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        ctx2 = cairo.Context(surface)
        ctx2.rectangle(0, 0, 640, 480)
        ctx2.set_source_rgb(1, 1, 1)
        ctx2.fill()
        ctx2.translate(0.1, 0.1)
        draw_path(ctx2, src, dest)
        surface.write_to_png("frame{}.png".format(frame_i))
        frame_i += 1

        any_collisions = False
        for i in range(0, n):
            if will_collide(src[i], dest[i], src[(i+1) % n], dest[(i+1) % n]):
                any_collisions = True
                print((src[i], dest[i], src[(i+1) % n], dest[(i+1) % n]))
                swap_items(dest, i, (i+1) % n)
                print((src[i], dest[i], src[(i+1) % n], dest[(i+1) % n]))
                print()
            else:
                print("Wont collide", (src[i], dest[i], src[(i+1) % n], dest[(i+1) % n]))
        else:
            print("any_collisions", any_collisions)

    draw_path(ctx, src, dest)


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
