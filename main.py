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
