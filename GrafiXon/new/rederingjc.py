import sys  # Obsługa systemu i argumentów
from glfw.GLFW import *  # Biblioteka GLFW do obsługi okien i zdarzeń
from OpenGL.GL import *  # OpenGL do renderowania
from OpenGL.GLU import *  # Funkcje pomocnicze OpenGL
import math  # Obsługa obliczeń matematycznych
import random  # Generowanie losowych kolorów
import numpy as np

# Zainicjalizowane zmienne globalne
camera_position = [0.0, 0.0, -10.0]
camera_angle_x = 0.0
camera_angle_y = 0.0
points = []

# Funkcja inicjalizacyjna
def startup():
    """Inicjalizuje środowisko OpenGL."""
    update_viewport(None, 400, 400)  # Ustawienie początkowego rozmiaru okna
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Ustawienie koloru tła (czarny)
    glEnable(GL_DEPTH_TEST)  # Włączenie bufora głębi do poprawnego renderowania 3D

# Obsługa zmiany widoku
def update_viewport(window, width, height):
    """Aktualizuje widok w przypadku zmiany rozmiaru okna."""
    if width == 0: width = 1  # Zapobieganie dzieleniu przez zero
    if height == 0: height = 1
    aspect_ratio = width / height  # Proporcja szerokości do wysokości okna
    glMatrixMode(GL_PROJECTION)  # Przełączanie na macierz projekcji
    glViewport(0, 0, width, height)  # Ustawienie obszaru widocznego
    glLoadIdentity()  # Resetowanie macierzy projekcji
    gluPerspective(45, aspect_ratio, 1.0, 50.0)  # Ustawienie perspektywy
    glMatrixMode(GL_MODELVIEW)  # Przełączanie na macierz widoku
    glLoadIdentity()  # Resetowanie macierzy widoku




# Rysowanie osi XYZ
def draw_axes():
    """Rysuje osie układu współrzędnych XYZ."""
    glBegin(GL_LINES)
    # Oś X (czerwona)
    glColor3f(1.0, 0.0, 0.0)  # Ustawienie koloru na czerwony
    glVertex3f(-7.0, 0.0, 0.0)  # Początek osi X
    glVertex3f(7.0, 0.0, 0.0)  # Koniec osi X
    # Oś Y (zielona)
    glColor3f(0.0, 1.0, 0.0)  # Ustawienie koloru na zielony
    glVertex3f(0.0, -7.0, 0.0)  # Początek osi Y
    glVertex3f(0.0, 7.0, 0.0)  # Koniec osi Y
    # Oś Z (niebieska)
    glColor3f(0.0, 0.0, 1.0)  # Ustawienie koloru na niebieski
    glVertex3f(0.0, 0.0, -7.0)  # Początek osi Z
    glVertex3f(0.0, 0.0, 7.0)  # Koniec osi Z
    glEnd()


def generate_points(N):
    """Generuje siatkę punktów."""
    points = []
    for i in range(N + 1):  # Iteracja po wierszach siatki
        row_points = []
        for j in range(N + 1):  # Iteracja po kolumnach siatki
            u, v = i / N, j / N  # Normalizacja współrzędnych
            row_points.append([getx(u, v), gety(u, v), getz(u, v)])  # Dodawanie punktu do wiersza
        points.append(row_points)  # Dodawanie wiersza punktów do siatki
    return points


# Obliczanie współrzędnych punktów
def getx(u, v):
    """Oblicza współrzędną X dla danego u i v."""
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)


def gety(u, v):
    """Oblicza współrzędną Y dla danego u i v."""
    return (160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5)


def getz(u, v):
    """Oblicza współrzędną Z dla danego u i v."""
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)

