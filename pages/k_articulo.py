# pages/seir_tablas_beta.py
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import solve_ivp

# ==================== Registrar página multipage ====================
dash.register_page(__name__, path="/seir-tablas", name="SEIR (Tablas y β)")

# ==================== Modelo SEIR normalizado ====================

def seir_rhs(t, y, beta, mu, alpha, delta, mu_i, nu):
    """
    Sistema SEIR normalizado del artículo:

      dS/dt = mu - (alpha * I + mu + nu) * S
      dE/dt = alpha * I * S - (beta + mu) * E
      dI/dt = beta * E - (mu_i + delta + mu) * I
      dR/dt = delta * I + nu * S - mu * R

    donde S, E, I, R son fracciones respecto a N.
    """
    S, E, I, R = y

    dS = mu - (alpha * I + mu + nu) * S
    dE = alpha * I * S - (beta + mu) * E
    dI = beta * E - (mu_i + delta + mu) * I
    dR = delta * I + nu * S - mu * R

    return [dS, dE, dI, dR]


def simular_seir_tablas(
    N, S0_cnt, E0_cnt, I0_cnt, R0_cnt,
    mu, alpha, delta, mu_i, nu,
    beta_list,
    tmax, npoints
):
    """
    Simula el modelo con las condiciones y parámetros dados
    para cada valor de β en beta_list.
    Devuelve:
      t, resultados_expuestos, resultados_infectados
    donde resultados_expuestos / infectados son listas de arrays:
      [E_beta1(t)*N, E_beta2(t)*N, ...], etc.
    """
    # Normalizar condiciones iniciales (fracciones respecto a N)
    N  = float(N)
    S0 = float(S0_cnt) / N
    E0 = float(E0_cnt) / N
    I0 = float(I0_cnt) / N
    R0 = float(R0_cnt) / N

    y0 = [S0, E0, I0, R0]

    mu    = float(mu)
    alpha = float(alpha)
    delta = float(delta)
    mu_i  = float(mu_i)
    nu    = float(nu)

    tmax    = max(float(tmax), 1.0)
    npoints = int(max(npoints, 10))
    t_eval  = np.linspace(0, tmax, npoints)

    resultados_E = []
    resultados_I = []

    for beta in beta_list:
        beta = float(beta)
        sol = solve_ivp(
            lambda t, y: seir_rhs(t, y, beta, mu, alpha, delta, mu_i, nu),
            [0, tmax],
            y0,
            t_eval=t_eval,
            method="RK45"
        )
        S, E, I, R = sol.y
        # Convertir fracciones a población (como en tu código original)
        resultados_E.append(E * N)
        resultados_I.append(I * N)

    return t_eval, resultados_E, resultados_I


def make_figure_expuestos(t, resultados_E, betas, colores, etiquetas):
    fig = go.Figure()

    for E_pop, beta, color, label in zip(resultados_E, betas, colores, etiquetas):
        fig.add_trace(go.Scatter(
            x=t, y=E_pop,
            mode="lines",
            line=dict(width=2, color=color),
            name=label,
            hovertemplate="t: %{x:.2f}<br>E(t): %{y:.2f}<extra></extra>"
        ))

    fig.update_layout(
        title=dict(
            text="<b>Fig. 6 – Expuestos E(t) para distintos β</b>",
            font=dict(size=18, color="red"),
            x=0.5,
            y=0.93
        ),
        xaxis_title="Time (day)",
        yaxis_title="Exposed E(t)",
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor="#b1b1f1",
        plot_bgcolor="white",
        font=dict(family="Outfit", size=11, color="black"),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2),
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor="lightpink",
        zeroline=True, zerolinewidth=2, zerolinecolor="red",
        showline=True, linecolor="black", linewidth=2, mirror=True,
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor="lightpink",
        zeroline=True, zerolinewidth=2, zerolinecolor="red",
        showline=True, linecolor="black", linewidth=2, mirror=True,
    )

    return fig


def make_figure_infectados(t, resultados_I, betas, colores, etiquetas):
    fig = go.Figure()

    for I_pop, beta, color, label in zip(resultados_I, betas, colores, etiquetas):
        fig.add_trace(go.Scatter(
            x=t, y=I_pop,
            mode="lines",
            line=dict(width=2, color=color),
            name=label,
            hovertemplate="t: %{x:.2f}<br>I(t): %{y:.2f}<extra></extra>"
        ))

    fig.update_layout(
        title=dict(
            text="<b>Fig. 7 – Infectados I(t) para distintos β</b>",
            font=dict(size=18, color="red"),
            x=0.5,
            y=0.93
        ),
        xaxis_title="Time (day)",
        yaxis_title="Infected I(t)",
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor="#b1b1f1",
        plot_bgcolor="white",
        font=dict(family="Outfit", size=11, color="black"),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2),
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor="lightpink",
        zeroline=True, zerolinewidth=2, zerolinecolor="red",
        showline=True, linecolor="black", linewidth=2, mirror=True,
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor="lightpink",
        zeroline=True, zerolinewidth=2, zerolinecolor="red",
        showline=True, linecolor="black", linewidth=2, mirror=True,
    )

    return fig


