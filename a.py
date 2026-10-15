class RadarDragon:
    
    region1: int
    region2: int
    
    def __init__(self, region1: int, region2: int):
        self.region1 = region1
        self.region2 = region2
    
    def buscar_esferas(self):
        total_encontradas = self.region1 + self.region2
        total_esferas = 7
        faltantes = total_esferas - total_encontradas

        return total_encontradas, faltantes
radar_bulma = RadarDragon(3, 2)

encontradas, faltantes = radar_bulma.buscar_esferas()

print("--- Radar de Bulma ---")
print("Esferas encontradas:", encontradas)
print("Esferas faltantes para completar las 7:", faltantes)
