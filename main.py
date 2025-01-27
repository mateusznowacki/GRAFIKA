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

# Kamera na powierzchni planet
current_camera_target = None  # Obiekt, na który patrzy kamera
camera_distance = 2.0  # Odległość kamery od środka obiektu


def init_lighting():
    """
    Białe światło punktowe (GL_LIGHT0) w (0,0,0).
    Słońce ma w planet.py -> GL_EMISSION, wygląda na świecące.
    """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    ambient = [0.1, 0.1, 0.1, 1.0]
    diffuse = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
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

    yaw += dx * mouse_sensitivity
    pitch -= dy * mouse_sensitivity

    if pitch > 89.0:
        pitch = 89.0
    if pitch < -89.0:
        pitch = -89.0


def on_key(window, key, scancode, action, mods):
    global keys_pressed, current_camera_target, solar_system

    if action == glfw.PRESS:
        keys_pressed.add(key)

        # Kamery na obiektach (1-8 dla planet, np. Słońca, Ziemi itd.)
        if key in [glfw.KEY_1, glfw.KEY_2, glfw.KEY_3, glfw.KEY_4, glfw.KEY_5, glfw.KEY_6, glfw.KEY_7, glfw.KEY_8]:
            planet_index = key - glfw.KEY_1  # Oblicz indeks planety
            if planet_index < len(solar_system.planets):
                current_camera_target = solar_system.planets[planet_index]
                print(f"Kamera na planecie: {current_camera_target.name}")

        # Wyjście z trybu kamery na powierzchni (klawisz 0)
        if key == glfw.KEY_0:
            current_camera_target = None
            print("Powrót do trybu free-fly kamery")

    elif action == glfw.RELEASE:
        if key in keys_pressed:
            keys_pressed.remove(key)

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def set_camera_view():
    global camera_pos, yaw, pitch, current_camera_target, camera_distance

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if current_camera_target is not None:
        # Kamera na powierzchni planety
        eye = [
            current_camera_target.pos_x,
            current_camera_target.radius + camera_distance,  # Na powierzchni
            current_camera_target.pos_z
        ]
        center = [
            current_camera_target.pos_x,
            current_camera_target.radius / 2,  # Centrum planety
            current_camera_target.pos_z
        ]
        up = [0.0, 1.0, 0.0]
        gluLookAt(
            eye[0], eye[1], eye[2],
            center[0], center[1], center[2],
            up[0], up[1], up[2]
        )
    else:
        # Free-fly kamera
        yaw_rad = math.radians(yaw)
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


def update_camera_controls(delta_time):
    global camera_pos, yaw, pitch, current_camera_target

    if current_camera_target is not None:
        # Kamera na powierzchni obiektu
        return
    else:
        # Free-fly kamera
        yaw_rad = math.radians(yaw)
        pitch_rad = math.radians(pitch)

        forward = [
            math.cos(pitch_rad) * math.sin(yaw_rad),
            math.sin(pitch_rad),
            -math.cos(pitch_rad) * math.cos(yaw_rad)
        ]
        right = [
            math.sin(yaw_rad + math.pi / 2.0),
            0.0,
            -math.cos(yaw_rad + math.pi / 2.0)
        ]

        speed = move_speed
        if glfw.KEY_LEFT_SHIFT in keys_pressed:
            speed *= 5.0

        if glfw.KEY_W in keys_pressed:
            camera_pos[0] += forward[0] * speed * delta_time
            camera_pos[1] += forward[1] * speed * delta_time
            camera_pos[2] += forward[2] * speed * delta_time
        if glfw.KEY_S in keys_pressed:
            camera_pos[0] -= forward[0] * speed * delta_time
            camera_pos[1] -= forward[1] * speed * delta_time
            camera_pos[2] -= forward[2] * speed * delta_time
        if glfw.KEY_A in keys_pressed:
            camera_pos[0] -= right[0] * speed * delta_time
            camera_pos[2] -= right[2] * speed * delta_time
        if glfw.KEY_D in keys_pressed:
            camera_pos[0] += right[0] * speed * delta_time
            camera_pos[2] += right[2] * speed * delta_time
        if glfw.KEY_Q in keys_pressed:
            camera_pos[1] += speed * delta_time
        if glfw.KEY_E in keys_pressed:
            camera_pos[1] -= speed * delta_time


def update_time_scale():
    global solar_system

    if glfw.KEY_Z in keys_pressed:
        new_scale = max(1.0, solar_system.time_scale - 1.0)
        if new_scale != solar_system.time_scale:
            solar_system.time_scale = new_scale
            print(f"Skala czasu: {solar_system.time_scale} dni/sek")
            keys_pressed.remove(glfw.KEY_Z)

    if glfw.KEY_X in keys_pressed:
        new_scale = solar_system.time_scale + 1.0
        if new_scale != solar_system.time_scale:
            solar_system.time_scale = new_scale
            print(f"Skala czasu: {solar_system.time_scale} dni/sek")
            keys_pressed.remove(glfw.KEY_X)


def main():
    global solar_system

    if not glfw.init():
        print("Nie udało się zainicjalizować GLFW.")
        return

    window = glfw.create_window(1280, 720, "Układ Słoneczny", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key)
    glfw.set_cursor_pos_callback(window, on_mouse_move)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, 1280.0 / 720.0, 0.1, 2000.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    solar_system = SolarSystem()
    init_lighting()

    # Inicjalizacja czasu
    last_time = glfw.get_time()

    # Instrukcja sterowania
    print("=== Sterowanie ===")
    print("Free-fly kamera:")
    print("  W/S - ruch do przodu/tyłu")
    print("  A/D - ruch w lewo/prawo (strafe)")
    print("  Q/E - ruch w górę/dół")
    print("  Mysz - obrót kamery (yaw/pitch)")
    print("  Shift - przyspieszenie ruchu")
    print("\nKamery na obiektach:")
    print("  1 - Kamera na Słońcu")
    print("  2 - Kamera na Merkurym")
    print("  3 - Kamera na Wenus")
    print("  4 - Kamera na Ziemi")
    print("  5 - Kamera na Marsie")
    print("  6 - Kamera na Jowiszu")
    print("  7 - Kamera na Saturnie")
    print("  8 - Kamera na Uranie")
    print("  0 - Powrót do free-fly kamery")
    print("\nSkala czasu:")
    print("  Z - zmniejsz skalę czasu (spowolnij symulację)")
    print("  X - zwiększ skalę czasu (przyspiesz symulację)")
    print("ESC - wyjście")

    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        delta_time = current_time - last_time
        last_time = current_time

        glfw.poll_events()
        update_camera_controls(delta_time)
        update_time_scale()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        set_camera_view()
        solar_system.update(delta_time)
        solar_system.draw()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
