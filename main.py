#!/usr/bin/env python3
import os
import sys
from ctypes import cdll
from subprocess import Popen


import jajkolinia
import jajkopunkt
import jajkotrojkat

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

def main_menu():
    print("\n=== MENU ===")
    print("1. Jajko - punkty")
    print("2. Jajko - linie")
    print("3. Jajko - trójkąty")
    print("5. Wyjście")
    return input("Wybierz tryb: ")

def run_program(choice):
    if choice == "1":
        print("Uruchamiam: Jajko - punkty")
        show_instructions()
        jajkopunkt.run()
    elif choice == "2":
        print("Uruchamiam: Jajko - linie")
        show_instructions()
        jajkolinia.run()
    elif choice == "3":
        print("Uruchamiam: Jajko - trójkąty")
        show_instructions()
        print("Klawisz S - Przełączanie trybu cieniowania (Flat/Smooth))")
        jajkotrojkat.run()
    else:
        print("Nieprawidłowy wybór.")

def main():
    while True:
        choice = main_menu()
        if choice == "5":
            print("Koniec programu.")
            break
        run_program(choice)

if __name__ == "__main__":
    main()
