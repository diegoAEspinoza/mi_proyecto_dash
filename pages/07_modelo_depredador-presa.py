import dash 
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import solve_ivp
from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(__name__, name='Modelo Presa–Depredador')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Modelo Presa–Depredador (Lotka-Volterra)", className="card-title text-center mb-4"),
        html.P(
            "Modelo clásico que describe la interacción cíclica entre dos especies: las presas crecen libremente, pero son consumidas por los depredadores, quienes a su vez dependen de ellas para sobrevivir.",
            className="text-center"
        ),
        html.Hr(),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Ecuaciones Diferenciales", className="card-title text-center"),
                html.Div(
                    html.Img(
                        src=r"https://latex.codecogs.com/svg.latex?\begin{cases}\frac{dx}{dt}=\alpha x-\beta xy\\\frac{dy}{dt}=\delta xy-\gamma y\end{cases}",
                        style={'height': '70px', 'display': 'block', 'margin': '10px auto'}
                    ),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Comportamiento", className="card-title text-center"),
                dcc.Markdown("""
                    * Las poblaciones oscilan **cíclicamente**.
                    * El pico de presas **precede** al de depredadores.
                    * Sin intervención, el sistema es **neutro estable** (ciclos perpetuos).
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("¿Cuándo se usa?", className="card-title text-center"),
                dcc.Markdown("""
                    * **Ecología:** Dinámica de especies (liebres y linces).
                    * **Epidemiología:** Modelos SIR simplificados.
                    * **Economía:** Competencia entre mercados o tecnologías.
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Puntos de Equilibrio", className="card-title text-center"),
                dcc.Markdown("""
                    * **(0, 0):** Extinción (inestable).
                    * **(γ/δ, α/β):** Coexistencia (centro, neutro estable).
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),
        
        dbc.Row([
            dbc.Col(
                dbc.Card(dbc.CardBody([
                    html.H5("Descripción de Variables", className="card-title text-center"),
                    dcc.Markdown("""
                        * **x(t):** Población de **presas** en el tiempo t.
                        * **y(t):** Población de **depredadores** en el tiempo t.
                        * **α:** Tasa de crecimiento natural de presas.
                        * **β:** Tasa de encuentro/predación.
                        * **γ:** Tasa de mortalidad de depredadores.
                        * **δ:** Eficiencia de conversión (presas → depredadores).
                    """, style={'paddingLeft': '20px'})
                ]), style=INFO_CARD_STYLE)
            ),
        ], className="mb-4"),

        html.Hr(className="my-4"),
        dbc.Row([
            dbc.Col([
                html.H4("Parámetros", className="text-center fw-bold mb-3"),
                
                dbc.Label("Presas Iniciales (x₀):", className="small"),
                dcc.Input(id='predprey-x0-input', type='number', value=40, min=0.1, step=0.1,
                          style=INPUT_STYLE_COMPACT, className="mb-2"),
                
                dbc.Label("Depredadores Iniciales (y₀):", className="small"),
                dcc.Input(id='predprey-y0-input', type='number', value=9, min=0.1, step=0.1,
                          style=INPUT_STYLE_COMPACT, className="mb-2"),
                
                dbc.Label("α (crecimiento presas):", className="small"),
                dcc.Input(id='predprey-alpha-input', type='number', value=1.0, min=0.01, step=0.01,
                          style=INPUT_STYLE_COMPACT, className="mb-2"),
                
                dbc.Label("β (tasa de predación):", className="small"),
                dcc.Input(id='predprey-beta-input', type='number', value=0.1, min=0.001, step=0.001,
                          style=INPUT_STYLE_COMPACT, className="mb-2"),
                
                dbc.Label("γ (mortalidad depredadores):", className="small"),
                dcc.Input(id='predprey-gamma-input', type='number', value=1.5, min=0.01, step=0.01,
                          style=INPUT_STYLE_COMPACT, className="mb-2"),
                
                dbc.Label("δ (eficiencia conversión):", className="small"),
                dcc.Input(id='predprey-delta-input', type='number', value=0.075, min=0.001, step=0.001,
                          style=INPUT_STYLE_COMPACT, className="mb-2"),
                
                dbc.Label("Tiempo Final (tₘₐₓ):", className="small"),
                dcc.Input(id='predprey-time-max-input', type='number', value=15, min=1, step=0.5,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                html.Div(id='predprey-result', className="text-center fw-bold mt-3 text-primary"),
            ], md=3),
            dbc.Col([
                dcc.Tabs([
                    dcc.Tab(label='Poblaciones vs Tiempo', children=[
                        dcc.Graph(id='predprey-time-graph', style={'height': '100%'})
                    ]),
                    dcc.Tab(label='Fase (Presas vs Depredadores)', children=[
                        dcc.Graph(id='predprey-phase-graph', style={'height': '100%'})
                    ])
                ])
            ], md=9),
        ], align="start", className="mt-4"),
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

def lotka_volterra(t, z, alpha, beta, gamma, delta):
    x, y = z
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]

@callback(
    [Output('predprey-time-graph', 'figure'),
     Output('predprey-phase-graph', 'figure'),
     Output('predprey-result', 'children')],
    [Input('predprey-x0-input', 'value'),
     Input('predprey-y0-input', 'value'),
     Input('predprey-alpha-input', 'value'),
     Input('predprey-beta-input', 'value'),
     Input('predprey-gamma-input', 'value'),
     Input('predprey-delta-input', 'value'),
     Input('predprey-time-max-input', 'value')]
)
def update_predprey_graph(x0, y0, alpha, beta, gamma, delta, t_max):
    if None in (x0, y0, alpha, beta, gamma, delta, t_max):
        return dash.no_update, dash.no_update, ""

    if any(v <= 0 for v in [x0, y0, alpha, beta, gamma, delta]):
        return dash.no_update, dash.no_update, "⚠️ Todos los parámetros deben ser > 0"

    t_eval = np.linspace(0, t_max, 500)

    try:
        sol = solve_ivp(
            lotka_volterra,
            [0, t_max],
            [x0, y0],
            args=(alpha, beta, gamma, delta),
            t_eval=t_eval,
            method='RK45',
            rtol=1e-6
        )
    except Exception as e:
        return dash.no_update, dash.no_update, f"⚠️ Error en integración: {str(e)}"

    if not sol.success:
        return dash.no_update, dash.no_update, "⚠️ La integración falló. Intenta con otros parámetros."

    t = sol.t
    x = sol.y[0]
    y = sol.y[1]

    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(x=t, y=x, mode='lines', name='Presas (x)', line=dict(color='green', width=2)))
    fig_time.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Depredadores (y)', line=dict(color='red', width=2)))
    fig_time.update_layout(
        title="Poblaciones a lo largo del tiempo",
        xaxis_title="Tiempo (t)",
        yaxis_title="Población",
        template="plotly_white",
        font=dict(family="Outfit, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=50, b=40),
        plot_bgcolor='lightyellow'
    )
    fig_time.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='lightgray')
    fig_time.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='lightgray')

    fig_phase = go.Figure()
    fig_phase.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='purple', width=2)))
    fig_phase.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='markers', marker=dict(color='blue', size=8), name='Inicio'))
    fig_phase.update_layout(
        title="Diagrama de Fase: Presas vs Depredadores",
        xaxis_title="Presas (x)",
        yaxis_title="Depredadores (y)",
        template="plotly_white",
        font=dict(family="Outfit, sans-serif"),
        margin=dict(l=40, r=20, t=50, b=40),
        plot_bgcolor='lightcyan'
    )
    fig_phase.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='lightgray')
    fig_phase.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='lightgray')

    return fig_time, fig_phase, f" Simulación completada hasta t = {t_max}"