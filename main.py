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

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

yellow_light_enabled = True
blue_light_enabled = True


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
    blue_light_ambient = [0.0, 0.0, 0.1, 1.0]
    blue_light_diffuse = [0.0, 0.0, 1.0, 1.0]
    blue_light_specular = [0.5, 0.5, 1.0, 1.0]
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
            yellow_light_enabled = not yellow_light_enabled
            if yellow_light_enabled:
                glEnable(GL_LIGHT0)
            else:
                glDisable(GL_LIGHT0)

        # Włącz/wyłącz światło niebieskie
        if key == GLFW_KEY_2:
            blue_light_enabled = not blue_light_enabled
            if blue_light_enabled:
                glEnable(GL_LIGHT1)
            else:
                glDisable(GL_LIGHT1)

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

    window = glfwCreateWindow(800, 800, "Jajko 3D", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)

    # Inicjalizacja MouseEventHandler
    mouse_handler = MouseEventHandler()
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
    """Wyświetla menu z instrukcją obsługi w terminalu."""
    print("=== Instrukcja obsługi ===")
    print()
    print("Sterowanie światłem żółtym (GL_LIGHT0):")
    print("  W     - Obrót w górę (phi - zmniejszenie kąta)")
    print("  S     - Obrót w dół (phi - zwiększenie kąta)")
    print("  A     - Obrót w lewo (theta - zmniejszenie kąta)")
    print("  D     - Obrót w prawo (theta - zwiększenie kąta)")
    print("  Z     - Zmniejszenie odległości od środka (radius - zmniejszenie)")
    print("  X     - Zwiększenie odległości od środka (radius - zwiększenie)")
    print("  1     - Włącz/wyłącz światło żółte")
    print()
    print("Sterowanie światłem niebieskim (GL_LIGHT1):")
    print("  Strzałka w górę    - Obrót w górę (phi - zmniejszenie kąta)")
    print("  Strzałka w dół     - Obrót w dół (phi - zwiększenie kąta)")
    print("  Strzałka w lewo    - Obrót w lewo (theta - zmniejszenie kąta)")
    print("  Strzałka w prawo   - Obrót w prawo (theta - zwiększenie kąta)")
    print("  , (przecinek)      - Zmniejszenie odległości od środka (radius - zmniejszenie)")
    print("  . (kropka)         - Zwiększenie odległości od środka (radius - zwiększenie)")
    print("  2                  - Włącz/wyłącz światło niebieskie")
    print()
    print("Sterowanie kamerą:")
    print("  Lewy przycisk myszy - Obrót kamery")
    print("  Scroll myszki       - Zoom kamery")
    print()
    print("=========================")

if __name__ == "__main__":
    main()
