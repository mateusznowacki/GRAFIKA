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
        self.yaw = 0.0  # Rotation along Y-axis
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
        glRotatef(self.yaw, 0.0, 1.0, 0.0)  # Rotate around Y-axis

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


    def register_callbacks(self, window):
        """Register GLFW callbacks for mouse input."""
        glfwSetCursorPosCallback(window, self.mouse_callback)
        glfwSetMouseButtonCallback(window, self.mouse_button_callback)
        glfwSetScrollCallback(window, self.scroll_callback)




# def mouse_motion_callback(window, x_pos, y_pos):
#     global delta_x, delta_y, mouse_x_pos_old, mouse_y_pos_old, theta, phi
#
#     delta_x = x_pos - mouse_x_pos_old
#     delta_y = y_pos - mouse_y_pos_old
#     mouse_x_pos_old = x_pos
#     mouse_y_pos_old = y_pos
#
#     if left_mouse_button_pressed:
#         theta += delta_x * pix2angle * 0.01  # Obrót wokół osi Y
#         phi += delta_y * pix2angle * 0.01   # Obrót wokół osi X
#
#         # Ogranicz obrót phi, aby kamera nie przeszła za bieguny
#         phi = max(-math.pi / 2, min(math.pi / 2, phi))
#
#
#
# def mouse_button_callback(window, button, action, mods):
#     global left_mouse_button_pressed
#
#     if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
#         left_mouse_button_pressed = 1
#     elif button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_RELEASE:
#         left_mouse_button_pressed = 0
#
#
# def scroll_callback(window, xoffset, yoffset):
#     global viewer
#
#     # Zoom in/out
#     zoom_step = 1.0
#     if yoffset > 0:  # Scroll up
#         viewer[2] = max(1.0, viewer[2] - zoom_step)
#     elif yoffset < 0:  # Scroll down
#         viewer[2] += zoom_step