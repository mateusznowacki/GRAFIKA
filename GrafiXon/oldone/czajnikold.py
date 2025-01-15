#!/usr/bin/env python3
# Importowanie niezbędnych modułów
import sys  # Obsługa argumentów i komunikacji z systemem operacyjnym
import os  # Obsługa operacji na plikach i ścieżkach
import random  # Generowanie losowych wartości
from glfw.GLFW import *  # Biblioteka do obsługi okien i wejścia
from OpenGL.GL import *  # Funkcje OpenGL do renderowania
from OpenGL.GLU import *  # Funkcje pomocnicze OpenGL (np. perspektywa)
import numpy as np  # Obsługa obliczeń na tablicach wielowymiarowych

# Konfiguracja początkowa
color_mode = True  # true - tryb kolorowy, false - tryb czarno-biały
smooth_shading = False  # false - cieniowanie płaskie, true - cieniowanie gładkie
camera_angle_x = 0.0  # Kąt obrotu kamery wokół osi X w stopniach (początkowy brak obrotu)
camera_angle_y = 0.0  # Kąt obrotu kamery wokół osi Y w stopniach (początkowy brak obrotu)
last_mouse_x = 0.0  # Ostatnia pozycja kursora myszy na osi X (używana do obracania sceny)
last_mouse_y = 0.0  # Ostatnia pozycja kursora myszy na osi Y
is_dragging = False  # Czy mysz jest przeciągana (True - przycisk myszy wciśnięty)
draw_mode = GL_POINTS  # Tryb rysowania: GL_POINTS (punkty), GL_LINES (linie), GL_TRIANGLES (trójkąty)


# Generowanie losowych kolorów dla wierzchołków
def generate_colors(vertices):
    """Generuje losowe kolory RGB (czerwony, zielony, niebieski) dla każdego wierzchołka."""
    return [np.random.rand(3).tolist() for _ in vertices]  # Każdy wierzchołek dostaje losowy kolor (0-1 dla RGB)

# Funkcja inicjalizacyjna
def startup():
    """Ustawienia początkowe OpenGL."""
    update_viewport(None, 800, 600)  # Aktualizacja widoku z domyślnym rozmiarem okna 800x600
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Ustawienie koloru tła na czarny (RGB: 0, 0, 0; alfa: 1 - pełna przezroczystość)
    glEnable(GL_DEPTH_TEST)  # Włączenie bufora głębi, co pozwala na poprawne renderowanie 3D



# Obsługa widoku i okna
def update_viewport(window, width, height):
    """Aktualizuje parametry widoku po zmianie rozmiaru okna."""
    if width == 0: width = 1  # Zapobieganie dzieleniu przez 0
    if height == 0: height = 1
    aspect_ratio = width / height  # Obliczanie proporcji widoku
    glMatrixMode(GL_PROJECTION)  # Przełączenie na macierz projekcji
    glViewport(0, 0, width, height)  # Ustawienie widocznego obszaru okna
    glLoadIdentity()  # Resetowanie macierzy projekcji
    gluPerspective(45, aspect_ratio, 1.0, 50.0)  # Ustawienie perspektywy:
    # 45 - kąt widzenia w pionie (w stopniach)
    # aspect_ratio - proporcja szerokości do wysokości
    # 1.0 - minimalna odległość renderowania
    # 50.0 - maksymalna odległość renderowania
    glMatrixMode(GL_MODELVIEW)  # Przełączenie z powrotem na macierz widoku
    glLoadIdentity()  # Resetowanie macierzy widoku

