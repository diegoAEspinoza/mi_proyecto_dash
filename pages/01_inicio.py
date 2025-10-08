import dash
from dash import html
import dash_bootstrap_components as dbc
from styles import PROFILE_IMAGE_STYLE, INFO_CARD_STYLE

dash.register_page(__name__, name='Sobre Mí')

layout = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col(
                html.Img(src='assets/profile.jpg', style=PROFILE_IMAGE_STYLE),
                md=4,
                className="d-flex align-items-center"
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H2("Junior Alberto Yanac Minaya", className="card-title text-center"),
                        html.P(
                            "Soy estudiante de Computación Científica en la Universidad Nacional Mayor de San Marcos y actualmente curso el sexto ciclo.",
                            className="lead"
                        ),
                        html.P(
                            "Aún me encuentro en proceso de aprendizaje, fortaleciendo mis conocimientos en programación, matemáticas aplicadas y modelado computacional."
                        ),
                        html.P(
                            "Me interesa seguir desarrollándome en áreas como análisis de datos y simulación científica, y aprovechar lo aprendido para resolver problemas reales mediante el cómputo."
                        )
                    ]),
                    style=INFO_CARD_STYLE
                ),
                md=8,
                className="ps-md-5"
            ),
        ], align="center")
    ]),
    className="m-4",
)
