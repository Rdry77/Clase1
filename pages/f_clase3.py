from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash
import plotly.graph_objects as go
import numpy as np
dash.register_page(__name__, path='/pagina5', name='Campo Vectorial')

layout = dbc.Container([
    dbc.Row([
        # ------------------ COLUMNA IZQUIERDA (controles) ------------------
        dbc.Col([
            html.H2("Campo Vectorial 2D", className="text-primary fw-bold my-3"),

            html.Div([
                html.Label("Ecuación dx/dt =", className="form-label fw-semibold"),
                dcc.Input(id="input-fx", type="text", value="np.sin(X)",
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Ecuación dy/dt =", className="form-label fw-semibold"),
                dcc.Input(id="input-fy", type="text", value="np.cos(X)",
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Rango del Eje X:", className="form-label fw-semibold"),
                dcc.Input(id="input-xmax", type="number", value=5,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Rango del Eje Y:", className="form-label fw-semibold"),
                dcc.Input(id="input-ymax", type="number", value=5,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Div([
                html.Label("Mallado", className="form-label fw-semibold"),
                dcc.Input(id="input-n", type="number", value=15,
                          className="form-control", debounce=True)
            ], className="mb-3"),

            html.Button("Generar campo", id="btn-generar",
                        className="btn btn-primary w-100 my-2"),

            dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5("Ejemplos para probar:", className="fw-bold text-primary mb-0")
                    ),
                    dbc.CardBody([
                        html.P("• dx/dt = X,  dy/dt = Y", className="mb-2"),
                        html.P("• dx/dt = -Y, dy/dt = X", className="mb-2"),
                        html.P("• dx/dt = X*Y, dy/dt = np.cos(Y)", className="mb-0"),
                    ])
                ],
                className="shadow-sm border-0 mt-3"
            ),
        ], md=4, lg=4),  # <-- IZQUIERDA

        # ------------------ COLUMNA DERECHA (gráfico) ------------------
        dbc.Col([
            html.H2("Visualización del Campo Vectorial",
                    className="text-primary fw-bold my-3"),
            dcc.Graph(
                id="grafica-campo",
                style={"height": "460px", "width": "100%"},
                className="border rounded shadow-sm"
            ),
            html.Div(id='info-campo')
        ], md=8, lg=8)  # <-- DERECHA
    ], className="g-4")   # g-4 = espacio horizontal entre columnas
], fluid=True)

@dash.callback(
    Output("grafica-campo", "figure"),
    Output("info-campo", "children"),
    Input("btn-generar", "n_clicks"),
    State("input-fx", "value"),
    State("input-fy", "value"),
    State("input-xmax", "value"),
    State("input-ymax", "value"),
    State("input-n", "value"),
    prevent_initial_call=False
)

def graficar_campo(n_clicks, fx_str, fy_str, xmax, ymax, n):
    # Crear el mallado (rejilla)
    x = np.linspace(-xmax, xmax, n)
    y = np.linspace(-ymax, ymax, n)
    X, Y = np.meshgrid(x, y)
    info_mensaje = ""

    try:
        # Diccionario de funciones disponibles para eval()
        diccionario = {
            'X': X,
            'Y': Y,
            'np': np,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'exp': np.exp,
            'sqrt': np.sqrt
        }

        
        fx = eval(fx_str, {}, diccionario)
        fy = eval(fy_str, {}, diccionario)

        
        mag_max = np.max(np.sqrt(fx**2 + fy**2))
        mag_min = np.min(np.sqrt(fx**2 + fy**2))

   
        info_mensaje = f"Magnitud: min = {mag_min:.2f}, max = {mag_max:.2f}"

    except Exception as error:
        fx = np.zeros_like(X)
        fy = np.zeros_like(Y)
        info_mensaje = f"Error en las expresiones: {str(error)}"

    fig = go.Figure()

    for i in range(n):
        for j in range(n):
            # Puntos iniciales (x0, y0)
            x0, y0 = X[i, j], Y[i, j]
            # Puntos finales (x1, y1)
            x1, y1 = x0 + fx[i, j], y0 + fy[i, j]

            # Agregar una línea con marcador (flecha)
            fig.add_trace(go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines+markers",
                line=dict(color="blue", width=2),
                marker=dict(size=[3, 5], color=["blue", "red"]),
                showlegend=False,
                hovertemplate=(
                    f"Punto: ({x0:.1f}, {y0:.1f})<br>"
                    f"Vector: ({fx[i, j]:.2f}, {fy[i, j]:.2f})"
                )
            ))

    fig.update_layout(
    title=dict(
        text=f"<b>Campo Vectorial:</b> dx/dt = {fx_str}, dy/dt = {fy_str}",
        font=dict(size=16, color="green"),
        x=0.5  # Centra el título
    ),
    xaxis_title="x",
    yaxis_title="y",
    paper_bgcolor="lightyellow",  # Fondo del área total
    plot_bgcolor="white",         # Fondo del área del gráfico
    font=dict(family="Outfit", size=12),
    margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightpink',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='red',
        range=[-xmax * 1.1, xmax * 1.1]
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightpink',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='red',
        range=[-ymax * 1.1, ymax * 1.1]
    )
    return fig, info_mensaje