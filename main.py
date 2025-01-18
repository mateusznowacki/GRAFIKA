#!/usr/bin/env python3
import sys

from czajnik import load_obj, render_teapot
from events import *
from jajko import *

# Globalne zmienne
mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]
mouse_handler = MouseEventHandler()
att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

red_light_enabled = True
blue_light_enabled = True

mat_ambient = [0.3, 0.3, 0.3, 1.0]  # Bardziej widoczne ambient
mat_diffuse = [1.0, 1.0, 1.0, 1.0]  # Odbijane światło
mat_specular = [1.0, 1.0, 1.0, 1.0]  # Lśnienie
mat_shininess = 80.0  # Intensywniejsze odbicia


# Jasność światła czerw
light_ambient = [0.2, 0.0, 0.0, 1.0]  # Czerwona barwa ambient
light_diffuse = [1.0, 0.2, 0.2, 1.0]  # Intensywna czerwień
light_specular = [1.0, 0.4, 0.4, 1.0]  # Lśniąca czerwień

blue_light_ambient = [0.0, 0.0, 0.6, 1.0]  # Intensywniejsze ambient
blue_light_diffuse = [0.0, 0.0, 1.0, 1.0]  # Głębokie, mocno niebieskie światło
blue_light_specular = [0.5, 0.5, 1.0, 1.0]  # Subtelne lśnienie


# Pozycja początkowa światła czerw
mouse_handler.red_light_theta = 0.0
mouse_handler.red_light_phi = math.pi / 4

# Pozycja początkowa światła niebieskiego (po przeciwnej stronie jajka)
mouse_handler.blue_light_theta = math.pi  # 180 stopni
mouse_handler.blue_light_phi = math.pi / 4

att_constant = 1.0
att_linear = 0.1
att_quadratic = 0.01

teapot_points = None
teapot_faces = None
egg_points = generate_egg_points(50)


def startup():

    global teapot_points, teapot_faces

    glEnable(GL_CULL_FACE)            # Włącz culling
    glCullFace(GL_BACK)               # Usuń tylne ściany
    glFrontFace(GL_CCW)

    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # Ustawienia materiałowe
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # Konfiguracja światła żółtego
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    # Konfiguracja światła niebieskiego
    glLightfv(GL_LIGHT1, GL_AMBIENT, blue_light_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, blue_light_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, blue_light_specular)
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # Wczytanie punktów i ścian czajnika z pliku .obj
    teapot_file = "teapot.obj"
    if os.path.exists(teapot_file):
        teapot_points, teapot_faces = load_obj(teapot_file)
    else:
        print(f"Brak pliku: {teapot_file}, czajnik nie zostanie wczytany.")


def shutdown():
    pass

def update_light_position(handler):
    """Aktualizuje pozycje świateł czerwonego i niebieskiego."""
    # Pozycja światła czerwonego
    x_red = handler.red_light_radius * math.sin(handler.red_light_phi) * math.cos(handler.red_light_theta)
    y_red = handler.red_light_radius * math.cos(handler.red_light_phi)
    z_red = handler.red_light_radius * math.sin(handler.red_light_phi) * math.sin(handler.red_light_theta)
    glLightfv(GL_LIGHT0, GL_POSITION, [x_red, y_red, z_red, 1.0])

    # Pozycja światła niebieskiego
    x_blue = handler.blue_light_radius * math.sin(handler.blue_light_phi) * math.cos(handler.blue_light_theta)
    y_blue = handler.blue_light_radius * math.cos(handler.blue_light_phi)
    z_blue = handler.blue_light_radius * math.sin(handler.blue_light_phi) * math.sin(handler.blue_light_theta)
    glLightfv(GL_LIGHT1, GL_POSITION, [x_blue, y_blue, z_blue, 1.0])



def render(time):

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Ustawienie kamery
    gluLookAt(0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Aktualizacja pozycji świateł
    if red_light_enabled :
        glEnable(GL_LIGHT0)
    else :
        glDisable(GL_LIGHT0)
    if blue_light_enabled :
        glEnable(GL_LIGHT1)
    else :
        glDisable(GL_LIGHT1)

    update_light_position()

    # Rysowanie osi XYZ
    draw_xyz_axes()

    glFlush()




def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, width / height, 0.1, 300.0)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    global current_object
    if not glfwInit():
        sys.exit(-1)

    display_instructions()
        # W main():


    window = glfwCreateWindow(800, 800, "Jajko 3D", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)

    # Inicjalizacja MouseEventHandler

    mouse_handler.register_callbacks(window)

    glfwSwapInterval(1)
    startup()

    while not glfwWindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Zastosowanie transformacji kamery
        mouse_handler.apply_transformations()

        # Aktualizacja pozycji światła
        update_light_position(mouse_handler)

        # Rysowanie osi XYZ
        draw_xyz_axes()


        current_object = mouse_handler.current_object

            # Rysowanie wybranego obiektu
        if current_object == "egg":
            render_egg(egg_points)
        elif current_object == "teapot":
            if teapot_points and teapot_faces:
                render_teapot(teapot_points, teapot_faces)
            else:
                print("Czajnik nie został wczytany!")

        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()

def display_instructions():
    print("=== Instrukcja obsługi ===")
    print("Przełączanie miedzy czajnikiem a jajkiem: j - jajko, c - czajnik")
    print("Włączanie/wyłączanie świateł: 1 - światło czerwone, 2 - światło niebieskie")
    print("W/A/S/D - Sterowanie światłem czerwonym")
    print("Z/X - Sterowanie promieniem światła czerwonego")
    print("Strzałki - Sterowanie światłem niebieskim")
    print(",/. - Sterowanie promieniem światła niebieskiego")
    print("Scroll  - Sterowanie zoomem kamery")
    print("Myszka + lewy przycisk myszy  - Sterowanie kamera")
    print("=========================")

if __name__ == "__main__":
    main()
