import pandas as pd


def limpiar_proveedores(data_frame_sucio):
    data_frame_limpio = data_frame_sucio.copy()

    # Procesar textos de proveedores
    data_frame_limpio["nombre"] = data_frame_limpio["nombre"].astype("string").str.strip()
    data_frame_limpio["telefono"] = data_frame_limpio["telefono"].astype("string").str.strip()
    data_frame_limpio["email"] = data_frame_limpio["email"].astype("string").str.strip().str.lower()

    # Limpiar valores numéricos
    data_frame_limpio["id_proveedor"] = pd.to_numeric(data_frame_limpio["id_proveedor"], errors="coerce")
    data_frame_limpio["cantidad_productos"] = pd.to_numeric(data_frame_limpio["cantidad_productos"], errors="coerce")

    # Validar datos obligatorios y formatos
    data_frame_limpio = data_frame_limpio[data_frame_limpio["id_proveedor"] > 0]
    data_frame_limpio = data_frame_limpio[data_frame_limpio["nombre"] != ""]
    data_frame_limpio = data_frame_limpio.dropna(subset=["id_proveedor", "nombre"])

    data_frame_limpio["id_proveedor"] = data_frame_limpio["id_proveedor"].astype("Int64")
    data_frame_limpio["cantidad_productos"] = data_frame_limpio["cantidad_productos"].astype("Int64")

    data_frame_limpio["email"] = data_frame_limpio["email"].where(
        data_frame_limpio["email"].str.contains("@", na=False),
        pd.NA
    )

    data_frame_limpio["telefono"] = data_frame_limpio["telefono"].where(
        data_frame_limpio["telefono"].str.isnumeric(),
        pd.NA
    )

    data_frame_limpio = data_frame_limpio[data_frame_limpio["cantidad_productos"].ge(0)]

    # Eliminar duplicados y agregar columna de validación de eliminación
    data_frame_limpio = data_frame_limpio.drop_duplicates()
    data_frame_limpio["puede_eliminar"] = data_frame_limpio["cantidad_productos"] == 0

    return data_frame_limpio
