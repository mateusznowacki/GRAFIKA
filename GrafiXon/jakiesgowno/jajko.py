import math
from OpenGL.GL import *
import os
from PIL import Image


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


def render_egg_with_texture(points, texture_id):
    """
    Rysuje jajko za pomocą siatki punktów 3D i nakłada teksturę.
    :param points: Tablica punktów 3D wygenerowana przez funkcję generate_egg_points.
    :param texture_id: Identyfikator tekstury OpenGL.
    """
    n = len(points)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_TRIANGLES)
    for i in range(n - 1):
        for j in range(n - 1):
            # Obliczanie współrzędnych tekstury
            t1 = (j / (n - 1), i / (n - 1))
            t2 = ((j + 1) / (n - 1), i / (n - 1))
            t3 = (j / (n - 1), (i + 1) / (n - 1))
            t4 = ((j + 1) / (n - 1), (i + 1) / (n - 1))

            # Punkty siatki
            p1 = points[i][j]
            p2 = points[i][j + 1]
            p3 = points[i + 1][j]
            p4 = points[i + 1][j + 1]

            # Rysowanie dwóch trójkątów dla każdego prostokąta
            glTexCoord2f(*t1)
            glVertex3f(*p1)
            glTexCoord2f(*t2)
            glVertex3f(*p2)
            glTexCoord2f(*t3)
            glVertex3f(*p3)

            glTexCoord2f(*t2)
            glVertex3f(*p2)
            glTexCoord2f(*t4)
            glVertex3f(*p4)
            glTexCoord2f(*t3)
            glVertex3f(*p3)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def load_texture(texture_path):
    """
    Ładuje teksturę z pliku w formacie .png lub .tga.
    :param texture_path: Ścieżka do pliku tekstury.
    :return: Identyfikator tekstury OpenGL.
    """
    if not os.path.exists(texture_path):
        print(f"Błąd: Plik tekstury {texture_path} nie istnieje!")
        return None

    image = Image.open(texture_path).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGB").tobytes()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0,
        GL_RGB, GL_UNSIGNED_BYTE, img_data
    )
    return texture_id


def draw_xyz_axes():
    """
    Rysuje osie układu współrzędnych XYZ w kontekście jajka.
    """
    glBegin(GL_LINES)
    # Oś X (czerwona)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    # Oś Y (zielona)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    # Oś Z (niebieska)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()
