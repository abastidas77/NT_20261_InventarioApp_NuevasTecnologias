import random
from datetime import datetime, timedelta


def generar_movimientos(numero_registros):
    """Genera movimientos de inventario sintéticos con errores controlados."""
    tipos = ["ENTRADA", "SALIDA"]
    producto_ids = [1, 2, 3, 4, 5]
    
    movimientos = []
    id_actual = 1
    fecha_base = datetime.now()

    for _ in range(numero_registros):
        movimiento = {
            "id_movimiento": id_actual,
            "tipo": random.choice(tipos),
            "producto_id": random.choice(producto_ids),
            "cantidad": random.randint(1, 10),
            "fecha": (fecha_base - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S'),
            "anulado": False,
            "fecha_anulacion": ""
        }
        id_actual += 1

        # Inyección de errores controlados (similar a proveedores)
        probabilidad_error = random.random()

        if probabilidad_error < 0.10:
            movimiento["id_movimiento"] = None

        elif probabilidad_error < 0.20:
            movimiento["tipo"] = random.choice([None, "", "INVALIDO"])

        elif probabilidad_error < 0.30:
            movimiento["producto_id"] = random.choice([None, 0, 999])

        elif probabilidad_error < 0.40:
            movimiento["cantidad"] = random.choice([None, 0, -5])

        elif probabilidad_error < 0.50:
            movimiento["fecha"] = random.choice([None, "", "fecha-invalida"])

        elif probabilidad_error < 0.60:
            movimiento["anulado"] = random.choice([None, "si", "no"])

        movimientos.append(movimiento)

    return movimientos