import pandas as pd


def limpiar_movimientos(data_frame_sucio):
    """Limpia y valida datos de movimientos de inventario."""
    df = data_frame_sucio.copy()

    # Limpiar tipos de movimiento
    df["tipo"] = df["tipo"].astype("string").str.strip().str.upper()
    df["tipo"] = df["tipo"].where(df["tipo"].isin(["ENTRADA", "SALIDA"]), pd.NA)

    # Limpiar valores numéricos
    df["id_movimiento"] = pd.to_numeric(df["id_movimiento"], errors="coerce")
    df["producto_id"] = pd.to_numeric(df["producto_id"], errors="coerce")
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")

    # Validar datos obligatorios
    df = df[df["id_movimiento"] > 0]
    df = df[df["producto_id"] > 0]
    df = df.dropna(subset=["id_movimiento", "tipo", "producto_id"])

    # Convertir tipos
    df["id_movimiento"] = df["id_movimiento"].astype("Int64")
    df["producto_id"] = df["producto_id"].astype("Int64")
    df["cantidad"] = df["cantidad"].astype("Int64")

    # Validar cantidad mayor a cero
    df = df[df["cantidad"] > 0]

    # Validar y formatear fecha
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df.dropna(subset=["fecha"])
    df["fecha"] = df["fecha"].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Limpiar campo anulado
    df["anulado"] = df["anulado"].replace({True: True, False: False, "True": True, "False": False})
    df["anulado"] = df["anulado"].fillna(False).astype(bool)

    # Limpiar fecha_anulacion
    df["fecha_anulacion"] = df["fecha_anulacion"].fillna("")

    # Eliminar duplicados
    df = df.drop_duplicates()

    return df