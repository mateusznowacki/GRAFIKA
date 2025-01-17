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
        self.pitch = 0.0  # Rotation along X-axis (kamera)
        self.yaw = 0.0    # Rotation along Y-axis (kamera)
        self.mouse_button_pressed = False

        # Parametry światła
        self.light_theta = 0.0
        self.light_phi = math.pi / 4
        self.light_radius = 10.0

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
        """Callback do obsługi klawiatury (sterowanie światłem)."""
        angle_step = 0.2

        if action == GLFW_PRESS or action == GLFW_REPEAT:
            if key == GLFW_KEY_W:  # Obrót światła w dół
                self.light_phi += angle_step
            elif key == GLFW_KEY_S:  # Obrót światła w górę
                self.light_phi -= angle_step
            elif key == GLFW_KEY_A:  # Obrót światła w lewo
                self.light_theta -= angle_step
            elif key == GLFW_KEY_D:  # Obrót światła w prawo
                self.light_theta += angle_step


        self.light_phi %= 2 * math.pi  # Pozwala na pełny obrót (normalizacja kąta)


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
