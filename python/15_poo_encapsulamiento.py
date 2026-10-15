class Guerrero:
    nombre: str
    _poder: int

    def __init__(self, nombre: str, poder: int):
        self.nombre = nombre
        self._poder = poder

    def get_poder(self):
        return self._poder

vegeta=Guerrero("vegeta", 8000)
print("Guerrero: ", vegeta.nombre)
print("Poder: ", vegeta.get_poder())

class CuentaZeni:
    titular: str
    __saldo: int
    def __init__(self, titular: str, saldo: int):
        self.titular = titular
        self.__saldo = saldo

    def get_saldo(self):
        return self.__saldo

    def retirar_dinero(self, cantidad: int):
        if cantidad >0 and cantidad <= self.__saldo:
            self.__saldo -= cantidad
            print("Retiro realizado ", cantidad)
        else:
            print("Retiro no permitido")

cuenta = CuentaZeni("Mr. Satàn", 5000)
print("Titular: ", cuenta.titular)
print("Saldo inicial", cuenta.get_saldo())
cuenta.retirar_dinero(500)
print("saldo final", cuenta.get_saldo())