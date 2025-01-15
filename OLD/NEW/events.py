from glfw.GLFW import *
import math

"""
Moduł odpowiedzialny za obsługę zdarzeń (klawiatura, mysz, scroll).
W nim przechowujemy także globalne zmienne potrzebne do obracania/zoomowania.
"""

# Zmienne globalne do przechowywania stanu obrotu i przybliżenia
rotation_x = 0.0
rotation_y = 0.0
zoom = 1.0

last_mouse_x = 0.0
last_mouse_y = 0.0


def keyboard_key_callback(window, key, scancode, action, mods):
    """
    Obsługa klawiatury z poprawną logiką ustawiania flagi zamknięcia okna.
    """
    if action in (GLFW_PRESS, GLFW_REPEAT):
        if key == GLFW_KEY_ESCAPE:
            print("Próba zamknięcia okna...")
            glfwSetWindowShouldClose(window, GLFW_TRUE)  # Użycie poprawnej wartości `GLFW_TRUE`
        elif key == GLFW_KEY_UP:
            print("Obrót modelu w osi X w górę.")
            rotate_model('x', -0.1)
        elif key == GLFW_KEY_DOWN:
            print("Obrót modelu w osi X w dół.")
            rotate_model('x', 0.1)
        elif key == GLFW_KEY_LEFT:
            print("Obrót modelu w osi Y w lewo.")
            rotate_model('y', -0.1)
        elif key == GLFW_KEY_RIGHT:
            print("Obrót modelu w osi Y w prawo.")
            rotate_model('y', 0.1)
        else:
            print(f"Niewspierany klawisz: key={key}, action={action}")


def mouse_button_callback(window, button, action, mods):
    """
    Obsługa kliknięcia przycisku myszy. Zapamiętuje aktualną pozycję kursora,
    jeśli lewy przycisk myszy został wciśnięty.
    """
    global last_mouse_x, last_mouse_y
    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        try:
            last_mouse_x, last_mouse_y = glfwGetCursorPos(window)
            print(f"Lewy przycisk myszy wciśnięty. Pozycja: x={last_mouse_x}, y={last_mouse_y}")
        except Exception as e:
            print(f"Błąd podczas pobierania pozycji kursora: {e}")


def cursor_position_callback(window, xpos, ypos):
    """
    Obsługa przesunięcia kursora. Oblicza różnicę pozycji kursora i aktualizuje
    kąty obrotu sceny.
    """
    global rotation_x, rotation_y, last_mouse_x, last_mouse_y
    if glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_PRESS:
        try:
            dx = xpos - last_mouse_x
            dy = ypos - last_mouse_y
            last_mouse_x, last_mouse_y = xpos, ypos

            rotation_x += dy * 0.1
            rotation_y += dx * 0.1

            print(f"Obrót sceny: rotation_x={rotation_x:.2f}, rotation_y={rotation_y:.2f}")
        except Exception as e:
            print(f"Błąd podczas aktualizacji pozycji kursora: {e}")


def scroll_callback(window, xoffset, yoffset):
    """
    Obsługa scrolla myszy. Zmienia wartość zoomu w zależności od kierunku scrolla.
    """
    global zoom
    try:
        new_zoom = zoom + yoffset * 0.1
        zoom = max(0.1, new_zoom)
        print(f"Zoom zaktualizowany: {zoom:.2f}")
    except Exception as e:
        print(f"Błąd podczas aktualizacji zoomu: {e}")
