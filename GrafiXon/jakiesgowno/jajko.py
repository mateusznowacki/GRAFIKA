import math
from OpenGL.GL import *
import os
from PIL import Image

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
            normals[i][j] = [x / length, y / length, z / length]

    return normals


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
    glColor3f(1.0, 1.0, 1.0)  # Ustaw biały kolor

    glBegin(GL_TRIANGLES)
    for i in range(n - 1):
        for j in range(n - 1):
            repeat_factor = 1.0  # Powtórz teksturę w pionie i poziomie
            t1 = (j / (n - 1) * repeat_factor, i / (n - 1) * repeat_factor)
            t2 = ((j + 1) / (n - 1) * repeat_factor, i / (n - 1) * repeat_factor)
            t3 = (j / (n - 1) * repeat_factor, (i + 1) / (n - 1) * repeat_factor)
            t4 = ((j + 1) / (n - 1) * repeat_factor, (i + 1) / (n - 1) * repeat_factor)

            # Punkty siatki
            p1 = points[i][j]       # Punkt (i, j)
            p2 = points[i][j + 1]   # Punkt (i, j+1)
            p3 = points[i + 1][j]   # Punkt (i+1, j)
            p4 = points[i + 1][j + 1]  # Punkt (i+1, j+1)

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
    glDisable(GL_TEXTURE_2D)


def load_texture(texture_path):
    """
    Ładuje teksturę z pliku w formacie TGA.
    :param texture_path: Ścieżka do pliku tekstury.
    :return: Identyfikator tekstury OpenGL.
    """
    if not os.path.exists(texture_path):
        print(f"Błąd: Plik tekstury {texture_path} nie istnieje!")
        return None

    try:
        from PIL import Image

        # Ładowanie obrazu i konwersja na dane RGB
        image = Image.open(texture_path).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGB").tobytes()

        # Generowanie tekstury
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

    except Exception as e:
        print(f"Błąd podczas ładowania tekstury: {e}")
        return None


def draw_xyz_axes():
    """
    Rysuje osie układu współrzędnych XYZ w kontekście jajka.
    """
    axis_length = 8.0  # Nowa długość osi

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
