import math
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

class Planet:
    """
    Klasa reprezentująca pojedynczą planetę (lub Słońce).
    Zamiast elipsy w środku (0,0), używamy wersji z ogniskiem w (0,0),
    bo w prawdziwym układzie gwiazda znajduje się w ognisku orbity.

    Wzór (parametr E = 'anomalny' kąt orbitalny):
      x = a * (cos E - e)
      z = b * sin E
    gdzie b = a*sqrt(1-e^2).
    Ognisko elipsy jest w (0,0), a=semimajor axis, e=ekscentryczność.

    Promień planety = self.radius.
    Słońce ma radius=1.0 i włączony emission.
    """
    def __init__(
            self,
            name="Planet",
            radius=1.0,
            texture_file="earth.jpg",
            semi_major_axis=1.0,   # w AU (potem * distance_scale)
            eccentricity=0.0,
            orbital_period=365.0,  # w dniach
            axis_tilt=0.0,         # nachylenie osi
            day_length=1.0,        # doba planety (dni)
            distance_scale=8.0     # zwiększona skala, żeby planety nie wchodziły w Słońce
    ):
        self.name = name
        self.radius = radius
        self.texture_file = texture_file

        # Parametry orbity keplerowskiej z ogniskiem w (0,0):
        # x = a(cos E - e), z = b sin E, b = a * sqrt(1-e^2)
        self.a = semi_major_axis * distance_scale
        self.e = eccentricity
        self.b = self.a * math.sqrt(1.0 - self.e**2)
        self.orbital_period = orbital_period

        self.axis_tilt = axis_tilt
        self.day_length = day_length

        # Czas planety (w dniach) w symulacji
        self.planet_time = 0.0

        # Pozycja w płaszczyźnie XZ
        self.pos_x = 0.0
        self.pos_z = 0.0

        # Rotacja wokół osi
        self.rotation_angle = 0.0

        # Tekstura
        self.texture_id = None
        self.load_texture()

    def load_texture(self):
        """Wczytanie tekstury z pliku 'textures/...'. """
        try:
            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            image_path = f"textures/{self.texture_file}"
            image = Image.open(image_path)
            image_data = image.convert("RGB").tobytes()
            width, height = image.size

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGB,
                width,
                height,
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                image_data
            )

            glBindTexture(GL_TEXTURE_2D, 0)
        except Exception as e:
            print(f"[Planet {self.name}] Błąd wczytywania tekstury '{self.texture_file}': {e}")
            self.texture_id = None

    def update(self, delta_days):
        """
        Aktualizuje pozycję planety o delta_days dni.
        Kąt E(t) = 2π * (planet_time / orbital_period).
        x = a(cosE - e), z = b sinE
        Rotacja wokół osi -> rotation_angle
        """
        self.planet_time += delta_days

        # Kąt orbitalny (w radianach)
        E = 2.0 * math.pi * (self.planet_time / self.orbital_period)

        # Elipsa z ogniskiem w (0,0)
        self.pos_x = self.a * (math.cos(E) - self.e)
        self.pos_z = self.b * math.sin(E)

        # Rotacja planety (1 obrót = day_length dni)
        if self.day_length != 0.0:
            self.rotation_angle = 360.0 * (self.planet_time / self.day_length)
        else:
            self.rotation_angle = 0.0
        self.rotation_angle %= 360.0

    def draw_orbit(self):
        """
        Rysuje elipsę (orbitę) w płaszczyźnie XZ, taką, że ognisko jest w (0,0).
        x(E) = a(cosE - e), z(E) = b sinE
        """
        if self.a <= 0.0:
            return  # jeśli Słońce (a=0), brak orbity

        glDisable(GL_LIGHTING)
        glColor3f(0.0, 1.0, 0.0)  # zielony
        glBegin(GL_LINE_LOOP)
        segments = 180
        for i in range(segments):
            E = 2.0 * math.pi * (i / segments)
            x = self.a * (math.cos(E) - self.e)
            z = self.b * math.sin(E)
            glVertex3f(x, 0.0, z)
        glEnd()
        glEnable(GL_LIGHTING)

        # Przywróć biały kolor
        glColor3f(1.0, 1.0, 1.0)

    def draw(self):
        """Rysuje orbitę i potem kulę planety (lub Słońce) w jej położeniu."""
        self.draw_orbit()

        glPushMatrix()

        # Przesunięcie na aktualną pozycję
        glTranslatef(self.pos_x, 0.0, self.pos_z)

        # Oś nachylenia
        glRotatef(self.axis_tilt, 0.0, 0.0, 1.0)
        # Rotacja wokół własnej osi
        glRotatef(self.rotation_angle, 0.0, 1.0, 0.0)

        # Słońce ma emission
        if self.name.lower() == "sun":
            glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 1.0, 0.6, 1.0])
        else:
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

        # Teksturowanie
        if self.texture_id is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        else:
            glDisable(GL_TEXTURE_2D)

        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluSphere(quadric, self.radius, 32, 32)
        gluDeleteQuadric(quadric)

        if self.texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()
