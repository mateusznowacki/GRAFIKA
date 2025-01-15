import sys  # Obsługa systemu i argumentów
from glfw.GLFW import *  # Biblioteka GLFW do obsługi okien i zdarzeń
from OpenGL.GL import *  # OpenGL do renderowania
from OpenGL.GLU import *  # Funkcje pomocnicze OpenGL
import math  # Obsługa obliczeń matematycznych
import random  # Generowanie losowych kolorów
import numpy as np

from GrafiXon.new.rederingjc import render_egg_with_texture, render_teapot_with_texture, generate_egg
from filecontroller import load_texture  # Zakładając, że masz funkcję load_texture w filecontroller.py

# Inicjalizacja zmiennych kamery
camera_position = [0.0, 0.0, -10.0]  # Początkowa pozycja kamery
camera_angle_x = 0.0  # Początkowy kąt obrotu wokół osi X
camera_angle_y = 0.0  # Początkowy kąt obrotu wokół osi Y

def startup():
    """Inicjalizuje środowisko OpenGL."""
    global camera_position, camera_angle_x, camera_angle_y
    camera_position = [0.0, 0.0, -10.0]  # Początkowa pozycja kamery
    camera_angle_x = 0.0  # Początkowy kąt obrotu wokół osi X
    camera_angle_y = 0.0  # Początkowy kąt obrotu wokół osi Y

    update_viewport(None, 400, 400)  # Ustawienie początkowego rozmiaru okna
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Ustawienie koloru tła na czarny
    glEnable(GL_DEPTH_TEST)  # Włączenie bufora głębokości do poprawnego renderowania 3D


# Funkcja obsługi zmiany rozmiaru okna
def update_viewport(window, width, height):
    if height == 0:
        height = 1
    aspect_ratio = width / height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, aspect_ratio, 1.0, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# Funkcje obsługi klawiszy
def key_callback(window, key, scancode, action, mods):
    pass  # Implementacja obsługi klawiszy


# Funkcje obsługi przycisków myszy
def mouse_button_callback(window, button, action, mods):
    pass  # Implementacja obsługi przycisków myszy


# Funkcja obsługi pozycji kursora
def cursor_position_callback(window, xpos, ypos):
    pass  # Implementacja obsługi kursora


# Funkcja główna programu
def main():
    # Inicjalizacja GLFW
    if not glfwInit():
        sys.exit(-1)

    # Tworzenie okna
    window = glfwCreateWindow(800, 600, "OpenGL Application", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    # Ustawienie kontekstu OpenGL
    glfwMakeContextCurrent(window)

    # Ustawienie callbacków
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, key_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetCursorPosCallback(window, cursor_position_callback)

    # Inicjalizacja ustawień OpenGL
    startup()

    # Wybór trybu (jajko z teksturą lub czajnik)
    mode = input("Wybierz tryb (1: jajko z teksturą, 2: czajnik z teksturą): ")
    texture_file = r"C:\Users\matty\PycharmProjects\GRAFIKA2\texture\las.tga"  # Ścieżka do tekstury (możesz zmienić)

    # Ładowanie tekstury
    texture_id = load_texture(texture_file)
    if texture_id is None:
        print("Błąd ładowania tekstury. Kończenie programu.")
        sys.exit(-1)

    if mode == "1":
        N = 50  # Domyślna liczba wierzchołków dla jajka
        points = generate_egg(N)  # Generowanie jajka
        # Główna pętla renderująca dla jajka
        while not glfwWindowShouldClose(window):
            render_egg_with_texture(texture_id, N)  # Renderowanie jajka z teksturą
            glfwSwapBuffers(window)
            glfwPollEvents()

    # elif mode == "2":
    #     filename = input("Podaj ścieżkę do pliku .obj (czajnik): ")
    #   #  vertices, faces = load_obj_and_generate_model(filename)  # Wczytywanie czajnika
    #     # Główna pętla renderująca dla czajnika
    #     while not glfwWindowShouldClose(window):
    #         render_teapot_with_texture(texture_id, vertices, faces)  # Renderowanie czajnika z teksturą
    #         glfwSwapBuffers(window)
    #         glfwPollEvents()

    else:
        print("Nieprawidłowy wybór.")
        glfwTerminate()
        sys.exit(-1)

    # Zakończenie działania GLFW
    glfwTerminate()


if __name__ == "__main__":
    main()
