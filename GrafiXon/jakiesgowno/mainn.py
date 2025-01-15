import sys
import os
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from jajko import generate_egg_points, render_egg_with_texture, load_texture, draw_xyz_axes
from events import MouseEventHandler

viewer = [0.0, 0.0, 10.0]
texture_id = None
egg_points = None
textures = {}
texture_paths = {
    "las": r"C:\Users\matty\PycharmProjects\GRAFIKA2\texture\las.tga",
    "cegla": r"C:\Users\matty\PycharmProjects\GRAFIKA2\texture\cegla.tga",
    "piasek": r"C:\Users\matty\PycharmProjects\GRAFIKA2\texture\piasek.tga"
}
current_texture = "piasek"
mouse_handler = MouseEventHandler()

def load_all_textures():
    """Ładuje wszystkie tekstury z podanych ścieżek."""
    global texture_paths
    textures = {}
    for name, path in texture_paths.items():
        textures[name] = load_texture(path)
        if not textures[name]:
            print(f"Błąd ładowania tekstury: {path}")
            sys.exit(-1)
    return textures

def startup():
    global egg_points, texture_id, textures
    """Inicjalizacja OpenGL i generowanie jajka."""
    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0,1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    # Generowanie punktów jajka
    egg_points = generate_egg_points(50)

    # Wczytywanie wszystkich tekstur
    textures = load_all_textures()
    texture_id = textures[current_texture]

def shutdown():
    """Czyszczenie zasobów OpenGL."""
    pass

def render(time):
    """Renderowanie sceny."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Zastosowanie transformacji myszki
    mouse_handler.apply_transformations()

    # Rysowanie osi XYZ
    draw_xyz_axes()

    # Rysowanie jajka z teksturą
    render_egg_with_texture(egg_points, texture_id)

    glFlush()

def update_viewport(window, width, height):
    """Aktualizacja widoku po zmianie rozmiaru okna."""
    global pix2angle
    pix2angle = 360.0 / width
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, width / height, 0.1, 300.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard_key_callback(window, key, scancode, action, mods):
    """Obsługa klawiatury - dodaj zmiany tekstur."""
    global current_texture, texture_id
    if action == GLFW_PRESS:
        if key == GLFW_KEY_1:
            current_texture = "las"
        elif key == GLFW_KEY_2:
            current_texture = "cegla"
        elif key == GLFW_KEY_3:
            current_texture = "piasek"
        texture_id = textures[current_texture]
    if key == GLFW_KEY_ESCAPE:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

def main():
    """Główna funkcja programu."""
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, "Jajko z teksturą", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)

    # Rejestracja callbacków myszki
    mouse_handler.register_callbacks(window)

    glfwSwapInterval(1)

    print("Wybierz teksturę dla jajka:")
    print("1 - Las")
    print("2 - Cegła")
    print("3 - Piasek")

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()

if __name__ == '__main__':
    main()
