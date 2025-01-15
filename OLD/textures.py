def load_texture():
    """Ładuje losową teksturę z podanego folderu."""
    try:
        texture_files = [f for f in os.listdir(folder_path) if f.endswith('.tga')]
        if not texture_files:
            raise FileNotFoundError("Brak plików tekstur w folderze.")

        random_texture = random.choice(texture_files)  # Wybór losowej tekstury
        texture_path = os.path.join(folder_path, random_texture)
        print(f"Wczytywanie tekstury: {texture_path}")

        # Wczytywanie pliku tekstury
        image = Image.open(texture_path).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = numpy.array(image, dtype=numpy.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Parametry tekstury
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        return texture_id
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(-1)
