import pandas as pd

def limpiar_simulacion(data_frame_sucio):
    
    data_frame_limpio=data_frame_sucio.copy()
    
    #rutina para evaluar textos
    #seleccionar todas las columnas de tipo texto y eliminar sus espacios y convertir a minusculas
    columnas_texto=["nombre"]
    for columna in columnas_texto:
        data_frame_limpio[columna]=data_frame_limpio[columna].astype("string").str.strip().str.lower()
    
    #rutina para evaluar numeros
    #evaluar que las columnas numericas si son numeros  
    data_frame_limpio["id"]=pd.to_numeric(data_frame_limpio["id"])
    data_frame_limpio["precio"]=pd.to_numeric(data_frame_limpio["precio"])
    data_frame_limpio["cantidad"]=pd.to_numeric(data_frame_limpio["cantidad"])
    
    #CRITERIO DE VALIDACION 2: El precio debe ser mayor a 0
    data_frame_limpio=data_frame_limpio[data_frame_limpio["precio"]>0]
    
    #CRITERIO DE VALIDACION 3: La cantidad debe ser mayor o igual a 0
    data_frame_limpio=data_frame_limpio[data_frame_limpio["cantidad"]>=0]
    
    #CRITERIO DE VALIDACION 1: El nombre es obligatorio
    #rutina para evaluar campos obligatorios que vienen vacios
    columnas_obligatorias=["id","nombre","precio","cantidad"]
    data_frame_limpio=data_frame_limpio.dropna(subset=columnas_obligatorias)
    
    data_frame_limpio=data_frame_limpio.drop_duplicates()
    
    
    return data_frame_limpio
    
    
    