# Główna funkcja renderowania
def render(vertices, faces, colors):
    """Renderuje obiekt przy użyciu OpenGL."""
    global camera_angle_x, camera_angle_y, color_mode, draw_mode, smooth_shading
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Czyszczenie ekranu i bufora głębi
    glLoadIdentity()  # Resetowanie macierzy widoku

    # Transformacja kamery
    glTranslatef(0.0, 0.0, -10.0)  # Oddalenie kamery (przesunięcie wzdłuż osi Z o -10 jednostek)
    glRotatef(camera_angle_x, 1.0, 0.0, 0.0)  # Obrót wokół osi X (camera_angle_x stopni)
    glRotatef(camera_angle_y, 0.0, 1.0, 0.0)  # Obrót wokół osi Y (camera_angle_y stopni)

    draw_axes()  # Rysowanie osi XYZ

    # Ustawienie trybu cieniowania
    glShadeModel(GL_SMOOTH if smooth_shading else GL_FLAT)  # GL_SMOOTH - cieniowanie gładkie, GL_FLAT - cieniowanie płaskie

    # Renderowanie w zależności od trybu rysowania
    if draw_mode == GL_POINTS:
        glPointSize(1)  # Ustawienie rozmiaru punktów na 1 piksel
        glBegin(GL_POINTS)  # Rozpoczęcie rysowania punktów
        for i, vertex in enumerate(vertices):
            glColor3fv(colors[i] if color_mode else [1.0, 1.0, 1.0])  # Ustawienie koloru wierzchołka
            glVertex3fv(vertex)  # Rysowanie punktu w pozycji wierzchołka
        glEnd()

    elif draw_mode == GL_LINES:
        glBegin(GL_LINES)  # Rozpoczęcie rysowania linii
        for face in faces:
            for i in range(len(face)):
                v1 = vertices[face[i]]  # Pierwszy wierzchołek linii
                v2 = vertices[face[(i + 1) % len(face)]]  # Następny wierzchołek (z domknięciem)
                glColor3fv(colors[face[i]] if color_mode else [1.0, 1.0, 1.0])  # Ustawienie koloru
                glVertex3fv(v1)  # Punkt początkowy linii
                glVertex3fv(v2)  # Punkt końcowy linii
        glEnd()

    elif draw_mode == GL_TRIANGLES:
        glBegin(GL_TRIANGLES)  # Rozpoczęcie rysowania trójkątów
        for face in faces:
            if len(face) == 3:  # Upewnienie się, że ściana jest trójkątem
                for i in range(3):  # Iteracja przez wierzchołki trójkąta
                    glColor3fv(colors[face[i]] if color_mode else [1.0, 1.0, 1.0])  # Ustawienie koloru
                    glVertex3fv(vertices[face[i]])  # Dodanie wierzchołka
        glEnd()

    glFlush()  # Wymuszenie zakończenia renderowania

# Obsługa klawiatury
def key_callback(window, key, scancode, action, mods):
    """Reagowanie na klawisze."""
    global camera_angle_x, camera_angle_y, color_mode, draw_mode, smooth_shading
    if action == GLFW_PRESS or action == GLFW_REPEAT:  # Klawisz wciśnięty lub trzymany
        if key == GLFW_KEY_C:  # Zmiana trybu kolorowania
            color_mode = not color_mode
        elif key == GLFW_KEY_T:  # Zmiana trybu rysowania (punkty, linie, trójkąty)
            if draw_mode == GL_POINTS:
                draw_mode = GL_LINES
                print("Tryb rysowania: Linie")
            elif draw_mode == GL_LINES:
                draw_mode = GL_TRIANGLES
                print("Tryb rysowania: Trójkąty")
            elif draw_mode == GL_TRIANGLES:
                draw_mode = GL_POINTS
                print("Tryb rysowania: Punkty")
        elif key == GLFW_KEY_S:  # Przełączanie cieniowania
            smooth_shading = not smooth_shading
        elif key == GLFW_KEY_UP:  # Obrót kamery w górę
            camera_angle_x -= 5.0  # Zmniejszenie kąta X o 5 stopni
        elif key == GLFW_KEY_DOWN:  # Obrót kamery w dół
            camera_angle_x += 5.0  # Zwiększenie kąta X o 5 stopni
        elif key == GLFW_KEY_LEFT:  # Obrót kamery w lewo
            camera_angle_y -= 5.0  # Zmniejszenie kąta Y o 5 stopni
        elif key == GLFW_KEY_RIGHT:  # Obrót kamery w prawo
            camera_angle_y += 5.0  # Zwiększenie kąta Y o 5 stopni

