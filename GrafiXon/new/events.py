
# Importowanie modułów
import sys  # Obsługa systemu i argumentów
from glfw.GLFW import *  # Biblioteka GLFW do obsługi okien i zdarzeń
from OpenGL.GL import *  # OpenGL do renderowania
from OpenGL.GLU import *  # Funkcje pomocnicze OpenGL
import math  # Obsługa obliczeń matematycznych
import random  # Generowanie losowych kolorów

from GrafiXon.new.rederingjc import change_vertex_count


# Obsługa zdarzeń myszy
def mouse_button_callback(window, button, action, mods):
    """Obsługuje kliknięcia myszy."""
    global is_dragging
    if button == GLFW_MOUSE_BUTTON_LEFT:  # Sprawdzenie, czy kliknięto lewy przycisk myszy
        is_dragging = (action == GLFW_PRESS)  # Włączanie trybu przeciągania, gdy przycisk wciśnięty

def cursor_position_callback(window, xpos, ypos):
    """Śledzi pozycję kursora myszy w celu obracania kamerą."""
    global last_mouse_x, last_mouse_y, camera_angle_x, camera_angle_y, is_dragging
    if is_dragging:  # Obrót kamery, gdy mysz jest przeciągana
        dx = xpos - last_mouse_x  # Obliczanie zmiany pozycji kursora w osi X
        dy = ypos - last_mouse_y  # Obliczanie zmiany pozycji kursora w osi Y
        camera_angle_x += dy * 0.1  # Aktualizacja kąta obrotu kamery wokół osi X
        camera_angle_y += dx * 0.1  # Aktualizacja kąta obrotu kamery wokół osi Y
    last_mouse_x = xpos  # Zapisywanie bieżącej pozycji kursora X
    last_mouse_y = ypos  # Zapisywanie bieżącej pozycji kursora Y

# Obsługa klawiatury
def key_callback(window, key, scancode, action, mods):
    """Obsługuje klawisze wciśnięte przez użytkownika."""
    global color_mode, smooth_shading, camera_angle_x, camera_angle_y
    if action == GLFW_PRESS or action == GLFW_REPEAT:  # Reakcja na klawisz wciśnięty lub trzymany
        if key == GLFW_KEY_C:  # Przełączanie trybu kolorowego
            color_mode = not color_mode
        elif key == GLFW_KEY_S:  # Przełączanie trybu cieniowania
            smooth_shading = not smooth_shading
        elif key == GLFW_KEY_V:  # Zmiana liczby wierzchołków
            change_vertex_count()
        elif key == GLFW_KEY_UP:  # Obrót kamery w górę
            camera_angle_x -= 5.0  # Zmniejszenie kąta obrotu wokół osi X
        elif key == GLFW_KEY_DOWN:  # Obrót kamery w dół
            camera_angle_x += 5.0  # Zwiększenie kąta obrotu wokół osi X
        elif key == GLFW_KEY_LEFT:  # Obrót kamery w lewo
            camera_angle_y -= 5.0  # Zmniejszenie kąta obrotu wokół osi Y
        elif key == GLFW_KEY_RIGHT:  # Obrót kamery w prawo
            camera_angle_y += 5.0  # Zwiększenie kąta obrotu wokół osi Y
