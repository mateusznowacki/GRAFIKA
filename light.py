import math
from OpenGL.GL import *
from OpenGL.GLU import *

# Configuration for lights
lights = {
    "1": {"id": GL_LIGHT0, "position": [0.0, 0.0, 5.0, 1.0], "ambient": [0.2, 0.2, 0.0, 1.0],
          "diffuse": [1.0, 1.0, 0.0, 1.0], "specular": [1.0, 1.0, 0.0, 1.0], "active": False},
    "2": {"id": GL_LIGHT1, "position": [5.0, 0.0, 0.0, 1.0], "ambient": [0.0, 0.0, 0.2, 1.0],
          "diffuse": [0.0, 0.0, 1.0, 1.0], "specular": [0.0, 0.0, 1.0, 1.0], "active": False},
}

def setup_material():
    """Ustawienia materiału."""
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)

light_angles = {
    "1": {"azimuth": 0.0, "elevation": 0.0, "radius": 5.0},
    "2": {"azimuth": 90.0, "elevation": 0.0, "radius": 5.0},
}

def setup_lights():
    """Initial configuration for OpenGL lights."""
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)  # Two-sided lighting
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0])  # Global ambient light

    for key, light in lights.items():
        glEnable(light["id"])
        glLightfv(light["id"], GL_AMBIENT, light["ambient"])
        glLightfv(light["id"], GL_DIFFUSE, light["diffuse"])
        glLightfv(light["id"], GL_SPECULAR, light["specular"])
        glLightfv(light["id"], GL_POSITION, light["position"])
        if not light["active"]:
            glDisable(light["id"])

def toggle_light(light_key):
    """Toggle a light on/off."""
    if light_key in lights:
        light = lights[light_key]
        light["active"] = not light["active"]
        if light["active"]:
            glEnable(light["id"])
            print(f"Light {light_key} enabled.")
        else:
            glDisable(light["id"])
            print(f"Light {light_key} disabled.")

def move_light_spherical(light_key, direction):
    """Move a light in spherical coordinates."""
    if light_key in light_angles:
        angles = light_angles[light_key]
        step = 10.0

        if direction == "up":
            angles["elevation"] = min(angles["elevation"] + step, 90.0)
        elif direction == "down":
            angles["elevation"] = max(angles["elevation"] - step, -90.0)
        elif direction == "left":
            angles["azimuth"] -= step
        elif direction == "right":
            angles["azimuth"] += step

        # Convert spherical to Cartesian
        azimuth_rad = math.radians(angles["azimuth"])
        elevation_rad = math.radians(angles["elevation"])
        radius = angles["radius"]

        x = radius * math.cos(elevation_rad) * math.cos(azimuth_rad)
        y = radius * math.sin(elevation_rad)
        z = radius * math.cos(elevation_rad) * math.sin(azimuth_rad)

        lights[light_key]["position"] = [x, y, z, 1.0]
        glLightfv(lights[light_key]["id"], GL_POSITION, lights[light_key]["position"])

def draw_light_position():
    """Visualize the positions of active lights."""
    glDisable(GL_LIGHTING)
    for key, light in lights.items():
        if light["active"]:
            glPushMatrix()
            glTranslatef(*light["position"][:3])
            color = light["diffuse"][:3]
            glColor3fv(color)
            #glutSolidSphere(0.2, 16, 16)
            glPopMatrix()
    glEnable(GL_LIGHTING)

def apply_lights():
    """Ensure all active lights are applied."""
    for key, light in lights.items():
        if light["active"]:
            glEnable(light["id"])
            glLightfv(light["id"], GL_POSITION, light["position"])
        else:
            glDisable(light["id"])
