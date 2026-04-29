import pandas as pd
from utils.simulacion import generar_simulacion
from notebook.limpieza import limpiar_simulacion

print("=" * 60)
print("SISTEMA DE REGISTRO Y CONTROL DE INVENTARIO")
print("=" * 60)

# Generar simulacion de 1000 productos con datos sucios
print("\n1. Generando simulación de 1000 productos...")
simulaciones = generar_simulacion(1000)
print(f"   Productos generados: {len(simulaciones)}")

# Convertir a DataFrame
print("\n2. Convirtiendo a DataFrame...")
simulaciones_ordenadas = pd.DataFrame(simulaciones)
print(f"   Registros con errores: {len(simulaciones_ordenadas)}")

# Limpiar datos según criterios de validación
print("\n3. Limpiando datos según criterios de validación...")
print("   - El nombre es obligatorio")
print("   - El precio debe ser mayor a 0")
print("   - La cantidad debe ser mayor o igual a 0")
simulaciones_limpias = limpiar_simulacion(simulaciones_ordenadas)
print(f"   Productos válidos después de limpieza: {len(simulaciones_limpias)}")
print(f"   Productos eliminados: {len(simulaciones_ordenadas) - len(simulaciones_limpias)}")

print("\n4. Datos limpios y validados:")
print("=" * 60)
print(simulaciones_limpias)
print("=" * 60)
print(f"\nResumen del inventario:")
print(f"Total de productos únicos: {len(simulaciones_limpias)}")
print(f"Cantidad total en inventario: {simulaciones_limpias['cantidad'].sum()}")
print(f"Valor total del inventario: ${simulaciones_limpias['precio'].sum():,.0f}")



# CODIGO MATEO


import os
import pandas as pd
from datetime import datetime

from utils.HU_inventarioSimulacion import generar_movimientos
from utils.HU_limpiezaMovimientos import limpiar_movimientos


# Rutas absolutas basadas en la ubicación del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTOS_PATH = os.path.join(BASE_DIR, "utils", "productos.csv")
MOVIMIENTOS_PATH = os.path.join(BASE_DIR, "utils", "movimientos.csv")


class InventarioError(Exception):
    pass


class GestionInventario:
    def __init__(self):
        self.productos = pd.read_csv(PRODUCTOS_PATH, comment='#')
        self.movimientos = pd.DataFrame(columns=[
            "id_movimiento", "tipo", "producto_id", "cantidad", 
            "fecha", "anulado", "fecha_anulacion"
        ])

    def guardar_movimientos(self):
        self.movimientos.to_csv(MOVIMIENTOS_PATH, index=False)

    def guardar_productos(self):
        self.productos.to_csv(PRODUCTOS_PATH, index=False)

    def existe_producto(self, producto_id):
        return producto_id in self.productos['id_producto'].values

    def stock_actual(self, producto_id):
        fila = self.productos[self.productos['id_producto'] == producto_id]
        if fila.empty:
            return 0
        return int(fila.iloc[0]['stock'])

    # HUM-09: Registrar movimiento
    def registrar_movimiento(self, tipo, producto_id, cantidad, fecha=None):
        """Registra entrada o salida de productos."""
        if tipo not in ['ENTRADA', 'SALIDA']:
            raise InventarioError('Tipo de movimiento inválido. Use ENTRADA o SALIDA.')
        if not self.existe_producto(producto_id):
            raise InventarioError(f'El producto {producto_id} no existe')
        if cantidad <= 0:
            raise InventarioError('La cantidad debe ser mayor a cero')
        if fecha is None:
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Validar fecha
        try:
            datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise InventarioError('Fecha inválida')
        
        # HUM-10: Validar stock para salida
        stock = self.stock_actual(producto_id)
        if tipo == 'SALIDA' and cantidad > stock:
            raise InventarioError(f'No hay suficiente stock. Stock actual: {stock}')
        
        # HUM-11: Actualizar stock automáticamente
        if tipo == 'ENTRADA':
            nuevo_stock = stock + cantidad
        else:
            nuevo_stock = stock - cantidad
        
        if nuevo_stock < 0:
            raise InventarioError('El stock no puede quedar negativo')
        
        self.productos.loc[self.productos['id_producto'] == producto_id, 'stock'] = nuevo_stock
        
        # Registrar movimiento
        nuevo_id = int(self.movimientos['id_movimiento'].max() + 1) if not self.movimientos.empty else 1
        nuevo = {
            'id_movimiento': nuevo_id,
            'tipo': tipo,
            'producto_id': producto_id,
            'cantidad': cantidad,
            'fecha': fecha,
            'anulado': False,
            'fecha_anulacion': ''
        }
        self.movimientos = pd.concat([self.movimientos, pd.DataFrame([nuevo])], ignore_index=True)
        self.guardar_movimientos()
        self.guardar_productos()
        return nuevo_id

    # HUM-12: Anular movimiento
    def anular_movimiento(self, id_movimiento):
        """Anula un movimiento existente."""
        mov = self.movimientos[(self.movimientos['id_movimiento'] == id_movimiento) & 
                               (self.movimientos['anulado'] == False)]
        if mov.empty:
            raise InventarioError('Movimiento no existe o ya está anulado')
        
        mov = mov.iloc[0]
        producto_id = mov['producto_id']
        cantidad = int(mov['cantidad'])
        tipo = mov['tipo']
        
        stock = self.stock_actual(producto_id)
        
        # Revertir stock: ENTRADA resta, SALIDA suma
        if tipo == 'ENTRADA':
            nuevo_stock = stock - cantidad
        else:
            nuevo_stock = stock + cantidad
        
        if nuevo_stock < 0:
            raise InventarioError('No se puede anular: stock insuficiente')
        
        self.productos.loc[self.productos['id_producto'] == producto_id, 'stock'] = nuevo_stock
        
        # Marcar como anulado
        self.movimientos.loc[self.movimientos['id_movimiento'] == id_movimiento, 'anulado'] = True
        self.movimientos.loc[self.movimientos['id_movimiento'] == id_movimiento, 'fecha_anulacion'] = \
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.guardar_movimientos()
        self.guardar_productos()

    def listar_movimientos(self, tipo=None, producto_id=None, anulado=None):
        df = self.movimientos.copy()
        if tipo:
            df = df[df['tipo'] == tipo]
        if producto_id:
            df = df[df['producto_id'] == producto_id]
        if anulado is not None:
            df = df[df['anulado'] == anulado]
        return df.sort_values('fecha', ascending=False)

    def listar_productos(self):
        return self.productos


