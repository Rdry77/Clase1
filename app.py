import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
]

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets
)

# ===============================
# NAVBAR con menú hamburguesa lateral
# ===============================
navbar = dbc.Navbar(
    dbc.Container(
        [
            # Botón hamburguesa (solo móvil/tablet)
            dbc.Button(
                html.I(className="fa fa-bars fa-lg"),
                id="open-offcanvas",
                color="dark",
                className="d-lg-none ms-auto"  # Solo aparece en pantallas pequeñas
            ),

            # Menú normal (pantallas grandes)
            dbc.Nav(
    [
        dbc.NavLink(page["name"], href=page["relative_path"], active="exact")
        for page in dash.page_registry.values()
    ],
    className="ms-auto d-none d-lg-flex nav-small-text",  # 🔥 clase añadida
    pills=True,
),

        ],
        fluid=True
    ),
    color="light",
    dark=False,
    className="border-bottom mb-4"
)

# ===============================
# OFFCANVAS (menú lateral)
# ===============================
offcanvas = dbc.Offcanvas(
    [
        dbc.Nav(
            [
                dbc.NavLink(page["name"], href=page["relative_path"], active="exact", className="my-2")
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="offcanvas-dark-links"
        )
    ],
    id="offcanvas-menu",
    title="Menú",
    placement="start",
    is_open=False,
    className="offcanvas-dark"  # <--- ESTA CLASE ES CLAVE
)


# ===============================
# LAYOUT PRINCIPAL
# ===============================
app.layout = html.Div([

    # 🎯 TÍTULO PRINCIPAL DE LA PÁGINA
    html.H1(
        "Técnicas de Modelamiento Matemático",
        className="text-center mt-4 mb-4",   # centrado + margenes
        style={"fontWeight": "bold", "fontSize": "2.5rem"}
    ),

    navbar,        # Barra de navegación responsiva
    offcanvas,     # Menú lateral
    dash.page_container  # El contenido de cada página
])


# ===============================
# CALLBACK OFFCANVAS
# ===============================
@app.callback(
    Output("offcanvas-menu", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    State("offcanvas-menu", "is_open"),
    prevent_initial_call=True
)
def toggle_offcanvas(n, is_open):
    return not is_open


# ===============================
# RUN
# ===============================
if __name__ == '__main__':
    app.run(debug=True)
