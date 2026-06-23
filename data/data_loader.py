import pandas as pd
import numpy as np
import os

def load_and_clean_data():
    posibles_rutas = [
        os.path.join('data', 'DataAjuste_variableajustada.csv'),
        'DataAjuste_variableajustada.csv',
        os.path.join('data', 'DataAjuste.csv')
    ]
    
    df = None
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            for sep in [';', ',']:
                try:
                    df = pd.read_csv(ruta, encoding='latin1', sep=sep, decimal=',', on_bad_lines='skip')
                    if len(df.columns) > 1:
                        print(f"📖 Dataset cargado con éxito. Columnas encontradas: {len(df.columns)}")
                        break
                except Exception:
                    continue
            if df is not None:
                break
            
    if df is None:
        print("⚠️ Archivo no encontrado. Iniciando simulación con el diccionario completo de variables...")
        np.random.seed(42)
        n_samples = 10000
        df = pd.DataFrame({
            'CUENTA': range(1, n_samples + 1),
            'ACD_CODIGO': np.random.choice(['Sabanalarga', 'Barranquilla', 'Soledad'], size=n_samples),
            'CICLO': np.random.randint(1, 10, size=n_samples),
            'CATEGORIA': np.random.choice(['1', '2', '3', '4'], p=[0.5, 0.3, 0.15, 0.05], size=n_samples),
            'PLAN_FACTURACION': np.random.choice(['Residencial', 'Comercial'], size=n_samples),
            'FACTURACION_PROMEDIO': np.random.exponential(scale=120000, size=n_samples),
            'M3_PROMEDIO': np.random.normal(loc=22, scale=8, size=n_samples).clip(0),
            'VALOR_PAGO_PROMEDIO': np.random.exponential(scale=115000, size=n_samples),
            'FACTURACION_PERIODO': np.random.exponential(scale=125000, size=n_samples),
            'M3_PERIODO': np.random.normal(loc=23, scale=9, size=n_samples).clip(0),
            'CANTIDAD_AJUSTES_ULT_6_MESES': np.random.choice([0, 1, 2, 3], p=[0.8, 0.12, 0.06, 0.02], size=n_samples),
            'VALOR_AJUSTE_PROMEDIO': np.random.exponential(scale=30000, size=n_samples),
            'AJUSTE_EN_ULT_6_MESES': np.random.choice([0, 1], p=[0.8, 0.2], size=n_samples),
            'VALOR_AJUSTE_PERIODO': np.random.choice([0, 1], p=[0.98, 0.02], size=n_samples)
        })

    # 1. Limpieza de nombres de columnas
    df.columns = df.columns.str.strip().str.upper()
    
    # 2. Conversión Estricta a Numéricos (Manejando comas decimales latinas)
    columnas_numericas = [
        'FACTURACION_PROMEDIO', 'M3_PROMEDIO', 'VALOR_PAGO_PROMEDIO', 
        'FACTURACION_PERIODO', 'M3_PERIODO', 'CANTIDAD_AJUSTES_ULT_6_MESES', 
        'VALOR_AJUSTE_PROMEDIO', 'AJUSTE_EN_ULT_6_MESES', 'VALOR_AJUSTE_PERIODO'
    ]
    
    for col in columnas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    # Forzar la variable objetivo a entero binario (0 o 1)
    if 'VALOR_AJUSTE_PERIODO' in df.columns:
        df['VALOR_AJUSTE_PERIODO'] = df['VALOR_AJUSTE_PERIODO'].astype(int)

    # 3. 🔥 INGENIERÍA DE CARACTERÍSTICAS SENIOR (Feature Engineering)
    # Creamos indicadores de anomalías basados en las reglas del negocio de servicios públicos
    if 'M3_PERIODO' in df.columns and 'M3_PROMEDIO' in df.columns:
        df['DESVIACION_M3'] = df['M3_PERIODO'] - df['M3_PROMEDIO']
        df['ALERTA_ALTO_CONSUMO'] = np.where(df['M3_PERIODO'] > (df['M3_PROMEDIO'] * 1.5), 1, 0)
        
    if 'FACTURACION_PERIODO' in df.columns and 'FACTURACION_PROMEDIO' in df.columns:
        df['DESVIACION_FACTURACION'] = df['FACTURACION_PERIODO'] - df['FACTURACION_PROMEDIO']

    return df