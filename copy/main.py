#!/usr/bin/env python3
import sys
import math
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


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


def generate_egg_points(n):
    points = []
    for i in range(n):
        u = i / (n - 1)
        row = []
        for j in range(n):
            v = j / (n - 1)

            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v)

            row.append((x, y, z))
        points.append(row)
    return points


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


def update_light_position():
    global light_theta, light_phi, light_radius
    x = light_radius * math.sin(light_phi) * math.cos(light_theta)
    y = light_radius * math.cos(light_phi)
    z = light_radius * math.sin(light_phi) * math.sin(light_theta)

    glLightfv(GL_LIGHT0, GL_POSITION, [x, y, z, 1.0])


def render_egg(points):
    glBegin(GL_TRIANGLES)
    for i in range(len(points) - 1):
        for j in range(len(points[i]) - 1):
            glVertex3fv(points[i][j])
            glVertex3fv(points[i][j + 1])
            glVertex3fv(points[i + 1][j])

            glVertex3fv(points[i + 1][j])
            glVertex3fv(points[i][j + 1])
            glVertex3fv(points[i + 1][j + 1])
    glEnd()


def render(time):
    global theta, phi, egg_rotation_x, egg_rotation_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Ustawienie kamery
    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Aktualizacja pozycji światła
    update_light_position()

    # Obrót jajka na podstawie ruchu myszy
    glRotatef(egg_rotation_x, 1.0, 0.0, 0.0)  # Obrót wokół osi X
    glRotatef(egg_rotation_y, 0.0, 1.0, 0.0)  # Obrót wokół osi Y

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


def keyboard_key_callback(window, key, scancode, action, mods):
    global light_theta, light_phi

    angle_step = 0.2  # Zwiększono z 0.1 na 0.2

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_W:  # Obrót światła w dół
            light_phi += angle_step
        elif key == GLFW_KEY_S:  # Obrót światła w górę
            light_phi -= angle_step
        elif key == GLFW_KEY_A:  # Obrót światła w prawo
            light_theta += angle_step
        elif key == GLFW_KEY_D:  # Obrót światła w lewo
            light_theta -= angle_step
        elif key == GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y, mouse_x_pos_old, mouse_y_pos_old
    global egg_rotation_x, egg_rotation_y

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos

    if left_mouse_button_pressed:
        egg_rotation_y += delta_x * pix2angle * 0.2  # Zwiększono z 0.1 na 0.2
        egg_rotation_x += delta_y * pix2angle * 0.2  # Zwiększono z 0.1 na 0.2

    # Ograniczenie rotacji X
        egg_rotation_x = max(-90.0, min(90.0, egg_rotation_x))



def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    elif button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_RELEASE:
        left_mouse_button_pressed = 0


def scroll_callback(window, xoffset, yoffset):
    global viewer

    # Zoom in/out
    zoom_step = 1.0
    if yoffset > 0:  # Scroll up
        viewer[2] = max(1.0, viewer[2] - zoom_step)
    elif yoffset < 0:  # Scroll down
        viewer[2] += zoom_step


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, "Jajko 3D", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetScrollCallback(window, scroll_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()


if __name__ == "__main__":
    main()
