#!/usr/bin/env python3
# Importowanie modułów
import sys  # Obsługa systemu i argumentów
from glfw.GLFW import *  # Biblioteka GLFW do obsługi okien i zdarzeń
from OpenGL.GL import *  # OpenGL do renderowania
from OpenGL.GLU import *  # Funkcje pomocnicze OpenGL
import math  # Obsługa obliczeń matematycznych
import random  # Generowanie losowych kolorów

# Konfiguracja globalna
color_mode = True  # True - tryb kolorowy, False - tryb czarno-biały
smooth_shading = False  # False - cieniowanie płaskie, True - cieniowanie gładkie
N = 50  # Domyślna liczba wierzchołków w siatce
camera_position = [0.0, 0.0, -20.0]  # Pozycja kamery w przestrzeni
camera_angle_x = 0.0  # Początkowy kąt obrotu kamery wokół osi X
camera_angle_y = 0.0  # Początkowy kąt obrotu kamery wokół osi Y
last_mouse_x = 0.0  # Ostatnia pozycja kursora myszy na osi X
last_mouse_y = 0.0  # Ostatnia pozycja kursora myszy na osi Y
is_dragging = False  # Czy mysz jest przeciągana (True, jeśli wciśnięto lewy przycisk myszy)




# # Wyświetlanie informacji o liczbie punktów
# def print_points_info():
#     """Wypisuje aktualną liczbę punktów w siatce."""
#     print(f"Aktualna liczba punktów: {N * N}")
#




# Funkcja główna programu
def main():
    """Główna funkcja programu, inicjalizująca i uruchamiająca pętlę renderowania."""
    global N, points, colors
    print_points_info()  # Wyświetlenie informacji o liczbie punktów na początku

    if not glfwInit():  # Inicjalizacja biblioteki GLFW
        sys.exit(-1)  # Wyjście z programu, jeśli inicjalizacja nie powiodła się
    window = glfwCreateWindow(400, 400, "Jajko - triangulacja z kamerą i myszą", None, None)  # Tworzenie okna
    if not window:  # Sprawdzenie, czy okno zostało poprawnie utworzone
        glfwTerminate()
        sys.exit(-1)
    glfwMakeContextCurrent(window)  # Ustawienie kontekstu OpenGL dla okna
    glfwSetFramebufferSizeCallback(window, update_viewport)  # Obsługa zmiany rozmiaru okna
    glfwSetKeyCallback(window, key_callback)  # Obsługa klawiatury
    glfwSetMouseButtonCallback(window, mouse_button_callback)  # Obsługa przycisków myszy
    glfwSetCursorPosCallback(window, cursor_position_callback)  # Śledzenie pozycji kursora
    glfwSwapInterval(1)  # Synchronizacja z odświeżaniem ekranu
    startup()  # Inicjalizacja ustawień OpenGL

    while not glfwWindowShouldClose(window):  # Pętla renderowania (działa, dopóki okno jest otwarte)
        render()  # Renderowanie sceny
        glfwSwapBuffers(window)  # Wymiana buforów (odświeżenie okna)
        glfwPollEvents()  # Obsługa zdarzeń (klawiatura, mysz itp.)
    glfwTerminate()  # Zwolnienie zasobów GLFW po zamknięciu programu

# Wywołanie funkcji głównej, jeśli uruchamiany jako skrypt
if __name__ == '__main__':
    main()

# Alternatywne wywołanie funkcji głównej
def run():
    """Funkcja alternatywna do uruchomienia programu."""
    main()

