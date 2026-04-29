import random
from datetime import datetime, timedelta


def generar_movimientos_inventario(numero_registros):
    """Genera registros simulados de movimientos de inventario con errores controlados."""
    
    tipos_movimiento = ["Entrada", "Salida"]
    productos = ["Producto A", "Producto B", "Producto C", "Producto D", "Producto E"]
    
    movimientos = []
    id_actual = 2001
    fecha_base = datetime.now()
    
    for _ in range(numero_registros):
        # Generar fecha aleatoria en los últimos 30 días
        dias_atras = random.randint(0, 30)
        fecha = fecha_base - timedelta(days=dias_atras)
        
        movimiento = {
            "id_movimiento": id_actual,
            "tipo": random.choice(tipos_movimiento),
            "fecha": fecha.strftime("%Y-%m-%d"),
            "cantidad": random.randint(1, 100),
            "id_producto": random.choice(productos)
        }
        id_actual += 1
        
        # Inyección de errores controlados (30% de probabilidad)
        probabilidad_error = random.random()
        
        if probabilidad_error < 0.10:
            # ID nulo
            movimiento["id_movimiento"] = None
            
        elif probabilidad_error < 0.20:
            # Tipo inválido
            movimiento["tipo"] = random.choice([None, "", "   ", "ENTRADA", "SALIDA"])
            
        elif probabilidad_error < 0.30:
            # Fecha inválida
            movimiento["fecha"] = random.choice([None, "", "2024-13-45", "fecha-invalida"])
            
        elif probabilidad_error < 0.40:
            # Cantidad inválida
            movimiento["cantidad"] = random.choice([None, -1, 0, "abc", 999999])
            
        elif probabilidad_error < 0.50:
            # Producto inválido
            movimiento["id_producto"] = random.choice([None, "", "   ", "Producto X"])
            
        elif probabilidad_error < 0.60:
            # Duplicar ID para crear conflicto
            movimiento["id_movimiento"] = id_actual - 2
            
        elif probabilidad_error < 0.70:
            # Movimiento futuro (fecha posterior a hoy)
            fecha_futura = fecha_base + timedelta(days=random.randint(1, 10))
            movimiento["fecha"] = fecha_futura.strftime("%Y-%m-%d")
            
        elif probabilidad_error < 0.80:
            # Cantidad excesiva (posible error de digitación)
            movimiento["cantidad"] = random.randint(1000, 9999)
            
        elif probabilidad_error < 0.90:
            # Tipo en mayúsculas inconsistentes
            movimiento["tipo"] = random.choice(["entrada", "SALIDA", "Entrada", "SALIDA"])
            
        # Sin error - 10% de los casos
        movimientos.append(movimiento)
    
    return movimientos


def generar_entradas_inventario(numero_registros):
    """Genera registros de entradas de inventario."""
    
    productos = ["Producto A", "Producto B", "Producto C"]
    razones = ["Entrada de producto", "Reposición de stock", "Compra", "Devolución"]
    
    entradas = []
    id_actual = 3001
    
    for _ in range(numero_registros):
        entrada = {
            "id_entrada": id_actual,
            "producto": random.choice(productos),
            "cantidad": random.randint(10, 500),
            "razon": random.choice(razones),
            "fecha": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
            "validado": random.choice([True, False, None])
        }
        id_actual += 1
        
        # Errores controlados
        if random.random() < 0.15:
            entrada["cantidad"] = random.choice([None, -1, 0])
        if random.random() < 0.10:
            entrada["validado"] = None
            
        entradas.append(entrada)
    
    return entradas


def generar_salidas_inventario(numero_registros):
    """Genera registros de salidas de inventario."""
    
    productos = ["Producto A", "Producto B", "Producto C"]
    razones = ["Venta", "Retiro", "Ajuste negativo", "Devolución a proveedor"]
    
    salidas = []
    id_actual = 4001
    
    for _ in range(numero_registros):
        salida = {
            "id_salida": id_actual,
            "producto": random.choice(productos),
            "cantidad": random.randint(1, 100),
            "razon": random.choice(razones),
            "fecha": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
            "validado": random.choice([True, False, None])
        }
        id_actual += 1
        
        # Errores controlados
        if random.random() < 0.15:
            salida["cantidad"] = random.choice([None, -1, 0])
        if random.random() < 0.10:
            salida["validado"] = None
            
        salidas.append(salida)
    
    return salidas