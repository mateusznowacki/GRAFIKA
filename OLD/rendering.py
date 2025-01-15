def generate_egg():
    global triangles
    v_loops = 15  # Liczba wierzchołków w obwodzie jajka
    h_loops = 15  # Liczba obwodów
    s = 5  # Skala jajka

    for i in range(v_loops):
        lat0 = math.pi * (-0.5 + float(i) / v_loops)
        y0 = s * 0.7 * math.sin(lat0)
        zr0 = s * 0.5 * math.cos(lat0)

        lat1 = math.pi * (-0.5 + float(i + 1) / v_loops)
        y1 = s * 0.7 * math.sin(lat1)
        zr1 = s * 0.5 * math.cos(lat1)

        for j in range(h_loops):
            lng0 = 2 * math.pi * float(j) / h_loops
            lng1 = 2 * math.pi * float(j + 1) / h_loops

            x0, z0 = math.cos(lng0), math.sin(lng0)
            x1, z1 = math.cos(lng1), math.sin(lng1)

            v1 = (x0 * zr0, y0, z0 * zr0)
            v2 = (x1 * zr0, y0, z1 * zr0)
            v3 = (x1 * zr1, y1, z1 * zr1)
            v4 = (x0 * zr1, y1, z0 * zr1)

            color = (random.random(), random.random(), random.random())
            model.append({'vertices': [v1, v2, v3], 'color': color})
            color = (random.random(), random.random(), random.random())
            model.append({'vertices': [v1, v3, v4], 'color': color})


def render_model():
    if not model:
        return

    glPointSize(2.0)
    glBegin(draw_mode)

    if draw_mode == GL_POINTS or draw_mode == GL_LINES:
        glColor3f(0.0, 0.65, 0.0)
        for triangle in model:
            glVertex3fv(triangle['vertices'][0])
            glVertex3fv(triangle['vertices'][1])
            glVertex3fv(triangle['vertices'][1])
            glVertex3fv(triangle['vertices'][2])
            glVertex3fv(triangle['vertices'][2])
            glVertex3fv(triangle['vertices'][0])
    else:
        for triangle in model:
            glColor3fv(triangle['color'])

            glTexCoord2f(0.0, 0.0)
            glVertex3fv(triangle['vertices'][0])
            glTexCoord2f(1.0, 0.0)
            glVertex3fv(triangle['vertices'][1])
            glTexCoord2f(0.5, 1.0)
            glVertex3fv(triangle['vertices'][2])

            # for vertex in triangle['vertices']:
            #   glVertex3fv(vertex)
    glEnd()


def render(time):
    global rotation_x, rotation_y, zoom
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -15.0)
    glScalef(zoom, zoom, zoom)
    glRotatef(rotation_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_y, 0.0, 1.0, 0.0)

    setup_lights()
    axes()
    render_model_gouraud()
    glFlush()


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def phong_shading(vertex, normal, light_pos, light_color):
    light_dir = numpy.subtract(light_pos, vertex)
    light_dir = light_dir / numpy.linalg.norm(light_dir)

    ambient = numpy.multiply(light_color, LIGHT_AMBIENT)

    diffuse = numpy.multiply(light_color, max(0.0, numpy.dot(normal, light_dir)) * LIGHT_DIFFUSE)

    view_dir = numpy.array([0.0, 0.0, 1.0])
    reflect_dir = 2 * numpy.dot(normal, light_dir) * normal - light_dir
    reflect_dir = reflect_dir / numpy.linalg.norm(reflect_dir)
    specular = numpy.multiply(light_color, LIGHT_SPECULAR * max(0.0, numpy.dot(view_dir, reflect_dir)) ** 32)

    return numpy.add(numpy.add(ambient, diffuse), specular)


def calculate_normals():
    global model
    for triangle in model:
        v1, v2, v3 = triangle['vertices']
        u = numpy.subtract(v2, v1)
        v = numpy.subtract(v3, v1)
        normal = numpy.cross(u, v)
        normal = normal / numpy.linalg.norm(normal)

        triangle['normals'] = [normal, normal, normal]


def render_model_gouraud():
    if not model:
        return

    glBegin(GL_TRIANGLES)

    n = 2
    for triangle in model:
        vertices = triangle['vertices']
        normals = triangle['normals']

        # Pozycje świateł
        light_1_pos = calculate_light_position(light1_coords[0], light1_coords[1], light1_coords[2])
        light_2_pos = calculate_light_position(light2_coords[0], light2_coords[1], light2_coords[2])

        for i in range(3):
            normal = normals[i]
            vertex = vertices[i]

            # Obliczenie kolor na podstawie obu świateł
            color_1 = phong_shading(vertex, normal, light_1_pos, LIGHT_1_COLOR)
            color_2 = phong_shading(vertex, normal, light_2_pos, LIGHT_2_COLOR)
            final_color = numpy.clip(numpy.add(color_1, color_2), 0.0, 1.0)

            if n % 2 == 1:
                if i == 0:
                    glTexCoord2f(0.0, 0.0)
                elif i == 1:
                    glTexCoord2f(1.0, 0.0)
                elif i == 2:
                    glTexCoord2f(0.0, 1.0)
            else:
                if i == 0:
                    glTexCoord2f(0.0, 0.0)
                elif i == 1:
                    glTexCoord2f(1.0, 1.0)
                elif i == 2:
                    glTexCoord2f(1.0, 1.0)

            glColor3fv(final_color)
            glVertex3fv(vertex)
            n = n + 1
    glEnd()
