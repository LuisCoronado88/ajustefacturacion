import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Importar capas de datos y layouts modulares de las pestañas
from data.data_loader import load_and_clean_data
from tabs import contextoproblema, metodologia, eda, Modelo

# 1. Inicializar la aplicación Dash con un tema nativo Bootstrap profesional (FLATLY)
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    title="AjustePredictor - Dashboard Corporativo"
)
server = app.server

# 2. Carga unificada de datos estructurados globales (650k filas de facturación)
df_global = load_and_clean_data()

# 3. Diseño del Layout Principal (Navbar + Contenedor de Tabs + Footer)
app.layout = dbc.Container([
    # Encabezado Corporativo (Navbar) - Corregido sin el argumento 'fluid' directo
    dbc.Navbar([
        dbc.Container([
            html.A(
                dbc.Row([
                  #  dbc.Col(html.Img(src="https://cdn-icons-png.flaticon.com/512/3208/3208726.png", height="40px")),
                    dbc.Col(dbc.NavbarBrand("AJUSTE-PREDICTOR", className="ms-2 text-white h3 font-weight-bold")),
                ], align="center", className="g-0"),
                href="#", style={"textDecoration": "none"}
            ),
            html.Span("Módulo Analítico de Control de Ingresos", className="text-white-50 navbar-text d-none d-md-block")
        ], fluid=True)
    ], className="navbar-custom navbar-dark mb-4 py-2"),
    
    # Navegación Principal por Pestañas (Tabs)
    dbc.Tabs([
        dbc.Tab(label="Contexto del Problema", tab_id="tab-contexto"),
        dbc.Tab(label="Metodología ML", tab_id="tab-metodologia"),
        dbc.Tab(label="Análisis de Datos (EDA)", tab_id="tab-eda"),
        dbc.Tab(label="Evaluación del Modelo", tab_id="tab-modelo"),
    ], id="tabs-navegacion", active_tab="tab-contexto", className="mb-3"),
    
    # Contenedor Dinámico donde se inyectará el layout de la pestaña activa
    html.Div(id="contenedor-pestaña-activa"),
    
    # Footer Institucional
    html.Footer([
        html.Hr(),
        html.P("© 2026 Panel Analítico AjustePredictor. Todos los derechos reservados.", className="text-center text-muted small")
    ], className="mt-5")
], fluid=True)

# 4. Callback Orquestador de Navegación de Pestañas
@app.callback(
    Output("contenedor-pestaña-activa", "children"),
    Input("tabs-navegacion", "active_tab")
)
def renderizar_contenido_pestañas(tab_id):
    if tab_id == "tab-contexto":
        return contextoproblema.layout
    elif tab_id == "tab-metodologia":
        return metodologia.layout
    elif tab_id == "tab-eda":
        return eda.get_layout(df_global)
    elif tab_id == "tab-modelo":
        return Modelo.layout
    return html.Div("Error: Pestaña no encontrada.")

# 5. Lanzar el Servidor en modo de desarrollo local (Sintaxis Moderna Dash v2.x)
if __name__ == "__main__":
    app.run(debug=True, port=8050)