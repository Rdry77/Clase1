from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path='/pagina7', name='Modelo SEIR')

# -------------------- UI --------------------
layout = dbc.Container([
    dbc.Row([
        # Columna izquierda: controles
        dbc.Col([
            html.H2("Modelo SEIR - Epidemiología", className="text-primary fw-bold my-3"),

            html.Div([
                html.Label("Población Total (N):", className="form-label fw-semibold"),
                dcc.Input(id="seir-N", type="number", value=1000,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Tasa de transmisión (β):", className="form-label fw-semibold"),
                dcc.Input(id="seir-beta", type="number", value=0.3, step=0.01,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Tasa de incubación (σ):", className="form-label fw-semibold"),
                dcc.Input(id="seir-sigma", type="number", value=0.2, step=0.01,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Tasa de recuperación (ɣ):", className="form-label fw-semibold"),
                dcc.Input(id="seir-gamma", type="number", value=0.1, step=0.01,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Expuestos iniciales (E₀):", className="form-label fw-semibold"),
                dcc.Input(id="seir-E0", type="number", value=0,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Infectados iniciales (I₀):", className="form-label fw-semibold"),
                dcc.Input(id="seir-I0", type="number", value=1,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Tiempo de simulación (días):", className="form-label fw-semibold"),
                dcc.Input(id="seir-tiempo", type="number", value=160,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Button("Simular Epidemia", id="seir-btn", className="btn btn-primary w-100 my-2"),

        ], md=4, lg=4),

        # Columna derecha: figura
        dbc.Col([
            html.H2("Evolución del Modelo SEIR", className="text-primary fw-bold my-3"),
            dcc.Graph(
                id="grafica-seir",
                style={"height": "460px", "width": "100%"},
                className="border rounded shadow-sm"
            )
        ], md=8, lg=8)
    ], className="g-4")
], fluid=True)

# -------------------- ODEs SEIR --------------------
def seir_rhs(y, t, beta, sigma, gamma, N):
    """
    y = [S, E, I, R]
    S' = -β S I / N
    E' =  β S I / N - σ E
    I' =  σ E - γ I
    R' =  γ I
    """
    S, E, I, R = y
    dS = -beta * S * I / N
    dE =  beta * S * I / N - sigma * E
    dI =  sigma * E - gamma * I
    dR =  gamma * I
    return [dS, dE, dI, dR]

# -------------------- Callback --------------------
@dash.callback(
    Output("grafica-seir", "figure"),
    Input("seir-btn", "n_clicks"),
    State("seir-N", "value"),
    State("seir-beta", "value"),
    State("seir-sigma", "value"),
    State("seir-gamma", "value"),
    State("seir-E0", "value"),
    State("seir-I0", "value"),
    State("seir-tiempo", "value"),
    prevent_initial_call=False
)
def simular_seir(n_clicks, N, beta, sigma, gamma, E0, I0, tiempo_max):
    # Condiciones iniciales
    S0 = N - E0 - I0
    R0 = 0
    y0 = [S0, E0, I0, R0]

    # Vector de tiempo
    t = np.linspace(0, tiempo_max, 300)

    # Resolver SEIR
    try:
        sol = odeint(seir_rhs, y0, t, args=(beta, sigma, gamma, N))
        S, E, I, R = sol.T
    except Exception as e:
        # Fallback en caso de error numérico
        print(f"Error en la simulación SEIR: {e}")
        S = np.full_like(t, S0)
        E = np.full_like(t, E0)
        I = np.full_like(t, I0)
        R = np.full_like(t, R0)

    # Figura
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode="lines", name="Susceptibles",
                             line=dict(color="royalblue", width=2),
                             hovertemplate='Día: %{x:.0f}<br>S: %{y:.0f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=t, y=E, mode="lines", name="Expuestos",
                             line=dict(color="orange", width=2),
                             hovertemplate='Día: %{x:.0f}<br>E: %{y:.0f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=t, y=I, mode="lines", name="Infectados",
                             line=dict(color="crimson", width=2),
                             hovertemplate='Día: %{x:.0f}<br>I: %{y:.0f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=t, y=R, mode="lines", name="Recuperados",
                             line=dict(color="seagreen", width=2),
                             hovertemplate='Día: %{x:.0f}<br>R: %{y:.0f}<extra></extra>'))

    # Estilo igual que el SIR que ya usas
    fig.update_layout(
        title=dict(text="<b>Evolución del Modelo SEIR</b>", x=0.5,
                   font=dict(size=16, color="darkblue")),
        xaxis_title="Tiempo (días)",
        yaxis_title="Número de personas",
        paper_bgcolor="lightgray",
        plot_bgcolor="white",
        font=dict(family="Outfit", size=12),
        legend=dict(orientation="h", yanchor="bottom", xanchor="right", y=1.02, x=0.5),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightpink',
                     zeroline=True, zerolinewidth=2, zerolinecolor='black')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightpink',
                     zeroline=True, zerolinewidth=2, zerolinecolor='black')

    return fig
