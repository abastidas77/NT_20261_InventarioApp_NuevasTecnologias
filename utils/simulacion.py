import random

def generar_simulacion(numeroSimulaciones):

    productos=["Laptop","Mouse","Teclado","Monitor","Cable USB"]
    precios=[50000,15000,80000,250000,5000]
    cantidades=[10,25,30,5,100]

    simulaciones=[]
    for _ in range(numeroSimulaciones):

        simulacion={
            "id":random.randint(1,200),
            "nombre":random.choice(productos),
            "precio":random.choice(precios),
            "cantidad":random.randint(0,100)
        }

        #Inyectando errores controlados 
        probabilidadError=random.random()
        if(probabilidadError<0.15):
            simulacion["nombre"]=None
        elif(probabilidadError<0.3):
            simulacion["nombre"]=random.choice(["articulo x","producto y"])
        elif(probabilidadError<0.45):
            simulacion["precio"]=random.choice([0,-5000,None])
        elif(probabilidadError<0.6):
            simulacion["precio"]=random.choice([-50000,-15000])
        elif(probabilidadError<0.75):
            simulacion["cantidad"]=None
        elif(probabilidadError<0.9):
            simulacion["nombre"]=" "+simulacion["nombre"].upper()

        simulaciones.append(simulacion)
    return simulaciones
