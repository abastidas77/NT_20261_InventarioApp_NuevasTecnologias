import pandas as pd
from datetime import datetime


def limpiar_movimientos_inventario(data_frame_sucio):
    """Limpia y valida los datos de movimientos de inventario."""
    
    df = data_frame_sucio.copy()
    
    # Limpiar textos
    df["tipo"] = df["tipo"].astype("string").str.strip().str.title()
    df["id_producto"] = df["id_producto"].astype("string").str.strip()
    
    # Convertir y validar IDs
    df["id_movimiento"] = pd.to_numeric(df["id_movimiento"], errors="coerce")
    df = df[df["id_movimiento"] > 0]
    df = df.dropna(subset=["id_movimiento"])
    df["id_movimiento"] = df["id_movimiento"].astype("Int64")
    
    # Validar tipo de movimiento
    df["tipo"] = df["tipo"].where(
        df["tipo"].isin(["Entrada", "Salida"]),
        pd.NA
    )
    
    # Validar y convertir fechas
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce")
    # No permitir fechas futuras
    fecha_hoy = datetime.now()
    df["fecha"] = df["fecha"].where(df["fecha"] <= fecha_hoy, pd.NA)
    df = df.dropna(subset=["fecha"])
    df["fecha"] = df["fecha"].dt.strftime("%Y-%m-%d")
    
    # Validar cantidades
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df = df[df["cantidad"] > 0]
    df = df[df["cantidad"] <= 1000]  # Cantidad máxima razonable
    df = df.dropna(subset=["cantidad"])
    df["cantidad"] = df["cantidad"].astype("Int64")
    
    # Validar productos
    productos_validos = ["Producto A", "Producto B", "Producto C", "Producto D", "Producto E"]
    df["id_producto"] = df["id_producto"].where(
        df["id_producto"].isin(productos_validos),
        pd.NA
    )
    df = df.dropna(subset=["id_producto"])
    
    # Eliminar duplicados por ID
    df = df.drop_duplicates(subset=["id_movimiento"], keep="first")
    
    # Agregar campos de control
    df["pendiente_validar"] = df["cantidad"] > 500  # Movimientos grandes requieren validación
    df["error_cantidad"] = df["cantidad"] > 500
    
    return df


def limpiar_entradas_inventario(data_frame_sucio):
    """Limpia y valida los datos de entradas de inventario."""
    
    df = data_frame_sucio.copy()
    
    # Limpiar textos
    df["producto"] = df["producto"].astype("string").str.strip()
    df["razon"] = df["razon"].astype("string").str.strip()
    
    # Convertir y validar IDs
    df["id_entrada"] = pd.to_numeric(df["id_entrada"], errors="coerce")
    df = df[df["id_entrada"] > 0]
    df = df.dropna(subset=["id_entrada"])
    df["id_entrada"] = df["id_entrada"].astype("Int64")
    
    # Validar cantidades
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df = df[df["cantidad"] > 0]
    df = df.dropna(subset=["cantidad"])
    df["cantidad"] = df["cantidad"].astype("Int64")
    
    # Validar productos
    productos_validos = ["Producto A", "Producto B", "Producto C"]
    df["producto"] = df["producto"].where(
        df["producto"].isin(productos_validos),
        pd.NA
    )
    df = df.dropna(subset=["producto"])
    
    # Validar fechas
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce")
    df = df.dropna(subset=["fecha"])
    df["fecha"] = df["fecha"].dt.strftime("%Y-%m-%d")
    
    # Eliminar duplicados
    df = df.drop_duplicates(subset=["id_entrada"], keep="first")
    
    # Campo de validación
    df["validado"] = df["validado"].fillna(False).astype("bool")
    
    return df


def limpiar_salidas_inventario(data_frame_sucio):
    """Limpia y valida los datos de salidas de inventario."""
    
    df = data_frame_sucio.copy()
    
    # Limpiar textos
    df["producto"] = df["producto"].astype("string").str.strip()
    df["razon"] = df["razon"].astype("string").str.strip()
    
    # Convertir y validar IDs
    df["id_salida"] = pd.to_numeric(df["id_salida"], errors="coerce")
    df = df[df["id_salida"] > 0]
    df = df.dropna(subset=["id_salida"])
    df["id_salida"] = df["id_salida"].astype("Int64")
    
    # Validar cantidades
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df = df[df["cantidad"] > 0]
    df = df.dropna(subset=["cantidad"])
    df["cantidad"] = df["cantidad"].astype("Int64")
    
    # Validar productos
    productos_validos = ["Producto A", "Producto B", "Producto C"]
    df["producto"] = df["producto"].where(
        df["producto"].isin(productos_validos),
        pd.NA
    )
    df = df.dropna(subset=["producto"])
    
    # Validar fechas
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce")
    df = df.dropna(subset=["fecha"])
    df["fecha"] = df["fecha"].dt.strftime("%Y-%m-%d")
    
    # Eliminar duplicados
    df = df.drop_duplicates(subset=["id_salida"], keep="first")
    
    # Campo de validación
    df["validado"] = df["validado"].fillna(False).astype("bool")
    
    return df


def obtener_movimientos_recientes(data_frame, dias=7):
    """Obtiene movimientos de los últimos N días."""
    from datetime import datetime, timedelta
    
    fecha_limite = datetime.now() - timedelta(days=dias)
    df_fechas = pd.to_datetime(data_frame["fecha"], format="%Y-%m-%d", errors="coerce")
    
    return data_frame[df_fechas >= fecha_limite].copy()


def obtener_movimientos_por_tipo(data_frame, tipo):
    """Filtra movimientos por tipo (Entrada/Salida)."""
    return data_frame[data_frame["tipo"] == tipo].copy()


def obtener_movimientos_con_errores(data_frame):
    """Obtiene movimientos que requieren revisión."""
    errores = data_frame[
        (data_frame.get("pendiente_validar", False) == True) |
        (data_frame.get("error_cantidad", False) == True)
    ].copy()
    return errores