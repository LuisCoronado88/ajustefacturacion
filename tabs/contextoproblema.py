from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H3("Contexto Comercial y Objetivos del Proyecto", className="text-primary mb-4"),
    
    # Fila de Alerta / Diagnóstico Comercial
    dbc.Alert([
        html.H5("🚨 El Reto de la Facturación y el Control de Ingresos", className="alert-heading font-weight-bold"),
        html.P(
            "En las empresas de servicios públicos domiciliarios, las desviaciones de consumo y errores en la cadena de lectura "
            "provocan reclamaciones masivas. Cuando una reclamación es procedente, se genera un Ajuste de Facturación (Clase 1). "
            "Operar de forma reactiva inunda al equipo de auditoría con revisiones manuales e impacta directamente el flujo de caja.",
            className="mb-0"
        )
    ], color="warning", className="shadow-sm border-0 mb-4"),

    # Pilares del Problema (Cards)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("📉 Impacto Financiero", className="text-white m-0"), className="bg-danger"),
                dbc.CardBody([
                    html.P(
                        "Cada ajuste aplicado representa una pérdida o retraso en la recaudación del periodo. Detectar tarde las "
                        "anomalías crónicas de los medidores o los errores de digitación eleva el costo de fricción con el usuario.",
                        className="card-text text-muted"
                    )
                ])
            ], className="shadow-sm border-0 h-100")
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("⏳ Ineficiencia Operativa", className="text-white m-0"), className="bg-secondary"),
                dbc.CardBody([
                    html.P(
                        "Analizar un universo de más de 650,000 contratos buscando menos del 2% de casos con anomalías críticas "
                        "es humanamente imposible sin herramientas predictivas. El equipo técnico requiere un filtro quirúrgico.",
                        className="card-text text-muted"
                    )
                ])
            ], className="shadow-sm border-0 h-100")
        ], md=6),
    ], className="mb-4"),

    # Objetivos Centrales de AjustePredictor
    dbc.Card([
        dbc.CardBody([
            html.H5("🎯 Objetivos Estratégicos de AjustePredictor", className="text-primary mb-3"),
            html.Ol([
                html.Li([
                    html.Strong("Predecir con certeza: "), 
                    "Anticipar en el ciclo de precrítica si una cuenta específica presentará un ajuste el próximo mes basándose en picos físicos e historial."
                ], className="mb-2 text-muted"),
                html.Li([
                    html.Strong("Optimizar la Operación: "), 
                    "Asignar las órdenes de inspección en terreno únicamente a las cuentas que el modelo filtre con alta probabilidad de anomalía."
                ], className="mb-2 text-muted"),
                html.Li([
                    html.Strong("Blindaje Analítico: "), 
                    "Implementar un pipeline automatizado, auditable y basado en datos reales de la operación de la compañía."
                ], className="mb-2 text-muted"),
            ])
        ])
    ], className="shadow-sm border-0 mb-4")
], className="tab-content-padding")