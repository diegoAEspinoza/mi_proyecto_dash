import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(__name__, name='Modelo Logístico')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Modelo de Crecimiento Logístico", className="card-title text-center mb-4"),
        html.P(
            "El modelo logístico es una mejora realista del modelo exponencial. Introduce un factor crucial: la 'capacidad de carga' (K), que es el tamaño máximo de población que un entorno puede sostener.",
            className="text-center"
        ),
        html.Hr(),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Ecuación Diferencial", className="card-title text-center"),
                html.Div(
                    html.Img(src=r"https://latex.codecogs.com/svg.latex?\frac{dP}{dt}=rP(1-\frac{P}{K})", style={'height': '50px', 'display': 'block', 'margin': '10px auto'}),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Solución de la E.D.O.", className="card-title text-center"),
                html.Div(
                    html.Img(src=r"https://latex.codecogs.com/svg.latex?P(t)=\frac{K}{1+\left(\frac{K-P_0}{P_0}\right)e^{-rt}}", style={'height': '60px', 'display': 'block', 'margin': '10px auto'}),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("¿Cuándo se usa?", className="card-title text-center"),
                dcc.Markdown("""
                    * **Ecología:** Crecimiento de poblaciones.
                    * **Negocios:** Adopción de productos.
                    * **Medicina:** Crecimiento de tumores.
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Puntos Críticos", className="card-title text-center"),
                dcc.Markdown("""
                    * **P = 0:** Equilibrio **inestable**.
                    * **P = K:** Equilibrio **estable** (atractor).
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card(dbc.CardBody([
                    html.H5("Descripción de Variables", className="card-title text-center"),
                    dcc.Markdown("""
                        * **P(t):** Población en el tiempo t.
                        * **P₀:** Población inicial (en t=0).
                        * **K:** Capacidad de carga del sistema.
                        * **r:** Tasa de crecimiento intrínseca.
                        * **t:** Tiempo.
                    """, style={'paddingLeft': '20px'})
                ]), style=INFO_CARD_STYLE)
            ),
        ], className="mb-4"),

        html.Hr(className="my-4"),
        dbc.Row([
            dbc.Col([
                html.H4("Parámetros", className="text-center fw-bold mb-3"),
                dbc.Label("Población Inicial (P₀):", className="small"),
                dcc.Input(id='log-initial-pop-input', type='number', value=10, min=1, style=INPUT_STYLE_COMPACT, className="mb-3"),
                dbc.Label("Tasa de Crecimiento (r):", className="small"),
                dcc.Input(id='log-rate-input', type='number', value=0.15, min=0.01, step=0.01, style=INPUT_STYLE_COMPACT, className="mb-3"),
                dbc.Label("Capacidad de Carga (K):", className="small"),
                dcc.Input(id='log-capacity-input', type='number', value=150, min=10, style=INPUT_STYLE_COMPACT, className="mb-3"),
            ], md=3),
            dbc.Col(
                dcc.Graph(id='logistic-graph', style={'height': '100%'}),
                md=9
            ),
        ], align="center", className="mt-4"),
    ]),
    className="m-4",
)

layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap'
    ),
    html.Div(
        page_content,
        style={'fontFamily': 'Outfit, sans-serif'}
    )
])

@callback(
    Output('logistic-graph', 'figure'),
    [Input('log-initial-pop-input', 'value'),
     Input('log-rate-input', 'value'),
     Input('log-capacity-input', 'value')]
)
def update_logistic_graph(p0, r, k):
    if p0 is None or r is None or k is None:
        return dash.no_update
    
    if p0 >= k:
        p0 = k / 2

    t = np.linspace(0, 60, 400)
    P = k / (1 + ((k - p0) / p0) * np.exp(-r * t))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines',
        line=dict(color='blue', width=2),
        name='Ecuación Logística'
    ))
    
    fig.add_trace(go.Scatter(
        x=[t[0], t[-1]], y=[k, k], mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name='Capacidad de carga'
    ))
    
    fig.add_trace(go.Scatter(
        x=[t[0], t[-1]],
        y=[P[0], P[-1]],
        mode='markers',
        marker=dict(color='black', size=10),
        showlegend=False
    ))
    
    fig.update_layout(
        title_text="Campo de vectores de dP/dt = rP(1 - P/K)",
        title_x=0.5,
        xaxis_title="Tiempo (t)",
        yaxis_title="Población (P)",
        template="plotly_white",
        height=550,
        font=dict(family="Outfit, sans-serif"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=20, t=60, b=40),
        plot_bgcolor='lightblue'
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='red', gridcolor='lightgray')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='red', gridcolor='lightgray')
    
    return fig  