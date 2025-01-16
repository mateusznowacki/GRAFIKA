import math
import os
from OpenGL.GL import *



def load_obj(filename):
    """
    Wczytuje wierzchołki (v ...) i ściany (f ...) z pliku .obj.
    :param filename: Ścieżka do pliku .obj.
    :return: (vertices, faces)
        vertices: lista krotek (x, y, z)
        faces: lista krotek (i1, i2, i3)
               z indeksami wierzchołków tworzących trójkąt
    """
    vertices = []
    faces = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                # Wierzchołki (np. "v -3.0 1.8 0.0")
                if line.startswith('v '):
                    parts = line.split()
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    vertices.append((x, y, z))
                # Ściany (np. "f 1 2 3" lub "f 1/1/1 2/2/2 3/3/3")
                elif line.startswith('f '):
                    parts = line.split()[1:]  # Pomijamy 'f'
                    # Pobieramy tylko indeksy wierzchołków
                    face_indices = [int(p.split('/')[0]) - 1 for p in parts]
                    if len(face_indices) >= 3:
                        for i in range(1, len(face_indices) - 1):
                            i1 = face_indices[0]
                            i2 = face_indices[i]
                            i3 = face_indices[i + 1]
                            faces.append((i1, i2, i3))
    except FileNotFoundError:
        print(f"Plik {filename} nie został znaleziony.")
        return [], []

    return vertices, faces


def render_teapot(vertices, faces):
    """
    Rysuje czajnik za pomocą wczytanych wierzchołków (vertices) i ścian (faces),
    w jednolitym białym kolorze, jako siatkę trójkątów.
    :param vertices: Lista krotek (x, y, z).
    :param faces: Lista krotek (i1, i2, i3) - indeksy wierzchołków.
    """
    glColor3f(1.0, 1.0, 1.0)  # Ustaw jednolity biały kolor

    glBegin(GL_TRIANGLES)
    for (i1, i2, i3) in faces:
        # Pobieramy współrzędne 3 wierzchołków
        (vx1, vy1, vz1) = vertices[i1]
        (vx2, vy2, vz2) = vertices[i2]
        (vx3, vy3, vz3) = vertices[i3]

        # Rysujemy trójkąt
        glVertex3f(vx1, vy1, vz1)
        glVertex3f(vx2, vy2, vz2)
        glVertex3f(vx3, vy3, vz3)
    glEnd()


def load_texture(texture_path):
    """
    Ładuje teksturę z pliku w formacie TGA lub PNG.
    :param texture_path: Ścieżka do pliku tekstury.
    :return: Identyfikator tekstury OpenGL.
    """
    if not os.path.exists(texture_path):
        print(f"Błąd: Plik tekstury {texture_path} nie istnieje!")
        return None

    try:
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

    except Exception as e:
        print(f"Błąd podczas ładowania tekstury: {e}")
        return None


def draw_xyz_axes():
    """
    Rysuje osie układu współrzędnych XYZ w kontekście czajnika (lub dowolnego obiektu).
    """
    axis_length = 8.0

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