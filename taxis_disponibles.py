class LineaTaxis:
    zona_centro: int
    zona_norte: int
    total_flota:int

    def __init__(self, zona_centro: int, zona_norte: int, total_flota: int = 15):
        self.zona_centro = zona_centro
        self.zona_norte = zona_norte
        self.total_flota = total_flota

    def estado_flota(self):
        taxis_calle = self.zona_centro + self.zona_norte
        taxis_base = self.total_flota - taxis_calle
        return taxis_calle, taxis_base

despacho_manana = LineaTaxis(6, 4)
taxis_calle, taxis_base = despacho_manana.estado_flota()

print("--- Central de TAXIS FAST: Linea de Taxis ---")
print(f"Taxis operando en la calle: {taxis_calle}")
print(f"Taxis esperando en la base: {taxis_base}")
