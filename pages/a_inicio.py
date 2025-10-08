import dash
from dash import html
import dash_bootstrap_components as dbc

# Registra la página en tu aplicación, usando un orden para la navegación
# Asegúrate de que el 'order' sea apropiado para tu navegación (ej. 1 si 'Inicio' es 0)
dash.register_page(__name__, path='/', name='Inicio', order=1)

# Estilos CSS personalizados para el fondo y otros elementos
# Puedes poner esto en tu archivo assets/style.css o directamente aquí en una sección de html.Style
custom_styles = {
    'background-image': 'url("/assets/abstract_background.png")', # Asegúrate de tener una imagen de fondo en /assets
    'background-size': 'cover',
    'background-position': 'center',
    'background-repeat': 'no-repeat',
    'padding': '50px 0',
    'min-height': 'calc(100vh - 80px)', # Ajusta para la altura de tu navbar/footer si los tienes
    'display': 'flex',
    'align-items': 'center',
}

# Puedes poner los íconos de redes sociales como imágenes en tu carpeta /assets
# y usar un html.Img para cada uno, o usar fuentes de íconos si las configuras.
# Para este ejemplo, usaremos placeholders de texto o puedes usar iconos de Dash
# (requeriría una configuración adicional si quieres logos exactos)

layout = dbc.Container(
    [
        dbc.Row(
            [
                # Columna izquierda para el texto y enlaces
                dbc.Col(
                    [
                        html.H2("Hola, Soy [Tu Nombre]", className="display-4 fw-bold mb-3"),
                        html.P("Soy estudiante en el curso de [Nombre del Curso] y este es mi proyecto de Dash."),
                        html.P("Estoy aprendiendo a usar Dash para crear aplicaciones web interactivas y visualizaciones de datos. Me apasiona [Tus intereses relacionados con el curso, ej. la ciencia de datos, la programación o las matemáticas]."),
                        
                        # Botón "About Me"
                        dbc.Button(
                            "Más Sobre Mí", 
                            href="#", # Puedes vincular a otra sección o página si deseas
                            color="primary", 
                            className="btn-lg my-4"
                        ),
                        
                        # Iconos de redes sociales (puedes reemplazarlos con html.Img o iconos reales)
                        html.Div([
                            html.A(dbc.Button(html.I(className="bi bi-linkedin"), outline=True, color="secondary", className="me-2"), href="[Enlace LinkedIn]", target="_blank"),
                            html.A(dbc.Button(html.I(className="bi bi-github"), outline=True, color="secondary", className="me-2"), href="[Enlace GitHub]", target="_blank"),
                            html.A(dbc.Button(html.I(className="bi bi-envelope"), outline=True, color="secondary", className="me-2"), href="mailto:[Tu Email]", target="_blank"),
                            # Añade más enlaces si necesitas (ej. Twitter, Instagram, etc.)
                        ], className="d-flex") # d-flex para que los botones estén en línea
                    ],
                    md=6, # Ocupa 6 de 12 columnas en pantallas medianas y grandes
                    className="d-flex flex-column justify-content-center p-5" # Alineación vertical y padding
                ),

                # Columna derecha para la imagen del avatar
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/jigar_sable_avatar.png", # Asegúrate de que esta imagen esté en /assets
                            className="img-fluid rounded-circle shadow-lg" # Estilo de imagen de Bootstrap
                        )
                    ],
                    md=6, # Ocupa 6 de 12 columnas
                    className="d-flex justify-content-center align-items-center p-5" # Centra la imagen
                ),
            ],
            align="center", # Alinea el contenido de las columnas al centro verticalmente
            className="g-0", # Elimina el espacio entre las columnas para un fondo continuo
            style={'min-height': 'inherit'} # Hereda la altura mínima del contenedor padre
        ),
    ],
    fluid=True, # El contenedor ocupa todo el ancho de la ventana
    className="p-0", # Elimina el padding del contenedor para que el fondo llegue a los bordes
    style=custom_styles # Aplica los estilos de fondo
)