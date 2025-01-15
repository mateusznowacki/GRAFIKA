
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