def main():
    inv = GestionInventario()
    
    # Generar y limpiar movimientos
    movimientos_sucios = generar_movimientos(10)
    movimientos_df = pd.DataFrame(movimientos_sucios)
    movimientos_limpios = limpiar_movimientos(movimientos_df)
    inv.movimientos = movimientos_limpios
    
    print("=== STOCK INICIAL ===")
    print(inv.listar_productos()[["id_producto", "nombre", "stock"]])
    
    print("\n=== HUM-09: REGISTRAR MOVIMIENTO ===")
    try:
        id_mov = inv.registrar_movimiento("ENTRADA", 1, 5)
        print(f"Entrada registrada ID: {id_mov}")
    except InventarioError as e:
        print(f"Error: {e}")
    
    print("\n=== HUM-10: VALIDAR SALIDA (sin stock suficiente) ===")
    try:
        inv.registrar_movimiento("SALIDA", 3, 100)
    except InventarioError as e:
        print(f"Error esperado: {e}")
    
    print("\n=== HUM-10: VALIDAR SALIDA (con stock) ===")
    try:
        id_mov = inv.registrar_movimiento("SALIDA", 2, 3)
        print(f"Salida registrada ID: {id_mov}")
    except InventarioError as e:
        print(f"Error: {e}")
    
    print("\n=== STOCK ACTUALIZADO (HUM-11) ===")
    print(inv.listar_productos()[["id_producto", "nombre", "stock"]])
    
    print("\n=== MOVIMIENTOS REGISTRADOS ===")
    print(inv.listar_movimientos())
    
    print("\n=== HUM-12: ANULAR MOVIMIENTO ===")
    # Usar el primer movimiento no anulado disponible
    movimientos_activos = inv.listar_movimientos(anulado=False)
    if not movimientos_activos.empty:
        id_a_anular = int(movimientos_activos.iloc[0]['id_movimiento'])
        try:
            inv.anular_movimiento(id_a_anular)
            print(f"Movimiento {id_a_anular} anulado correctamente")
        except InventarioError as e:
            print(f"Error: {e}")
    else:
        print("No hay movimientos para anular")
    
    print("\n=== STOCK TRAS ANULACIÓN ===")
    print(inv.listar_productos()[["id_producto", "nombre", "stock"]])
    
    print("\n=== MOVIMIENTOS FINALES ===")
    print(inv.listar_movimientos())


if __name__ == "__main__":
    main()
    
    
    #CODIGO RAFA
    
    
    import pandas as pd

