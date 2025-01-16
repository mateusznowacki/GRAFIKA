import sys
import os
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from jajko import generate_egg_points, render_egg, draw_xyz_axes
from events import MouseEventHandler
from czajnik import * # Import funkcji dla czajnika

# ----- Zmienne globalne -----
viewer = [0.0, 0.0, 10.0]
egg_points = None
teapot_points = None
teapot_faces = None
current_object = "egg"  # Domyślnie wyświetlamy jajko
light_theta = 0.0  # Początkowy kąt w płaszczyźnie XY (ruch w lewo/prawo)
light_phi = math.pi / 4  # Początkowy kąt od osi Z (ruch w górę/dół)
light_radius = 10.0  # Stała odległość światła od jajka
light_color = [0.0, 0.0, 1.0, 1.0]  # Niebieski kolor światła


mouse_handler = MouseEventHandler()

# ----- Funkcje inicjalizacyjne -----
def startup():
    """
    Inicjalizacja OpenGL, generowanie jajka i ustawienia światła.
    """
    global egg_points

    # Ustawienia viewportu
    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Czarny kolor tła
    glEnable(GL_DEPTH_TEST)           # Włączenie testu głębokości

    # Włączenie cullingu (ignorowanie niewidocznych powierzchni)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)  # Ignorowanie tylnej strony trójkątów
    glFrontFace(GL_CCW)  # Front to wierzchołki w kolejności przeciwnie do ruchu wskazówek zegara (CCW)

    # Włączenie oświetlenia
    glEnable(GL_LIGHTING)  # Włączenie systemu oświetlenia
    glEnable(GL_LIGHT0)    # Aktywacja źródła światła nr 0
    glEnable(GL_COLOR_MATERIAL)  # Materiał obiektu dostosowuje się do kolorów

    # Generowanie punktów jajka
    egg_points = generate_egg_points(50)

    # Ustawienie początkowej pozycji światła
    update_light_position()


def shutdown():
    """Czyszczenie zasobów OpenGL."""
    pass


def update_light_position():
    """
    Aktualizuje pozycję światła na podstawie kątów sferycznych.
    """
    # Obliczanie pozycji światła w układzie sferycznym
    x = light_radius * math.sin(light_phi) * math.cos(light_theta)
    y = light_radius * math.cos(light_phi)
    z = light_radius * math.sin(light_phi) * math.sin(light_theta)

    # Ustawienie pozycji światła w OpenGL
    light_position = [x, y, z, 1.0]  # Pozycja światła
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)  # Ustawienie pozycji światła
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)      # Rozproszone światło
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)     # Odbite światło



# ----- Funkcja renderująca -----
def render(time):
    """
    Renderowanie sceny.
    """
    global current_object

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Aktualizacja pozycji światła
    update_light_position()

    # Zastosowanie transformacji myszki
    mouse_handler.apply_transformations()

    # Rysowanie osi XYZ
    draw_xyz_axes()

    # Rysowanie wybranego obiektu
    if current_object == "egg":
        render_egg(egg_points)  # Renderowanie jajka
    elif current_object == "teapot":
        if teapot_points and teapot_faces:
            render_teapot(teapot_points, teapot_faces)  # Renderowanie czajnika
        else:
            print("Czajnik nie został wczytany!")

    glFlush()


# ----- Funkcje callbacków -----
def update_viewport(window, width, height):
    """Aktualizacja widoku po zmianie rozmiaru okna."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, width / height, 0.1, 300.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard_key_callback(window, key, scancode, action, mods):
    """
    Obsługa klawiatury - sterowanie światłem orbitalnym wokół jajka.
    """
    global light_theta, light_phi

    angle_step = 0.5 # Szybszy ruch światła

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_W:  # Ruch w górę (zmniejszenie phi)
            light_phi = max(0.1, light_phi - angle_step)
        elif key == GLFW_KEY_S:  # Ruch w dół (zwiększenie phi)
            light_phi = min(math.pi - 0.1, light_phi + angle_step)
        elif key == GLFW_KEY_A:  # Obrót w lewo (zmniejszenie theta)
            light_theta -= angle_step
        elif key == GLFW_KEY_D:  # Obrót w prawo (zwiększenie theta)
            light_theta += angle_step

        # Aktualizacja pozycji światła
        update_light_position()

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

# ----- Funkcja główna -----
def main():
    """Główna funkcja programu."""
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, "Jajko vs Czajnik", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)

    # Rejestracja callbacków myszki
    mouse_handler.register_callbacks(window)

    glfwSwapInterval(1)
    startup()

    print("MENU GŁÓWNE:")
    print("1 - Jajko")
    print("2 - Czajnik")
    print("3 - Wyjście")
    print("Mysz (LPM) - obracanie modelu, Scroll - zoom\n")

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()

if __name__ == '__main__':
    main()
