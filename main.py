import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from solar_system import SolarSystem

# Kamerka free-fly
camera_pos = [0.0, 5.0, 80.0]
yaw = 0.0
pitch = -10.0
move_speed = 20.0
mouse_sensitivity = 0.05

last_mouse_x = None
last_mouse_y = None

keys_pressed = set()

def init_lighting():
    """
    Białe światło punktowe (GL_LIGHT0) w (0,0,0).
    Słońce ma w planet.py -> GL_EMISSION, wygląda na świecące.
    """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    ambient  = [0.1, 0.1, 0.1, 1.0]
    diffuse  = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT,  ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)

def on_mouse_move(window, xpos, ypos):
    global last_mouse_x, last_mouse_y, yaw, pitch
    if last_mouse_x is None or last_mouse_y is None:
        last_mouse_x, last_mouse_y = xpos, ypos
        return

    dx = xpos - last_mouse_x
    dy = ypos - last_mouse_y
    last_mouse_x, last_mouse_y = xpos, ypos

    yaw   += dx * mouse_sensitivity
    pitch -= dy * mouse_sensitivity

    if pitch > 89.0:
        pitch = 89.0
    if pitch < -89.0:
        pitch = -89.0

def on_key(window, key, scancode, action, mods):
    global keys_pressed
    if action == glfw.PRESS:
        keys_pressed.add(key)
    elif action == glfw.RELEASE:
        if key in keys_pressed:
            keys_pressed.remove(key)

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def update_camera_controls(delta_time):
    global camera_pos, yaw, pitch

    yaw_rad   = math.radians(yaw)
    pitch_rad = math.radians(pitch)

    # Kierunek "przód"
    forward = [
        math.cos(pitch_rad) * math.sin(yaw_rad),
        math.sin(pitch_rad),
        -math.cos(pitch_rad) * math.cos(yaw_rad)
    ]
    # "w prawo" (strafe)
    right = [
        math.sin(yaw_rad + math.pi / 2.0),
        0.0,
        -math.cos(yaw_rad + math.pi / 2.0)
    ]
    # w górę
    up = [0.0, 1.0, 0.0]

    speed = move_speed
    if glfw.KEY_LEFT_SHIFT in keys_pressed:
        speed *= 5.0

    # W/S
    if glfw.KEY_W in keys_pressed:
        camera_pos[0] += forward[0] * speed * delta_time
        camera_pos[1] += forward[1] * speed * delta_time
        camera_pos[2] += forward[2] * speed * delta_time
    if glfw.KEY_S in keys_pressed:
        camera_pos[0] -= forward[0] * speed * delta_time
        camera_pos[1] -= forward[1] * speed * delta_time
        camera_pos[2] -= forward[2] * speed * delta_time

    # A/D
    if glfw.KEY_A in keys_pressed:
        camera_pos[0] -= right[0] * speed * delta_time
        camera_pos[2] -= right[2] * speed * delta_time
    if glfw.KEY_D in keys_pressed:
        camera_pos[0] += right[0] * speed * delta_time
        camera_pos[2] += right[2] * speed * delta_time

    # Q/E
    if glfw.KEY_Q in keys_pressed:
        camera_pos[1] += speed * delta_time
    if glfw.KEY_E in keys_pressed:
        camera_pos[1] -= speed * delta_time

def set_camera_view():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    yaw_rad   = math.radians(yaw)
    pitch_rad = math.radians(pitch)
    forward = [
        math.cos(pitch_rad) * math.sin(yaw_rad),
        math.sin(pitch_rad),
        -math.cos(pitch_rad) * math.cos(yaw_rad)
    ]
    eye = camera_pos
    center = [
        eye[0] + forward[0],
        eye[1] + forward[1],
        eye[2] + forward[2]
    ]
    up = [0.0, 1.0, 0.0]

    gluLookAt(
        eye[0], eye[1], eye[2],
        center[0], center[1], center[2],
        up[0], up[1], up[2]
    )

def main():
    if not glfw.init():
        print("Nie udało się zainicjalizować GLFW.")
        return

    window = glfw.create_window(1280, 720, "Układ Słoneczny - Słońce w ognisku (Kepler), mniejszy promień", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key)
    glfw.set_cursor_pos_callback(window, on_mouse_move)
    # Ukrycie kursora i zablokowanie w oknie
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    glEnable(GL_DEPTH_TEST)
    # Włączenie culling:
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    # Ustawiamy perspektywę
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, 1280.0/720.0, 0.1, 2000.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Tworzymy układ
    solar_system = SolarSystem()
    init_lighting()

    last_time = glfw.get_time()

    print("Sterowanie free-fly:")
    print("  W/S - przód/tył")
    print("  A/D - lewo/prawo (strafe)")
    print("  Q/E - góra/dół")
    print("  Mysz - obrót (yaw/pitch)")
    print("  Shift - przyspieszenie ruchu")
    print("Skala czasu:")
    print("  1,2,3,4 - 1 sek = 1/7/30/60 dni")
    print("ESC - wyjście")

    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        delta_time = current_time - last_time
        last_time = current_time

        glfw.poll_events()
        update_camera_controls(delta_time)

        # Sterowanie skalą czasu
        if glfw.KEY_1 in keys_pressed:
            solar_system.time_scale = 1.0
        if glfw.KEY_2 in keys_pressed:
            solar_system.time_scale = 7.0
        if glfw.KEY_3 in keys_pressed:
            solar_system.time_scale = 30.0
        if glfw.KEY_4 in keys_pressed:
            solar_system.time_scale = 60.0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        set_camera_view()

        # Ustaw światło w (0,0,0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])

        # Aktualizacja planet
        solar_system.update(delta_time)

        # Rysowanie
        solar_system.draw()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
