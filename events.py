import math
from OpenGL.GL import *
from OpenGL.GLU import *
from glfw.GLFW import *


class MouseEventHandler:
    def __init__(self):
        self.last_x = 0.0
        self.last_y = 0.0
        self.first_mouse = True
        self.scroll_offset = -20.0
        self.pitch = 0.0  # Rotation along X-axis
        self.yaw = 0.0    # Rotation along Y-axis
        self.mouse_button_pressed = False
        self.current_object = "egg"
        self.shading_mode = "Gouraud"

        # Parametry światła żółtego
        self.red_light_theta = 0.0
        self.red_light_phi = math.pi / 4
        self.red_light_radius = 10.0

        # Parametry światła niebieskiego
        self.blue_light_theta = math.pi / 2
        self.blue_light_phi = math.pi / 3
        self.blue_light_radius = 15.0

    def mouse_callback(self, window, xpos, ypos):
        """Callback do obsługi ruchu myszy (kamera)."""
        if not self.mouse_button_pressed:
            return

        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False
            return

        # Oblicz przesunięcia
        x_offset = xpos - self.last_x
        y_offset = ypos - self.last_y
        self.last_x = xpos
        self.last_y = ypos

        sensitivity = 0.3
        x_offset *= sensitivity
        y_offset *= sensitivity

        self.yaw += x_offset
        self.pitch -= y_offset

        # Ograniczanie obrotu w osi X (pitch)
        self.pitch = max(-89.0, min(89.0, self.pitch))

    def mouse_button_callback(self, window, button, action, mods):
        """Callback do obsługi przycisków myszy."""
        if button == GLFW_MOUSE_BUTTON_LEFT:
            if action == GLFW_PRESS:
                self.mouse_button_pressed = True
                self.first_mouse = True
            elif action == GLFW_RELEASE:
                self.mouse_button_pressed = False

    def scroll_callback(self, window, xoffset, yoffset):
        """Callback do obsługi scrolla (zoom kamery)."""
        self.scroll_offset += yoffset
        self.scroll_offset = max(-50.0, min(50.0, self.scroll_offset))  # Ograniczenie zoomu

    def keyboard_key_callback(self, window, key, scancode, action, mods):
        """Callback do obsługi klawiatury (sterowanie światłami żółtym i niebieskim)."""
        angle_step = 0.3  # Krok zmiany kąta
        radius_step = 0.4  # Krok zmiany promienia

        if action == GLFW_PRESS or action == GLFW_REPEAT:
            # Sterowanie światłem żółtym (WASD + Z/X)
            if key == GLFW_KEY_W:
                self.red_light_phi = max(0.0, self.red_light_phi - angle_step)
            elif key == GLFW_KEY_S:
                self.red_light_phi = min(math.pi, self.red_light_phi + angle_step)
            elif key == GLFW_KEY_D:
                self.red_light_theta -= angle_step
            elif key == GLFW_KEY_A:
                self.red_light_theta += angle_step
            elif key == GLFW_KEY_Z:
                self.red_light_radius = max(1.0, self.red_light_radius - radius_step)
            elif key == GLFW_KEY_X:
                self.red_light_radius += radius_step

            # Sterowanie światłem niebieskim (strzałki + ,/.)
            elif key == GLFW_KEY_UP:
                self.blue_light_phi = max(0.0, self.blue_light_phi - angle_step)
            elif key == GLFW_KEY_DOWN:
                self.blue_light_phi = min(math.pi, self.blue_light_phi + angle_step)
            elif key == GLFW_KEY_RIGHT:
                self.blue_light_theta -= angle_step
            elif key == GLFW_KEY_LEFT:
                self.blue_light_theta += angle_step
            elif key == GLFW_KEY_COMMA:
                self.blue_light_radius = max(1.0, self.blue_light_radius - radius_step)
            elif key == GLFW_KEY_PERIOD:
                self.blue_light_radius += radius_step

            if key == GLFW_KEY_J:
                self.current_object = "egg"
                print("Wybrano: Jajko")
            elif key == GLFW_KEY_C:
                self.current_object = "teapot"
                print("Wybrano: Czajnik")

            # Przełączanie trybu cieniowania
            elif key == GLFW_KEY_G:
                self.shading_mode = "Gouraud"
                glShadeModel(GL_SMOOTH)  # Ustawienie modelu cieniowania
                print("Wybrano cieniowanie: Gouraud")
            elif key == GLFW_KEY_P:
                self.shading_mode = "Phong"
                glShadeModel(GL_FLAT)  # Symulacja Phong shading (brak interpolacji kolorów)
                print("Wybrano cieniowanie: Phong")

            # Włączanie/wyłączanie światła żółtego
            elif key == GLFW_KEY_1:
                self.red_light_enabled = not getattr(self, "red_light_enabled", True)
                if self.red_light_enabled:
                    glEnable(GL_LIGHT0)
                    print("Światło czerwone: WŁĄCZONE")
                else:
                    glDisable(GL_LIGHT0)
                    print("Światło czerowne: WYŁĄCZONE")

            # Włączanie/wyłączanie światła niebieskiego
            elif key == GLFW_KEY_2:
                self.blue_light_enabled = not getattr(self, "blue_light_enabled", True)
                if self.blue_light_enabled:
                    glEnable(GL_LIGHT1)
                    print("Światło niebieskie: WŁĄCZONE")
                else:
                    glDisable(GL_LIGHT1)
                    print("Światło niebieskie: WYŁĄCZONE")

        # Normalizacja kątów
        self.red_light_theta %= 2 * math.pi
        self.blue_light_theta %= 2 * math.pi


    def apply_transformations(self):
        """Zastosowanie transformacji kamery."""
        # Zoom
        glTranslatef(0.0, 0.0, self.scroll_offset)

        # Rotacja
        glRotatef(self.pitch, 1.0, 0.0, 0.0)
        glRotatef(self.yaw, 0.0, 1.0, 0.0)

    def register_callbacks(self, window):
        """Rejestracja callbacków."""
        glfwSetCursorPosCallback(window, self.mouse_callback)
        glfwSetMouseButtonCallback(window, self.mouse_button_callback)
        glfwSetScrollCallback(window, self.scroll_callback)
        glfwSetKeyCallback(window, self.keyboard_key_callback)
