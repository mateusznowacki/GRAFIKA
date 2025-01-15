import sys
import os
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from jajko import generate_egg_points, render_egg, draw_xyz_axes
from events import MouseEventHandler
from czajnik import render_teapot, load_obj  # Import funkcji dla czajnika

# ----- Zmienne globalne -----
viewer = [0.0, 0.0, 10.0]
egg_points = None
teapot_points = None
teapot_faces = None
current_object = "egg"  # Domyślnie wyświetlamy jajko
mouse_handler = MouseEventHandler()

# ----- Funkcje inicjalizacyjne -----
def startup():
    """Inicjalizacja OpenGL, generowanie jajka i wczytywanie czajnika."""
    global egg_points, teapot_points, teapot_faces

    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # Włączenie cullingu
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)  # Ignoruj tylne strony trójkątów
    glFrontFace(GL_CCW)  # Określ, że front jest CCW (counter-clockwise)

    # Generowanie punktów jajka
    egg_points = generate_egg_points(50)

    # Wczytanie punktów i ścian czajnika z pliku .obj
    teapot_file = "teapot.obj"
    if os.path.exists(teapot_file):
        teapot_points, teapot_faces = load_obj(teapot_file)
    else:
        print(f"Brak pliku: {teapot_file}, czajnik nie zostanie wczytany.")

def shutdown():
    """Czyszczenie zasobów OpenGL."""
    pass

# ----- Funkcja renderująca -----
def render(time):
    """Renderowanie sceny."""
    global current_object
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Zastosowanie transformacji myszki
    mouse_handler.apply_transformations()

    # Rysowanie osi XYZ
    draw_xyz_axes()

    # Rysowanie wybranego obiektu
    if current_object == "egg":
        render_egg(egg_points)  # Renderowanie jajka w białym kolorze
    elif current_object == "teapot":
        if teapot_points and teapot_faces:
            render_teapot(teapot_points, teapot_faces)  # Renderowanie czajnika w białym kolorze
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
    """Obsługa klawiatury."""
    global current_object
    if action == GLFW_PRESS:
        if key == GLFW_KEY_1:
            current_object = "egg"
            print("Wybrano: Jajko")
        elif key == GLFW_KEY_2:
            current_object = "teapot"
            print("Wybrano: Czajnik")
        elif key == GLFW_KEY_3:
            print("Wyjście z programu.")
            glfwSetWindowShouldClose(window, GLFW_TRUE)

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
