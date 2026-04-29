import random


def generar_proveedores(numero_registros):
    nombres = ["Proveedor A", "Proveedor B", "Proveedor C", "SolucionesXYZ", "Distribuciones 1"]
    telefonos = ["3012345678", "3209876543", "3001122334"]
    correos = ["contacto@proveedor.com", "ventas@distribucion.com", "info@soluciones.com"]

    proveedores = []
    id_actual = 1001

    for _ in range(numero_registros):
        proveedor = {
            "id_proveedor": id_actual,
            "nombre": random.choice(nombres),
            "telefono": random.choice(telefonos),
            "email": random.choice(correos),
            "cantidad_productos": random.randint(0, 3)
        }
        id_actual += 1

        # Inyección de errores controlados
        probabilidad_error = random.random()

        if probabilidad_error < 0.15:
            proveedor["id_proveedor"] = None

        elif probabilidad_error < 0.30:
            proveedor["nombre"] = random.choice([None, "", "   "])

        elif probabilidad_error < 0.45:
            proveedor["telefono"] = random.choice([None, "abc-123", "1234"])

        elif probabilidad_error < 0.60:
            proveedor["email"] = random.choice([None, "correo_sin_arroba.com", "user@"])

        elif probabilidad_error < 0.75:
            proveedor["cantidad_productos"] = random.choice([None, -1])

        elif probabilidad_error < 0.90:
            proveedor["nombre"] = proveedor["nombre"].upper()

        proveedores.append(proveedor)

    return proveedores
