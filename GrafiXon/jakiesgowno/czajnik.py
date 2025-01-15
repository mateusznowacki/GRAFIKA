#!/usr/bin/env python3
import sys
import os
from glfw.GLFW import *  # Importowanie funkcji z biblioteki GLFW do zarządzania oknami, zdarzeniami wejścia/wyjścia i obsługi kontekstu OpenGL
from OpenGL.GL import *  # Importowanie funkcji OpenGL do renderowania grafiki 3D, takich jak rysowanie prymitywów 3D, operacje na macierzach i zarządzanie stanem
import numpy as np  # Importowanie biblioteki numpy do obsługi operacji matematycznych i pracy z tablicami

# Funkcja do załadowania pliku .obj - wczytuje współrzędne wierzchołków i ściany
def load_obj(filename):
    vertices = []  # Lista do przechowywania współrzędnych wierzchołków
    faces = []  # Lista do przechowywania ścian (obecnie nieużywana)
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):  # Linie definiujące wierzchołki (oznaczone jako 'v')
                    parts = line.strip().split()
                    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])  # Dodanie współrzędnych wierzchołka do listy
                elif line.startswith('f '):  # Linie definiujące ściany (oznaczone jako 'f')
                    parts = line.strip().split()
                    face = [int(part.split('/')[0]) - 1 for part in parts[1:]]  # Przesunięcie indeksów (indeksowanie od 0 w Pythonie)
                    faces.append(face)
    except FileNotFoundError:
        print(f"Plik {filename} nie został znaleziony.")
        sys.exit(-1)
    return np.array(vertices), faces  # Zwrócenie wierzchołków jako tablica numpy oraz lista ścian (jeśli jest używana)

# Funkcja inicjalizująca ustawienia OpenGL
def startup():
    update_viewport(None, 800, 600)  # Inicjalizacja widoku dla okna o wymiarach 800x600 pikseli
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Ustawienie koloru tła na czarny (wartości RGBA)
    glEnable(GL_DEPTH_TEST)  # Włączenie testu głębokości dla poprawnego renderowania obiektów 3D (zakrywanie obiektów)

# Funkcja do obsługi zamykania programu (obecnie nieużywana, ale może służyć do sprzątania zasobów)
def shutdown():
    pass

# Funkcja aktualizująca widok przy zmianie rozmiaru okna
def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height  # Obliczenie współczynnika proporcji okna

    glMatrixMode(GL_PROJECTION)  # Przełączenie do macierzy projekcji (perspektywa/ortogonalność)
    glViewport(0, 0, width, height)  # Ustawienie widoku w oknie
    glLoadIdentity()  # Resetowanie macierzy projekcji

    # Ustawienie projekcji ortogonalnej w zależności od proporcji okna
    if width <= height:
        glOrtho(-5.0, 5.0, -5.0 / aspect_ratio, 5.0 / aspect_ratio, 5.0, -5.0)
    else:
        glOrtho(-5.0 * aspect_ratio, 5.0 * aspect_ratio, -5.0, 5.0, 5.0, -5.0)

    glMatrixMode(GL_MODELVIEW)  # Powrót do macierzy modelu/widoku
    glLoadIdentity()

# Funkcja do renderowania modelu jako zbioru punktów
def render(vertices):
    global angle_x, angle_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Czyszczenie buforów koloru i głębokości
    glLoadIdentity()  # Resetowanie macierzy transformacji do stanu początkowego

    # Przesunięcie i obrót modelu
    glTranslatef(0.0, 0.0, 0.0)  # Przesunięcie modelu do środka układu współrzędnych (jeśli wymagane)
    glRotatef(angle_x, 1.0, 0.0, 0.0)  # Obrót modelu wokół osi X o kąt angle_x
    glRotatef(angle_y, 0.0, 1.0, 0.0)  # Obrót modelu wokół osi Y o kąt angle_y

    # Rysowanie wierzchołków jako punkty
    glColor3f(0.0, 1.0, 0.0)  # Ustawienie koloru rysowanych punktów (zielony)
    glPointSize(1)  # Ustawienie rozmiaru punktów
    glBegin(GL_POINTS)
    for vertex in vertices:  # Iteracja po wierzchołkach
        glVertex3fv(vertex)  # Rysowanie wierzchołka jako punktu w przestrzeni 3D
    glEnd()

    glFlush()  # Wymuszenie wyświetlenia narysowanych elementów

# Funkcja obsługująca zdarzenia klawiatury do obracania obiektu
def key_callback(window, key, scancode, action, mods):
    global angle_x, angle_y
    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_LEFT:
            angle_y -= 5.0  # Obrót modelu w lewo wokół osi Y
        elif key == GLFW_KEY_RIGHT:
            angle_y += 5.0  # Obrót modelu w prawo wokół osi Y
        elif key == GLFW_KEY_UP:
            angle_x -= 5.0  # Obrót modelu w górę wokół osi X
        elif key == GLFW_KEY_DOWN:
            angle_x += 5.0  # Obrót modelu w dół wokół osi X

# Funkcja główna programu
def main():
    global angle_x, angle_y
    angle_x = 0.0  # Początkowy kąt obrotu wokół osi X
    angle_y = 0.0  # Początkowy kąt obrotu wokół osi Y

    if not glfwInit():  # Inicjalizacja biblioteki GLFW
        print("Nie udało się zainicjalizować GLFW.")
        sys.exit(-1)

    window = glfwCreateWindow(800, 600, "Obj Viewer - Points", None, None)  # Tworzenie okna o rozmiarze 800x600 pikseli
    if not window:
        print("Nie udało się utworzyć okna.")
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)  # Ustawienie kontekstu dla bieżącego okna
    glfwSetFramebufferSizeCallback(window, update_viewport)  # Ustawienie funkcji wywoływanej przy zmianie rozmiaru okna
    glfwSetKeyCallback(window, key_callback)  # Ustawienie funkcji obsługującej zdarzenia klawiatury
    glfwSwapInterval(1)  # Włączenie synchronizacji pionowej (v-sync)

    startup()  # Inicjalizacja ustawień OpenGL

    # Pobranie ścieżki do pliku .obj
    script_dir = os.path.dirname(os.path.abspath(__file__))
    obj_file_path = os.path.join(script_dir, "teapot.obj")

    if not os.path.exists(obj_file_path):
        print(f"Plik {obj_file_path} nie został znaleziony.")
        sys.exit(-1)

    vertices, _ = load_obj(obj_file_path)  # Załadowanie pliku .obj
    while not glfwWindowShouldClose(window):  # Pętla renderująca do momentu zamknięcia okna
        render(vertices)  # Renderowanie modelu
        glfwSwapBuffers(window)  # Wymiana buforów
        glfwPollEvents()  # Obsługa zdarzeń wejściowych

    shutdown()  # Zakończenie działania programu
    glfwTerminate()  # Zakończenie działania biblioteki GLFW

if __name__ == '__main__':
    main()
