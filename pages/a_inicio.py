import dash
from dash import html
import dash_bootstrap_components as dbc

# Página de inicio
dash.register_page(__name__, path='/', name='Inicio', order=1)

# =========================
#  HERO / HEADER (tipo Initio)
# =========================
hero_section = html.Header(
    id="header",
    children=html.Div(
        id="head",
        className="parallax d-flex align-items-center justify-content-center",
        # Puedes controlar el fondo de este bloque con CSS en assets/styles.css
        children=html.H1(
            id="logo",
            className="text-center",
            children=[
                html.Img(
                    src="/assets/images/perfiluser.jpg",
                    className="img-circle img-thumbnail mb-3",
                    style={"width": "180px", "height": "180px", "objectFit": "cover"}
                ),
                html.Span("Rudy Palacios", className="d-block h2 fw-bold"),
                html.Span("Estoy aprendiendo a usar Dash para crear aplicaciones web interactivas y visualizaciones de datos. Me apasiona la ciencia de datos, la programación y el desarrollo de interfaces que hacen que los modelos matemáticos y los algoritmos de Machine Learning e Inteligencia Artificial sean accesibles y fáciles de entender.",className="lead text-center text-muted"),
                html.Span(
                    [
                        "Estudiante de Técnicas de Modelamiento Matemático",
                        html.Br(),
                        html.A(
                            "rudy.palacios@example.com",
                            href="mailto:rudy.palacios@example.com",
                            className="text-decoration-none"
                        )
                    ],
                    className="tagline text-muted"
                ),
            ]
        ),
        style={
            # Fondo tipo parallax (ajústalo en tu CSS si quieres efecto más pro)
            "backgroundSize": "cover",
            "backgroundPosition": "center",
            "backgroundRepeat": "no-repeat",
            "minHeight": "70vh",
        }
    )
)

# =========================
#  SECCIÓN TEXTO CENTRAL (lead)
# =========================
""" lead_section = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    "Let me tell you something my friend. Hope is a dangerous thing. ",
                    "Hope can drive a man insane. You ",
                    html.A("measure", href="#", className="text-decoration-none"),
                    " yourself by the people who measure themselves by you. ",
                    "It only took me ",
                    html.A("six days", href="#", className="text-decoration-none"),
                    "."
                ],
                className="lead text-center text-muted"
            ),
            md=12
        ),
        className="section topspace"
    ),
    className="mt-4"
) """

# =========================
#  SECCIÓN SERVICES
# =========================
services_cards = [
    {
        "title": "Custom website design",
        "text": ("I don't think they tried to market it to the billionaire, spelunking, "
                 "base-jumping crowd. I did the same thing to Gandhi, he didn't eat for three weeks. "
                 "I once heard a wise man say there are no perfect men."),
    },
    {
        "title": "Wordpress integration",
        "text": ("I don't think they tried to market it to the billionaire, spelunking, "
                 "base-jumping crowd. I did the same thing to Gandhi, he didn't eat for three weeks. "
                 "I once heard a wise man say there are no perfect men."),
    },
    {
        "title": "Application development",
        "text": ("I don't think they tried to market it to the billionaire, spelunking, "
                 "base-jumping crowd. I did the same thing to Gandhi, he didn't eat for three weeks. "
                 "I once heard a wise man say there are no perfect men."),
    },
    {
        "title": "SEO & SEM services",
        "text": ("I don't think they tried to market it to the billionaire, spelunking, "
                 "base-jumping crowd. I did the same thing to Gandhi, he didn't eat for three weeks. "
                 "I once heard a wise man say there are no perfect men."),
    },
]

services_section = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H2(
                    html.Span("Services"),
                    className="section-title text-center my-4"
                ),
                md=12
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3(card["title"], className="text-center h5 fw-bold mb-3"),
                        html.P(card["text"]),
                        html.Div(
                            dbc.Button(
                                "Read more",
                                href="#",
                                color="primary",
                                className="btn btn-action"
                            ),
                            className="text-center mt-3"
                        )
                    ],
                    xs=12, sm=6, md=3,
                    className="mb-4"
                )
                for card in services_cards
            ],
            className="row section featured topspace"
        ),
    ],
    className="mt-4"
)

# =========================
#  SECCIÓN RECENT WORKS
# =========================
""" recent_works_data = [
    {
        "title": "Sample title - big data solutions",
        "details": ["Web design", "Wordpress", "Logotype"],
        "img": "/assets/images/s1.jpg",
        "href": "#",
    },
    {
        "title": "Pure ipsum - development services for people",
        "details": ["Web design", "Wordpress"],
        "img": "/assets/images/s1.jpg",
        "href": "#",
    },
    {
        "title": "Lorem studios - interior and patio design",
        "details": ["Web design", "Logotype"],
        "img": "/assets/images/s1.jpg",
        "href": "#",
    },
    {
        "title": "Pure ipsum - development services for people",
        "details": ["Web design", "Wordpress"],
        "img": "/assets/images/s1.jpg",
        "href": "#",
    },
    {
        "title": "Lorem studios - interior and patio design",
        "details": ["Web design", "Logotype"],
        "img": "/assets/images/s1.jpg",
        "href": "#",
    },
    {
        "title": "Lorem studios - interior and patio design",
        "details": ["Web design", "Logotype"],
        "img": "/assets/images/s1.jpg",
        "href": "#",
    },
] """

