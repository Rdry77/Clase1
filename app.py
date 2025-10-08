import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# app = dash.Dash(__name__, use_pages=True)
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Técnicas de Modelamiento Matemático", className="app-header"),
    
    # Contenedor para la Navegación y la Línea
    html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink(page['name'], href=page["relative_path"], active="exact")
                    for page in dash.page_registry.values()
                ],
                # La clase mb-3 añade un pequeño margen inferior
                className="nav-navigation",
                horizontal=True,
            ),
        ],
        # La clase border-bottom añade una línea horizontal en la parte inferior
        className="border-bottom mb-3" 
    ),
    
    dash.page_container
], className="container-fluid")

if __name__ == '__main__':
    app.run(debug=True)