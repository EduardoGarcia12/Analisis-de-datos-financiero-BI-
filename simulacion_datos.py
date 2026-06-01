import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN DE LA RUTA DE DESTINO
# ==========================================
ruta_guardado = r"C:\Users\zabu\Desktop\finanzaspro\ecommerce_proyecto_bi.xlsx"

print("Generando el archivo Excel con datos financieros y de fraude...")
np.random.seed(42)
num_registros = 1500

# Generación de fechas aleatorias para el histórico 2025-2026
fecha_inicio = datetime(2025, 1, 1)
fechas = [
    fecha_inicio + timedelta(days=int(np.random.randint(0, 500)), 
                             hours=int(np.random.randint(0, 24)), 
                             minutes=int(np.random.randint(0, 60))) 
    for _ in range(num_registros)
]

# 1. PESTAÑA: Tienda_Online (Datos comerciales de la plataforma)
df_tienda = pd.DataFrame({
    'ID_TRANSACCION': [f"TRX-{i:06d}" for i in range(1, num_registros + 1)],
    'FECHA_VENTA': fechas,
    'id_cliente': [f"CLI-{np.random.randint(100, 350):05d}" for _ in range(num_registros)],
    'PRODUCTO_CATEGORIA': np.random.choice(['Electrónica', 'Ropa', 'Hogar', 'Deportes', 'Belleza'], num_registros, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
    'MONTO_TOTAL': np.round(np.random.exponential(scale=120, size=num_registros) + 15, 2),
    'DISPOSITIVO': np.random.choice(['móvil', 'MÓVIL', 'escritorio', 'PC', 'tablet', None], num_registros, p=[0.4, 0.2, 0.2, 0.1, 0.05, 0.05])
})

# Agregando ruidos y nulos a propósito para tu fase de limpieza
df_tienda.loc[np.random.choice(df_tienda.index, 40, replace=False), 'MONTO_TOTAL'] = np.nan
df_tienda.loc[np.random.choice(df_tienda.index, 20, replace=False), 'id_cliente'] = "  CLI-00999 "

# 2. PESTAÑA: Pasarela_Bancos (Procesamiento de pagos bancarios)
bancos = np.random.choice(['Banamex', 'BBVA', 'Santander', 'Stripe', 'Paypal'], num_registros)
df_bancos = pd.DataFrame({
    'id_transaccion': [f"trx-{i:06d}" for i in range(1, num_registros + 1)], # ID en minúsculas y desalineado
    'Metodo_Pago': np.random.choice(['Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia', 'E-wallet'], num_registros),
    'Banco_Emisor': bancos,
    'codigo_autorizacion': [f"AUTH-{np.random.randint(100000, 999999)}" if np.random.rand() > 0.05 else 'RECHAZADA' for _ in range(num_registros)],
    'Cargo_Validado': [f"$ {np.random.randint(10, 500)}" for _ in range(num_registros)] # Strings con símbolos de dinero
})

# 3. PESTAÑA: Monitoreo_Riesgo (Alertas de ciberseguridad y fraude)
df_riesgo = pd.DataFrame({
    'ID_Transaccion': [f"TRX-{i:06d}" for i in range(1, num_registros + 1)],
    'IP_Pais': np.random.choice(['México', 'Mexico', 'Estados Unidos', 'USA', 'Rusia', 'China', 'Brasil', 'Desconocido'], num_registros, p=[0.7, 0.05, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01]),
    'Score_Riesgo': np.round(np.random.uniform(0, 100, num_registros), 1),
})
df_riesgo['Es_Fraude_Confirmado'] = np.where(df_riesgo['Score_Riesgo'] > 82, 1, 0)

# Escritura del archivo final con las tres hojas independientes
with pd.ExcelWriter(ruta_guardado, engine='openpyxl') as writer:
    df_tienda.to_excel(writer, sheet_name='Tienda_Online', index=False)
    df_bancos.to_excel(writer, sheet_name='Pasarela_Bancos', index=False)
    df_riesgo.to_excel(writer, sheet_name='Monitoreo_Riesgo', index=False)

print(f"\n--- ¡PROCESO EXITOSO! ---")
print(f"El archivo de datos crudos se ha guardado en: {ruta_guardado}")
print("Pestañas disponibles para tu ETL: 'Tienda_Online', 'Pasarela_Bancos' y 'Monitoreo_Riesgo'.")