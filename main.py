#!/usr/bin/env python3
import sys
import math
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

from events import MouseEventHandler
from jajko import draw_xyz_axes, generate_egg_points, render_egg

# Globalne zmienne
viewer = [0.0, 0.0, 10.0]  # Pozycja kamery
theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

light_theta = 0.0
light_phi = math.pi / 4
light_radius = 10.0

egg_rotation_x = 0.0  # Obrót jajka wokół osi X
egg_rotation_y = 0.0  # Obrót jajka wokół osi Y

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

egg_points = generate_egg_points(50)


def startup():
    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)



def shutdown():
    pass


def update_light_position(mouse_handler):
    """Aktualizuje pozycję światła na podstawie parametrów z MouseEventHandler."""
    x = mouse_handler.light_radius * math.sin(mouse_handler.light_phi) * math.cos(mouse_handler.light_theta)
    y = mouse_handler.light_radius * math.cos(mouse_handler.light_phi)
    z = mouse_handler.light_radius * math.sin(mouse_handler.light_phi) * math.sin(mouse_handler.light_theta)

    glLightfv(GL_LIGHT0, GL_POSITION, [x, y, z, 1.0])





def render(time):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Ustawienie kamery - obrót wokół jajka
    r = 10.0  # Odległość kamery od jajka
    x = r * math.cos(phi) * math.cos(theta)
    y = r * math.sin(phi)
    z = r * math.cos(phi) * math.sin(theta)

    gluLookAt(x, y, z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Aktualizacja pozycji światła
    update_light_position()

    # Rysowanie osi XYZ
    draw_xyz_axes()

    # Rysowanie jajka
    render_egg(egg_points)

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
    if not glfwInit():
        sys.exit(-1)

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

if __name__ == "__main__":
    main()
