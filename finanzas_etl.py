import pandas as pd
import numpy as np

# Rutas de tus archivos
datos = r"C:\Users\zabu\Desktop\finanzaspro\ecommerce_proyecto_bi.xlsx"
datos_limpios = r"C:\Users\zabu\Desktop\finanzaspro\ecommerce_clean.xlsx"

def limpiar_hojas(df, numero_hoja):
    # 1. Estandarizar nombres de columnas a MAYÚSCULAS y quitar espacios
    df.columns = df.columns.astype(str).str.strip().str.upper()
    
    # 2. Estandarizar la llave primaria que une a todo el modelo comercial
    # Buscamos la columna sin importar si vino como ID_TRANSACCION o ID_TRANSACCION
    col_id = [c for c in df.columns if 'TRANSACCION' in c]
    if col_id:
        # Aseguramos que el ID sea texto, sin espacios y siempre en MAYÚSCULAS para que cruce bien
        df[col_id[0]] = df[col_id[0]].astype(str).str.strip().str.upper()
        # Renombramos explícitamente para homogeneizar todas las hojas
        df.rename(columns={col_id[0]: 'ID_TRANSACCION'}, inplace=True)
    
    # 3. Limpieza de Fechas (Solo aplica en la hoja de Tienda)
    if 'FECHA_VENTA' in df.columns: 
        df['FECHA_VENTA'] = pd.to_datetime(df['FECHA_VENTA'], errors='coerce')
        df = df.dropna(subset=['FECHA_VENTA']).copy()
        df['FECHA_VENTA'] = df['FECHA_VENTA'].dt.tz_localize(None)
    
    # 4. Limpieza específica de textos usando mapeos vectorizados (más eficiente que funciones)
    if 'IP_PAIS' in df.columns:
        df['IP_PAIS'] = df['IP_PAIS'].astype(str).str.strip().str.upper()
        mapeo_paises = {
            'MÉXICO': 'México', 'MEXICO': 'México',
            'ESTADOS UNIDOS': 'Estados Unidos', 'USA': 'Estados Unidos',
            'RUSIA': 'Rusia', 'CHINA': 'China', 'BRASIL': 'Brasil'
        }
        df['IP_PAIS_LIMPIA'] = df['IP_PAIS'].map(mapeo_paises).fillna('Desconocido')
        
    if 'PRODUCTO_CATEGORIA' in df.columns:
        df['PRODUCTO_CATEGORIA'] = df['PRODUCTO_CATEGORIA'].astype(str).str.strip().str.upper()
        mapeo_cat = {'BELLEZA': 'Belleza', 'DEPORTES': 'Deportes', 'ELECTRÓNICA': 'Electrónica', 'ELECTRONICA': 'Electrónica', 'HOGAR': 'Hogar', 'ROPA': 'Ropa'}
        df['PRODUCTO_CATEGORIA_LIMPIO'] = df['PRODUCTO_CATEGORIA'].map(mapeo_cat).fillna('Unknown')
        
    if 'DISPOSITIVO' in df.columns:
        df['DISPOSITIVO'] = df['DISPOSITIVO'].astype(str).str.strip().str.upper()
        mapeo_disp = {'ESCRITORIO': 'Escritorio', 'PC': 'PC', 'MÓVIL': 'Móvil', 'MOVIL': 'Móvil', 'TABLET': 'Tablet'}
        df['DISPOSITIVO_LIMPIO'] = df['DISPOSITIVO'].map(mapeo_disp).fillna('Unknown')
        
    if 'BANCO_EMISOR' in df.columns:
        df['BANCO_EMISOR'] = df['BANCO_EMISOR'].astype(str).str.strip().str.upper()
        mapeo_bancos = {'BANAMEX': 'Banamex', 'BBVA': 'BBVA', 'PAYPAL': 'Paypal', 'SANTANDER': 'Santander', 'STRIPE': 'Stripe'}
        df['BANCO_EMISOR_LIMPIO'] = df['BANCO_EMISOR'].map(mapeo_bancos).fillna('Unknown')

    # 5. Limpieza e imputación de montos financieros numericos
    if 'MONTO_TOTAL' in df.columns:
        df['MONTO_TOTAL'] = pd.to_numeric(df['MONTO_TOTAL'], errors='coerce')
        df['MONTO_TOTAL'] = df['MONTO_TOTAL'].fillna(df['MONTO_TOTAL'].mean())
        
    if 'CARGO_VALIDADO' in df.columns:
        # Quitamos el signo de pesos y espacios antes de convertir a número
        df['CARGO_VALIDADO'] = df['CARGO_VALIDADO'].astype(str).str.replace('$', '', regex=False).str.strip()
        df['CARGO_VALIDADO'] = pd.to_numeric(df['CARGO_VALIDADO'], errors='coerce')
        df['CARGO_VALIDADO'] = df['CARGO_VALIDADO'].fillna(df['CARGO_VALIDADO'].mean())

    if 'SCORE_RIESGO' in df.columns:
        df['SCORE_RIESGO'] = pd.to_numeric(df['SCORE_RIESGO'], errors='coerce')
        df['SCORE_RIESGO'] = df['SCORE_RIESGO'].fillna(df['SCORE_RIESGO'].mean())

    return df

