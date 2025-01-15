import math
import random

class EggRenderer:
    """
    Klasa odpowiedzialna za generowanie modelu jajka.
    Metoda generate_egg_triangles() tworzy listę trójkątów,
    gdzie każdy trójkąt składa się z wierzchołków z pozycją 'vertex' oraz kolorem 'color'.
    """

    def generate_egg_triangles(self, num_points=30):
        """
        Generuje model jajka jako siatkę trójkątów.
        Zwraca listę trójkątów, gdzie każdy trójkąt to lista słowników z kluczami 'vertex' i 'color'.

        :param num_points: liczba podziałów w pionie i poziomie
        :return: lista trójkątów [[{'vertex': (x, y, z), 'color': (r, g, b)}, ...], ...]
        """
        vertices = []
        triangles = []
        s = 5.0  # skala jajka

        # Generowanie wierzchołków
        for i in range(num_points + 1):
            lat = math.pi * (-0.5 + float(i) / num_points)
            y = s * 0.7 * math.sin(lat)
            zr = s * 0.5 * math.cos(lat)

            row = []
            for j in range(num_points + 1):
                lng = 2.0 * math.pi * float(j) / num_points
                x = zr * math.cos(lng)
                z = zr * math.sin(lng)
                color = (random.random(), random.random(), random.random())
                row.append({'vertex': (x, y, z), 'color': color})
            vertices.append(row)

        # Generowanie trójkątów
        for i in range(num_points):
            for j in range(num_points):
                p1 = vertices[i][j]
                p2 = vertices[i + 1][j]
                p3 = vertices[i + 1][j + 1]
                p4 = vertices[i][j + 1]

                # Dodajemy dwa trójkąty tworzące czworokąt
                triangles.append([p1, p2, p3])
                triangles.append([p1, p3, p4])

        return triangles