from utils.HU_proveedoresSimulacion import generar_proveedores
from utils.HU3_limpiezaProveedores import limpiar_proveedores


def crear_proveedor(data_frame, nombre, telefono=None, email=None):
    nuevo_id = int(data_frame["id_proveedor"].max() + 1) if not data_frame.empty else 1001
    registro = {
        "id_proveedor": nuevo_id,
        "nombre": nombre.strip() if nombre else "",
        "telefono": telefono.strip() if telefono else None,
        "email": email.strip().lower() if email else None,
        "cantidad_productos": 0,
        "puede_eliminar": True
    }
    nuevo_df = pd.DataFrame([registro])
    return pd.concat([data_frame, nuevo_df], ignore_index=True)


def editar_proveedor(data_frame, id_proveedor, cambios):
    indice = data_frame.index[data_frame["id_proveedor"] == id_proveedor]
    if len(indice) == 0:
        return data_frame
    for campo, valor in cambios.items():
        if campo in data_frame.columns:
            data_frame.at[indice[0], campo] = valor
    return data_frame


def eliminar_proveedor(data_frame, id_proveedor):
    proveedor = data_frame[data_frame["id_proveedor"] == id_proveedor]
    if proveedor.empty:
        return data_frame
    if int(proveedor.iloc[0]["cantidad_productos"]) != 0:
        print(f"No se puede eliminar el proveedor {id_proveedor}: tiene productos asociados.")
        return data_frame
    return data_frame[data_frame["id_proveedor"] != id_proveedor]


def buscar_proveedor(data_frame, termino):
    return data_frame[data_frame["nombre"].str.contains(termino, case=False, na=False)]


def main():
    proveedores = generar_proveedores(10)
    proveedores_df = pd.DataFrame(proveedores)
    proveedores_limpios = limpiar_proveedores(proveedores_df)

    print("--- Proveedores generados ---")
    print(proveedores_limpios)

    print("\n--- Registrar nuevo proveedor ---")
    proveedores_limpios = crear_proveedor(proveedores_limpios, "Proveedor Nuevo", "3123456789", "nuevo@proveedor.com")
    print(proveedores_limpios.tail(1))

    print("\n--- Buscar proveedores por nombre 'Proveedor' ---")
    encontrados = buscar_proveedor(proveedores_limpios, "Proveedor")
    print(encontrados[["id_proveedor", "nombre", "telefono", "email"]])

    print("\n--- Editar proveedor ---")
    proveedores_limpios = editar_proveedor(proveedores_limpios, 1001, {"telefono": "3200000000", "email": "actualizado@proveedor.com"})
    print(proveedores_limpios[proveedores_limpios["id_proveedor"] == 1001])

    print("\n--- Eliminar proveedor si no tiene productos asociados ---")
    proveedores_limpios = eliminar_proveedor(proveedores_limpios, proveedores_limpios.iloc[0]["id_proveedor"])
    print(proveedores_limpios)


if __name__ == "__main__":
    main()

# CODIGO MILE

import pandas as pd
from datetime import datetime, timedelta

from utils.HU1_inventarioSimulacion import (
    generar_movimientos_inventario,
    generar_entradas_inventario,
    generar_salidas_inventario
)
from utils.HU_limpiezaInventario import (
    limpiar_movimientos_inventario,
    limpiar_entradas_inventario,
    limpiar_salidas_inventario,
    obtener_movimientos_recientes,
    obtener_movimientos_por_tipo,
    obtener_movimientos_con_errores
)


# ==================== HU-15: Movimiento de Inventario ====================

def crear_movimiento(data_frame, tipo, fecha, cantidad, id_producto):
    """Registra un nuevo movimiento de inventario."""
    nuevo_id = int(data_frame["id_movimiento"].max() + 1) if not data_frame.empty else 2001
    registro = {
        "id_movimiento": nuevo_id,
        "tipo": tipo.strip().title() if tipo else "",
        "fecha": fecha,
        "cantidad": cantidad,
        "id_producto": id_producto.strip() if id_producto else "",
        "pendiente_validar": cantidad > 500,
        "error_cantidad": cantidad > 500
    }
    nuevo_df = pd.DataFrame([registro])
    return pd.concat([data_frame, nuevo_df], ignore_index=True)


