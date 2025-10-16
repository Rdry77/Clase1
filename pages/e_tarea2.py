import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc 
# Importa tu función utilitaria
from utils.functions import build_logistic_figure
dash.register_page(__name__, path='/pagina4', name='Pagina 4')

layout = dbc.Container([
     dbc.Row([
        dbc.Col([
            html.H2("Modelo Mejorado - Separado por funciones", className="text-center my-4")
        ])
    ]),
    dbc.Row([
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Parámetros del modelo"),
                dbc.CardBody([
                    dbc.Label("Población inicial P(0):"),
                    dbc.Input(id="input-p0", type="number", value=200, className="mb-2"),

                    dbc.Label("Tasa de crecimiento (r):"),
                    dbc.Input(id="input-r", type="number", value=0.04, className="mb-2"),

                    dbc.Label("Capacidad de carga (K):"),
                    dbc.Input(id="input-k", type="number", value=750, className="mb-2"),

                    dbc.Label("Tiempo máximo (t):"),
                    dbc.Input(id="input-t", type="number", value=100, className="mb-3"),

                    dbc.Button("Generar gráfica", id="btn-generar", color="primary", className="w-100")
                ])
            ], className="shadow")
        ], md=4),

        # === COLUMNA DERECHA: GRÁFICA ===
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Gráfica del modelo"),
                dbc.CardBody([
                    dcc.Graph(
                        id='grafica-poblacion2',
                        style={'height': '350px', 'width': '100%'}
                    )
                ])
            ], className="shadow")
        ], md=8)
    ], className="mt-4")
], fluid=True)


@dash.callback(
    Output('grafica-poblacion2', 'figure'),
    Input('btn-generar', 'n_clicks'),
    State('input-p0', 'value'),
    State('input-r', 'value'),
    State('input-k', 'value'),
    State('input-t', 'value'),
    prevent_initial_call=False
)
def actualizar_grafica(n_clicks, P0, r, K, t_max):
    if None in (P0, r, K, t_max):
        # Devuelve figura vacía o un placeholder si faltan datos
        return build_logistic_figure(0, 0.0, 1, 1)  # o go.Figure()
    # Delegas todo el dibujo a la función de utils
    return build_logistic_figure(P0, r, K, t_max, npoints=20)


