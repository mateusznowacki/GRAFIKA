#!/usr/bin/env python3
import sys
from subprocess import Popen

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
    print("4. Czajnik")
    print("5. Wyjście")
    return input("Wybierz tryb: ")

def run_program(choice):
    executables = {
        "1": "jajkopunkt.py",
        "2": "jajkolinia.py",
        "3": "jajkotrojkat.py",
        "4": "czajnik.py",
    }

    if choice in executables:
        executable = executables[choice]
        try:
            # Wyświetlenie instrukcji obsługi
            show_instructions()
            # Uruchomienie programu w tym samym procesie (blokuje do zakończenia programu)
            Popen([sys.executable, executable]).wait()
        except FileNotFoundError:
            print(f"Błąd: Plik {executable} nie istnieje.")
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
