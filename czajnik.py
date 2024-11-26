#!/usr/bin/env python3
import sys
import os
import random
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Konfiguracja
color_mode = True  # true - kolorowy, false - czarno-biały
smooth_shading = False  # false - flat shading (domyślnie), true - smooth shading
camera_angle_x = 0.0  # Kąt obrotu kamery wokół osi X
camera_angle_y = 0.0  # Kąt obrotu kamery wokół osi Y
last_mouse_x = 0.0  # Ostatnia pozycja myszy X
last_mouse_y = 0.0  # Ostatnia pozycja myszy Y
is_dragging = False  # Czy mysz jest przeciągana (przycisk wciśnięty)
draw_mode = GL_POINTS  # Tryb rysowania: punkty, linie, trójkąty


# Funkcja do załadowania pliku .obj
def load_obj(filename):
    vertices = []
    faces = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    parts = line.strip().split()
                    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif line.startswith('f '):  # Wczytanie ścian (trójkątów)
                    parts = line.strip().split()
                    face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                    faces.append(face)
    except FileNotFoundError:
        print(f"Plik {filename} nie został znaleziony.")
        sys.exit(-1)
    return np.array(vertices), faces


# Generowanie losowych kolorów dla wierzchołków
def generate_colors(vertices):
    return [np.random.rand(3).tolist() for _ in vertices]


# Funkcja inicjalizacyjna
def startup():
    update_viewport(None, 800, 600)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


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


# Renderowanie modelu
def render(vertices, faces, colors):
    global camera_angle_x, camera_angle_y, color_mode, draw_mode, smooth_shading
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Obrót kamery
    glTranslatef(0.0, 0.0, -10.0)  # Oddalenie kamery
    glRotatef(camera_angle_x, 1.0, 0.0, 0.0)
    glRotatef(camera_angle_y, 0.0, 1.0, 0.0)
    # Rysowanie osi
    draw_axes()

    # Wybór trybu cieniowania
    if smooth_shading:
        glShadeModel(GL_SMOOTH)
    else:
        glShadeModel(GL_FLAT)

    if draw_mode == GL_POINTS:
        glPointSize(1)
        glBegin(GL_POINTS)
        for i, vertex in enumerate(vertices):
            if color_mode:
                glColor3fv(colors[i])  # Kolory losowe
            else:
                glColor3f(1.0, 1.0, 1.0)  # Kolor biały
            glVertex3fv(vertex)
        glEnd()

    elif draw_mode == GL_LINES:
        glBegin(GL_LINES)
        for face in faces:
            for i in range(len(face)):
                v1 = vertices[face[i]]
                v2 = vertices[face[(i + 1) % len(face)]]
                if color_mode:
                    glColor3fv(colors[face[i]])
                else:
                    glColor3f(1.0, 1.0, 1.0)
                glVertex3fv(v1)
                glVertex3fv(v2)
        glEnd()

    elif draw_mode == GL_TRIANGLES:
        glBegin(GL_TRIANGLES)
        for face in faces:
            if len(face) == 3:  # Upewnienie się, że ściana jest trójkątem
                for i in range(3):
                    if color_mode:
                        glColor3fv(colors[face[i]])
                    else:
                        glColor3f(1.0, 1.0, 1.0)
                    glVertex3fv(vertices[face[i]])
        glEnd()

    glFlush()


# Obsługa klawiatury
def key_callback(window, key, scancode, action, mods):
    global camera_angle_x, camera_angle_y, color_mode, draw_mode, smooth_shading
    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_C:  # Przełączanie trybu koloru
            color_mode = not color_mode
        elif key == GLFW_KEY_T:  # Zmiana trybu rysowania
            if draw_mode == GL_POINTS:
                draw_mode = GL_LINES
                print("Tryb rysowania: Linie")
            elif draw_mode == GL_LINES:
                draw_mode = GL_TRIANGLES
                print("Tryb rysowania: Trójkąty")
            elif draw_mode == GL_TRIANGLES:
                draw_mode = GL_POINTS
                print("Tryb rysowania: Punkty")
        elif key == GLFW_KEY_S:  # Przełączanie trybu cieniowania
            smooth_shading = not smooth_shading

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
    global camera_angle_x, camera_angle_y, draw_mode, smooth_shading
    camera_angle_x = 0.0
    camera_angle_y = 0.0
    print("Sterowanie:")
    print("  - T: Zmiana trybu rysowania (Punkty, Linie, Trójkąty)")
    print("  - S: Przełączanie trybu cieniowania (Flat/Smooth)")

    if not glfwInit():
        print("Nie udało się zainicjalizować GLFW.")
        sys.exit(-1)

    window = glfwCreateWindow(800, 600, "Obj Viewer - Dynamic Rendering", None, None)
    if not window:
        print("Nie udało się utworzyć okna.")
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, key_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetCursorPosCallback(window, cursor_position_callback)
    glfwSwapInterval(1)

    startup()

    # Pobranie ścieżki do pliku .obj
    script_dir = os.path.dirname(os.path.abspath(__file__))
    obj_file_path = os.path.join(script_dir, "teapot.obj")

    if not os.path.exists(obj_file_path):
        print(f"Plik {obj_file_path} nie został znaleziony.")
        sys.exit(-1)

    vertices, faces = load_obj(obj_file_path)
    colors = generate_colors(vertices)

    while not glfwWindowShouldClose(window):
        render(vertices, faces, colors)
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == '__main__':
    main()