def proceso_etl_completo():
    try: 
        # Diccionario para guardar las hojas procesadas temporalmente
        hojas_limpias = {}
        nombres_hojas_origen = ['Tienda_Online', 'Pasarela_Bancos', 'Monitoreo_Riesgo']
        
        with pd.ExcelWriter(datos_limpios, engine='openpyxl') as writer: 
            
            # 1. Procesar y guardar hojas individuales
            for indice, nombre_hoja in enumerate(nombres_hojas_origen):
                print(f"Procesando hoja original: {nombre_hoja}...")
                
                # Leemos la hoja desde el inicio (header=0 es el estándar si no hay desfases)
                df_original = pd.read_excel(datos, sheet_name=nombre_hoja, header=0)
                
                # Ejecutamos la limpieza
                df_procesado = limpiar_hojas(df_original, indice)
                
                # Guardamos en el nuevo Excel corporativo
                nombre_destino = f"{nombre_hoja}_Limpio"
                df_procesado.to_excel(writer, sheet_name=nombre_destino, index=False)
                
                # Almacenamos en memoria para el cruce horizontal final
                hojas_limpias[nombre_hoja] = df_procesado
                print(f" -> Guardada hoja '{nombre_destino}'. Registros: {len(df_procesado)}")
            
            # 2. CONSTRUCCIÓN DE LA TABLA DE HECHOS MEDIANTE UN MERGE HORIZONTAL (JOINS)
            print("\nUnificando hojas mediante cruces horizontales (Joins)...")
            
            # Cruzamos la Tienda con los Bancos usando el ID de transacción
            fact_finanzas = pd.merge(hojas_limpias['Tienda_Online'], 
                                     hojas_limpias['Pasarela_Bancos'], 
                                     on='ID_TRANSACCION', 
                                     how='inner')
            
            # Cruzamos el resultado con la tabla de Riesgo
            fact_finanzas = pd.merge(fact_finanzas, 
                                     hojas_limpias['Monitoreo_Riesgo'], 
                                     on='ID_TRANSACCION', 
                                     how='inner')

            # 3. Recorte y orden de las columnas analíticas finales
            columnas_finales = [
                'ID_TRANSACCION', 'FECHA_VENTA', 'ID_CLIENTE', 
                'PRODUCTO_CATEGORIA_LIMPIO', 'DISPOSITIVO_LIMPIO', 'MONTO_TOTAL',
                'METODO_PAGO', 'BANCO_EMISOR_LIMPIO', 'CODIGO_AUTORIZACION', 'CARGO_VALIDADO',
                'IP_PAIS_LIMPIA', 'SCORE_RIESGO', 'ES_FRAUDE_CONFIRMADO'
            ]
            
            # Aseguramos de extraer solo las columnas que logramos procesar bien
            columnas_existentes = [col for col in columnas_finales if col in fact_finanzas.columns]
            fact_finanzas = fact_finanzas[columnas_existentes].copy()

            # Guardamos la tabla de hechos centralizada en el mismo libro
            fact_finanzas.to_excel(writer, sheet_name='Fact_Finanzas', index=False)

        print(f"\n--- ¡ETL GLOBAL FINALIZADO CON ÉXITO! ---")
        print(f"Registros consolidados en 'Fact_Finanzas': {len(fact_finanzas)}")
        print(f"Archivo unificado guardado en: {datos_limpios}")
        return True
        
    except Exception as e:
        print(f"Hubo un error en el proceso ETL: {e}")
        return False

if __name__ == '__main__':
    proceso_etl_completo()