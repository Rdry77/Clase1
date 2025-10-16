# pages/logistico_interactivo.py
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

# --- Página multipage (puedes cambiar el path/name si quieres) ---
dash.register_page(__name__, path='/pagina2', name='Pagina 2', order=2)

# ---------- Helpers ----------
def logistic_solution(t, P0, r, K):
    # P(t) = K / (1 + ((K-P0)/P0) * exp(-r t))
    P0 = float(P0)
    r  = float(r)
    K  = float(K)
    t  = np.asarray(t, dtype=float)

    # Evitar división por cero y valores negativos absurdos
    if P0 <= 0:
        return np.zeros_like(t)
    if K <= 0:
        return np.zeros_like(t)

    return K / (1.0 + ((K - P0) / P0) * np.exp(-r * t))

def make_figure(P0, r, K, tmax, npoints):
    tmax = max(float(tmax), 1.0)
    npoints = int(max(npoints, 10))
    t = np.linspace(0, tmax, npoints)
    P = logistic_solution(t, P0, r, K)

    trace = go.Scatter(
        x=t, y=P,
        mode='lines+markers',
        line=dict(dash='solid', color='black', width=2),
        marker=dict(color='blue', symbol='circle', size=8),
        name='P(t) logístico',
        hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
    )

    fig = go.Figure(data=trace)

    # Línea de capacidad de carga
    fig.add_hline(
        y=K,
        line_dash="dot",
        line_color="gray",
        annotation_text="K (capacidad de carga)",
        annotation_position="top left"
    )

    fig.update_layout(
        title=dict(text='<b>Crecimiento de la población</b>', font=dict(size=20, color='red'), x=0.5, y=0.93),
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor='#b1b1f1',
        plot_bgcolor='white',
        font=dict(family='Outfit', size=11, color='black'),
        showlegend=False
    )
    fig.update_xaxes(
    range=[0, 250], 
    showgrid=True, gridwidth=1, gridcolor='lightpink',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True,
    )
    fig.update_yaxes(
        range=[100, 1000], 
        showgrid=True, gridwidth=1, gridcolor='lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='red',
        showline=True, linecolor='black', linewidth=2, mirror=True,
    )

    return fig

# ---------- Layout ----------
layout = dbc.Container([
    dbc.Row([
        # Texto descriptivo
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H2("Crecimiento de la población y capacidad de carga", className="title card-title"),
                    dcc.Markdown(
                        r"""
Para modelar el crecimiento de una población con **recursos limitados**, introducimos las variables principales. 
La variable $t$ representa el **tiempo**, y $P(t)$ la **población** en dicho tiempo. Si $P(t)$ es diferenciable, 
entonces su primera derivada $\frac{dP}{dt}$ es la **tasa instantánea de cambio** de la población.

Cuando existe un límite ambiental, llamado **capacidad de carga** $K>0$, la población no puede crecer indefinidamente. 
El **modelo logístico de Verhulst** incorpora este límite mediante la ecuación diferencial
$
\frac{dP}{dt} = r\,P\!\left(1-\frac{P}{K}\right),
$
donde $r>0$ es la **tasa intrínseca de crecimiento**. 


Con condición inicial $P(0)=P_0$, la **solución explícita** es
$
P(t)=\frac{K}{\,1+\left(\frac{K-P_0}{P_0}\right)e^{-rt}}.
$



                        """,
                        mathjax=True
                    ),
                ]),
                className="h-100"
            ),
            className="mb-4", md=6
        ),

        # Controles + gráfica
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H2("Gráfica", className="title card-title"),

                    # Controles
                    dbc.Row([
                        dbc.Col([
                            html.Label("Población inicial P₀"),
                            dcc.Input(id="inp-P0", type="number", value=100, min=0, step=1, style={"width":"100%"})
                        ], md=4),
                        dbc.Col([
                            html.Label("Tasa r"),
                            dcc.Input(id="inp-r", type="number", value=0.03, step=0.005, style={"width":"100%"})
                        ], md=4),
                        dbc.Col([
                            html.Label("Capacidad de carga K"),
                            dcc.Input(id="inp-K", type="number", value=1000, min=1, step=10, style={"width":"100%"})
                        ], md=4),
                    ], className="mb-2"),

                    dbc.Row([
                        dbc.Col([
                            html.Label("Tiempo máximo"),
                            dcc.Input(id="inp-tmax", type="number", value=300, min=1, step=5, style={"width":"100%"})
                        ], md=6),
                        dbc.Col([
                            html.Label("Puntos de la curva"),
                            dcc.Slider(id="inp-npoints", min=20, max=500, step=10, value=20,
                                       marks={20:"20", 200:"200", 500:"500"})
                        ], md=6),
                    ], className="mb-3"),

                    dcc.Graph(id="graph-logistico", style={'height': '360px', 'width': '100%'}),

                    html.Div(id="info-logistico", style={"marginTop":"6px","color":"#333"})
                ])
            ),
            className="mb-4", md=6
        ),
    ])
], fluid=True)

# ---------- Callbacks ----------
@dash.callback(
    Output("graph-logistico", "figure"),
    Output("info-logistico", "children"),
    Input("inp-P0", "value"),
    Input("inp-r", "value"),
    Input("inp-K", "value"),
    Input("inp-tmax", "value"),
    Input("inp-npoints", "value"),
)
def update_graph(P0, r, K, tmax, npoints):
    # Sane defaults
    P0 = 0 if P0 is None else P0
    r  = 0.0 if r is None else r
    K  = 1.0 if K is None else K
    tmax = 100 if tmax is None else tmax
    npoints = 200 if npoints is None else npoints

    fig = make_figure(P0, r, K, tmax, npoints)

    info = (
        f"Modelo: dP/dt = r·P·(1 - P/K).  "
        f"Solución: P(t) = K / (1 + ((K - P₀)/P₀) e^(-r t)).  "
        f"Usando P₀={P0:g}, r={r:g}, K={K:g}, t_max={tmax:g}, puntos={npoints}."
    )
    return fig, info

# ---------- Ejecutar standalone (opcional) ----------
if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = layout
    app.run_server(debug=True)
