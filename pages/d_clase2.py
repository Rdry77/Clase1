import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/pagina3', name='Pagina 3')

layout = dbc.Container([
    dbc.Row([
        # === COLUMNA IZQUIERDA: PARÁMETROS ===
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
                        id='grafica-poblacion',
                        style={'height': '350px', 'width': '100%'}
                    )
                ])
            ], className="shadow")
        ], md=8)
    ], className="mt-4")
], fluid=True)




### Callbacks ###
@dash.callback(
    Output('grafica-poblacion', 'figure'),
    Input('btn-generar', 'n_clicks'),
    State('input-p0', 'value'),
    State('input-r', 'value'),
    State('input-k', 'value'),
    State('input-t', 'value'),
    prevent_initial_call=False
)
def actualizar_grafica(n_clicks, P0, r, K, t_max):
    # Generar los valores de tiempo
    t = np.linspace(0, t_max, 20)

    # Ecuacion
    P = (P0 * K * np.exp(r * t)) / ((K - P0) + P0 * np.exp(r * t))

    # Crear grafico de la poblacion
    trace_poblacion = go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        name='P(t)',
        line=dict(
            color='black',
            width=2
        ),
        marker=dict(
            size=6,
            color='blue',
            symbol='circle'
        ),
        hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
    )

    # Crear grafico de la capacidad de carga
    trace_capacidad = go.Scatter(
        x=[0, t_max],
        y=[K, K],
        mode='lines',
        name='K',
        line=dict(
            color='red',
            width=2,
            dash='dot'
        ),
        hovertemplate='K: %{y:.2f}<extra></extra>'
    )

    fig = go.Figure(data=[trace_poblacion, trace_capacidad])

    return fig


