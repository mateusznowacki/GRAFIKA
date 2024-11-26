#!/usr/bin/env python3
import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# Konfiguracja
color_mode = True  # true - kolorowy, false - czarno-biały
N = 50  # Domyślna liczba wierzchołków
camera_angle_x = 0.0  # Kąt obrotu kamery wokół osi X
camera_angle_y = 0.0  # Kąt obrotu kamery wokół osi Y
last_mouse_x = 0.0  # Ostatnia pozycja myszy X
last_mouse_y = 0.0  # Ostatnia pozycja myszy Y
is_dragging = False  # Czy mysz jest przeciągana (przycisk wciśnięty)

# Funkcja inicjalizacyjna
def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

# Obsługa widoku
def update_viewport(window, width, height):
    if width == 0: width = 1
    if height == 0: height = 1
    aspect_ratio = width / height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    gluPerspective(45, aspect_ratio, 1.0, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Obliczenia
def getx(u, v): return (-90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u) * math.cos(math.pi * v)
def gety(u, v): return (160*u**4 - 320*u**3 + 160*u**2 - 5)
def getz(u, v): return (-90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u) * math.sin(math.pi * v)

# Generowanie punktów i kolorów
def generate_points(N):
    points, colors = [], []
    for i in range(N + 1):
        row_points, row_colors = [], []
        for j in range(N + 1):
            u, v = i / N, j / N
            row_points.append([getx(u, v), gety(u, v), getz(u, v)])
            row_colors.append([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])
        points.append(row_points)
        colors.append(row_colors)
    return points, colors

points, colors = generate_points(N)

# Wyświetlanie informacji o liczbie punktów
def print_points_info():
    print(f"Aktualna liczba punktów: {N * N}")

# Rysowanie osi
def draw_axes():
    glBegin(GL_LINES)
    # Oś X
    glColor3f(1.0, 0.0, 0.0)  # Czerwona oś X
    glVertex3f(-7.0, 0.0, 0.0)
    glVertex3f(7.0, 0.0, 0.0)
    # Oś Y
    glColor3f(0.0, 1.0, 0.0)  # Zielona oś Y
    glVertex3f(0.0, -7.0, 0.0)
    glVertex3f(0.0, 7.0, 0.0)
    # Oś Z
    glColor3f(0.0, 0.0, 1.0)  # Niebieska oś Z
    glVertex3f(0.0, 0.0, -7.0)
    glVertex3f(0.0, 0.0, 7.0)
    glEnd()

# Rysowanie modelu
def render():
    global points, colors, color_mode, camera_angle_x, camera_angle_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Ustawienie kamery
    glTranslatef(0.0, 0.0, -20.0)  # Oddalenie kamery
    glRotatef(camera_angle_x, 1.0, 0.0, 0.0)  # Obrót kamery wokół osi X
    glRotatef(camera_angle_y, 0.0, 1.0, 0.0)  # Obrót kamery wokół osi Y

    draw_axes()  # Rysowanie osi

    glBegin(GL_LINES)
    for i in range(N):
        for j in range(N):
            # Rysowanie linii wzdłuż osi u (poziomych)
            if color_mode:
                glColor3fv(colors[i][j])  # Kolorowy tryb
            else:
                glColor3f(1.0, 1.0, 1.0)  # Czarno-biały tryb
            glVertex3fv(points[i][j])       # Punkt początkowy
            glVertex3fv(points[i + 1][j])   # Punkt końcowy

            # Rysowanie linii wzdłuż osi v (pionowych)
            glVertex3fv(points[i][j])       # Punkt początkowy
            glVertex3fv(points[i][j + 1])   # Punkt końcowy
    glEnd()
    glFlush()

# Funkcja do zmiany liczby wierzchołków
def change_vertex_count():
    global N, points, colors
    try:
        new_N = int(input("Podaj nową liczbę wierzchołków: "))
        if new_N > 0:
            N = new_N
            points, colors = generate_points(N)  # Regeneracja punktów
            print_points_info()
        else:
            print("Liczba wierzchołków musi być większa od 0.")
    except ValueError:
        print("Nieprawidłowa wartość. Wpisz liczbę całkowitą.")

# Obsługa klawiatury
def key_callback(window, key, scancode, action, mods):
    global color_mode, N, points, colors, camera_angle_x, camera_angle_y
    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_C:  # Przełączanie trybu koloru
            color_mode = not color_mode
        elif key == GLFW_KEY_V:  # Zmiana liczby wierzchołków
            change_vertex_count()
        elif key == GLFW_KEY_UP:  # Obrót kamery w górę
            camera_angle_x -= 5.0
        elif key == GLFW_KEY_DOWN:  # Obrót kamery w dół
            camera_angle_x += 5.0
        elif key == GLFW_KEY_LEFT:  # Obrót kamery w lewo
            camera_angle_y -= 5.0
        elif key == GLFW_KEY_RIGHT:  # Obrót kamery w prawo
            camera_angle_y += 5.0

# Obsługa myszy
def mouse_button_callback(window, button, action, mods):
    global is_dragging
    if button == GLFW_MOUSE_BUTTON_LEFT:
        is_dragging = (action == GLFW_PRESS)

def cursor_position_callback(window, xpos, ypos):
    global last_mouse_x, last_mouse_y, camera_angle_x, camera_angle_y, is_dragging
    if is_dragging:
        dx = xpos - last_mouse_x
        dy = ypos - last_mouse_y
        camera_angle_x += dy * 0.1
        camera_angle_y += dx * 0.1
    last_mouse_x = xpos
    last_mouse_y = ypos

# Funkcja główna
def main():
    print_points_info()  # Wyświetlenie początkowej liczby punktów
    if not glfwInit(): sys.exit(-1)
    window = glfwCreateWindow(400, 400, "Jajko - linie", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, key_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetCursorPosCallback(window, cursor_position_callback)
    glfwSwapInterval(1)
    startup()
    while not glfwWindowShouldClose(window):
        render()
        glfwSwapBuffers(window)
        glfwPollEvents()
    glfwTerminate()

if __name__ == '__main__':
    main()

def run():
    main()  # Wywołanie istniejącej funkcji głównej
