from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
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

    def apply_transformations(self):
        """Apply mouse-based transformations (rotation and zoom)."""
        # Apply zoom
        glTranslatef(0.0, 0.0, self.scroll_offset)

        # Apply rotation
        glRotatef(self.pitch, 1.0, 0.0, 0.0)  # Rotate around X-axis
        glRotatef(self.yaw, 0.0, 1.0, 0.0)   # Rotate around Y-axis

    def register_callbacks(self, window):
        """Register GLFW callbacks for mouse input."""
        glfwSetCursorPosCallback(window, self.mouse_callback)
        glfwSetMouseButtonCallback(window, self.mouse_button_callback)
        glfwSetScrollCallback(window, self.scroll_callback)