def editar_movimiento(data_frame, id_movimiento, cambios):
    """Edita un movimiento existente."""
    indice = data_frame.index[data_frame["id_movimiento"] == id_movimiento]
    if len(indice) == 0:
        return data_frame
    for campo, valor in cambios.items():
        if campo in data_frame.columns:
            data_frame.at[indice[0], campo] = valor
    # Actualizar campos de control
    if "cantidad" in cambios:
        data_frame.at[indice[0], "pendiente_validar"] = cambios["cantidad"] > 500
        data_frame.at[indice[0], "error_cantidad"] = cambios["cantidad"] > 500
    return data_frame


def eliminar_movimiento(data_frame, id_movimiento):
    """Elimina un movimiento por ID."""
    return data_frame[data_frame["id_movimiento"] != id_movimiento]


def buscar_movimiento(data_frame, termino):
    """Busca movimientos por producto o tipo."""
    return data_frame[
        data_frame["id_producto"].str.contains(termino, case=False, na=False) |
        data_frame["tipo"].str.contains(termino, case=False, na=False)
    ]


# ==================== HU-16: Entradas de Inventario ====================

def crear_entrada(data_frame, producto, cantidad, razon, fecha=None):
    """Registra una nueva entrada de inventario."""
    nuevo_id = int(data_frame["id_entrada"].max() + 1) if not data_frame.empty else 3001
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")
    registro = {
        "id_entrada": nuevo_id,
        "producto": producto.strip() if producto else "",
        "cantidad": cantidad,
        "razon": razon.strip() if razon else "",
        "fecha": fecha,
        "validado": False
    }
    nuevo_df = pd.DataFrame([registro])
    return pd.concat([data_frame, nuevo_df], ignore_index=True)


def validar_entrada(data_frame, id_entrada):
    """Valida una entrada de inventario."""
    indice = data_frame.index[data_frame["id_entrada"] == id_entrada]
    if len(indice) > 0:
        data_frame.at[indice[0], "validado"] = True
    return data_frame


def obtener_entradas_por_producto(data_frame, producto):
    """Filtra entradas por producto."""
    return data_frame[data_frame["producto"] == producto].copy()


# ==================== HU-17: Salidas de Inventario ====================

def crear_salida(data_frame, producto, cantidad, razon, fecha=None):
    """Registra una nueva salida de inventario."""
    nuevo_id = int(data_frame["id_salida"].max() + 1) if not data_frame.empty else 4001
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")
    registro = {
        "id_salida": nuevo_id,
        "producto": producto.strip() if producto else "",
        "cantidad": cantidad,
        "razon": razon.strip() if razon else "",
        "fecha": fecha,
        "validado": False
    }
    nuevo_df = pd.DataFrame([registro])
    return pd.concat([data_frame, nuevo_df], ignore_index=True)


def validar_salida(data_frame, id_salida):
    """Valida una salida de inventario."""
    indice = data_frame.index[data_frame["id_salida"] == id_salida]
    if len(indice) > 0:
        data_frame.at[indice[0], "validado"] = True
    return data_frame


def obtener_salidas_por_producto(data_frame, producto):
    """Filtra salidas por producto."""
    return data_frame[data_frame["producto"] == producto].copy()


# ==================== HU-18: Movimientos Recientes ====================

def movimientos_dia(data_frame):
    """Movimientos del día actual."""
    hoy = datetime.now().strftime("%Y-%m-%d")
    return data_frame[data_frame["fecha"] == hoy].copy()


def movimientos_semana(data_frame):
    """Movimientos de la última semana."""
    return obtener_movimientos_recientes(data_frame, dias=7)


def movimientos_mes(data_frame):
    """Movimientos del último mes."""
    return obtener_movimientos_recientes(data_frame, dias=30)


# ==================== HU-19: Control y Revisión ====================

def movimientos_pendientes(data_frame):
    """Movimientos pendientes de validar."""
    return data_frame[
        (data_frame.get("pendiente_validar", False) == True) |
        (data_frame.get("validado", True) == False)
    ].copy()


def movimientos_con_errores(data_frame):
    """Movimientos con errores en cantidades."""
    return data_frame[data_frame.get("error_cantidad", False) == True].copy()


def auditoria_inventario(data_frame):
    """Genera reporte de auditoría."""
    print("\n" + "="*60)
    print("AUDITORÍA DE INVENTARIO")
    print("="*60)
    
    total = len(data_frame)
    pendientes = len(movimientos_pendientes(data_frame))
    errores = len(movimientos_con_errores(data_frame))
    
    print(f"Total de movimientos: {total}")
    print(f"Pendientes de validar: {pendientes}")
    print(f"Con errores de cantidad: {errores}")
    
    if pendientes > 0:
        print(f"\n--- Movimientos pendientes ---")
        print(movimientos_pendientes(data_frame))
    
    if errores > 0:
        print(f"\n--- Movimientos con errores ---")
        print(movimientos_con_errores(data_frame))
    
    return {
        "total": total,
        "pendientes": pendientes,
        "errores": errores
    }


