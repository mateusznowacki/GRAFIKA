# W pliku filecontroller.py
from OpenGL.GL import *
import os
import numpy as np
import sys

def load_texture(filename):
    """Ładuje teksturę z pliku .tga."""
    if not os.path.exists(filename):
        print(f"Nie znaleziono pliku tekstury: {filename}")
        return None

    # Otwórz plik .tga
    try:
        with open(filename, 'rb') as file:
            # Przeskocz nagłówki pliku TGA
            header = file.read(18)
            width, height = header[12:14], header[14:16]
            width = int.from_bytes(width, byteorder='little')
            height = int.from_bytes(height, byteorder='little')

            # Wczytaj dane pikseli
            image_data = file.read(width * height * 3)  # 3 bytes na każdy piksel (RGB)

            # Generowanie tekstury OpenGL
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            # Załaduj teksturę
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

            return texture_id
    except Exception as e:
        print(f"Błąd ładowania tekstury: {e}")
        return None


# Funkcja do wczytywania pliku .obj
def load_obj(filename):
    """Wczytuje plik .obj i zwraca listę wierzchołków oraz ścian."""
    vertices = []  # Lista współrzędnych wierzchołków (x, y, z)
    faces = []  # Lista ścian (indeksy wierzchołków)
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):  # Wierzchołek - linia zaczyna się od 'v'
                    parts = line.strip().split()
                    vertices.append([
                        float(parts[1]),  # Współrzędna X
                        float(parts[2]),  # Współrzędna Y
                        float(parts[3])  # Współrzędna Z
                    ])
                elif line.startswith('f '):  # Ściana (face) - linia zaczyna się od 'f'
                    parts = line.strip().split()
                    face = [int(p.split('/')[0]) - 1 for p in parts[1:]]  # Indeksy wierzchołków (numeracja od 1)
                    faces.append(face)
    except FileNotFoundError:
        print(f"Plik {filename} nie został znaleziony.")  # Obsługa błędu braku pliku
        sys.exit(-1)  # Kończenie programu z kodem błędu -1
    return np.array(vertices), faces  # Zwracanie tablicy wierzchołków i listy ścian