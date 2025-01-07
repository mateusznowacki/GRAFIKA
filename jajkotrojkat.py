#!/usr/bin/env python3
import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Konfiguracja
color_mode = False  # Białe jajko
shading_mode = "phong"  # Domyślnie cieniowanie Phonga
smooth_shading = True  # Cieniowanie gładkie (Phonga lub Gourauda)
N = 50  # Liczba wierzchołków
camera_angle_x = 0.0  # Kąt obrotu kamery wokół osi X
camera_angle_y = 0.0  # Kąt obrotu kamery wokół osi Y

# Pozycja i kąty sferyczne światła
light1_angle = [0.0, 0.0]  # Kąt sferyczny światła 1
light2_angle = [45.0, 90.0]  # Kąt sferyczny światła 2
light1_position = [0.0, 0.0, 1.0, 1.0]
light2_position = [0.0, 0.0, -1.0, 1.0]

# Obsługa myszy
is_dragging = False
last_mouse_x = 0.0
last_mouse_y = 0.0

# Funkcja inicjalizacyjna
def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    # Materiał jajka
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])  # Białe jajko
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)

    # Światło 1 (czerwone)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 0.0, 0.0, 1.0])

    # Światło 2 (niebieskie)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.2, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.0, 0.0, 1.0, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.0, 0.0, 1.0, 1.0])

# Aktualizacja widoku
def update_viewport(window, width, height):
    if width == 0: width = 1
    if height == 0: height = 1
    aspect_ratio = width / height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    gluPerspective(45, aspect_ratio, 1.0, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Obliczanie pozycji światła na podstawie kątów sferycznych
def update_light_position(angle, light_position):
    theta, phi = angle
    radius = 10.0
    light_position[0] = radius * math.sin(math.radians(theta)) * math.cos(math.radians(phi))
    light_position[1] = radius * math.sin(math.radians(theta)) * math.sin(math.radians(phi))
    light_position[2] = radius * math.cos(math.radians(theta))

# Generowanie punktów jajka
def generate_points(N):
    points = []
    for i in range(N + 1):
        row_points = []
        for j in range(N + 1):
            u, v = i / N, j / N
            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v)
            row_points.append([x, y, z])
        points.append(row_points)
    return points

points = generate_points(N)

# Obliczanie normalnych
def compute_normal(point):
    length = math.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
    if length == 0:
        return [0.0, 0.0, 1.0]
    return [point[0] / length, point[1] / length, point[2] / length]

# Rysowanie jajka
def draw_egg():
    glShadeModel(GL_SMOOTH if smooth_shading else GL_FLAT)
    glBegin(GL_TRIANGLES)
    for i in range(N):
        for j in range(N):
            # Wierzchołki i normalne dla pierwszego trójkąta
            glNormal3fv(compute_normal(points[i][j]))
            glVertex3fv(points[i][j])

            glNormal3fv(compute_normal(points[i + 1][j]))
            glVertex3fv(points[i + 1][j])

            glNormal3fv(compute_normal(points[i][j + 1]))
            glVertex3fv(points[i][j + 1])

            # Wierzchołki i normalne dla drugiego trójkąta
            glNormal3fv(compute_normal(points[i + 1][j + 1]))
            glVertex3fv(points[i + 1][j + 1])

            glNormal3fv(compute_normal(points[i][j + 1]))
            glVertex3fv(points[i][j + 1])

            glNormal3fv(compute_normal(points[i + 1][j]))
            glVertex3fv(points[i + 1][j])
    glEnd()

# Funkcja renderująca
def render():
    global light1_angle, light2_angle, light1_position, light2_position

    # Aktualizacja pozycji świateł
    light1_angle[0] += 1.0
    light1_angle[1] += 0.5
    light2_angle[0] += 0.7
    light2_angle[1] += 0.3

    update_light_position(light1_angle, light1_position)
    update_light_position(light2_angle, light2_position)

    glLightfv(GL_LIGHT0, GL_POSITION, light1_position)
    glLightfv(GL_LIGHT1, GL_POSITION, light2_position)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -20.0)
    glRotatef(camera_angle_x, 1.0, 0.0, 0.0)
    glRotatef(camera_angle_y, 0.0, 1.0, 0.0)

    draw_egg()
    glFlush()

# Obsługa klawiatury
def key_callback(window, key, scancode, action, mods):
    global smooth_shading
    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_S:  # Przełączanie cieniowania
            smooth_shading = not smooth_shading

# Obsługa myszy
def mouse_button_callback(window, button, action, mods):
    global is_dragging
    if button == GLFW_MOUSE_BUTTON_LEFT:
        is_dragging = (action == GLFW_PRESS)

def cursor_position_callback(window, xpos, ypos):
    global last_mouse_x, last_mouse_y, camera_angle_x, camera_angle_y, is_dragging
    if is_dragging:
        dx = xpos - last_mouse_x
        dy = ypos - last_mouse_y
        camera_angle_x += dy * 0.1
        camera_angle_y += dx * 0.1
    last_mouse_x = xpos
    last_mouse_y = ypos

# Funkcja główna
def main():
    if not glfwInit(): sys.exit(-1)
    window = glfwCreateWindow(400, 400, "Jajko - triangulacja i cieniowanie", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, key_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetCursorPosCallback(window, cursor_position_callback)
    startup()

    while not glfwWindowShouldClose(window):
        render()
        glfwSwapBuffers(window)
        glfwPollEvents()
    glfwTerminate()

if __name__ == "__main__":
    main()

def run():
    main()
