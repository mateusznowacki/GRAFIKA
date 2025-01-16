import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from light import apply_lights, setup_material, toggle_light, move_light_spherical
from jajko import generate_egg_points, render_egg, compute_vertex_normals
from czajnik import render_teapot, load_obj

viewer = [0.0, 0.0, 10.0]
current_object = "egg"
egg_points = None
egg_normals = None
teapot_points = None
teapot_faces = None


def startup():
    global egg_points, egg_normals, teapot_points, teapot_faces

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    setup_material()

    glEnable(GL_LIGHTING)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])

    egg_points = generate_egg_points(50)
    egg_normals = compute_vertex_normals(egg_points)

    teapot_file = "teapot.obj"
    teapot_points, teapot_faces = load_obj(teapot_file)


def render(time):
    global current_object

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(*viewer, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    apply_lights()

    if current_object == "egg":
        render_egg(egg_points, egg_normals)
    elif current_object == "teapot":
        render_teapot(teapot_points, teapot_faces)

    glFlush()


def keyboard_key_callback(window, key, scancode, action, mods):
    global current_object

    if action == GLFW_PRESS:
        if key == GLFW_KEY_J:
            current_object = "egg"
        elif key == GLFW_KEY_C:
            current_object = "teapot"
        elif key == GLFW_KEY_1:
            toggle_light("1")
        elif key == GLFW_KEY_2:
            toggle_light("2")
        elif key in [GLFW_KEY_W, GLFW_KEY_S, GLFW_KEY_A, GLFW_KEY_D]:
            move_light_spherical("1", {GLFW_KEY_W: "up", GLFW_KEY_S: "down", GLFW_KEY_A: "left", GLFW_KEY_D: "right"}[key])
        elif key in [GLFW_KEY_UP, GLFW_KEY_DOWN, GLFW_KEY_LEFT, GLFW_KEY_RIGHT]:
            move_light_spherical("2", {GLFW_KEY_UP: "up", GLFW_KEY_DOWN: "down", GLFW_KEY_LEFT: "left", GLFW_KEY_RIGHT: "right"}[key])
        elif key == GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, GLFW_TRUE)


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, "Egg and Teapot with Lighting", None, None)
    glfwMakeContextCurrent(window)
    glfwSetKeyCallback(window, keyboard_key_callback)

    startup()

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == "__main__":
    main()
