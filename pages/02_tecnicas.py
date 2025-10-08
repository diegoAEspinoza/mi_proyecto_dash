import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from styles import INFO_CARD_STYLE

dash.register_page(__name__, path='/', name='Técnicas de Modelado')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Técnicas de Modelamiento Matemático", className="card-title text-center mb-4"),
        html.P(
            "El modelamiento matemático es el arte de traducir problemas del mundo real a un lenguaje matemático. Utilizamos ecuaciones y conceptos para representar, analizar y predecir el comportamiento de diferentes sistemas. La elección de la técnica depende de la naturaleza del problema:",
            className="text-center"
        ),
        html.Hr(),
        dcc.Markdown("""
            * **Modelos Deterministas vs. Estocásticos:** Producen la misma salida para una entrada dada o incorporan aleatoriedad.
            * **Modelos Estáticos vs. Dinámicos:** No consideran el tiempo y representan un sistema en un punto fijo, o describen cómo un sistema evoluciona.
            * **Modelos Lineales vs. No Lineales:** Se basan en si las relaciones entre las variables son simples y directas, o complejas y variables.
            * **Modelos Discretos vs. Continuos:** Describen variables en puntos de tiempo específicos o de forma continua.
        """, className="mt-4"),
    ]),
    className="m-4",
    style=INFO_CARD_STYLE
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