from OpenGL.GL import *
from glfw.GLFW import *
import math

class MouseEventHandler:
    def __init__(self):
        self.last_x = 0.0
        self.last_y = 0.0
        self.first_mouse = True
        self.scroll_offset = -20.0
        self.pitch = 0.0  # Rotation along X-axis
        self.yaw = 0.0    # Rotation along Y-axis
        self.mouse_button_pressed = False

        # Parametry światła
        self.light_theta = 0.0  # Kąt obrotu w płaszczyźnie XY
        self.light_phi = math.pi / 4  # Kąt od osi Z
        self.light_radius = 10.0  # Odległość światła

    def mouse_callback(self, window, xpos, ypos):
        """Callback to handle mouse movement for object rotation."""
        if not self.mouse_button_pressed:
            return

        # If it's the first interaction since button press, update positions without applying offsets
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False
            return

        # Calculate offsets
        x_offset = xpos - self.last_x
        y_offset = ypos - self.last_y
        self.last_x = xpos
        self.last_y = ypos

        sensitivity = 0.3
        x_offset *= sensitivity
        y_offset *= sensitivity

        self.yaw += x_offset
        self.pitch -= y_offset

        # Limit pitch to prevent extreme rotation
        self.pitch = max(-89.0, min(89.0, self.pitch))

    def mouse_button_callback(self, window, button, action, mods):
        """Callback to handle mouse button events."""
        if button == GLFW_MOUSE_BUTTON_LEFT:
            if action == GLFW_PRESS:
                self.mouse_button_pressed = True
                self.first_mouse = True  # Reset first mouse interaction after each button press
            elif action == GLFW_RELEASE:
                self.mouse_button_pressed = False

    def scroll_callback(self, window, xoffset, yoffset):
        """Callback to handle scroll events for zooming."""
        self.scroll_offset += yoffset
        self.scroll_offset = max(-50.0, min(50.0, self.scroll_offset))  # Limit zoom

    def keyboard_callback(self, window, key, scancode, action, mods):
        """Callback to handle keyboard events for light control."""
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

            # Ograniczenie wartości phi
            self.light_phi = max(0.1, min(math.pi - 0.1, self.light_phi))

    def apply_transformations(self):
        """Apply mouse-based transformations (rotation and zoom)."""
        # Apply zoom
        glTranslatef(0.0, 0.0, self.scroll_offset)

        # Apply rotation
        glRotatef(self.pitch, 1.0, 0.0, 0.0)  # Rotate around X-axis
        glRotatef(self.yaw, 0.0, 1.0, 0.0)   # Rotate around Y-axis

    def apply_light_transformations(self):
        """Apply light transformations based on keyboard input."""
        x = self.light_radius * math.sin(self.light_phi) * math.cos(self.light_theta)
        y = self.light_radius * math.cos(self.light_phi)
        z = self.light_radius * math.sin(self.light_phi) * math.sin(self.light_theta)

        glLightfv(GL_LIGHT0, GL_POSITION, [x, y, z, 1.0])  # Aktualizacja pozycji światła

    def register_callbacks(self, window):
        """Register GLFW callbacks for mouse and keyboard input."""
        glfwSetCursorPosCallback(window, self.mouse_callback)
        glfwSetMouseButtonCallback(window, self.mouse_button_callback)
        glfwSetScrollCallback(window, self.scroll_callback)
        glfwSetKeyCallback(window, self.keyboard_callback)
