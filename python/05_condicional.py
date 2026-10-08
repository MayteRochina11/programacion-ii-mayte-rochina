# Condicional if 
# Simple 
combustible = 10
if combustible >= 10 :
    print("Suficiente para despegar")

# Condicional if-else 
creditos = int(input("Ingrese la cantidad de creditos: "))
precio_repuesto = int(input("Ingrese el precio del repuesto: "))
if creditos >= precio_repuesto:
    print("Puedes comprar el repuesto")
else:
    print("No tienes suficientes créditos")

# if anidado
if creditos >= precio_repuesto:
    print("Puedes comprar el repuesto")
    if creditos > precio_repuesto:
        print("Te sobraran creditos")
    else:
        print("Te quedad justo con los creditos necesarios")
else: 
    print("No tienes suficientes créditos")

# Condicional if-elif-else
if creditos > precio_repuesto:
    print("Puedes comprar el repuesto y te sobraran creditos")
elif creditos == precio_repuesto:
    print("Puedes comprar el repuesto y te quedas justo con los creditos necesarios")
else:
    print("No tienes suficientes créditos")


tipo_respuesto = input("Ingrese el tipo de repuesto que desea comprar (Motor, Ala o Escudo): ")
if tipo_respuesto == "Motor" and creditos >= precio_repuesto:
    print("El repuesto es un Motor")
elif tipo_respuesto == "Ala" and creditos >= precio_repuesto:
    print("El repuesto es un Ala")
elif tipo_respuesto == "Escudo" and creditos >= precio_repuesto:
    print("El repuesto es un Escudo")
else:
    print("No tienes suficiente crédito para comprar el repuesto o el tipo de repuesto es inválido")

peso_paquete = int(input("ingrese el peso del paquete:"))
zona_destino = int(input("INGRESE EL NUMERO DEL DESTINO: "))

zona_destino = 1 or zona_destino == 2 or zona_destino == 3


zona_1_kilo = 5.0 
zona_2_kilo = 7.5
zona_3_kilo = 10.0 
if peso_paquete == zona_destino == 1:
    print("El costo del envio es de: ", peso_paquete * zona_1_kilo)
elif peso_paquete == zona_destino == 2:
    print("El costo del envio es de: ", peso_paquete * zona_2_kilo)
elif peso_paquete == zona_destino == 3:
    print("El costo del envio es de: ", peso_paquete * zona_3_kilo)
else:
    print("Zona de destino inválida o peso del paquete no permitido")
    

 