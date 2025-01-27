from planet import Planet

class SolarSystem:
    """
    Klasa zarządzająca planetami i ich orbitami.
    Zapewnia równomierne odstępy między orbitami.
    """
    def __init__(self):
        self.planets = []
        self.moons = []  # Lista księżyców powiązanych z planetami
        self.time_scale = 1.0  # 1 sekunda = 1 dzień w symulacji
        self.init_solar_system()

    def init_solar_system(self):
        """
        Tworzenie planet z równomiernymi odstępami między orbitami.
        """
        # Minimalna odległość między orbitami (skalowana)
        orbit_gap = 10.0  # stały odstęp między orbitami (w jednostkach skali)

        # Dane planet (z rzeczywistymi parametrami orbitalnymi)
        planets_data = [
            {"name": "Mercury", "radius": 0.3, "eccentricity": 0.205, "orbital_period": 88.0, "texture": "mercury.jpg"},
            {"name": "Venus", "radius": 0.5, "eccentricity": 0.0068, "orbital_period": 224.7, "texture": "venus.jpg"},
            {"name": "Earth", "radius": 0.5, "eccentricity": 0.0167, "orbital_period": 365.25, "texture": "earth.jpg"},
            {"name": "Mars", "radius": 0.4, "eccentricity": 0.0934, "orbital_period": 687.0, "texture": "mars.jpg"},
            {"name": "Jupiter", "radius": 1.2, "eccentricity": 0.0489, "orbital_period": 4333.0, "texture": "jupiter.jpg"},
            {"name": "Saturn", "radius": 1.1, "eccentricity": 0.0565, "orbital_period": 10759.0, "texture": "saturn.jpg"},
            {"name": "Uranus", "radius": 0.9, "eccentricity": 0.046, "orbital_period": 30660.0, "texture": "uranus.jpg"},
            {"name": "Neptune", "radius": 0.85, "eccentricity": 0.009, "orbital_period": 60190.0, "texture": "neptune.jpg"},
        ]

        # Dodanie Słońca
        self.planets.append(Planet(
            name="Sun",
            radius=2.0,
            texture_file="sun.jpg",
            semi_major_axis=0.0,
            eccentricity=0.0,
            orbital_period=1.0,  # Słońce nie porusza się
            axis_tilt=0.0,
            day_length=25.0,  # Obrót Słońca wokół własnej osi
            distance_scale=1.0,
            center=None  # Słońce nie orbituje wokół niczego
        ))

        # Dodanie planet z równymi odstępami między orbitami
        for i, planet in enumerate(planets_data):
            semi_major_axis = (i + 1) * orbit_gap  # równomierne rozmieszczenie orbit

            # Zapewnienie braku przecinania się orbit dla ostatnich planet
            if i >= len(planets_data) - 2:
                semi_major_axis += orbit_gap * 2  # Zwiększenie odległości ostatnich dwóch planet

            new_planet = Planet(
                name=planet["name"],
                radius=planet["radius"],
                texture_file=planet["texture"],
                semi_major_axis=semi_major_axis,
                eccentricity=planet["eccentricity"],
                orbital_period=planet["orbital_period"],
                axis_tilt=0.0,
                day_length=1.0,
                distance_scale=1.0,  # brak dodatkowego skalowania
                center=self.planets[0]  # Wszystkie planety orbitują wokół Słońca
            )
            self.planets.append(new_planet)

            # Dodanie księżyca dla Ziemi
            if planet["name"] == "Earth":
                moon = Planet(
                    name="Moon",
                    radius=0.1,
                    texture_file="moon.jpg",
                    semi_major_axis=1.0,  # Odległość od Ziemi (przybliżona w jednostkach skali)
                    eccentricity=0.0549,
                    orbital_period=27.3,  # Orbitalny okres księżyca w dniach
                    axis_tilt=0.0,
                    day_length=27.3,  # Doba księżyca
                    distance_scale=1.0,  # Skala odległości dla księżyca
                    center=new_planet  # Księżyc orbituje wokół Ziemi
                )
                self.moons.append((new_planet, moon))

    def update(self, real_delta_time):
        """
        Aktualizuje pozycje planet w zależności od czasu rzeczywistego (sekundy).
        """
        delta_days = real_delta_time * self.time_scale
        for planet in self.planets:
            planet.update(delta_days)
        for earth, moon in self.moons:
            moon.update(delta_days)

    def draw(self):
        """
        Rysuje wszystkie planety, ich orbity i księżyce.
        """
        for planet in self.planets:
            planet.draw()
        for earth, moon in self.moons:
            moon.draw()