# ==================== Layout ====================

layout = dbc.Container([
    dbc.Row([
        # Columna izquierda: explicación + parámetros
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H2("Modelo SEIR (artículo Indonesia)", className="title card-title"),
                    dcc.Markdown(
                        r"""
Esta página implementa el modelo SEIR **normalizado** usado en el artículo, con las ecuaciones:

$$\frac{dS}{dt} = \mu - (\alpha I + \mu + \nu)S$$

$$\frac{dE}{dt} = \alpha I S - (\beta + \mu)E$$

$$\frac{dI}{dt} = \beta E - (\mu_i + \delta + \mu)I$$

$$\frac{dR}{dt} = \delta I + \nu S - \mu R$$

donde $S, E, I, R$ son fracciones de la población total $N$.
Los parámetros de la Tabla 3 son, por defecto:

- $\mu = 6.25\times10^{-3}$,
- $\alpha = 0.62\times10^{-8}$,
- $\delta = 0.0006667$,
- $\mu_i = 7.344\times10^{-7}$,
- $\nu = 0.50$.

Las condiciones iniciales provienen de la Tabla 2 (normalizada). Aquí usamos
las cantidades absolutas para que tú puedas modificarlas, y luego se
normalizan internamente.
                        """,
                        mathjax=True
                    ),

                    html.Hr(),

                    html.H5("Condiciones iniciales (en personas)"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("Población total N"),
                            dcc.Input(
                                id="inp-N-tablas",
                                type="number",
                                value=269600000,  
                                inputMode="numeric",
                                pattern="[0-9]*",
                                min=1,
                                step=1000,
                                style={"width": "100%"}
                            )
                        ], md=6),
                    ], className="mb-2"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("S₀ (Susceptibles)"),
                            dcc.Input(
                                id="inp-S0-tablas",
                                type="number",
                                value=37538,
                                min=0,
                                step=1,
                                style={"width": "100%"}
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("E₀ (Expuestos)"),
                            dcc.Input(
                                id="inp-E0-tablas",
                                type="number",
                                value=13923,
                                min=0,
                                step=1,
                                style={"width": "100%"}
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("I₀ (Infectados)"),
                            dcc.Input(
                                id="inp-I0-tablas",
                                type="number",
                                value=23191,
                                min=0,
                                step=1,
                                style={"width": "100%"}
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("R₀ (Recuperados)"),
                            dcc.Input(
                                id="inp-R0-tablas",
                                type="number",
                                value=13213,
                                min=0,
                                step=1,
                                style={"width": "100%"}
                            )
                        ], md=3),
                    ], className="mb-3"),

                    html.H5("Parámetros de la Tabla 3"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("μ (natalidad/mortalidad)"),
                            dcc.Input(
                                id="inp-mu-tablas",
                                type="number",
                                value=6.25e-3,
                                step=1e-4,
                                style={"width": "100%"}
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("α (contagio S→E)"),
                            dcc.Input(
                                id="inp-alpha-tablas",
                                type="number",
                                value=0.62e-8,
                                step=1e-9,
                                style={"width": "100%"}
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("δ (recuperación I→R)"),
                            dcc.Input(
                                id="inp-delta-tablas",
                                type="number",
                                value=0.0006667,
                                step=1e-4,
                                style={"width": "100%"}
                            )
                        ], md=4),
                    ], className="mb-2"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("μᵢ (mortalidad por COVID)"),
                            dcc.Input(
                                id="inp-mui-tablas",
                                type="number",
                                value=7.344e-7,
                                step=1e-7,
                                style={"width": "100%"}
                            )
                        ], md=6),
                        dbc.Col([
                            html.Label("ν (vacunación)"),
                            dcc.Input(
                                id="inp-nu-tablas",
                                type="number",
                                value=0.50,
                                step=0.05,
                                style={"width": "100%"}
                            )
                        ], md=6),
                    ], className="mb-3"),

                    html.H5("Valores de β para comparar"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("β₁"),
                            dcc.Input(
                                id="inp-beta1-tablas",
                                type="number",
                                value=1/3,
                                step=0.05,
                                style={"width": "100%"}
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("β₂"),
                            dcc.Input(
                                id="inp-beta2-tablas",
                                type="number",
                                value=1/7,
                                step=0.05,
                                style={"width": "100%"}
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("β₃"),
                            dcc.Input(
                                id="inp-beta3-tablas",
                                type="number",
                                value=1/14,
                                step=0.05,
                                style={"width": "100%"}
                            )
                        ], md=4),
                    ], className="mb-3"),

                    html.H5("Rango de tiempo"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("Tiempo máximo (días)"),
                            dcc.Input(
                                id="inp-tmax-tablas",
                                type="number",
                                value=60,
                                min=1,
                                step=1,
                                style={"width": "100%"}
                            )
                        ], md=6),
                        dbc.Col([
                            html.Label("Puntos de la simulación"),
                            dcc.Slider(
                                id="inp-npoints-tablas",
                                min=200,
                                max=2000,
                                step=100,
                                value=1500,
                                marks={200: "200", 1500: "1500", 2000: "2000"}
                            )
                        ], md=6),
                    ], className="mb-2"),
                ])
            ),
            className="mb-4", md=6
        ),

        # Columna derecha: gráficos
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H2("Gráficas E(t) e I(t) para distintos β", className="title card-title"),

                    dcc.Graph(
                        id="graph-expuestos-tablas",
                        style={"height": "320px", "width": "100%"}
                    ),

                    dcc.Graph(
                        id="graph-infectados-tablas",
                        style={"height": "320px", "width": "100%"}
                    ),

                    html.Div(
                        id="info-tablas",
                        style={"marginTop": "6px", "color": "#333"}
                    )
                ])
            ),
            className="mb-4", md=6
        ),
    ])
], fluid=True)


