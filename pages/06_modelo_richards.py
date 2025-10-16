import dash 
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(__name__, name='Modelo de Richards')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Modelo de Crecimiento de Richards", className="card-title text-center mb-4"),
        html.P(
            "El modelo de Richards generaliza el crecimiento logístico al incluir un parámetro de asimetría (ν), permitiendo ajustar la forma de la curva de crecimiento a datos reales con mayor precisión.",
            className="text-center"
        ),
        html.Hr(),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Ecuación Diferencial", className="card-title text-center"),
                html.Div(
                    html.Img(src=r"https://latex.codecogs.com/svg.latex?\frac{dP}{dt}=rP\left[1-\left(\frac{P}{K}\right)^\nu\right]", 
                             style={'height': '50px', 'display': 'block', 'margin': '10px auto'}),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Solución de la E.D.O.", className="card-title text-center"),
                html.Div(
                    html.Img(src=r"https://latex.codecogs.com/svg.latex?P(t)=\frac{K}{\left[1+\left(\left(\frac{K}{P_0}\right)^\nu-1\right)e^{-r\nu t}\right]^{1/\nu}}", 
                             style={'height': '70px', 'display': 'block', 'margin': '10px auto'}),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("¿Cuándo se usa?", className="card-title text-center"),
                dcc.Markdown("""
                    * **Biología:** Crecimiento de plantas y animales.
                    * **Epidemiología:** Curvas de infección asimétricas.
                    * **Agricultura:** Modelado de rendimiento de cultivos.
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Casos Especiales", className="card-title text-center"),
                dcc.Markdown("""
                    * **ν = 1** → Modelo logístico.
                    * **ν → 0** → Modelo de Gompertz.
                    * **ν > 1** → Inflección temprana.
                    * **ν < 1** → Inflección tardía.
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
                        * **K:** Capacidad de carga (máximo asintótico).
                        * **r:** Tasa de crecimiento intrínseca.
                        * **ν (nu):** Parámetro de forma (asimetría).
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
                dcc.Input(id='richards-initial-pop-input', type='number', value=10, min=0.1, step=0.1,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                dbc.Label("Capacidad de Carga (K):", className="small"),
                dcc.Input(id='richards-k-input', type='number', value=100, min=0.1, step=0.1,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                dbc.Label("Tasa de Crecimiento (r):", className="small"),
                dcc.Input(id='richards-rate-input', type='number', value=0.2, min=0.01, step=0.01,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                dbc.Label("Parámetro de Forma (ν):", className="small"),
                dcc.Input(id='richards-nu-input', type='number', value=0.8, min=0.01, step=0.01,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                dbc.Label("Tiempo Final (tₘₐₓ):", className="small"),
                dcc.Input(id='richards-time-max-input', type='number', value=30, min=1, step=0.5,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                dbc.Label("Tiempo a Evaluar (t):", className="small"),
                dcc.Input(id='richards-time-input', type='number', value=15, min=0, step=0.1,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                html.Div(id='richards-pop-result', className="text-center fw-bold mt-3 text-primary"),
            ], md=3),
            dbc.Col(
                dcc.Graph(id='richards-graph', style={'height': '100%'}),
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
    [Output('richards-graph', 'figure'),
     Output('richards-pop-result', 'children')],
    [Input('richards-initial-pop-input', 'value'),
     Input('richards-k-input', 'value'),
     Input('richards-rate-input', 'value'),
     Input('richards-nu-input', 'value'),
     Input('richards-time-max-input', 'value'),
     Input('richards-time-input', 'value')]
)
def update_richards_graph(p0, k, r, nu, t_max, t_eval):
    if None in (p0, k, r, nu, t_max, t_eval):
        return dash.no_update, ""

    if p0 <= 0 or k <= 0 or p0 >= k:
        return dash.no_update, "⚠️ Asegúrate de que 0 < P₀ < K"
    if nu <= 0:
        return dash.no_update, "⚠️ ν debe ser > 0"

    t_eval = min(t_eval, t_max)

    t = np.linspace(0, t_max, 400)
    
    try:
        ratio = (k / p0) ** nu
        exponent = -r * nu * t
        denominator = (1 + (ratio - 1) * np.exp(exponent)) ** (1 / nu)
        P = k / denominator

        P_eval = k / ((1 + ((k / p0) ** nu - 1) * np.exp(-r * nu * t_eval)) ** (1 / nu))
    except (OverflowError, ZeroDivisionError, ValueError):
        return dash.no_update, "⚠️ Error numérico: ajusta los parámetros (ν muy pequeño o r muy grande)"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines',
        line=dict(color='purple', width=2),
        name='Modelo de Richards'
    ))

    fig.add_trace(go.Scatter(
        x=[t_eval], y=[P_eval],
        mode='markers+text',
        marker=dict(color='red', size=10),
        text=[f"P({t_eval}) = {P_eval:.2f}"],
        textposition="top center",
        name='Evaluación'
    ))

    fig.add_hline(y=k, line_dash="dot", line_color="gray", annotation_text="K (capacidad)", 
                  annotation_position="bottom right")

    fig.update_layout(
        title_text="Crecimiento de Richards: dP/dt = rP[1 - (P/K)^ν]",
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

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='lightgray', range=[0, t_max])
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='lightgray')

    return fig, f" Población en t = {t_eval}: P(t) = {P_eval:.2f}"