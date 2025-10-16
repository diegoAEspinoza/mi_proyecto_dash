import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(__name__, name='Modelo de Gompertz')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Modelo de Crecimiento de Gompertz", className="card-title text-center mb-4"),
        html.P(
            "El modelo de Gompertz describe un crecimiento sigmoidal asimétrico. "
            "A diferencia del modelo logístico, la tasa de crecimiento disminuye de forma exponencial con el tiempo, "
            "por lo que la población se aproxima a la capacidad de carga de manera más suave.",
            className="text-center"
        ),
        html.Hr(),

        # Ecuaciones
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Ecuación Diferencial", className="card-title text-center"),
                html.Div(
                    html.Img(
                        src=r"https://latex.codecogs.com/svg.latex?\frac{dP}{dt}=rP\ln\left(\frac{K}{P}\right)",
                        style={'height': '50px', 'display': 'block', 'margin': '10px auto'}
                    ),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Solución de la E.D.O.", className="card-title text-center"),
                html.Div(
                    html.Img(
                        src=r"https://latex.codecogs.com/svg.latex?P(t)=K\,e^{-\ln\left(\frac{K}{P_0}\right)e^{-rt}}",
                        style={'height': '60px', 'display': 'block', 'margin': '10px auto'}
                    ),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),

        # Usos y puntos críticos
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("¿Cuándo se usa?", className="card-title text-center"),
                dcc.Markdown("""
                    * **Biología:** Crecimiento de tumores o bacterias.
                    * **Demografía:** Crecimiento poblacional.
                    * **Economía:** Difusión de tecnologías.
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

        # Variables
        dbc.Row([
            dbc.Col(
                dbc.Card(dbc.CardBody([
                    html.H5("Descripción de Variables", className="card-title text-center"),
                    dcc.Markdown("""
                        * **P(t):** Población en el tiempo t.
                        * **P₀:** Población inicial (en t=0).
                        * **K:** Capacidad de carga.
                        * **r:** Tasa de crecimiento intrínseca.
                        * **t:** Tiempo.
                    """, style={'paddingLeft': '20px'})
                ]), style=INFO_CARD_STYLE)
            ),
        ], className="mb-4"),

        html.Hr(className="my-4"),

        # Parámetros + gráfica
        dbc.Row([
            dbc.Col([
                html.H4("Parámetros", className="text-center fw-bold mb-3"),
                dbc.Label("Población Inicial (P₀):", className="small"),
                dcc.Input(id='gom-initial-pop-input', type='number', value=10, min=1,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                dbc.Label("Tasa de Crecimiento (r):", className="small"),
                dcc.Input(id='gom-rate-input', type='number', value=0.15, min=0.01, step=0.01,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                dbc.Label("Capacidad de Carga (K):", className="small"),
                dcc.Input(id='gom-capacity-input', type='number', value=150, min=10,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
            ], md=3),

            dbc.Col(
                dcc.Graph(id='gompertz-graph', style={'height': '100%'}),
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
    Output('gompertz-graph', 'figure'),
    [Input('gom-initial-pop-input', 'value'),
     Input('gom-rate-input', 'value'),
     Input('gom-capacity-input', 'value')]
)
def update_gompertz_graph(p0, r, k):
    if p0 is None or r is None or k is None:
        return dash.no_update

    if p0 >= k:
        p0 = k / 2

    t = np.linspace(0, 60, 400)
    P = k * np.exp(-np.log(k / p0) * np.exp(-r * t))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines',
        line=dict(color='purple', width=2),
        name='Ecuación de Gompertz'
    ))

    fig.add_trace(go.Scatter(
        x=[t[0], t[-1]], y=[k, k], mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name='Capacidad de carga (K)'
    ))

    fig.update_layout(
        title_text="Modelo de Gompertz: dP/dt = rP ln(K/P)",
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
        plot_bgcolor='lavender'
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='purple', gridcolor='lightgray')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='purple', gridcolor='lightgray')

    return fig
