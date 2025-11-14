import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
import requests
import datetime as dt

dash.register_page(__name__, path='/pagina8', name='Covid-19')


layout = dbc.Container([
    # Título
    dbc.Row([
        dbc.Col([
            html.H2(
                "Dashboard Covid-19",
                className="text-center text-primary fw-bold mb-4"
            ),
        ])
    ]),

    
    dbc.Row([

        # --------- COLUMNA IZQUIERDA ----------
        dbc.Col([
            html.Div([

               
                html.Label("Seleccione el país:", className="form-label fw-semibold mb-2"),
                dcc.Dropdown(
                    id="dropdown-pais",
                    options=[
                        {"label": "Perú", "value": "Peru"},
                        {"label": "México", "value": "Mexico"},
                        {"label": "Estados Unidos", "value": "USA"},
                        {"label": "Canadá", "value": "Canada"},
                    ],
                    value="Peru",
                    className="mb-3",
                    style={"width": "100%"}
                ),

               
                html.Label("Días históricos", className="form-label fw-semibold mb-2"),
                dcc.Dropdown(
                    id="dropdown-dias-covid",
                    options=[
                        {"label": "30 días", "value": 30},
                        {"label": "60 días", "value": 60},
                        {"label": "90 días", "value": 90},
                        {"label": "120 días", "value": 120},
                        {"label": "Todo el historial", "value": "all"},
                    ],
                    value=30,
                    className="mb-3",
                    style={"width": "100%"}
                ),

                
                dbc.Button(
                    "Actualizar Datos",
                    id="btn-actualizar-covid",
                    color="primary",
                    className="w-100 mb-3"
                ),

                
                html.Div(
                    id="info-actualizado-covid",
                    className="text-muted small"
                ),
            ], className="p-2")
        ], md=4, lg=4),

        # --------- COLUMNA DERECHA ----------
        dbc.Col([

            # Tarjetas
            dbc.Row([

                # Total casos
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Total casos", className="fw-bold text-secondary mb-1"),
                            html.H2(id="total-casos", className="fw-bold text-primary")
                        ])
                    ], className="shadow-sm text-center border-0",
                       style={"backgroundColor": "#f2f5fd"})
                ], md=6, lg=6, className="mb-3"),

                # Casos nuevos
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Casos nuevos", className="fw-bold text-warning mb-1"),
                            html.H2(id="casos-nuevos", className="fw-bold",
                                    style={"color": "#ff3838"})
                        ])
                    ], className="shadow-sm text-center border-0",
                       style={"backgroundColor": "#fff2e6"})
                ], md=6, lg=6, className="mb-3"),

               
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Total muertes", className="fw-bold mb-1",
                                    style={"color": "#d64545"}),
                            html.H2(id="total-muertes", className="fw-bold",
                                    style={"color": "#a31212"})
                        ])
                    ], className="shadow-sm text-center border-0",
                       style={"backgroundColor": "#fce2e2"})
                ], md=6, lg=6, className="mb-3"),

                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Recuperados", className="fw-bold mb-1",
                                    style={"color": "#58a85b"}),
                            html.H2(id="total-recuperados", className="fw-bold",
                                    style={"color": "#138f3b"})
                        ])
                    ], className="shadow-sm text-center border-0",
                       style={"backgroundColor": "#e8f9e8"})
                ], md=6, lg=6, className="mb-3"),
            ]),

          
            dcc.Graph(
                id="grafico-covid",
                style={"height": "460px", "width": "100%"},
                className="border rounded shadow-sm"
            )
        ], md=8, lg=8),

    ], className="g-4")

], fluid=True)



def obtener_datos_pais(pais):
    try:
        url = f"https://disease.sh/v3/covid-19/countries/{pais}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos del país {pais}: {e}")
        return None


def obtener_historico_pais(pais, dias):
    try:
        url = f"https://disease.sh/v3/covid-19/historical/{pais}"
        params = {"lastdays": dias}     # puede ser número o 'all'
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener histórico del país {pais}: {e}")
        return None


def formatear_numero(numero):
    """Devuelve el número con separador de miles o 'N/A' si viene vacío."""
    if numero is None:
        return "N/A"
    try:
        return f"{int(numero):,}".replace(",", ".")
    except Exception:
        return str(numero)



@dash.callback(
    Output("total-casos", "children"),
    Output("casos-nuevos", "children"),
    Output("total-muertes", "children"),
    Output("total-recuperados", "children"),
    Output("grafico-covid", "figure"),
    Output("info-actualizado-covid", "children"),
    Input("btn-actualizar-covid", "n_clicks"),
    State("dropdown-pais", "value"),
    State("dropdown-dias-covid", "value"),
    prevent_initial_call=True
)
def actualizar_dashboard_covid(n_clicks, pais, dias):

    datos_actuales = obtener_datos_pais(pais)
    historico = obtener_historico_pais(pais, dias)

 
    if not datos_actuales or not historico:
        fig = go.Figure()
        fig.add_annotation(
            text="❗ Error al obtener datos",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=15, color="red")
        )
        fig.update_layout(
            paper_bgcolor="lightcyan",
            plot_bgcolor="white"
        )
        return "N/A", "N/A", "N/A", "N/A", fig, "No se pudieron actualizar los datos."

  
    total_casos       = datos_actuales.get("cases", 0)
    casos_hoy         = datos_actuales.get("todayCases", 0)
    total_muertes     = datos_actuales.get("deaths", 0)
    total_recuperados = datos_actuales.get("recovered", 0)

    total_casos_text       = formatear_numero(total_casos)
    casos_hoy_text         = formatear_numero(casos_hoy)
    total_muertes_text     = formatear_numero(total_muertes)
    total_recuperados_text = formatear_numero(total_recuperados)


    timeline = historico.get("timeline", {})

  
    if isinstance(timeline, dict):
        casos_historicos   = timeline.get("cases", {})
        muertes_historicas = timeline.get("deaths", {})
    else:
        # Si viene lista, cogemos el primero
        casos_historicos   = historico[0]["timeline"]["cases"]
        muertes_historicas = historico[0]["timeline"]["deaths"]

    fechas          = list(casos_historicos.keys())
    valores_casos   = list(casos_historicos.values())
    valores_muertes = list(muertes_historicas.values())

    
    if not fechas:
        fig = go.Figure()
        fig.add_annotation(
            text="Sin datos históricos disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )
        fig.update_layout(template="plotly_white")
        return (total_casos_text, casos_hoy_text,
                total_muertes_text, total_recuperados_text,
                fig,
                f"Datos actualizados para {pais}, pero sin histórico.")

    
    fechas_dt = [dt.datetime.strptime(fecha, "%m/%d/%y") for fecha in fechas]

  
    fig = go.Figure()

   
    fig.add_trace(go.Scatter(
        x=fechas_dt,
        y=valores_casos,
        mode="lines",
        name="Casos Totales",
        line=dict(color="orange", width=2),
        hovertemplate="Fecha: %{x|%d %b %Y}<br>Casos: %{y}<extra></extra>"
    ))

   
    fig.add_trace(go.Scatter(
        x=fechas_dt,
        y=valores_muertes,
        mode="lines",
        name="Muertes Totales",
        line=dict(color="red", width=2),
        hovertemplate="Fecha: %{x|%d %b %Y}<br>Muertes: %{y}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>Evolución Covid-19 en {pais}</b>",
            x=0.5
        ),
        xaxis_title="Fecha",
        yaxis_title="Número de personas",
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return (
        total_casos_text,
        casos_hoy_text,
        total_muertes_text,
        total_recuperados_text,
        fig,
        f"Datos actualizados para {pais}."
    )