# ==================== Función Principal ====================

def main():
    print("="*60)
    print("SIMULACIÓN DE INVENTARIO - Historias de Usuario")
    print("="*60)
    
    # Generar y limpiar datos
    print("\n--- Generando movimientos de inventario (datos sucios) ---")
    movimientos_sucios = generar_movimientos_inventario(15)
    movimientos_df = pd.DataFrame(movimientos_sucios)
    print(f"Registros generados: {len(movimientos_df)}")
    
    print("\n--- Limpiando movimientos ---")
    movimientos_limpios = limpiar_movimientos_inventario(movimientos_df)
    print(f"Registros limpios: {len(movimientos_limpios)}")
    print(movimientos_limpios)
    
    # HU-16: Entradas
    print("\n" + "="*60)
    print("HU-16: Entradas de Inventario")
    print("="*60)
    entradas_sucias = generar_entradas_inventario(10)
    entradas_df = pd.DataFrame(entradas_sucias)
    entradas_limpias = limpiar_entradas_inventario(entradas_df)
    print(f"Entradas generadas: {len(entradas_limpias)}")
    print(entradas_limpias)
    
    # HU-17: Salidas
    print("\n" + "="*60)
    print("HU-17: Salidas de Inventario")
    print("="*60)
    salidas_sucias = generar_salidas_inventario(10)
    salidas_df = pd.DataFrame(salidas_sucias)
    salidas_limpias = limpiar_salidas_inventario(salidas_df)
    print(f"Salidas generadas: {len(salidas_limpias)}")
    print(salidas_limpias)
    
    # HU-15: Registrar nuevo movimiento
    print("\n" + "="*60)
    print("HU-15: Registrar nuevo movimiento")
    print("="*60)
    movimientos_limpios = crear_movimiento(
        movimientos_limpios,
        "Entrada",
        datetime.now().strftime("%Y-%m-%d"),
        50,
        "Producto A"
    )
    print("Nuevo movimiento registrado:")
    print(movimientos_limpios.tail(1))
    
    # HU-15: Buscar movimientos
    print("\n--- Buscar movimientos por producto 'Producto A' ---")
    encontrados = buscar_movimiento(movimientos_limpios, "Producto A")
    print(encontrados[["id_movimiento", "tipo", "fecha", "cantidad", "id_producto"]])
    
    # HU-15: Editar movimiento
    print("\n--- Editar movimiento #2001 ---")
    movimientos_limpios = editar_movimiento(movimientos_limpios, 2001, {"cantidad": 75})
    print(movimientos_limpios[movimientos_limpios["id_movimiento"] == 2001])
    
    # HU-16: Nueva entrada
    print("\n--- Registrar nueva entrada ---")
    entradas_limpias = crear_entrada(
        entradas_limpias,
        "Producto A",
        100,
        "Reposición de stock"
    )
    print(entradas_limpias.tail(1))
    
    # HU-17: Nueva salida
    print("\n--- Registrar nueva salida ---")
    salidas_limpias = crear_salida(
        salidas_limpias,
        "Producto B",
        25,
        "Venta"
    )
    print(salidas_limpias.tail(1))
    
    # HU-18: Movimientos recientes
    print("\n" + "="*60)
    print("HU-18: Movimientos Recientes")
    print("="*60)
    
    print("\n--- Movimientos del día ---")
    print(movimientos_dia(movimientos_limpios))
    
    print("\n--- Movimientos de la semana ---")
    print(movimientos_semana(movimientos_limpios))
    
    print("\n--- Movimientos del mes ---")
    print(movimientos_mes(movimientos_limpios))
    
    # HU-19: Control y Revisión
    print("\n" + "="*60)
    print("HU-19: Control y Revisión")
    print("="*60)
    
    print("\n--- Movimientos pendientes de validar ---")
    print(movimientos_pendientes(movimientos_limpios))
    
    print("\n--- Movimientos con errores en cantidades ---")
    print(movimientos_con_errores(movimientos_limpios))
    
    # Auditoría
    auditoria_inventario(movimientos_limpios)
    
    print("\n" + "="*60)
    print("EJECUCIÓN COMPLETA")
    print("="*60)


if __name__ == "__main__":
    main()