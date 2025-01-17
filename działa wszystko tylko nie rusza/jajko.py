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
    glBegin(GL_TRIANGLES)
    for i in range(len(points) - 1):
        for j in range(len(points[i]) - 1):
            glVertex3fv(points[i][j])
            glVertex3fv(points[i][j + 1])
            glVertex3fv(points[i + 1][j])

            glVertex3fv(points[i + 1][j])
            glVertex3fv(points[i][j + 1])
            glVertex3fv(points[i + 1][j + 1])
    glEnd()

#############################################################################
# def render_egg(points):
#     """
#     Rysuje jajko za pomocą siatki punktów 3D.
#     Uwzględnia poprawne kierunki rysowania dla obu połówek jajka.
#     :param points: Tablica punktów 3D wygenerowana przez funkcję generate_egg_points.
#     """
#     n = len(points)
#     glColor3f(1.0, 1.0, 1.0)  # Ustaw biały kolor
#
#     glBegin(GL_TRIANGLES)
#     for i in range(n - 1):
#         for j in range(n - 1):
#             # Punkty siatki
#             p1 = points[i][j]
#             p2 = points[i][j + 1]
#             p3 = points[i + 1][j]
#             p4 = points[i + 1][j + 1]
#
#             # Rysowanie trójkątów z uwzględnieniem kierunku rysowania
#             if i < n // 2:  # Górna połowa
#                 # Trójkąt 1
#                 glVertex3f(*p1)
#                 glVertex3f(*p3)
#                 glVertex3f(*p2)
#
#                 # Trójkąt 2
#                 glVertex3f(*p2)
#                 glVertex3f(*p3)
#                 glVertex3f(*p4)
#             else:  # Dolna połowa (odwrócone trójkąty)
#                 # Trójkąt 1
#                 glVertex3f(*p1)
#                 glVertex3f(*p2)
#                 glVertex3f(*p3)
#
#                 # Trójkąt 2
#                 glVertex3f(*p2)
#                 glVertex3f(*p4)
#                 glVertex3f(*p3)
#     glEnd()
##########################################################################

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
