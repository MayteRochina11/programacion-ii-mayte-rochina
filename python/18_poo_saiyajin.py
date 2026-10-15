from 17_poo_guerro import Guerro
class Saiyajin(Guerro):
    def __init__(self, nombre: str):
        super().__init__(nombre)

    def transformarse(self):
        print(self.nombre, "se transforma en Super Saiyajin")

goku = Saiyajin("Goku")
goku.presentarse()
goku.transformarse()