import math
from OpenGL.GL import *
import os


###########################################################
# def generate_egg_points(n):
#     """
#     Generuje punkty jajka na podstawie parametryzacji powierzchni.
#     :param n: Liczba punktów wzdłuż jednej osi (NxN siatka).
#     :return: Tablica punktów 3D w formacie (x, y, z).
#
# """
#     glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
#     glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.5, 0.3, 1.0])
#     glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
#     glMaterialf(GL_FRONT, GL_SHININESS, 50.0)  # Połyskliwość
#     points = []
#     for i in range(n):
#         u = i / (n - 1)
#         row = []
#         for j in range(n):
#             v = j / (n - 1)
#
#             # Wzory parametryczne jajka
#             x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)
#             y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
#             z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v)
#
#             row.append((x, y, z))
#         points.append(row)
#     return points
#################################################################################

def generate_egg_points(n):
    points = []
    for i in range(n):
        u = i / (n - 1)
        row = []
        for j in range(n):
            v = j / (n - 1)

            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v)

            row.append((x, y, z))
        points.append(row)
    return points


def render_egg(points):
    n = len(points)
    glBegin(GL_TRIANGLES)
    for i in range(n - 1):
        for j in range(n - 1):
            # Punkty siatki
            p1 = points[i][j]
            p2 = points[i][j + 1]
            p3 = points[i + 1][j]
            p4 = points[i + 1][j + 1]

            # Mapowanie cylindryczne współrzędnych tekstury
            t1 = ((j / (n - 1)) , (i / (n - 1)) )
            t2 = (((j + 1) / (n - 1)) , (i / (n - 1)) )
            t3 = ((j / (n - 1)) , ((i + 1) / (n - 1)) )
            t4 = (((j + 1) / (n - 1)) , ((i + 1) / (n - 1)) )

            # Obsługa szwu: Dopasowanie granicy tekstury
            if j == n - 2:  # Ostatni segment siatki
                t2 = (1.0 , t2[1])
                t4 = (1.0 , t4[1])

            # Rysowanie trójkątów z uwzględnieniem kierunku teksturowania
            if i < n // 2:  # Górna połowa (CCW teksturowanie)
                # Trójkąt 1
                glTexCoord2f(*t1)
                glVertex3f(*p1)
                glTexCoord2f(*t3)
                glVertex3f(*p3)
                glTexCoord2f(*t2)
                glVertex3f(*p2)

                # Trójkąt 2
                glTexCoord2f(*t2)
                glVertex3f(*p2)
                glTexCoord2f(*t3)
                glVertex3f(*p3)
                glTexCoord2f(*t4)
                glVertex3f(*p4)
            else:  # Dolna połowa (CW teksturowanie, odwrócone u/v)
                # Odwracamy mapowanie tekstury, aby poprawnie nałożyć teksturę na dolnej połowie
                t1 = (t1[0], 1.0  - t1[1])
                t2 = (t2[0], 1.0  - t2[1])
                t3 = (t3[0], 1.0  - t3[1])
                t4 = (t4[0], 1.0  - t4[1])

                # Trójkąt 1
                glTexCoord2f(*t1)
                glVertex3f(*p1)
                glTexCoord2f(*t2)
                glVertex3f(*p2)
                glTexCoord2f(*t3)
                glVertex3f(*p3)

                # Trójkąt 2
                glTexCoord2f(*t2)
                glVertex3f(*p2)
                glTexCoord2f(*t4)
                glVertex3f(*p4)
                glTexCoord2f(*t3)
                glVertex3f(*p3)
    glEnd()


def draw_xyz_axes():
    """
    Rysuje osie układu współrzędnych XYZ w kontekście jajka.
    """
    axis_length = 8.0  # Nowa długość osi
    glDisable(GL_LIGHTING)
    glBegin(GL_LINES)
    # Oś X (czerwona)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-axis_length, 0.0, 0.0)
    glVertex3f(axis_length, 0.0, 0.0)

    # Oś Y (zielona)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -axis_length, 0.0)
    glVertex3f(0.0, axis_length, 0.0)

    # Oś Z (niebieska)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -axis_length)
    glVertex3f(0.0, 0.0, axis_length)
    glEnd()
    glEnable(GL_LIGHTING)
