from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H3("Metodología de Ingeniería de Datos y Modelado", className="text-primary mb-4"),
    html.P(
        "Para garantizar que el modelo no memorice los datos (overfitting) y responda con total fiabilidad en producción, "
        "diseñamos un flujo metodológico senior dividido en cuatro fases estrictas:",
        className="text-muted mb-4"
    ),

    # Fases del Flujo Metodológico (Estructura de Bloques Secuenciales)
    dbc.Row([
        # Fase 1
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("FASE 1", className="badge bg-primary text-white mb-2"),
                    html.H5("Ingesta y Limpieza", className="text-dark font-weight-bold"),
                    html.P(
                        "Procesamiento del archivo plano (659,856 registros). Corrección automática de formatos decimales latinos "
                        "(conversión de textos con coma ',' a flotantes matemáticos puros) y remoción de ruidos de lectura.",
                        className="small text-muted"
                    )
                ])
            ], className="shadow-sm border-0 mb-3 h-100")
        ], md=3),

        # Fase 2
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("FASE 2", className="badge bg-info text-white mb-2"),
                    html.H5("Ingeniería Senior", className="text-dark font-weight-bold"),
                    html.P(
                        "Creación de variables de contraste comercial: DESVIACION_M3 (Consumo del periodo vs histórico) y "
                        "cruces con el historial semestral de reclamaciones ganadas por el usuario.",
                        className="small text-muted"
                    )
                ])
            ], className="shadow-sm border-0 mb-3 h-100")
        ], md=3),

        # Fase 3
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("FASE 3", className="badge bg-warning text-dark mb-2"),
                    html.H5("Validación Cruzada", className="text-dark font-weight-bold"),
                    html.P(
                        "Estrategia Stratified 5-Fold. Dividimos el dataset en 5 bloques, manteniendo el 1.28% de la clase positiva "
                        "homogéneo en cada uno, garantizando evaluaciones honestas con datos nunca antes vistos.",
                        className="small text-muted"
                    )
                ])
            ], className="shadow-sm border-0 mb-3 h-100")
        ], md=3),

        # Fase 4
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("FASE 4", className="badge bg-success text-white mb-2"),
                    html.H5("Optimización F1", className="text-dark font-weight-bold"),
                    html.P(
                        "Descarte de la Exactitud Global. Competencia de algoritmos donde coronamos a Gradient Boosting debido "
                        "a su excelente balance (F1-Score del 43.84%) impulsado por su precisión quirúrgica del 88.07%.",
                        className="small text-muted"
                    )
                ])
            ], className="shadow-sm border-0 mb-3 h-100")
        ], md=3),
    ], className="mb-4"),

    # Recuadro Técnico de Arquitectura de Software
    dbc.Card([
        dbc.CardHeader(html.H6("⚙️ Arquitectura de Software del Pipeline", className="m-0 font-weight-bold")),
        dbc.CardBody([
            html.P(
                "La solución está estructurada bajo el principio de separación de responsabilidades. Los módulos de backend "
                "(data_loader.py y train_models.py) aíslan la lógica matemática del modelo, mientras que la interfaz Dash actúa "
                "como un consumidor desacoplado en tiempo real. Esto permite actualizar el cerebro predictivo sin alterar la experiencia del usuario.",
                className="card-text small text-muted", style={"text-align": "justify"}
            )
        ], className="bg-light")
    ], className="border-0 shadow-sm")
], className="tab-content-padding")