import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from styles import INFO_CARD_STYLE

dash.register_page(__name__, path='/', name='Técnicas de Modelado')

layout = dbc.Card(
    dbc.CardBody([
        html.H2("Técnicas de Modelamiento Matemático", className="card-title text-center mb-4"),
        html.P(
            "El modelamiento matemático es el proceso de representar un fenómeno real mediante expresiones matemáticas, con el objetivo de analizarlo, comprenderlo y predecir su comportamiento.",
            className="text-center"
        ),
        html.P(
            "En esta asignatura, el estudiante aprende a formular, analizar y resolver modelos que surgen en distintas áreas de la ciencia, la ingeniería, la economía y la biología, entre otras.",
            className="text-center"
        ),
        html.Hr(),

        html.H5("Pasos Fundamentales del Modelamiento", className="text-center"),
        dcc.Markdown("""
            * **Identificación del problema real:** Reconocer las variables, parámetros y relaciones que influyen en el fenómeno.
            * **Formulación del modelo:** Traducir el problema a ecuaciones matemáticas que describan su comportamiento.
            * **Análisis y resolución:** Aplicar métodos analíticos o numéricos para estudiar el modelo y obtener resultados.
            * **Validación e interpretación:** Comparar los resultados con datos reales y ajustar el modelo según sea necesario.
            * **Simulación y predicción:** Usar herramientas computacionales para simular distintos escenarios y prever comportamientos futuros.
        """, className="mt-3"),

        html.Hr(),
        
        html.H5("Técnicas y Herramientas Introducidas", className="text-center"),
        dcc.Markdown("""
            * Ecuaciones diferenciales ordinarias y parciales
            * Modelos lineales y no lineales
            * Modelos discretos y continuos
            * Análisis de estabilidad
            * Métodos numéricos y simulaciones computacionales
        """, className="mt-3"),

        html.Hr(),

        html.P(
            "En conjunto, estas técnicas permiten convertir problemas reales en modelos matemáticos útiles, facilitando la toma de decisiones, la optimización de procesos y la comprensión profunda de sistemas complejos.",
            className="text-center fw-bold"
        )
    ]),
    className="m-4",
    style=INFO_CARD_STYLE
)
