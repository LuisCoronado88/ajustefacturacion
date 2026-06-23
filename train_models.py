import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from data.data_loader import load_and_clean_data

print("🚀 Iniciando Pipeline Senior Multi-Variable para Datos Desbalanceados...")
df = load_and_clean_data()

# Definir columnas predictoras según tu lista detallada
features_numericas = [
    'FACTURACION_PROMEDIO', 'M3_PROMEDIO', 'VALOR_PAGO_PROMEDIO', 
    'FACTURACION_PERIODO', 'M3_PERIODO', 'CANTIDAD_AJUSTES_ULT_6_MESES', 
    'VALOR_AJUSTE_PROMEDIO', 'AJUSTE_EN_ULT_6_MESES',
    'DESVIACION_M3', 'DESVIACION_FACTURACION', 'ALERTA_ALTO_CONSUMO'
]

features_categoricas = ['ACD_CODIGO', 'CICLO', 'CATEGORIA', 'PLAN_FACTURACION']

# Filtrar solo las que realmente existan en el CSV para evitar caídas
features_num_reales = [c for c in features_numericas if c in df.columns]
features_cat_reales = [c for c in features_categoricas if c in df.columns]

X = df[features_num_reales + features_cat_reales]
y = df['VALOR_AJUSTE_PERIODO']

print(f"📊 Variables Numéricas: {len(features_num_reales)} | Categóricas: {len(features_cat_reales)}")
print(f"⚖️ Balance de clases: Sin Ajuste (0): {list(y).count(0)} | Con Ajuste (1): {list(y).count(1)}")

# Preprocesamiento avanzado en paralelo
preprocesador = ColumnTransformer(transformers=[
    ('num', StandardScaler(), features_num_reales),
    ('cat', OneHotEncoder(handle_unknown='ignore'), features_cat_reales)
])

# Estrategia de validación para proteger el desbalanceo (1.28% de unos)
cv_estrategia = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

modelos = {
    'Regresión Logística (Balanced)': LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
    'Random Forest (Balanced)': RandomForestClassifier(class_weight='balanced', n_estimators=100, max_depth=10, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
}

metricas = ['accuracy', 'precision', 'recall', 'f1']
resultados = {}

print("\n🏋️ Evaluando modelos mediante Validación Cruzada Estratificada...")
for nombre, modelo in modelos.items():
    pipeline_completo = Pipeline([
        ('preprocesador', preprocesador),
        ('clasificador', modelo)
    ])
    
    scores = cross_validate(pipeline_completo, X, y, cv=cv_estrategia, scoring=metricas, n_jobs=-1)
    
    resultados[nombre] = {
        'F1-Score (Métrica Selección)': np.mean(scores['test_f1']),
        'Recall (Atrapar Ajustes)': np.mean(scores['test_recall']),
        'Precision (Evitar Falsas Alarmas)': np.mean(scores['test_precision']),
        'Accuracy Global': np.mean(scores['test_accuracy'])
    }

print("\n🏆 RESULTADOS FINALES DE LA ARQUITECTURA SENIOR:")
df_res = pd.DataFrame(resultados).T.sort_values(by='F1-Score (Métrica Selección)', ascending=False)
print(df_res.to_string())
print(f"\n🎯 El modelo ganador absoluto para producción es: {df_res.index[0]}")