##funciones sin parametros o simples
def activar_sistema():
    print("== sistema de naboo ==")
    print("sistema de control activado")

activar_sistema()

# Funciones con parametro 
def saludar_jedi(nombre):
    print(f"Que la fuerza te acompañe : {nombre}")

saludar_jedi("Qui-Gon Jim")
saludar_jedi("Obi-Wan kenobi")

def mostrar_nave(nombre, combustible):
    print(f"nave : {nombre}")
    print(f"cantidad combustible: {combustible}")

mostrar_nave("Caza N-1", 80)

# Funciones que vuelven dato o informacion
# return
def calcular_combustible(inicial, consumo):
    resultado = inicial - consumo

resultado = calcular_combustible(100,25)
print(f"Combustible : {resultado}")
