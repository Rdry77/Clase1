import numpy as np
import plotly.graph_objects as go

def build_logistic_figure(P0: float, r: float, K: float, t_max: float, npoints: int = 200) -> go.Figure:
    """Devuelve la figura del modelo logístico con línea horizontal en K."""
    # Tiempo
    t = np.linspace(0, float(t_max), int(npoints))

    # Modelo logístico
    P = (P0 * K * np.exp(r * t)) / ((K - P0) + P0 * np.exp(r * t))

    # Trace población
    trace_poblacion = go.Scatter(
        x=t, y=P, mode='lines+markers', name='P(t)',
        line=dict(color='black', width=2),
        marker=dict(size=6, color='blue', symbol='circle'),
        hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
    )

    # Trace capacidad de carga
    trace_capacidad = go.Scatter(
        x=[0, t_max], y=[K, K], mode='lines', name='K',
        line=dict(color='red', width=2, dash='dot'),
        hovertemplate='K: %{y:.2f}<extra></extra>'
    )

    fig = go.Figure(data=[trace_poblacion, trace_capacidad])
    fig.update_layout(
        title="Modelo mejorado",
        xaxis_title="t",
        yaxis_title="P(t)",
        margin=dict(l=40, r=20, t=40, b=40)
    )

    fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='lightpink',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True,
    )

    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='red',
        showline=True, linecolor='black', linewidth=2, mirror=True,
    )
    return fig
