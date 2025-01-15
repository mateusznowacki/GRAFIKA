import sys
import os
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from jajko import generate_egg_points, render_egg_with_texture, load_texture, draw_xyz_axes
from events import MouseEventHandler
from czajnik import *  # Import funkcji dla czajnika

# ----- Zmienne globalne -----
viewer = [0.0, 0.0, 10.0]
texture_id = None
egg_points = None
teapot_points = None
teapot_faces = None
textures = {}
texture_paths = {}
current_texture = None
texture_repeat_factor = 1.0
current_object = "egg"  # Domyślnie wyświetlamy jajko
mouse_handler = MouseEventHandler()

# ----- Funkcje do obsługi tekstur -----
def find_textures(folder="textures"):
    """Znajduje wszystkie pliki tekstur w podanym folderze."""
    texture_files = {}
    if not os.path.exists(folder):
        print(f"Błąd: Folder {folder} nie istnieje!")
        sys.exit(-1)
    for filename in os.listdir(folder):
        if filename.endswith(".tga") or filename.endswith(".png"):  # Obsługiwane formaty tekstur
            texture_name = os.path.splitext(filename)[0]
            texture_files[texture_name] = os.path.join(folder, filename)
    return texture_files

def load_all_textures():
    """Ładuje wszystkie tekstury z podanych ścieżek."""
    global texture_paths
    textures_local = {}
    for name, path in texture_paths.items():
        textures_local[name] = load_texture(path)
        if not textures_local[name]:
            print(f"Błąd ładowania tekstury: {path}")
            sys.exit(-1)
    return textures_local

# ----- Funkcje inicjalizacyjne -----
def startup():
    """Inicjalizacja OpenGL, generowanie jajka i wczytywanie czajnika."""
    global egg_points, texture_id, textures, texture_paths, current_texture
    global teapot_points, teapot_faces

    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    # Włączenie cullingu
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)  # Ignoruj tylne strony trójkątów
    glFrontFace(GL_CCW)  # Określ, że front jest CCW (counter-clockwise)

    # Znajdź i wczytaj wszystkie tekstury
    texture_paths = find_textures()
    textures = load_all_textures()

    # Ustaw pierwszą teksturę jako domyślną
    current_texture = next(iter(textures))  # Pierwszy klucz w słowniku
    texture_id = textures[current_texture]

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
    global texture_id, current_object
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Zastosowanie transformacji myszki
    mouse_handler.apply_transformations()

    # Rysowanie osi XYZ
    draw_xyz_axes()

    # Rysowanie wybranego obiektu
    if current_object == "egg":
        render_egg_with_texture(egg_points, texture_id, texture_repeat_factor)
    elif current_object == "teapot":
        if teapot_points and teapot_faces:
            render_teapot_with_texture(teapot_points, teapot_faces, texture_id, texture_repeat_factor)
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
    global current_texture, texture_id, texture_repeat_factor, current_object
    if action == GLFW_PRESS:
        keys = list(texture_paths.keys())
        index = -1 if current_texture not in keys else keys.index(current_texture)

        if key == GLFW_KEY_1:
            current_object = "egg"
            print("Wybrano: Jajko")
        elif key == GLFW_KEY_2:
            current_object = "teapot"
            print("Wybrano: Czajnik")
        elif key == GLFW_KEY_3:
            print("Wyjście z programu.")
            glfwSetWindowShouldClose(window, GLFW_TRUE)

        elif key == GLFW_KEY_UP:
            # Przełącz na poprzednią teksturę
            current_texture = keys[(index - 1) % len(keys)]
        elif key == GLFW_KEY_DOWN:
            # Przełącz na następną teksturę
            current_texture = keys[(index + 1) % len(keys)]
        elif key == GLFW_KEY_RIGHT:
            # Zwiększ powtarzanie tekstury
            texture_repeat_factor += 1.0
        elif key == GLFW_KEY_LEFT:
            # Zmniejsz powtarzanie tekstury
            texture_repeat_factor = max(1.0, texture_repeat_factor - 1.0)

        texture_id = textures[current_texture]
        print(f"Obiekt: {current_object}, Tekstura: {current_texture}, Powtarzanie: {texture_repeat_factor}")

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
    print("Strzałki (Góra/Dół) - zmiana tekstury")
    print("Strzałki (Lewo/Prawo) - zmiana powtarzania tekstury")
    print("Mysz (LPM) - obracanie modelu, Scroll - zoom\n")

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()

if __name__ == '__main__':
    main()
