import os
from PIL import Image
import numpy
from OpenGL.GL import *

from rendering import generate_egg


# Funkcje do obsługi tekstur

def load_texture_folder():
    """Ładuje wszystkie tekstury z folderu 'texture' i zwraca ich identyfikatory."""
    folder_path = "../texture"
    if not os.path.exists(folder_path):
        print(f"Błąd: Folder '{folder_path}' nie istnieje.")
        return {}

    textures = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".tga"):
            texture_path = os.path.join(folder_path, file_name)
            try:
                print(f"Wczytywanie tekstury: {texture_path}")
                image = Image.open(texture_path).transpose(Image.FLIP_TOP_BOTTOM)
                img_data = numpy.array(image, dtype=numpy.uint8)

                texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texture_id)

                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
                textures[file_name] = texture_id
            except Exception as e:
                print(f"Błąd podczas ładowania tekstury '{file_name}': {e}")

    return textures

# Funkcja menu

def menu():
    global draw_mode

    textures = load_texture_folder()

    print("Wybierz opcję:")
    print("Jajko:")
    print("1 - Cegła")
    print("2 - Las")
    print("3 - Piasek")
    print("Czajnik:")
    print("4 - Cegła")
    print("5 - Las")
    print("6 - Piasek")

    option = input("Wybór (1/2/3/4/5/6): ")

    draw_mode = GL_TRIANGLES  # Ustawiamy GL_TRIANGLES dla wszystkich opcji

    if option == "1":
        generate_egg()
        glBindTexture(GL_TEXTURE_2D, textures.get("cegla.tga", 0))
    elif option == "2":
        generate_egg()
        glBindTexture(GL_TEXTURE_2D, textures.get("las.tga", 0))
    elif option == "3":
        generate_egg()
        glBindTexture(GL_TEXTURE_2D, textures.get("piasek.tga", 0))
    elif option == "4":
       # load_model_from_file(get_path("czajnik.txt"))
        glBindTexture(GL_TEXTURE_2D, textures.get("cegla.tga", 0))
    elif option == "5":
        #load_model_from_file(get_path("czajnik.txt"))
        glBindTexture(GL_TEXTURE_2D, textures.get("las.tga", 0))
    elif option == "6":
        #load_model_from_file("czajnik.txt")
        glBindTexture(GL_TEXTURE_2D, textures.get("piasek.tga", 0))
    else:
        print("Niepoprawny wybór. Używam domyślnego trybu (trójkąty).")

    print("\nWyświetlono model. Proszę przejść do drugiego okna."
          "\nKlawisze '1'/'2'/'3' wybierają obiekt do sterowania (model / światło 1 / światło 2)"
          "\nModel obracany jest za pomocą klawiszy strzałek oraz 'k'/'i'."
          "\nŹródła światła: '+'/'-' : promień, strzałki góra/dół : elewacja, strzałki lewo/prawo : azymut"
          "\nPrzytrzymanie lewego przycisku myszy pozwala na obrót perspektywą."
          "\nKółko myszy służy do ustalania przybliżenia.")
