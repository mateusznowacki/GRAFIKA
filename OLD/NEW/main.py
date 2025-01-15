import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *

# Importujemy z naszego pliku egg_renderer
from egg_renderer import EggRenderer

# Importujemy callbacki i zmienne globalne z pliku events
import events

# Zmienna globalna - lista punktów naszego jajka
model = []

def startup():
    """
    Funkcja konfiguracyjna - ustawia parametry początkowe OpenGL.
    """
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glPointSize(5.0)

def render(time):
    """
    Funkcja wywoływana w każdej klatce - czyści bufor ekranu,
    ustawia macierz modelu i rysuje nasz model (jajko) jako trójkąty.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Ustawiamy przesunięcie, zoom i obrót z events.py
    glTranslatef(0.0, 0.0, -15.0)
    glScalef(events.zoom, events.zoom, events.zoom)
    glRotatef(events.rotation_x, 1.0, 0.0, 0.0)
    glRotatef(events.rotation_y, 0.0, 1.0, 0.0)

    # Rysowanie jajka jako trójkątów
    glBegin(GL_TRIANGLES)
    for triangle in model:
        for vertex in triangle:
            glColor3fv(vertex['color'])
            glVertex3fv(vertex['vertex'])
    glEnd()

    glFlush()

def update_viewport(window, width, height):
    """
    Callback zmiany rozmiaru okna - modyfikuje macierz projekcji (kamery).
    """
    if height == 0:
        height = 1

    aspect_ratio = width / height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    gluPerspective(45.0, aspect_ratio, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    """
    Funkcja główna - tworzy okno, inicjuje OpenGL i pętlę główną aplikacji.
    """
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, "Egg Model Example", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)

    # Ustawiamy callbacki z pliku events.py
    glfwSetKeyCallback(window, events.keyboard_key_callback)
    glfwSetMouseButtonCallback(window, events.mouse_button_callback)
    glfwSetCursorPosCallback(window, events.cursor_position_callback)
    glfwSetScrollCallback(window, events.scroll_callback)

    glfwSwapInterval(1)  # Synchronizacja klatek

    # Generujemy punkty naszego jajka
    global model
    egg_renderer = EggRenderer()
    model = egg_renderer.generate_egg_triangles(num_points=50)  # Więcej punktów dla gładszego modelu

    # Uruchamiamy podstawową konfigurację OpenGL
    startup()

    # Pętla główna
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()

if __name__ == "__main__":
    main()