# ==================== Callback ====================

@dash.callback(
    Output("graph-expuestos-tablas", "figure"),
    Output("graph-infectados-tablas", "figure"),
    Output("info-tablas", "children"),
    Input("inp-N-tablas", "value"),
    Input("inp-S0-tablas", "value"),
    Input("inp-E0-tablas", "value"),
    Input("inp-I0-tablas", "value"),
    Input("inp-R0-tablas", "value"),
    Input("inp-mu-tablas", "value"),
    Input("inp-alpha-tablas", "value"),
    Input("inp-delta-tablas", "value"),
    Input("inp-mui-tablas", "value"),
    Input("inp-nu-tablas", "value"),
    Input("inp-beta1-tablas", "value"),
    Input("inp-beta2-tablas", "value"),
    Input("inp-beta3-tablas", "value"),
    Input("inp-tmax-tablas", "value"),
    Input("inp-npoints-tablas", "value"),
)
def update_seir_tablas(
    N, S0, E0, I0, R0,
    mu, alpha, delta, mu_i, nu,
    beta1, beta2, beta3,
    tmax, npoints
):
    # Valores por defecto si vienen None
    N     = 100000   if N     is None else N
    S0    = 37538    if S0    is None else S0
    E0    = 13923    if E0    is None else E0
    I0    = 23191    if I0    is None else I0
    R0    = 13213    if R0    is None else R0
    mu    = 6.25e-3  if mu    is None else mu
    alpha = 0.62e-8  if alpha is None else alpha
    delta = 0.0006667 if delta is None else delta
    mu_i  = 7.344e-7 if mu_i  is None else mu_i
    nu    = 0.50     if nu    is None else nu
    beta1 = 1/3      if beta1 is None else beta1
    beta2 = 1/7      if beta2 is None else beta2
    beta3 = 1/14     if beta3 is None else beta3
    tmax  = 60       if tmax  is None else tmax
    npoints = 1500   if npoints is None else npoints

    betas = [beta1, beta2, beta3]
    etiquetas = [
        f"β₁ = {beta1:.4f}",
        f"β₂ = {beta2:.4f}",
        f"β₃ = {beta3:.4f}",
    ]
    colores = ["magenta", "black", "blue"]

    t, resultados_E, resultados_I = simular_seir_tablas(
        N, S0, E0, I0, R0,
        mu, alpha, delta, mu_i, nu,
        betas,
        tmax, npoints
    )

    fig_E = make_figure_expuestos(t, resultados_E, betas, colores, etiquetas)
    fig_I = make_figure_infectados(t, resultados_I, betas, colores, etiquetas)

    info = (
        "Simulación SEIR normalizado con parámetros de Tabla 3.  "
        f"N={N:g}, S₀={S0:g}, E₀={E0:g}, I₀={I0:g}, R₀={R0:g}, "
        f"μ={mu:.5g}, α={alpha:.5g}, δ={delta:.5g}, μᵢ={mu_i:.5g}, ν={nu:.3g}.  "
        f"β₁={beta1:.5g}, β₂={beta2:.5g}, β₃={beta3:.5g}, "
        f"t_max={tmax:g}, puntos={int(npoints)}.  "
        "Las curvas muestran E(t)·N (arriba) e I(t)·N (abajo) para cada valor de β."
    )

    return fig_E, fig_I, info
