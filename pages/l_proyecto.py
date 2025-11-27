import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go

dash.register_page(__name__, path="/sir-adopcion", name="Modelo SIR – Adopción App")

# ===============================================================
# Modelo SIR de adopción (β, γ, α)
# ===============================================================
def sir_rhs(t, y, beta, gamma, alpha, N):
    S, I, R = y
    dS = -(beta * S * I / N) - alpha * S
    dI = (beta * S * I / N) + alpha * S - gamma * I
    dR = gamma * I
    return [dS, dI, dR]


def simular_sir(N, S0, I0, R0, beta, gamma, alpha, tmax=120):
    y0 = [S0, I0, R0]
    t_eval = np.linspace(0, tmax, 1000)

    sol = solve_ivp(
        lambda t, y: sir_rhs(t, y, beta, gamma, alpha, N),
        [0, tmax], y0, t_eval=t_eval
    )

    return sol.t, sol.y

# ===============================================================
# Layout
# ===============================================================
layout = dbc.Container([
    dbc.Row([
        # =========================================
        # COLUMNA IZQUIERDA
        # =========================================
        dbc.Col(
            dbc.Card(
                dbc.CardBody([

                    html.H2("Modelo SIR para adopción de una app", className="card-title"),

                    dcc.Markdown(
    r"""
Este modelo describe la adopción de una aplicación entre estudiantes: 
- \( S(t) \): No usuarios potenciales 
- \( I(t) \): Usuarios activos que recomiendan la app 
- \( R(t) \): Usuarios pasivos o saturados 

Las ecuaciones del modelo son:

$$\frac{dS}{dt} = -\beta \frac{SI}{N} - \alpha S$$

$$\frac{dI}{dt} = \beta \frac{SI}{N} + \alpha S - \gamma I$$

$$\frac{dR}{dt} = \gamma I$$
    """,
    mathjax=True
),

                    html.Hr(),
                    html.H4("Condiciones iniciales"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("Población total N"),
                            dcc.Input(id="sirN", type="number", value=266, min=1, style={"width": "100%"})
                        ], md=4),
                        dbc.Col([
                            html.Label("S₀ (no usuarios)"),
                            dcc.Input(id="sirS0", type="number", value=261, min=0, style={"width": "100%"})
                        ], md=4),
                        dbc.Col([
                            html.Label("I₀ (activos)"),
                            dcc.Input(id="sirI0", type="number", value=5, min=0, style={"width": "100%"})
                        ], md=4),
                    ], className="mb-3"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("R₀ (pasivos)"),
                            dcc.Input(id="sirR0", type="number", value=0, min=0, style={"width": "100%"})
                        ], md=4),
                    ], className="mb-3"),

                    html.H4("Parámetros"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("β (contacto social)"),
                            dcc.Input(id="sirBeta", type="number", value=0.35, step=0.01,
                                      style={"width": "100%"})
                        ], md=4),

                        dbc.Col([
                            html.Label("γ (abandono)"),
                            dcc.Input(id="sirGamma", type="number", value=0.08, step=0.01,
                                      style={"width": "100%"})
                        ], md=4),

                        dbc.Col([
                            html.Label("α (adopción externa)"),
                            dcc.Input(id="sirAlpha", type="number", value=0.01, step=0.005,
                                      style={"width": "100%"})
                        ], md=4),
                    ]),

                    html.Hr(),
                    html.H5("Exploración de parámetros"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("β valores"),
                            dcc.Input(id="sirBetaList", type="text",
                                      value="0.20,0.35,0.50",
                                      style={"width": "100%"} )
                        ], md=6),
                        dbc.Col([
                            html.Label("γ valores"),
                            dcc.Input(id="sirGammaList", type="text",
                                      value="0.05,0.08,0.20",
                                      style={"width": "100%"} )
                        ], md=6),
                    ], className="mb-3"),

                ])
            ),
            md=5
        ),

        # =========================================
        # COLUMNA DERECHA – GRÁFICOS ORGANIZADOS
        # =========================================
        dbc.Col(
            dbc.Card(
                dbc.CardBody([

                    html.H3("Resultados del modelo", className="card-title"),

                    # ----------- FILA 1 (dos gráficos) ---------------
                    dbc.Row([
                        dbc.Col(
                            dcc.Graph(id="sir-baseline",
                                      style={"height": "320px", "width": "100%"}),
                            md=6
                        ),
                        dbc.Col(
                            dcc.Graph(id="sir-beta",
                                      style={"height": "320px", "width": "100%"}),
                            md=6
                        )
                    ], className="mb-3"),

                    # ----------- FILA 2 (un gráfico ancho) ----------
                    dbc.Row([
                        dbc.Col(
                            dcc.Graph(id="sir-gamma",
                                      style={"height": "320px", "width": "100%"}),
                            md=12
                        )
                    ]),

                ])
            ),
            md=7
        )
    ])
], fluid=True)


# ===============================================================
# CALLBACK
# ===============================================================
@dash.callback(
    Output("sir-baseline", "figure"),
    Output("sir-beta", "figure"),
    Output("sir-gamma", "figure"),
    Input("sirN", "value"),
    Input("sirS0", "value"),
    Input("sirI0", "value"),
    Input("sirR0", "value"),
    Input("sirBeta", "value"),
    Input("sirGamma", "value"),
    Input("sirAlpha", "value"),
    Input("sirBetaList", "value"),
    Input("sirGammaList", "value"),
)
def actualizar(N, S0, I0, R0, beta, gamma, alpha, betaList, gammaList):

    # ---------------- baseline ----------------
    t, (S, I, R) = simular_sir(N, S0, I0, R0, beta, gamma, alpha)

    fig_base = go.Figure()
    fig_base.add_trace(go.Scatter(x=t, y=S, name="S(t)", line=dict(color="orange")))
    fig_base.add_trace(go.Scatter(x=t, y=I, name="I(t)", line=dict(color="blue")))
    fig_base.add_trace(go.Scatter(x=t, y=R, name="R(t)", line=dict(color="green")))
    fig_base.update_layout(title="Adopción tecnológica (baseline)",
                           xaxis_title="Tiempo (días)", yaxis_title="Personas")

    # ---------------- variando β ----------------
    beta_vals = [float(x) for x in betaList.split(",")]
    fig_beta = go.Figure()

    for b in beta_vals:
        t2, (_, I2, _) = simular_sir(N, S0, I0, R0, b, gamma, alpha)
        fig_beta.add_trace(go.Scatter(x=t2, y=I2, name=f"I(t), beta={b}"))
    fig_beta.update_layout(title="Efecto de aumentar β (contacto social)",
                           xaxis_title="Tiempo (días)", yaxis_title="Adoptantes activos")

    # ---------------- variando γ ----------------
    gamma_vals = [float(x) for x in gammaList.split(",")]
    fig_gamma = go.Figure()

    for g in gamma_vals:
        t3, (_, I3, _) = simular_sir(N, S0, I0, R0, beta, g, alpha)
        fig_gamma.add_trace(go.Scatter(x=t3, y=I3, name=f"I(t), gamma={g}"))
    fig_gamma.update_layout(title="Efecto de aumentar γ (abandono)",
                            xaxis_title="Tiempo (días)", yaxis_title="Adoptantes activos")

    return fig_base, fig_beta, fig_gamma
