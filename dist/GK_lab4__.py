import os
import random
import sys
import numpy
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PIL import Image

rotation_x, rotation_y = 0.0, 0.0
zoom = 1.0
last_mouse_x, last_mouse_y = None, None
draw_mode = GL_POINTS
model = []
lines_horizontal = False
selected_texture = 1

# Stałe dla parametrów światła
LIGHT_1_COLOR = (1.0, 1.0, 1.0)
LIGHT_2_COLOR = (1.0, 1.0, 1.0)
LIGHT_AMBIENT = 0.5  # Zwiększona jasność otoczenia
LIGHT_DIFFUSE = 1.0  # Maksymalna jasność światła rozproszonego
LIGHT_SPECULAR = 1.0  # Maksymalna jasność refleksji

selected_object = 1         # Zmienna przechowująca aktualnie wybrany obiekt (domyślnie model)

light1_coords = [5.0, 0.0, math.pi / 4]  # [promień, azymut, elewacja]
light2_coords = [5.0, 0.0, -math.pi / 4] # [promień, azymut, elewacja]


def load_random_texture(folder_path="tekstury"):
    """Ładuje losową teksturę z podanego folderu."""
    try:
        texture_files = [f for f in os.listdir(folder_path) if f.endswith('.tga')]
        if not texture_files:
            raise FileNotFoundError("Brak plików tekstur w folderze.")

        random_texture = random.choice(texture_files)  # Wybór losowej tekstury
        texture_path = os.path.join(folder_path, random_texture)
        print(f"Wczytywanie tekstury: {texture_path}")

        # Wczytywanie pliku tekstury
        image = Image.open(texture_path).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = numpy.array(image, dtype=numpy.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Parametry tekstury
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        return texture_id
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(-1)


def calculate_light_position(radius, azimuth, elevation):
    x = radius * math.cos(elevation) * math.cos(azimuth)
    y = radius * math.sin(elevation)
    z = radius * math.cos(elevation) * math.sin(azimuth)
    return (x, y, z)

def update_light_position(light_coords, key):
    radius, azimuth, elevation = light_coords

    if key == GLFW_KEY_UP:
        elevation = min(elevation + 0.1, math.pi / 2)  # Ograniczenie elewacji do maksymalnie 90 stopni
    elif key == GLFW_KEY_DOWN:
        elevation = max(elevation - 0.1, -math.pi / 2)  # Ograniczenie elewacji do -90 stopni
    elif key == GLFW_KEY_LEFT:
        azimuth -= 0.1
    elif key == GLFW_KEY_RIGHT:
        azimuth += 0.1

    elif key == GLFW_KEY_MINUS:
        radius = max(radius - 0.1, 1.0)
    elif key == GLFW_KEY_EQUAL:
        radius += 0.1

    return [radius, azimuth, elevation]


def setup_lights():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # Pozycja i kolor pierwszego światła
    light_1_pos = calculate_light_position(light1_coords[0], light1_coords[1], light1_coords[2])
    glLightfv(GL_LIGHT0, GL_POSITION, light_1_pos + (1.0,))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (LIGHT_AMBIENT, LIGHT_AMBIENT, LIGHT_AMBIENT, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LIGHT_1_COLOR + (1.0,))
    glLightfv(GL_LIGHT0, GL_SPECULAR, LIGHT_1_COLOR + (1.0,))

    # Pozycja i kolor drugiego światła
    light_2_pos = calculate_light_position(light2_coords[0], light2_coords[1], light2_coords[2])
    glLightfv(GL_LIGHT1, GL_POSITION, light_2_pos + (1.0,))
    glLightfv(GL_LIGHT1, GL_AMBIENT, (LIGHT_AMBIENT, LIGHT_AMBIENT, LIGHT_AMBIENT, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, LIGHT_2_COLOR + (1.0,))
    glLightfv(GL_LIGHT1, GL_SPECULAR, LIGHT_2_COLOR + (1.0,))


def calculate_normals():
    global model
    for triangle in model:

        v1, v2, v3 = triangle['vertices']
        u = numpy.subtract(v2, v1)
        v = numpy.subtract(v3, v1)
        normal = numpy.cross(u, v)
        normal = normal / numpy.linalg.norm(normal)

        triangle['normals'] = [normal, normal, normal]

def phong_shading(vertex, normal, light_pos, light_color):

    light_dir = numpy.subtract(light_pos, vertex)
    light_dir = light_dir / numpy.linalg.norm(light_dir)

    ambient = numpy.multiply(light_color, LIGHT_AMBIENT)

    diffuse = numpy.multiply(light_color, max(0.0, numpy.dot(normal, light_dir)) * LIGHT_DIFFUSE)

    view_dir = numpy.array([0.0, 0.0, 1.0])
    reflect_dir = 2 * numpy.dot(normal, light_dir) * normal - light_dir
    reflect_dir = reflect_dir / numpy.linalg.norm(reflect_dir)
    specular = numpy.multiply(light_color, LIGHT_SPECULAR * max(0.0, numpy.dot(view_dir, reflect_dir))**32)

    return numpy.add(numpy.add(ambient, diffuse), specular)


def render_model_gouraud():
    if not model:
        return

    glBegin(GL_TRIANGLES)

    n = 2
    for triangle in model:
        vertices = triangle['vertices']
        normals = triangle['normals']

        # Pozycje świateł
        light_1_pos = calculate_light_position(light1_coords[0], light1_coords[1], light1_coords[2])
        light_2_pos = calculate_light_position(light2_coords[0], light2_coords[1], light2_coords[2])

        for i in range(3):
            normal = normals[i]
            vertex = vertices[i]

            # Obliczenie kolor na podstawie obu świateł
            color_1 = phong_shading(vertex, normal, light_1_pos, LIGHT_1_COLOR)
            color_2 = phong_shading(vertex, normal, light_2_pos, LIGHT_2_COLOR)
            final_color = numpy.clip(numpy.add(color_1, color_2), 0.0, 1.0)

            if n%2 == 1:
                if i == 0:
                    glTexCoord2f(0.0, 0.0)
                elif i == 1:
                    glTexCoord2f(1.0, 0.0)
                elif i == 2:
                    glTexCoord2f(0.0, 1.0)
            else:
                if i == 0:
                    glTexCoord2f(0.0, 0.0)
                elif i == 1:
                    glTexCoord2f(1.0, 1.0)
                elif i == 2:
                    glTexCoord2f(1.0, 1.0)

            glColor3fv(final_color)
            glVertex3fv(vertex)
            n = n+1
    glEnd()

def startup():
    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)  # Włączenie obsługi tekstur
    glShadeModel(GL_SMOOTH)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Wczytywanie losowej tekstury z folderu "tekstury"
    load_random_texture("tekstury")



def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def generate_egg():
    global triangles
    v_loops = 15    # Liczba wierzchołków w obwodzie jajka
    h_loops = 15    # Liczba obwodów
    s = 5           # Skala jajka

    for i in range(v_loops):
        lat0 = math.pi * (-0.5 + float(i) / v_loops)
        y0 = s * 0.7 * math.sin(lat0)
        zr0 = s * 0.5 * math.cos(lat0)

        lat1 = math.pi * (-0.5 + float(i + 1) / v_loops)
        y1 = s * 0.7 * math.sin(lat1)
        zr1 = s * 0.5 * math.cos(lat1)

        for j in range(h_loops):
            lng0 = 2 * math.pi * float(j) / h_loops
            lng1 = 2 * math.pi * float(j + 1) / h_loops

            x0, z0 = math.cos(lng0), math.sin(lng0)
            x1, z1 = math.cos(lng1), math.sin(lng1)

            v1 = (x0 * zr0, y0, z0 * zr0)
            v2 = (x1 * zr0, y0, z1 * zr0)
            v3 = (x1 * zr1, y1, z1 * zr1)
            v4 = (x0 * zr1, y1, z0 * zr1)

            color = (random.random(), random.random(), random.random())
            model.append({'vertices': [v1, v2, v3], 'color': color})
            color = (random.random(), random.random(), random.random())
            model.append({'vertices': [v1, v3, v4], 'color': color})


def load_model_from_file(filename):
    global model
    model = []

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            num_of_tris = int(lines[0].strip())
            i = 1
            tris_loaded = 0
            while tris_loaded < num_of_tris:
                v1 = list(map(float, lines[i].strip().split()))
                v2 = list(map(float, lines[i + 1].strip().split()))
                v3 = list(map(float, lines[i + 2].strip().split()))
                i = i + 4
                tris_loaded = tris_loaded + 1
                color = (7.0, 7.0, 7.0)
                model.append({'vertices': [v1, v2, v3], 'color': color})
    except Exception as e:
        print(f"Błąd podczas wczytywania pliku: {e}")


def rotate_model(axis, degree):
    global model
    transformed_model = []

    if axis == 'x':
        m = numpy.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, math.cos(degree), -math.sin(degree), 0.0],
            [0.0, math.sin(degree), math.cos(degree), 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    elif axis == 'y':
        m = numpy.array([
            [math.cos(degree), 0.0, math.sin(degree), 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-math.sin(degree), 0.0, math.cos(degree), 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    elif axis == 'z':
        m = numpy.array([
            [math.cos(degree), -math.sin(degree), 0.0, 0.0],
            [math.sin(degree), math.cos(degree), 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

    for triangle in model:
        new_vertices = []
        for vertex in triangle['vertices']:
            v = numpy.array([vertex[0], vertex[1], vertex[2], 1.0])
            transformed_vertex = numpy.dot(m, v)
            new_vertices.append([transformed_vertex[0], transformed_vertex[1], transformed_vertex[2]])

        new_normals = []
        if 'normals' in triangle:
            rotation_only = m[:3, :3]
            for normal in triangle['normals']:
                transformed_normal = numpy.dot(rotation_only, normal)
                transformed_normal = transformed_normal / numpy.linalg.norm(transformed_normal)
                new_normals.append(transformed_normal)

        transformed_triangle = {'vertices': new_vertices, 'color': triangle['color']}
        if new_normals:
            transformed_triangle['normals'] = new_normals

        transformed_model.append(transformed_triangle)

    model = transformed_model



def render_model():
    if not model:
        return

    glPointSize(2.0)
    glBegin(draw_mode)

    if draw_mode == GL_POINTS or draw_mode == GL_LINES:
        glColor3f(0.0, 0.65, 0.0)
        for triangle in model:
            glVertex3fv(triangle['vertices'][0])
            glVertex3fv(triangle['vertices'][1])
            glVertex3fv(triangle['vertices'][1])
            glVertex3fv(triangle['vertices'][2])
            glVertex3fv(triangle['vertices'][2])
            glVertex3fv(triangle['vertices'][0])
    else:
        for triangle in model:
            glColor3fv(triangle['color'])

            glTexCoord2f(0.0, 0.0)
            glVertex3fv(triangle['vertices'][0])
            glTexCoord2f(1.0, 0.0)
            glVertex3fv(triangle['vertices'][1])
            glTexCoord2f(0.5, 1.0)
            glVertex3fv(triangle['vertices'][2])

            #for vertex in triangle['vertices']:
            #   glVertex3fv(vertex)
    glEnd()


def render(time):
    global rotation_x, rotation_y, zoom
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -15.0)
    glScalef(zoom, zoom, zoom)
    glRotatef(rotation_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_y, 0.0, 1.0, 0.0)


    setup_lights()
    axes()
    render_model_gouraud()
    glFlush()


def update_viewport(window, width, height):
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()


    gluPerspective(45.0, aspect_ratio, 0.1, 100.0)  #

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard_key_callback(window, key, scancode, action, mods):
    global selected_object, light1_coords, light2_coords

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_1:
            selected_object = 1
            print("Sterowanie modelem")
        elif key == GLFW_KEY_2:
            selected_object = 2
            print("Sterowanie pierwszym źródłem światła")
        elif key == GLFW_KEY_3:
            selected_object = 3
            print("Sterowanie drugim źródłem światła")


        if selected_object == 1:  # Sterowanie modelem
            if key == GLFW_KEY_UP:
                rotate_model('x', -0.1)
            elif key == GLFW_KEY_DOWN:
                rotate_model('x', 0.1)
            elif key == GLFW_KEY_LEFT:
                rotate_model('y', -0.1)
            elif key == GLFW_KEY_RIGHT:
                rotate_model('y', 0.1)
            elif key == GLFW_KEY_I:
                rotate_model('z', -0.1)
            elif key == GLFW_KEY_K:
                rotate_model('z', 0.1)
        elif selected_object == 2:  # Sterowanie pierwszym źródłem światła
            light1_coords = update_light_position(light1_coords, key)

        elif selected_object == 3:  # Sterowanie drugim źródłem światła
            light2_coords = update_light_position(light2_coords, key)


def mouse_button_callback(window, button, action, mods):
    global last_mouse_x, last_mouse_y
    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        last_mouse_x, last_mouse_y = glfwGetCursorPos(window)


def cursor_position_callback(window, xpos, ypos):
    global rotation_x, rotation_y, last_mouse_x, last_mouse_y
    if glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_PRESS:

        dx = xpos - last_mouse_x
        dy = ypos - last_mouse_y
        last_mouse_x, last_mouse_y = xpos, ypos

        rotation_x += dy * 0.1
        rotation_y += dx * 0.1


def scroll_callback(window, xoffset, yoffset):
    global zoom

    zoom = max(0.1, zoom + yoffset * 0.1)

def menu():
    global draw_mode, lines_horizontal
    print("Wybierz opcję:\nJajko:\n1 - Punkty\n2 - Linie\n3 - Trójkąty")
    print("Czajnik:\n4 - Punkty\n5 - Linie\n6 - Trójkąty")
    option = input("Wybór (1/2/3/4/5/6): ")
    if option == "1":
        generate_egg()
        draw_mode = GL_POINTS
    elif option == "2":
        generate_egg()
        lines_horizontal = True
        draw_mode = GL_LINES
    elif option == "3":
        generate_egg()
        lines_horizontal = False
        draw_mode = GL_TRIANGLES
    elif option == "4":
        draw_mode = GL_POINTS
        load_model_from_file(get_path("czajnik.txt"))
    elif option == "5":
        draw_mode = GL_LINES
        load_model_from_file(get_path("czajnik.txt"))
    elif option == "6":
        draw_mode = GL_TRIANGLES
        load_model_from_file("czajnik.txt")
    else:
        print("Niepoprawny wybór. Używam domyślnego trybu (punkty).")
        draw_mode = GL_POINTS

    print("\nWyświetlono model. Proszę przejść do drugiego okna."
          "\nKlawisze '1'/'2'/'3' wybierają obiekt do sterowania (model / światło 1 / światło 2)"
          "\nModel obracany jest za pomocą klawiszy strzałek oraz 'k'/'i'."
          "\nŹródła światła: '+'/'-' : promień, strzałki góra/dół : elewacja, strzałki lewo/prawo : azymut"
          "\nPrzytrzymanie lewego przycisku myszy pozwala na obrót perspektywą."
          "\nKółko myszy służy do ustalania przybliżenia.")

def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("..")

    return os.path.join(base_path, relative_path)

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)

    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetCursorPosCallback(window, cursor_position_callback)
    glfwSetScrollCallback(window, scroll_callback)

    glfwSwapInterval(1)

    menu()
    calculate_normals()
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == '__main__':
    main()
