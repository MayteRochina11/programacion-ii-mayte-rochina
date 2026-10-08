# Operadores 
"""
Operadores aritméticos: 
+ Suma
- Resta
* Multiplicación
/ División
% Módulo (resto de la división)
- ** (Potenciación)
"""
valor1 = 10
valor2 = 3
suma = valor1 + valor2
resta = valor1 - valor2
multiplicacion = valor1 * valor2
division = valor1 / valor2
modulo = valor1 % valor2
potencia = valor1 ** valor2
print("Suma:", suma)
print("Resta:", resta)
print("Multiplicación:", multiplicacion)
print("División:", division)
print("Módulo:", modulo)
print("Potencia:", potencia)


print("Tabla de multiplicar del 5:")
multiplicador = 5
print("5 x 1 =", 5 * 1)
print("5 x 2 =", 5 * 2)
print("5 x 3 =", 5 * 3)
print("5 x 4 =", 5 * 4)
print("5 x 5 =", 5 * 5)
print("5 x 6 =", 5 * 6)
print("5 x 7 =", 5 * 7)
print("5 x 8 =", 5 * 8)
print("5 x 9 =", 5 * 9)
print("5 x 10 =", 5 * 10)

print("Area de un triangulo con base 5 y altura 10:", (5 * 10) / 2) 

#Operadores de comparacion
"""
- == Igual a
- != Diferente de
- > Mayor que
- < Menor que
- >= Mayor o igual que
- <= Menor o igual que
"""

velocidad_anakin = 950
velocidad_sebula = 900

print("¿Anakin es más rápido que Sebula?", velocidad_anakin > velocidad_sebula)
print("¿Anakin es igual de rápido que Sebula?", velocidad_anakin == velocidad_sebula)
print("¿Anakin es más lento que Sebula?", velocidad_anakin < velocidad_sebula)
print("¿Anakin es igual o más lento que Sebula?", velocidad_anakin <= velocidad_sebula)
print("¿Anakin es igual o más rápido que Sebula?", velocidad_anakin >= velocidad_sebula)
print("¿Anakin es diferente de Sebula?", velocidad_anakin != velocidad_sebula)

resultado = velocidad_anakin > velocidad_sebula
print("Resultado de la comparación:", resultado)
print("Tipo de resultado:", type(resultado))

# Operadores logicos
"""
- and (y)
- or (o)
- not (no)
"""
motor_encendido = True
escudo_activado = False
combustible = 80
print("¿Todos los sistemas estan funcionando", motor_encendido and escudo_activado) 
print("¿Al menos un sistema esta funcionando?", motor_encendido or escudo_activado)
print("¿El motor no esta encendido?", not motor_encendido)

cantidad_motores = 2
cantidad_alas = 4
combustible = 80
print("¿La nave tiene al menos 2 motores y 4 alas?", cantidad_motores >= 2 and cantidad_alas >= 4)
print("¿La nave tiene al menos 2 motores o 4 alas?", cantidad_motores >= 2 or cantidad_alas >= 4)
print("¿La nave no tiene al menos 2 motores?", not cantidad_motores >= 2 and combustible >= 50)

# Preferencia de operadores
"""
1. ()
2. ** (potenciación)
3. * / % (multiplicación, división, módulo)
4. + - (suma, resta)

"""
resultado_1 = 10 + 5 *2 
print("Resultado 1:", resultado_1)
resultado_2 = (10 + 5) * 2
print("Resultado 2:", resultado_2)




