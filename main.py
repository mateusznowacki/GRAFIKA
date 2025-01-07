#!/usr/bin/env python3
import os
import sys
from ctypes import cdll
from subprocess import Popen


import jajko

# pyinstaller --onefile --add-binary "C:\Users\matty\PycharmProjects\GrafikaLab\.venv\Lib\site-packages\glfw\glfw3.dll;glfw" main.py

def get_script_path(script_name):
    # Pobierz katalog główny EXE
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, script_name)

# Funkcja wyświetlająca instrukcję obsługi
def show_instructions():
    instructions = """
    === Instrukcja obsługi ===
    Program otwiera okno graficzne o określonych rozmiarach i pozwala na wizualizację obiektów 3D.
    Podstawowe sterowanie klawiaturą:
    • Strzałka w górę (↑) — Obraca obiekt wokół osi X w kierunku "góry".
    • Strzałka w dół (↓) — Obraca obiekt wokół osi X w kierunku "dołu".
    • Strzałka w lewo (←) — Obraca obiekt wokół osi Y w lewo.
    • Strzałka w prawo (→) — Obraca obiekt wokół osi Y w prawo.
    • Klawisz C — Przełącza widok z kolorowego na czarno-biały i odwrotnie.
    • Klawisz V — Żeby zmienić liczbe wierzchołkow nalezy kliknąć w okno i wybrać kalisz V następnie wpisać liczbę wierzchołków.
    • Żeby wybrać inne okno najpierw należy zamknąć aktualnie uruchomione.
    """
    print(instructions)




def main():
    jajko.run()

if __name__ == "__main__":
    main()