""" recentworks_section = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H2(
                    html.Span("Recent Works"),
                    className="section-title text-center my-4"
                ),
                md=12
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.A(
                                [
                                    html.Span(
                                        [
                                            html.Img(
                                                src=item["img"],
                                                className="img-fluid"
                                            ),
                                            html.Span(
                                                html.Span(
                                                    "See details →",
                                                    className="more"
                                                ),
                                                className="cover"
                                            )
                                        ],
                                        className="img d-block position-relative"
                                    ),
                                    html.Span(
                                        item["title"],
                                        className="title d-block mt-2 fw-semibold"
                                    ),
                                ],
                                href=item["href"],
                                className="thumbnail text-decoration-none d-block"
                            ),
                            html.Span(
                                [
                                    html.Span(
                                        [
                                            html.A(d, href="#", className="text-decoration-none")
                                        ] + ([", "] if i < len(item["details"]) - 1 else [])
                                    )
                                    for i, d in enumerate(item["details"])
                                ],
                                className="details d-block text-muted small mt-1"
                            ),
                        ]
                    ),
                    xs=12, sm=6, md=4, lg=4,
                    className="mb-4"
                )
                for item in recent_works_data
            ],
            className="thumbnails recentworks row"
        )
    ],
    className="mt-4"
) """

# =========================
#  FOOTER PRINCIPAL
# =========================
footer = html.Footer(
    id="footer",
    children=dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Contact", className="widget-title h5"),
                        html.Div(
                            html.P(
                                [
                                    "+51 999 999 999",
                                    html.Br(),
                                    html.A("rudy.palacios@example.com",
                                           href="mailto:rudy.palacios@example.com"),
                                    html.Br(), html.Br(),
                                    "Lima, Perú"
                                ]
                            ),
                            className="widget-body"
                        )
                    ],
                    md=3,
                    className="widget mb-4"
                ),
                dbc.Col(
                    [
                        html.H3("Follow me", className="widget-title h5"),
                        html.Div(
                            html.P(
                                [
                                    html.A(html.I(className="fa fa-twitter fa-2"), href="#", className="me-2"),
                                    html.A(html.I(className="fa fa-dribbble fa-2"), href="#", className="me-2"),
                                    html.A(html.I(className="fa fa-github fa-2"), href="#", className="me-2"),
                                    html.A(html.I(className="fa fa-facebook fa-2"), href="#", className="me-2"),
                                ],
                                className="follow-me-icons"
                            ),
                            className="widget-body"
                        )
                    ],
                    md=3,
                    className="widget mb-4"
                ),
                dbc.Col(
                    [
                        html.H3("Text widget", className="widget-title h5"),
                        html.Div(
                            html.Div(
                                [
                                    html.P(
                                        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. "
                                        "Atque, nihil natus explicabo ipsum quia iste aliquid repellat eveniet "
                                        "velit ipsa sunt libero sed aperiam id soluta officia asperiores adipisci maxime!"
                                    ),
                                    html.P(
                                        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. "
                                        "Atque, nihil natus explicabo ipsum quia iste aliquid repellat eveniet "
                                        "velit ipsa sunt libero sed aperiam id soluta officia asperiores adipisci maxime!"
                                    ),
                                ]
                            ),
                            className="widget-body"
                        )
                    ],
                    md=3,
                    className="widget mb-4"
                ),
                dbc.Col(
                    [
                        html.H3("Form widget", className="widget-title h5"),
                        html.Div(
                            html.P(
                                [
                                    "+51 999 999 999",
                                    html.Br(),
                                    html.A("rudy.palacios@example.com",
                                           href="mailto:rudy.palacios@example.com"),
                                    html.Br(), html.Br(),
                                    "Lima, Perú"
                                ]
                            ),
                            className="widget-body"
                        )
                    ],
                    md=3,
                    className="widget mb-4"
                ),
            ],
            className="row"
        )
    ),
    className="mt-5 pt-4 border-top"
)

# =========================
#  UNDERFOOTER
# =========================
underfooter = html.Footer(
    id="underfooter",
    children=dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        html.P("Lima, Perú"),
                        className="widget-body"
                    ),
                    md=6,
                    className="widget mb-2"
                ),
                dbc.Col(
                    html.Div(
                        html.P(
                            [
                                "Copyright © 2025, Rudy Palacios",
                                html.Br(),
                                "Design based on Initio template"
                            ],
                            className="text-md-end text-sm-start"
                        ),
                        className="widget-body"
                    ),
                    md=6,
                    className="widget mb-2"
                ),
            ]
        )
    ),
    className="py-3 border-top"
)

# =========================
#  LAYOUT FINAL
# =========================
layout = html.Div(
    [
        hero_section,
        html.Main(
            [
                #lead_section,
                services_section,
                #recentworks_section,
            ],
            id="main"
        ),
        footer,
        underfooter
    ],
    className="home"
)
