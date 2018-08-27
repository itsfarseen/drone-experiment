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


print(will_collide((599, 117), (366, 436), (272, 385), (434, 357)))
