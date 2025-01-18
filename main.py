#!/usr/bin/env python3
import sys
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

yellow_light_enabled = True
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
mouse_handler.yellow_light_theta = 0.0
mouse_handler.yellow_light_phi = math.pi / 4

# Pozycja początkowa światła niebieskiego (po przeciwnej stronie jajka)
mouse_handler.blue_light_theta = math.pi  # 180 stopni
mouse_handler.blue_light_phi = math.pi / 4

att_constant = 1.0
att_linear = 0.1
att_quadratic = 0.01



egg_points = generate_egg_points(50)

def startup():
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


def shutdown():
    pass

def update_light_position(handler):
    """Aktualizuje pozycje świateł żółtego i niebieskiego."""
    # Pozycja światła żółtego
    x_yellow = handler.yellow_light_radius * math.sin(handler.yellow_light_phi) * math.cos(handler.yellow_light_theta)
    y_yellow = handler.yellow_light_radius * math.cos(handler.yellow_light_phi)
    z_yellow = handler.yellow_light_radius * math.sin(handler.yellow_light_phi) * math.sin(handler.yellow_light_theta)
    glLightfv(GL_LIGHT0, GL_POSITION, [x_yellow, y_yellow, z_yellow, 1.0])

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
    if yellow_light_enabled :
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

    # Rysowanie jajka
    render_egg(egg_points)

    glFlush()

def keyboard_key_callback(window, key, scancode, action, mods):
    global yellow_light_enabled, blue_light_enabled

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        # Włącz/wyłącz światło żółte
        if key == GLFW_KEY_1:
            if yellow_light_enabled:
                glDisable(GL_LIGHT0)
                yellow_light_enabled = False
                print("Światło żółte: WYŁĄCZONE")
            else:
                glEnable(GL_LIGHT0)
                yellow_light_enabled = True
                print("Światło żółte: WŁĄCZONE")

        # Włącz/wyłącz światło niebieskie
        elif key == GLFW_KEY_2:
            if blue_light_enabled:
                glDisable(GL_LIGHT1)
                blue_light_enabled = False
                print("Światło niebieskie: WYŁĄCZONE")
            else:
                glEnable(GL_LIGHT1)
                blue_light_enabled = True
                print("Światło niebieskie: WŁĄCZONE")

        # Sterowanie światłem żółtym wokół jajka (WASD)
        elif key == GLFW_KEY_W:
            mouse_handler.yellow_light_phi = max(0.0, mouse_handler.yellow_light_phi - 0.1)
        elif key == GLFW_KEY_S:
            mouse_handler.yellow_light_phi = min(math.pi, mouse_handler.yellow_light_phi + 0.1)
        elif key == GLFW_KEY_D:
            mouse_handler.yellow_light_theta -= 0.1
        elif key == GLFW_KEY_A:
            mouse_handler.yellow_light_theta += 0.1

        # Sterowanie światłem niebieskim wokół jajka (strzałki)
        elif key == GLFW_KEY_UP:
            mouse_handler.blue_light_phi = max(0.0, mouse_handler.blue_light_phi - 0.1)
        elif key == GLFW_KEY_DOWN:
            mouse_handler.blue_light_phi = min(math.pi, mouse_handler.blue_light_phi + 0.1)
        elif key == GLFW_KEY_RIGHT:
            mouse_handler.blue_light_theta -= 0.1
        elif key == GLFW_KEY_LEFT:
            mouse_handler.blue_light_theta += 0.1

        # Normalizacja kątów (zapewnia płynny ruch)
        mouse_handler.yellow_light_theta %= 2 * math.pi
        mouse_handler.blue_light_theta %= 2 * math.pi



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

        # Rysowanie jajka
        render_egg(egg_points)

        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()

def display_instructions():
    print("=== Instrukcja obsługi ===")
    print("W/A/S/D - Sterowanie światłem czerwonym")
    print("Strzałki - Sterowanie światłem niebieskim")
    print("Scroll  - Sterowanie zoomem kamery")
    print("Myszka + lewy przycisk myszy  - Sterowanie kamera")
    print("=========================")

if __name__ == "__main__":
    main()