# Obsługa myszy
def mouse_button_callback(window, button, action, mods):
    """Reagowanie na przyciski myszy."""
    global is_dragging
    if button == GLFW_MOUSE_BUTTON_LEFT:
        is_dragging = (action == GLFW_PRESS)  # Przeciąganie aktywne, jeśli lewy przycisk wciśnięty

def cursor_position_callback(window, xpos, ypos):
    """Obsługa ruchu kursora myszy."""
    global last_mouse_x, last_mouse_y, camera_angle_x, camera_angle_y, is_dragging
    if is_dragging:  # Jeśli przeciągamy, zmieniamy kąty kamery
        dx = xpos - last_mouse_x  # Różnica pozycji kursora w osi X
        dy = ypos - last_mouse_y  # Różnica pozycji kursora w osi Y
        camera_angle_x += dy * 0.1  # Aktualizacja kąta X (z modyfikatorem 0.1 dla płynności)
        camera_angle_y += dx * 0.1  # Aktualizacja kąta Y
    last_mouse_x = xpos  # Aktualizacja pozycji X kursora
    last_mouse_y = ypos  # Aktualizacja pozycji Y kursora

# Funkcja główna
def main():
    """Główna funkcja programu."""
    global camera_angle_x, camera_angle_y, draw_mode, smooth_shading
    camera_angle_x = 0.0  # Resetowanie kąta X
    camera_angle_y = 0.0  # Resetowanie kąta Y

    if not glfwInit():  # Inicjalizacja GLFW
        print("Nie udało się zainicjalizować GLFW.")
        sys.exit(-1)

    # Tworzenie okna o wymiarach 800x600 z tytułem
    window = glfwCreateWindow(800, 600, "Obj Viewer - Dynamic Rendering", None, None)
    if not window:  # Jeśli okno nie zostało utworzone
        print("Nie udało się utworzyć okna.")
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)  # Ustawienie kontekstu OpenGL dla okna
    glfwSetFramebufferSizeCallback(window, update_viewport)  # Reakcja na zmianę rozmiaru okna
    glfwSetKeyCallback(window, key_callback)  # Obsługa klawiatury
    glfwSetMouseButtonCallback(window, mouse_button_callback)  # Obsługa przycisków myszy
    glfwSetCursorPosCallback(window, cursor_position_callback)  # Obsługa ruchu kursora
    glfwSwapInterval(1)  # Synchronizacja z odświeżaniem ekranu

    startup()  # Ustawienia początkowe OpenGL

    # Ładowanie modelu .obj (teapot.obj)
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  # Ścieżka do bieżącego katalogu
    obj_file_path = os.path.join(script_dir, "teapot.obj")  # Ścieżka do pliku teapot.obj
    if not os.path.exists(obj_file_path):  # Sprawdzenie, czy plik istnieje
        print(f"Plik {obj_file_path} nie został znaleziony.")
        sys.exit(-1)

    vertices, faces = load_obj(obj_file_path)  # Wczytanie wierzchołków i ścian
    colors = generate_colors(vertices)  # Generowanie losowych kolorów dla wierzchołków

    # Główna pętla programu
    while not glfwWindowShouldClose(window):  # Pętla trwa, dopóki okno nie zostanie zamknięte
        render(vertices, faces, colors)  # Renderowanie obiektu
        glfwSwapBuffers(window)  # Wymiana buforów
        glfwPollEvents()  # Obsługa zdarzeń (klawiatura, mysz, itp.)

    glfwTerminate()  # Zwolnienie zasobów GLFW po zakończeniu

# Uruchomienie programu
if __name__ == '__main__':
    main()
