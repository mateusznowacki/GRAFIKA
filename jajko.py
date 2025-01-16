import math
from OpenGL.GL import *
import os


def generate_egg_points(n):
    """
    Generuje punkty jajka na podstawie parametryzacji powierzchni.
    :param n: Liczba punktów wzdłuż jednej osi (NxN siatka).
    :return: Tablica punktów 3D w formacie (x, y, z).
    """
    points = []
    for i in range(n):
        u = i / (n - 1)
        row = []
        for j in range(n):
            v = j / (n - 1)

            # Wzory parametryczne jajka
            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v)

            row.append((x, y, z))
        points.append(row)
    return points


def render_egg(points, normals):
    """
    Renderuje jajko z użyciem punktów i normalnych.
    :param points: Lista punktów siatki 3D.
    :param normals: Lista normalnych siatki 3D.
    """
    n = len(points)
    glBegin(GL_TRIANGLES)
    for i in range(n - 1):
        for j in range(n - 1):
            # Trójkąt 1
            glNormal3fv(normals[i][j])
            glVertex3fv(points[i][j])

            glNormal3fv(normals[i + 1][j])
            glVertex3fv(points[i + 1][j])

            glNormal3fv(normals[i][j + 1])
            glVertex3fv(points[i][j + 1])

            # Trójkąt 2
            glNormal3fv(normals[i][j + 1])
            glVertex3fv(points[i][j + 1])

            glNormal3fv(normals[i + 1][j])
            glVertex3fv(points[i + 1][j])

            glNormal3fv(normals[i + 1][j + 1])
            glVertex3fv(points[i + 1][j + 1])
    glEnd()



def compute_normal(p1, p2, p3):
    """
    Oblicza wektor normalny dla trójkąta zdefiniowanego przez trzy punkty.
    :param p1: Punkt 1 (x, y, z).
    :param p2: Punkt 2 (x, y, z).
    :param p3: Punkt 3 (x, y, z).
    :return: Wektor normalny (x, y, z).
    """
    u = [p2[i] - p1[i] for i in range(3)]
    v = [p3[i] - p1[i] for i in range(3)]

    # Iloczyn wektorowy
    normal = [
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
        ]
    length = math.sqrt(sum(coord**2 for coord in normal))
    if length == 0:
        return [0.0, 0.0, 1.0]  # Domyślna normalna
    return [coord / length for coord in normal]

def compute_vertex_normals(points):
    """
    Oblicza normalne dla każdego wierzchołka siatki jajka.
    :param points: Lista punktów siatki 3D.
    :return: Tablica normalnych dla każdego wierzchołka.
    """
    n = len(points)
    normals = [[None for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            # Oblicz normalną jako wektor od środka jajka do wierzchołka
            x, y, z = points[i][j]
            length = math.sqrt(x**2 + y**2 + z**2)
            normal = [x / length, y / length, z / length]

            # Odwrócenie normalnych dla dolnej połowy jajka
            if i > n // 2:
                normal = [-coord for coord in normal]

            normals[i][j] = normal

    return normals


def draw_xyz_axes():
    """
    Rysuje osie układu współrzędnych XYZ w kontekście jajka.
    Uwzględnia oświetlenie (wyłączone na czas rysowania osi).
    """
    axis_length = 8.0  # Nowa długość osi

    glDisable(GL_LIGHTING)  # Wyłączenie oświetlenia
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
    glEnable(GL_LIGHTING)  # Ponowne włączenie oświetlenia


