droides = [
    {
        "codigo": "B1-001",
        "modelo": "B1",
        "energia": 90,
        "activo": True
    },
    {
        "codigo": "B1-002",
        "modelo": "B1",
        "energia": 40,
        "activo": True
    },
    {
        "codigo": "DRO-003",
        "modelo": "Droikeda",
        "energia": 80,
        "activo": True    
    }
]
cantidad_droides = len(droides)
print(cantidad_droides)
print(droides)
nuevo_droide= {
    
    "codigo": "B1-004",
    "modelo": "B1",
    "energia": 100,
    "activo": True    
}
#crud
#create 
droides.append(nuevo_droide)
print(len(droides))
print(droides)
# read
droide=droides[0]
print(f"codigo : {droide["codigo"]}")
print(f"modelo : {droide["modelo"]}")
print(f"energia : {droide["energia"]}")
print(f"activo : {droide["activo"]}")
#update
droide=droides[2]
droide["codigo"]="DRO-002"
droide["energia"]=85
droide["activo"]=False
print(f"droides : {droides}")

# delete
eliminado = droide.pop(2)
print(f"droides : {droides}")

