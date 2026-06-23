from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def get_layout(df):
    # Asegurar tipos de datos correctos
    df['VALOR_AJUSTE_PERIODO'] = pd.to_numeric(df['VALOR_AJUSTE_PERIODO'], errors='coerce').fillna(0).astype(int)
    df['AJUSTE_EN_ULT_6_MESES'] = pd.to_numeric(df['AJUSTE_EN_ULT_6_MESES'], errors='coerce').fillna(0).astype(int)
    
    # --- GRÁFICO 1: Proporción Real (Desbalanceo) ---
    conteo_clases = df['VALOR_AJUSTE_PERIODO'].value_counts().reset_index()
    conteo_clases.columns = ['Estado', 'Total_Usuarios']
    conteo_clases['Estado'] = conteo_clases['Estado'].map({0: 'Sin Ajuste (98.72%)', 1: 'Con Ajuste (1.28%)'})
    
    fig_proporcion = px.pie(
        conteo_clases, values='Total_Usuarios', names='Estado',
        title="Radiografía: El Reto del Desbalanceo",
        color='Estado', color_discrete_map={'Sin Ajuste (98.72%)': '#2c3e50', 'Con Ajuste (1.28%)': '#e74c3c'},
        hole=0.4
    )
    fig_proporcion.update_layout(template="plotly_white", margin=dict(t=50, b=20, l=20, r=20))

    # --- GRÁFICO 2: Desviación de Consumo ---
    df_sample = df.sample(n=min(20000, len(df)), random_state=42)
    fig_desviacion = px.box(
        df_sample, x='VALOR_AJUSTE_PERIODO', y='DESVIACION_M3',
        color='VALOR_AJUSTE_PERIODO',
        title="Impacto de la Desviación de Consumo (M3)",
        color_discrete_map={0: "#34495e", 1: "#e74c3c"},
        labels={'VALOR_AJUSTE_PERIODO': '¿Sufrió Ajuste?', 'DESVIACION_M3': 'Desviación en M3'}
    )
    fig_desviacion.update_layout(template="plotly_white", margin=dict(t=50, b=40, l=40, r=40))

    # --- 🔥 NUEVO GRÁFICO 3: Análisis de Reincidencia Comercial ---
    # Agrupamos para ver la relación entre ajustes pasados y el ajuste del periodo actual
    df_reincidencia = df.groupby(['AJUSTE_EN_ULT_6_MESES', 'VALOR_AJUSTE_PERIODO']).size().reset_index(name='Cuentas')
    df_reincidencia['Ajuste Semestre Anterior'] = df_reincidencia['AJUSTE_EN_ULT_6_MESES'].map({0: 'Sin Ajustes Previos', 1: 'Con Ajustes Previos'})
    df_reincidencia['Ajuste Mes Actual'] = df_reincidencia['VALOR_AJUSTE_PERIODO'].map({0: 'Estable (0)', 1: 'Requiere Ajuste (1)'})

    fig_reincidencia = px.bar(
        df_reincidencia, x='Ajuste Semestre Anterior', y='Cuentas', color='Ajuste Mes Actual',
        title="Patrón de Reincidencia: Historial Semestral vs Ajuste Actual",
        barmode='group',
        color_discrete_map={'Estable (0)': '#34495e', 'Requiere Ajuste (1)': '#e74c3c'},
        text_auto='.2s'
    )
    fig_reincidencia.update_layout(template="plotly_white", margin=dict(t=50, b=40, l=40, r=40))

    return html.Div([
        html.H3("Análisis Exploratorio de Datos Senior - Control de Pérdidas", className="text-primary mb-4"),
        html.P([
            "Visualizaciones estratégicas del universo de 659,856 registros. ",
            "Los gráficos demuestran que las anomalías no son eventos aislados, sino patrones predecibles ligados a picos de consumo y reincidencia histórica."
        ], className="text-muted mb-4"),
        
        # Fila 1: Distribución y Reincidencia
        dbc.Row([
            dbc.Col([
                dbc.Card([dbc.CardBody([dcc.Graph(figure=fig_proporcion)])], className="shadow-sm border-0 mb-4")
            ], md=5),
            dbc.Col([
                dbc.Card([dbc.CardBody([dcc.Graph(figure=fig_reincidencia)])], className="shadow-sm border-0 mb-4")
            ], md=7)
        ]),
        
        # Fila 2: Análisis de Desviaciones Físicas
        dbc.Row([
            dbc.Col([
                dbc.Card([dbc.CardBody([dcc.Graph(figure=fig_desviacion)])], className="shadow-sm border-0 mb-4")
            ], md=12)
        ])
    ], className="tab-content-padding")