def render_egg_with_texture(texture_id, N):
    """Renderuje jajko z nałożoną teksturą."""
    global model, camera_position, camera_angle_x, camera_angle_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(camera_position[0], camera_position[1], camera_position[2])
    glRotatef(camera_angle_x, 1.0, 0.0, 0.0)
    glRotatef(camera_angle_y, 0.0, 1.0, 0.0)

    draw_axes()

    glBindTexture(GL_TEXTURE_2D, texture_id)  # Przypisz teksturę

    glShadeModel(GL_SMOOTH)

    glBegin(GL_TRIANGLES)
    for i in range(N - 1):  # Iteruj po N-1, aby uniknąć przekroczenia zakresu
        for j in range(N - 1):  # Iteruj po N-1, aby uniknąć przekroczenia zakresu
            # Nałożenie tekstury na trójkąty
            glTexCoord2f(i / float(N), j / float(N))
            glVertex3fv(model[i][j])

            glTexCoord2f((i + 1) / float(N), j / float(N))
            glVertex3fv(model[i + 1][j])

            glTexCoord2f(i / float(N), (j + 1) / float(N))
            glVertex3fv(model[i][j + 1])

            glTexCoord2f((i + 1) / float(N), (j + 1) / float(N))
            glVertex3fv(model[i + 1][j + 1])

            glTexCoord2f(i / float(N), (j + 1) / float(N))
            glVertex3fv(model[i][j + 1])

            glTexCoord2f((i + 1) / float(N), j / float(N))
            glVertex3fv(model[i + 1][j])
    glEnd()

    glFlush()


def generate_egg(N):
    global model
    v_loops = 15  # Liczba wierzchołków w obwodzie jajka
    h_loops = 15  # Liczba obwodów
    s = 5  # Skala jajka

    for i in range(v_loops):
        lat0 = math.pi * (-0.5 + float(i) / v_loops)
        y0 = s * 0.7 * math.sin(lat0)
        zr0 = s * 0.5 * math.cos(lat0)

        lat1 = math.pi * (-0.5 + float(i + 1) / v_loops)
        y1 = s * 0.7 * math.sin(lat1)
        zr1 = s * 0.5 * math.cos(lat1)

        for j in range(h_loops):
            lng0 = 2 * math.pi * float(j) / h_loops
            lng1 = 2 * math.pi * float(j + 1) / h_loops

            x0, z0 = math.cos(lng0), math.sin(lng0)
            x1, z1 = math.cos(lng1), math.sin(lng1)

            v1 = (x0 * zr0, y0, z0 * zr0)
            v2 = (x1 * zr0, y0, z1 * zr0)
            v3 = (x1 * zr1, y1, z1 * zr1)
            v4 = (x0 * zr1, y1, z0 * zr1)

            color = (random.random(), random.random(), random.random())
            model.append({'vertices': [v1, v2, v3], 'color': color})
            color = (random.random(), random.random(), random.random())
            model.append({'vertices': [v1, v3, v4], 'color': color})


def render_teapot_with_texture(texture_id, vertices, faces):
    """Renderuje czajnik z nałożoną teksturą."""
    global camera_position, camera_angle_x, camera_angle_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(camera_position[0], camera_position[1], camera_position[2])
    glRotatef(camera_angle_x, 1.0, 0.0, 0.0)
    glRotatef(camera_angle_y, 0.0, 1.0, 0.0)

    draw_axes()

    glBindTexture(GL_TEXTURE_2D, texture_id)  # Przypisz teksturę

    glShadeModel(GL_SMOOTH)

    glBegin(GL_TRIANGLES)
    for face in faces:
        for idx in face:
            glTexCoord2f(vertices[idx][0], vertices[idx][1])  # Współrzędne tekstury (przykładowe)
            glVertex3fv(vertices[idx])
    glEnd()

    glFlush()






# Funkcja do zmiany liczby wierzchołków
def change_vertex_count():
    """Pozwala użytkownikowi zmienić liczbę wierzchołków siatki."""
    global N, points, colors
    try:
        new_N = int(input("Podaj nową liczbę wierzchołków: "))  # Wczytanie nowej wartości N
        if new_N > 0:  # Sprawdzenie, czy liczba jest większa od 0
            N = new_N
            points, colors = generate_points(N)  # Generowanie nowej siatki punktów i kolorów

        else:
            print("Liczba wierzchołków musi być większa od 0.")  # Informacja o nieprawidłowej wartości
    except ValueError:  # Obsługa błędów w przypadku nieprawidłowego wejścia
        print("Nieprawidłowa wartość. Wpisz liczbę całkowitą.")
