import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import requests
import datetime as dt


dash.register_page(__name__, path="/pagina_clima_pe", name="TAREA API (Clima-Peru)")


CIUDADES_PE = {
    "Lima": (-12.0464, -77.0428),
    "Arequipa": (-16.4090, -71.5375),
    "Cusco": (-13.5319, -71.9675),
    "Trujillo": (-8.1117, -79.0288),
    "Piura": (-5.1945, -80.6328),
    "Chiclayo": (-6.7714, -79.8409),
    "Huancayo": (-12.0651, -75.2049),
    "Iquitos": (-3.7491, -73.2538),
    "Tacna": (-18.0066, -70.2463),
    "Puno": (-15.8402, -70.0219),
}


VAR_API = {
    "temperatura": "temperature_2m",
    "humedad": "relativehumidity_2m",
    "viento": "windspeed_10m",
}


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Dashboard del Clima (Perú)",
                    className="text-center text-primary fw-bold mb-4")
        ])
    ]),

    dbc.Row([

        # ====== COLUMNA IZQUIERDA: Card con entradas ======
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Parámetros de consulta",
                            className="mb-0 fw-bold text-primary")
                ),
                dbc.CardBody([

                    # Ciudad (solo Perú)
                    html.Label("Ciudad:", className="form-label fw-semibold"),
                    dcc.Dropdown(
                        id="dropdown-ciudad-pe",
                        options=[
                            {"label": nombre, "value": nombre}
                            for nombre in CIUDADES_PE.keys()
                        ],
                        value="Lima",
                        className="mb-3",
                        style={"width": "100%"}
                    ),

                    # Variable
                    html.Label("Variable:", className="form-label fw-semibold"),
                    dcc.Dropdown(
                        id="dropdown-variable-pe",
                        options=[
                            {"label": "Temperatura (°C)", "value": "temperatura"},
                            {"label": "Humedad relativa (%)", "value": "humedad"},
                            {"label": "Velocidad del viento (km/h)", "value": "viento"},
                        ],
                        value="temperatura",
                        className="mb-3",
                        style={"width": "100%"}
                    ),

                    # Rango de horas
                    html.Label("Rango de horas:", className="form-label fw-semibold"),
                    dcc.Dropdown(
                        id="dropdown-horas-pe",
                        options=[
                            {"label": "Últimas 24 horas", "value": 24},
                            {"label": "Últimas 48 horas", "value": 48},
                            {"label": "Últimas 72 horas", "value": 72},
                            {"label": "Todo lo disponible", "value": "all"},
                        ],
                        value=24,
                        className="mb-3",
                        style={"width": "100%"}
                    ),

                    # Botón
                    dbc.Button(
                        "Actualizar clima",
                        id="btn-actualizar-clima-pe",
                        color="primary",
                        className="w-100 mb-2"
                    ),

                    # Texto de información
                    html.Div(
                        id="info-clima-pe",
                        className="text-muted small mt-1"
                    ),
                ])
            ])
        ], md=4, lg=4),

        # ====== COLUMNA DERECHA: Card con gráfico ======
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Evolución meteorológica",
                            className="mb-0 fw-bold text-primary")
                ),
                dbc.CardBody([
                    dcc.Graph(
                        id="grafico-clima-pe",
                        style={"height": "420px", "width": "100%"},
                        className="border rounded"
                    )
                ])
            ])
        ], md=8, lg=8),

    ], className="g-4"),

], fluid=True)



@dash.callback(
    Output("grafico-clima-pe", "figure"),
    Output("info-clima-pe", "children"),
    Input("btn-actualizar-clima-pe", "n_clicks"),
    State("dropdown-ciudad-pe", "value"),
    State("dropdown-horas-pe", "value"),
    State("dropdown-variable-pe", "value"),
    prevent_initial_call=True
)
def actualizar_clima_pe(n_clicks, ciudad, horas, variable):

    if n_clicks is None:
        fig_vacia = go.Figure()
        fig_vacia.add_annotation(
            text="Haz clic en 'Actualizar clima' para ver datos.",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )
        fig_vacia.update_layout(template="plotly_white")
        return fig_vacia, ""

  
    lat, lon = CIUDADES_PE.get(ciudad, CIUDADES_PE["Lima"])

   
    var_api = VAR_API[variable]


    url = "https://api.open-meteo.com/v1/forecast"
    """params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(VAR_API.values()),
        "timezone": "auto"
    }"""
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(VAR_API.values()),
        "timezone": "auto",
        "past_days": 3   
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        fig_err = go.Figure()
        fig_err.add_annotation(
            text=f"Error al obtener datos del clima: {e}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(color="red")
        )
        fig_err.update_layout(template="plotly_white")
        return fig_err, "No se pudieron obtener datos del clima."

    hourly = data.get("hourly", {})
    tiempos = hourly.get("time", [])
    valores = hourly.get(var_api, [])

 
    tiempos_dt = [dt.datetime.fromisoformat(t) for t in tiempos]

 
    ahora = dt.datetime.now(tiempos_dt[0].tzinfo)  
    tiempos_pasados = []
    valores_pasados = []

    for tt, vv in zip(tiempos_dt, valores):
        if tt <= ahora:
            tiempos_pasados.append(tt)
            valores_pasados.append(vv)

   
    if not tiempos_pasados:
        fig_vacia = go.Figure()
        fig_vacia.add_annotation(
            text="No hay datos históricos disponibles (solo pronóstico futuro).",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )
        fig_vacia.update_layout(template="plotly_white")
        return fig_vacia, "Sin datos históricos disponibles."

    
    tiempos_dt = tiempos_pasados
    valores = valores_pasados

    
    if horas != "all":
        horas = int(horas)
        if len(tiempos_dt) > horas:
            tiempos_dt = tiempos_dt[-horas:]
            valores = valores[-horas:]

    
    if variable == "temperatura":
        etiqueta_y = "Temperatura (°C)"
    elif variable == "humedad":
        etiqueta_y = "Humedad relativa (%)"
    else:
        etiqueta_y = "Velocidad del viento (km/h)"

   
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tiempos_dt,
        y=valores,
        mode="lines+markers",
        name=etiqueta_y,
        line=dict(width=2),
        hovertemplate="Fecha: %{x|%d %b %Y %H:%M}<br>Valor: %{y:.2f}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>{etiqueta_y} en {ciudad}</b>",
            x=0.5
        ),
        xaxis_title="Fecha y hora",
        yaxis_title=etiqueta_y,
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    info_texto = f"Datos actualizados para {ciudad} ({len(valores)} registros)."
    return fig, info_texto
