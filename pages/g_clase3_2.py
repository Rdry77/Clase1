from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint
dash.register_page(__name__, path='/pagina6', name='Modelo SIR')

layout = dbc.Container([
    dbc.Row([
        # ------------------ COLUMNA IZQUIERDA (controles) ------------------
        dbc.Col([
            html.H2("Modelo SIR - Epidemiologia", className="text-primary fw-bold my-3"),

            html.Div([
                html.Label("Poblacion Total (N):", className="form-label fw-semibold"),
                dcc.Input(id="input-N", type="number", value=1000,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Tasa de transmision (β)", className="form-label fw-semibold"),
                dcc.Input(id="input-beta", type="number", value=0.3, step=0.01,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Tasa de recuperacion (ɣ)", className="form-label fw-semibold"),
                dcc.Input(id="input-gamma", type="number", value=0.1,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Infectados iniciales", className="form-label fw-semibold"),
                dcc.Input(id="input-I0", type="number", value=1,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Tiempo de simulacion", className="form-label fw-semibold"),
                dcc.Input(id="input-tiempo", type="number", value=100,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Button("Simular Epidemia", id="btn-simular",
                        className="btn btn-primary w-100 my-2"),

            
        ], md=4, lg=4),  # <-- IZQUIERDA

        # ------------------ COLUMNA DERECHA (gráfico) ------------------
        dbc.Col([
            html.H2("Visualización del Campo Vectorial",
                    className="text-primary fw-bold my-3"),
            dcc.Graph(
                id="grafica-sir",
                style={"height": "460px", "width": "100%"},
                className="border rounded shadow-sm"
            )
        ], md=8, lg=8)  # <-- DERECHA
    ], className="g-4")   # g-4 = espacio horizontal entre columnas
], fluid=True)

def modelo_sir(y, t, beta, gamma, N):
    S,I,R = y

    dS_dt = -beta * S * I / N
    dI_dt = beta * S * I / N - gamma * I
    dR_dt = gamma * I

    return [dS_dt, dI_dt, dR_dt]

# --- Callback para actualizar la gráfica ---
@dash.callback(
    Output("grafica-sir", "figure"),
    Input("btn-simular", "n_clicks"),
    State("input-N", "value"),
    State("input-beta", "value"),
    State("input-gamma", "value"),
    State("input-I0", "value"),
    State("input-tiempo", "value"),
    prevent_initial_call=False
)



def simular_sir(n_clicks, N, beta, gamma, I0, tiempo_max):
    S0 = N - I0
    R0_inicial = 0
    y0 = [S0, I0, R0_inicial]

    # Crear el vector de tiempo
    t = np.linspace(0, tiempo_max, 200)

    try:
        solucion = odeint(modelo_sir, y0, t, args=(beta, gamma, N))
        S, I, R = solucion.T

    except Exception as e:
        # Si ocurre un error en la integración, generar valores constantes
        S = np.full_like(t, S0)
        I = np.full_like(t, I0)
        R = np.full_like(t, R0_inicial)
        

    # Crear la figura
    fig = go.Figure()

    # --- Curva de Susceptibles ---
    fig.add_trace(go.Scatter(
        x=t,
        y=S,
        mode="lines",
        name="Susceptibles (5)",
        line=dict(color="blue", width=2),
        hovertemplate='Día: %{x:.0f}<br>Susceptibles: %{y:.0f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=t,
        y=I,
        mode="lines",
        name="Infectados (I)",
        line=dict(color="red", width=2),
        hovertemplate='Día: %{x:.0f}<br>Infectados: %{y:.0f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=t,
        y=R,
        mode="lines",
        name="Recuperados (R)",
        line=dict(color="green", width=2),
        hovertemplate='Día: %{x:.0f}<br>Recuperados: %{y:.0f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text="<b>Evolución del Modelo SIR</b>",
            x=0.5,  # Centrar título
            font=dict(size=16, color="darkblue")
        ),
        xaxis_title="Tiempo (días)",
        yaxis_title="Número de personas",
        paper_bgcolor="lightgray",   # Fondo general
        plot_bgcolor="white",        # Fondo del área de la gráfica
        font=dict(family="Outfit", size=12),

        legend=dict(
            orientation="h",       # horizontal
            yanchor="bottom",
            xanchor="right",
            y=1.02,
            x=0.5
        ),

        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightpink',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightpink',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    )

    return fig