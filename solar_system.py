from planet import Planet

class SolarSystem:
    """
    Klasa zarządzająca planetami i ich orbitami.
    Zapewnia odpowiednie odstępy między orbitami planet.
    """
    def __init__(self):
        self.planets = []
        self.time_scale = 1.0  # 1 sekunda = 1 dzień w symulacji
        self.init_solar_system()

    def init_solar_system(self):
        """
        Tworzenie planet z poprawionymi odstępami między orbitami.
        """
        # Skale odległości
        distance_scale_near = 50.0   # Skala dla bliższych planet
        distance_scale_far = 50.0    # Skala bazowa dla dalszych planet
        far_scale = 0.3              # Współczynnik zmniejszenia odległości dalszych planet
        orbit_gap = 10.0             # Minimalny odstęp między orbitami (dla bliższych planet)

        # Dane planet (w AU i dniach)
        planets_data = [
            # Bliższe planety
            {"name": "Mercury", "radius": 0.3, "semi_major_axis": 0.39, "eccentricity": 0.205, "orbital_period": 88.0, "texture": "mercury.jpg", "scale": distance_scale_near},
            {"name": "Venus", "radius": 0.5, "semi_major_axis": 0.72 + orbit_gap / distance_scale_near, "eccentricity": 0.0068, "orbital_period": 224.7, "texture": "venus.jpg", "scale": distance_scale_near},
            {"name": "Earth", "radius": 0.5, "semi_major_axis": 1.0 + 2 * orbit_gap / distance_scale_near, "eccentricity": 0.0167, "orbital_period": 365.25, "texture": "earth.jpg", "scale": distance_scale_near},
            {"name": "Mars", "radius": 0.4, "semi_major_axis": 1.52 + 3 * orbit_gap / distance_scale_near, "eccentricity": 0.0934, "orbital_period": 687.0, "texture": "mars.jpg", "scale": distance_scale_near},

            # Dalsze planety
            {"name": "Jupiter", "radius": 1.2, "semi_major_axis": 5.20, "eccentricity": 0.0489, "orbital_period": 4333.0, "texture": "jupiter.jpg", "scale": distance_scale_far * far_scale},
            {"name": "Saturn", "radius": 1.1, "semi_major_axis": 9.58, "eccentricity": 0.0565, "orbital_period": 10759.0, "texture": "saturn.jpg", "scale": distance_scale_far * far_scale},
            {"name": "Uranus", "radius": 0.9, "semi_major_axis": 19.2, "eccentricity": 0.046, "orbital_period": 30660.0, "texture": "uranus.jpg", "scale": distance_scale_far * far_scale},
            {"name": "Neptune", "radius": 0.85, "semi_major_axis": 30.05, "eccentricity": 0.009, "orbital_period": 60190.0, "texture": "neptune.jpg", "scale": distance_scale_far * far_scale},
            {"name": "Pluto", "radius": 0.25, "semi_major_axis": 39.48, "eccentricity": 0.2488, "orbital_period": 90560.0, "texture": "pluto.jpg", "scale": distance_scale_far * far_scale}
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
            distance_scale=1.0
        ))

        # Dodanie planet
        for planet in planets_data:
            self.planets.append(Planet(
                name=planet["name"],
                radius=planet["radius"],
                texture_file=planet["texture"],
                semi_major_axis=planet["semi_major_axis"],
                eccentricity=planet["eccentricity"],
                orbital_period=planet["orbital_period"],
                axis_tilt=0.0,
                day_length=1.0,
                distance_scale=planet["scale"]
            ))

    def update(self, real_delta_time):
        """
        Aktualizuje pozycje planet w zależności od czasu rzeczywistego (sekundy).
        """
        delta_days = real_delta_time * self.time_scale
        for planet in self.planets:
            planet.update(delta_days)

    def draw(self):
        """
        Rysuje wszystkie planety i ich orbity.
        """
        for planet in self.planets:
            planet.draw()
