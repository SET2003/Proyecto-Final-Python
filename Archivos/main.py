# --------- PAQUETES IMPORTADOS ---------

# Librerias estándar de Python
import datetime
import time
from io import BytesIO

# Paquetes de terceros
import altair as alt
import folium
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import streamlit_antd_components as sac
from streamlit_folium import st_folium


# --------- CONFIGURACIÓN PÁGINA ---------

st.set_page_config(
    page_title="Proyecto Generador Fotovoltaico",
    page_icon=":material/solar_power:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# Página del Proyecto de Generador Fotovoltaico",
        # VER DE MODIFICAR ESTE MENU
    },
)

# --------- CONFIGURACIÓN SIDEBAR ---------

# CSS personalizado para la sidebar
custom_css = """
<style>
/* Estilo básico de la sidebar */
[data-testid="stSidebar"] {
    transition: all 0.3s ease; /* Animación para el hover */
    background-color: #fffff;
    padding: 1rem;
}

/* Efecto hover */
[data-testid="stSidebar"]:hover {
    background-color: #fffff; /* Cambia el color al pasar el ratón */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Efecto de sombra opcional */
    transform: scale(1.02); /* Aumenta ligeramente el tamaño */
}
</style>
"""

# Aplicar el CSS personalizado
st.markdown(custom_css, unsafe_allow_html=True)

#  Paquete para la sidebar
with st.sidebar:
    st.image("Archivos\\Imagenes\\logo-utn.png")
    st.logo(
        "Archivos\\Imagenes\\home-header.png",
        size="large",
        link="https://www.frsf.utn.edu.ar/",
        icon_image="Archivos\\Imagenes\\UTN-FRSF.jpg",
    )
    st.write("---")
    seccion = sac.menu(
        [
            sac.MenuItem("Acerca de", icon="house-fill"),
            sac.MenuItem(
                "Generador",
                icon="sun-fill",
                children=[
                    sac.MenuItem("Datos", icon="clipboard-data-fill"),
                    sac.MenuItem("Estadísticas", icon="bar-chart-line-fill"),
                    sac.MenuItem("Mapas", icon="map-fill"),
                ],
            ),
            sac.MenuItem("Ayuda", icon="question-circle-fill"),
            sac.MenuItem("Feedback", icon="chat-right-heart-fill"),
            sac.MenuItem(type="divider"),
            sac.MenuItem(
                "links de interés",
                type="group",
                children=[
                    sac.MenuItem(
                        "Información panel UTN-FRSF",
                        icon="link-45deg",
                        href="""https://www.hissuma-materiales.com.ar/
                        productos/panel-solar-hissuma-solar-doble-vidrio-240w/
                        """,
                    ),
                    sac.MenuItem(
                        "Información inversor UTN-FRSF",
                        icon="link-45deg",
                        href="""https://files.sma.de/downloads/SBxx-1VL-40-DS-es-52.pdf
                        """,
                    ),
                    sac.MenuItem(
                        "Google Maps",
                        icon="link-45deg",
                        href="https://www.google.com.ar/maps/preview",
                    ),
                    sac.MenuItem(
                        "Windy",
                        icon="link-45deg",
                        href="https://www.windy.com/?-31.638,-60.693,5",
                    ),
                    sac.MenuItem(
                        "Global Solar Atlas",
                        icon="link-45deg",
                        href="https://globalsolaratlas.info/map",
                    ),
                    sac.MenuItem(
                        "NASA POWER",
                        icon="link-45deg",
                        href="https://power.larc.nasa.gov/",
                    ),
                    sac.MenuItem(
                        "Servicio Meteorológico Nacional",
                        icon="link-45deg",
                        href="https://www.smn.gob.ar/clima/vigilancia-mapas",
                    ),
                ],
            ),
        ],
        open_all=True,
        color="#2aa7e1",
    )
# --------- TEXTO JUSTIFICADO, VARIABLES EN LATEX ---------

# Defino fuera del if correspondiente a 'Acerca de', el texto a usar para el
# texto justificado con letras de variables en latex


def justificado_latex(texto, altura=400):
    texto1 = """
    <link
    href='https://fonts.googleapis.com/css?family=Source+Sans+Pro'
    rel='stylesheet'
    type='text/css'>

    <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/katex@0.16.15/dist/katex.min.css"
    integrity="sha384-Htz9HMhiwV8GuQ28Xr9pEs1B4qJiYu/nYLLwlDklR53QibDfmQzi7rYxXhMH/5/u"
    crossorigin="anonymous">

    <script
    defer
    src="https://cdn.jsdelivr.net/npm/katex@0.16.15/dist/katex.min.js"
    integrity="sha384-bxmi2jLGCvnsEqMuYLKE/KsVCxV3PqmKeK6Y6+lmNXBry6+luFkEOsmp5vD9I/7+"
    crossorigin="anonymous">
    </script>

    <script
    defer
    src="https://cdn.jsdelivr.net/npm/katex@0.16.15/dist/contrib/auto-render.min.js"
    integrity="sha384-hCXGrW6PitJEwbkoStFjeJxv+fSOOQKOPbJxSfM6G5sWZjAyWhXiTIIAmQqnlLlh"
    crossorigin="anonymous">
    </script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            renderMathInElement(document.body, {
            // customised options
            // • auto-render specific keys, e.g.:
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\(', right: '\\)', display: false},
                {left: '\\[', right: '\\]', display: true}
            ],
            // • rendering keys, e.g.:
            throwOnError : false
            });
        });
    </script>

    <div style='text-align: justify;
    font-family: "Source Sans Pro", sans-serif;
    padding: 0px;
    font-weight: 400;
    font-size: 1rem;
    line-height: 1.6;
    color: rgb(49, 51, 63);
    background-color: rgb(255, 255, 255);
    text-size-adjust: 100%;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    -webkit-font-smoothing: auto;'>
            <p>"""

    texto2 = """</p>
    </div>"""

    return components.html(texto1 + texto + texto2, height=altura)


# --------- VERIFICACIÓN DE DATOS ---------

if "datos" not in st.session_state:
    datos = pd.read_excel(
        "Archivos\\Datos_climatologicos_Santa_Fe_2019.xlsx", index_col=0
    )
    G, T = datos.columns
    N = 12
    Gstd = 1000
    Tr = 25
    Ppico = 240
    kp = -0.0044
    rend = 0.97
    Pinv = 2.5
    umbral_minimo = 0
    datos["Temperatura de Celda (°C)"] = datos[T] + 0.031 * datos[G]
    Tc = datos["Temperatura de Celda (°C)"]
    datos["Potencia (kW)"] = (
        N * datos[G] / Gstd * Ppico * (1 + kp * (Tc - Tr)) * rend * 1e-3
    )
    Pmin = umbral_minimo / 100 * Pinv
    datos["Potencia (kW)"] = datos["Potencia (kW)"].where(
        datos["Potencia (kW)"] < Pinv, Pinv
    )
    datos["Potencia (kW)"] = datos["Potencia (kW)"].where(
        datos["Potencia (kW)"] > Pmin, 0
    )
    st.session_state["datos"] = datos
    st.session_state["tabla_en_uso"] = "Pred"

if "fecha_inicial" not in st.session_state:
    st.session_state["fecha_inicial"] = datos.index[0]
    st.session_state["fecha_final"] = datos.index[-1]

if "tiempo_inicial" not in st.session_state:
    st.session_state["tiempo_inicial"] = datos.index[0].time()
    st.session_state["tiempo_final"] = datos.index[-1].time()

if "fecha_inicial_est" not in st.session_state:
    st.session_state["fecha_inicial_est"] = datos.index[0]
    st.session_state["fecha_final_est"] = datos.index[-1]


# --------- SECCIONES ---------

# --- Sección 1: Acerca de ---
if seccion == "Acerca de":
    st.header("Acerca de esta aplicación", divider="grey")
    st.image("Archivos\\Imagenes\\banner_panelessolares.jpg",
             use_container_width=True)
    st.subheader("Descripción")

    st.markdown(
        """<div style='text-align: justify;'>
    Esta aplicación, desarrollada como proyecto final en la asignatura
    "Introducción a la programación científica con MATLAB y PYTHON" en el
    marco de la Facultad Regional Santa Fe - UTN, se centra en el análisis de
    distintos datos de un generador fotovotaico (GFV) para el cálculo de la
    potencia que éste es capaz de entregar. Además, de acuerdo a la
    información cargada de temperaturas, irradiancias y tiempo, se calculan
    otros datos estadísticos de interés, así como gráficas y mapas
    interactivos. Se toma como base incial el generador de la Facultad
    Regional Santa Fe de la Universidad Tecnológica Nacional (ver links
    de interés).
    </div> """,
        unsafe_allow_html=True,
    )

    st.subheader("Objetivos del proyecto")
    """
    * **Permitir al usuario cargar los datos de su propio generador** y
    otorgarle los resultados del análisis en tiempos específicos que desee.
    * **Analizar el comportamiento del generador fotovoltaico de la Facultad
    Regional Santa Fe - UTN.**
    * Utilizar sintaxis *Python* y la librería *Streamlit* para crear la
    aplicación web interactiva.
    * Usar la librería *Pandas* para el manejo de *dataframes*.
    """
    st.subheader(
        "¿Cómo funciona?",
        help="""En este apartado se describe el funcionamiento del GFV, así
        como el modelo matemático utilizado. Extraído de *Guía del
        Proyecto*""",
    )

    st.markdown(
        """<div style='text-align: justify;'>
    Un generador fotovoltaico (GFV) convierte parte de la energía proveniente
    de la radicación solar en la forma eléctrica. La instalación se ejecuta en
    forma modular; una cantidad N de paneles (o módulos) se vinculan a través
    de sus terminales de salida en una configuración mixta serie-paralelo. El
    conexionado serie se utiliza cuando se pretende incrementar la potencia de
    salida elevando el nivel de tensión eléctrica (diferencia de potencial
    total del conjunto). El conexionado paralelo, por su parte, se realiza
    cuando el incremento de potencia se logra elevando el nivel de la
    corriente entregada. En la práctica, un GFV puede utilizar una combinación
    de módulos conectados en serie, los que a su vez se vinculan en paralelo
    con otros conjuntos de conexionados serie.
    La tensión eléctrica provista por un GFV es del tipo continua, es decir,
    que se mantiene constante siempre que lo hagan las condiciones de
    radiación solar y temperatura. No obstante, dado que esto último no es
    posible, se requiere de un equipo electrónico que funciona como
    controlador, que busca estabilizar las condiciones de operación siempre
    que sea posible. Una variante muy difundida altera convenientemente dicha
    tensión para que la potencia erogada sea la máxima posible de acuerdo con
    las condiciones meteorológicas del momento. Asimismo, en virtud de que las
    redes eléctricas no suelen operar con tensión continua, sino
    en forma alterna (con una variación sinusoidal en el tiempo), un circuito
    electrónico “inversor” es requerido para realizar la conversión. Es
    habitual que un único equipamiento cumpla simultáneamente las funciones de
    controlador e inversor. </div> """,
        unsafe_allow_html=True,
    )
    """

    """
    """
    **1. Estimación de potencia generada**
    """

    st.markdown(
        """<div style='text-align: justify;'>
    Existen numerosos modelos matemáticos para representar el funcionamiento
    de un GFV. La configuración de las conexiones entre módulos es relevante
    si se pretende que el modelo obtenga la tensión y corriente de operación.
    En otras circunstancias, cuando interese fundamentalmente la potencia
    eléctrica entregada, pueden emplearse modelos simplificados. Por caso, la
    siguiente expresión obtiene la potencia eléctrica P (en kilo-Watt)
    obtenida por un GFV, siempre que todos los módulos sean idénticos y cuando
    se utiliza un controlador de potencia que altera la condición de tensión
    de trabajo para maximizar el rendimiento.
    </div> """,
        unsafe_allow_html=True,
    )

    st.latex(
        """
    P = N\\cdot \\frac{G}{G_{std}}\\cdot P_{pico}\\cdot\\left[1+k_{p}\\cdot
    (T_{c}-T_{r})\\right ]\\cdot\\eta\\cdot 10^{-3}
    """
    )

    """
    Donde:\n
    $ N $: Número de módulos fotovoltaicos.\n
    $ G $: Irradiancia global incidente en forma normal a los módulos $ W $/
    $ m^{2} $.\n
    $ G_{std} $: Irradiancia estándar, comúnmente en $ W $/$ m^{2} $.\n
    $ P_{pico} $: Potencia pico de cada módulo en $ W $.\n
    $ k_{p} $: Coeficiente de temperatura-potencia en $ °C^{-1} $.\n
    $ T_{c} $: Temperatura de la celda.\n
    $ T_{r} $: Temperatura de referencia ($ 25 °C $).\n
    $ \\eta $: Rendimiento global del sistema.\n
\n
    **2. Corrección de temperatura de celda**
    """
    justificado_latex("""
        La temperatura de la celda difiere de la temperatura ambiente $ T
        $. En la literatura se disponen decenas de modelos matemáticos que
        permiten estimar $ T_{c} $  a partir de mediciones de $ T $. El modelo
        más sencillo, válido únicamente en ausencia de viento, indica que la
        relación se puede aproximar según:\n
    """, altura=65)

    st.latex(
        """ T_{c}= T + 0.031\\left [ °C \\cdot m^{2}/W \\right ]
            \\cdot G"""
    )

    justificado_latex(
        """ <div style='text-align: justify;'>
    Se destaca, por otra parte, que las mediciones de irradiancia que se toman
    a partir de una estación meteorológica, normalmente no coinciden con $ G $,
    puesto que se realizan sobre una superficie de prueba horizontal, y no en
    relación a la disposición real de los módulos. La obtención de $ G $ a
    partir de las mediciones es compleja y depende, entre otras cosas, de las
    coordenadas geográficas del GFV, es decir, su latitud y longitud; de la
    disposición espacial de los módulos, incluidas las inclinaciones; del
    momento preciso de análisis, es decir, año, mes, día, hora y zona horaria
    de implantación de la instalación; de la humedad relativa y temperatura
    del ambiente; y de las características de lo que se encuentra en los
    alrededores, en relación a su capacidad para reflejar en forma directa o
    difusa la radiación. No obstante, a los efectos de esta práctica, se
    utilizarán mediciones de irradiancia asumiendo, por simplicidad, que sus
    valores corresponden a $ G $.
    </div> \n""",
        altura=139,
    )

    """
    **3. Límites de generación**
    """

    justificado_latex(
        """
    Los circuitos inversores funcionan adecuadamente siempre que la producción,
    en términos de potencia,supere un umbral mínimo $ \\mu $, habitualmente
    expresado en forma porcentual, en relación a la potencia nominal $ P_{inv}
    $ del equipo. Si este umbral no es superado, la instalación no entrega
    potencia eléctrica. Asimismo, el valor $ P_{inv} $, en kilo-Watts, opera
    como límite superior del GFV. En consecuencia, la potencia real $ P_{r} $
    que entrega la instalación se puede calcular como:
    """,
        altura=100,
    )

    st.latex("""P_{min} = \\cfrac{\\mu (\\%)}{100} \\cdot P_{inv}""")

    st.latex(
        """\\begin{cases}
    0 & \\text{si} \\,\\,P\\leq P_{min} \\\\
    P & \\text{si}  \\,\\, P_{min}\\leq P_{inv} \\\\
    P_{inv} & \\text{si} \\,\\, P> P_{inv}
    \\end{cases} """
    )

    st.info(
        """Para información acerca de la carga y extracción de datos, así como
        un glosario de términos, consulte la sección *Ayuda* del menú lateral.
        """,
        icon="ℹ️",
    )

    st.subheader("Integrantes del equipo", divider="violet")
    col1, col2, col3 = st.columns([0.33, 0.33, 0.33])

    with col1:
        with st.expander(
            "**Santiago Ernesto Torres**", expanded=True,
            icon=":material/engineering:"
        ):

            st.markdown("*UTN - Facultad Regional Santa Fe*")
            st.markdown(":material/mail: storres@frsf.utn.edu.ar")
            st.markdown(":material/call: 342-516-1517")
            st.image("Archivos//Imagenes//Foto_santiago.png",
                     use_container_width=True)

    with col2:
        with st.expander(
            "**Leandro Ruíz Díaz**", expanded=True,
            icon=":material/engineering:"
        ):

            st.markdown("*UTN - Facultad Regional Santa Fe*")
            st.markdown(":material/mail: lruizdiaz@frsf.utn.edu.ar")
            st.markdown(":material/call: 340-452-2507")
            st.image("Archivos//Imagenes//Foto_leandro.png",
                     use_container_width=True)

    with col3:
        with st.expander(
            "**Manuel Garelik**", expanded=True, icon=":material/engineering:"
        ):
            st.markdown("*UTN - Facultad Regional Santa Fe*")
            st.markdown(":material/mail: magarelik@frsf.utn.edu.ar")
            st.markdown(":material/call: 342-554-7236")
            st.image("Archivos//Imagenes//Foto_manuel.png",
                     use_container_width=True)


# --- Sección 2.1: Datos ---
if seccion == "Datos":

    st.image(
        "Archivos//Imagenes//banner_calculo.jpg",
        use_container_width=True)
    # Todos los datos que tiene que cargar el usuario, utiliza como
    # predeterminados los de la UTN

    st.header("Carga de datos climatológicos", divider="blue")

    if "toggle_datos_especificos" not in st.session_state:
        # En este caso el código se ejecutaría por primera vez
        datos_especificos = st.toggle("Cargar nueva tabla")
        st.session_state["toggle_datos_especificos"] = datos_especificos
    else:
        # Es decir, si ya hay en session state datos especificos, porque
        # ya se corrió al menos una vez la página

        if st.session_state["toggle_datos_especificos"] is True:
            # Se verifica si interruptor quedo activado antes, queda activado:
            datos_especificos = st.toggle("Cargar nueva tabla", value=True)
        else:
            # Si el interruptor quedo desactivado, se deja desactivado:
            datos_especificos = st.toggle("Cargar nueva tabla")

        st.session_state["toggle_datos_especificos"] = datos_especificos
        # Se guarda el toggle de datos específicos con los valores ingresados
    st.info(
        """Los datos ingresados en forma de tabla deben estar completos,
        respetando intervalos de tiempo constantes. Si no se ingresan, se
        realizará el cálculo con los datos climatológicos de Santa Fe de 2019.
        """,
        icon="ℹ️",
    )

    if datos_especificos:  # Se activó el toggle
        datos_usuario = None
        datos_usuario = st.file_uploader(
            "Ingresá el archivo",
            help="Arrastra el archivo aquí o súbelo mediante el botón",
            accept_multiple_files=False,
        )
        if datos_usuario is None:
            # Verifica si el usuario subió un archivo
            st.session_state["datos_usuario"] = datos_usuario
            # Si no lo subió, se guarda None en session state
        else:
            # Si subió el archivo, este se lee y guarda en session state
            datos_usuario = pd.read_excel(datos_usuario, index_col=0)
            st.session_state["datos_usuario"] = datos_usuario

    if datos_especificos is False:  # No se activó el toggle
        # Si no hay datos especificos en el sesion state
        datos = st.session_state["datos"]
        st.session_state["tabla_en_uso"] = "Pred"
        # Se usa la tabla y datos predeterminados
    else:
        # Se verifica si los datos cargados son un dataframe
        if isinstance(datos_usuario, pd.DataFrame):
            st.session_state["datos_bien_cargados"] = st.session_state[
                "datos_usuario"]
            # Si están bien cargados, se usan
        else:
            datos = st.session_state["datos"]
            st.session_state["tabla_en_uso"] = "Pred"
            # Si están mal cargados, se usan los predeterminados

    if datos_especificos:
        if "datos_bien_cargados" not in st.session_state:
            datos = st.session_state["datos"]
            st.session_state["tabla_en_uso"] = "Pred"
            # Si no hay datos bien cargados en el session state, se usan pred.
        else:
            # Si estan bien cargados, se reemplazan en datos
            datos = st.session_state["datos_bien_cargados"]
            st.session_state["tabla_en_uso"] = "Usua"
    else:
        datos = st.session_state["datos"]
        st.session_state["tabla_en_uso"] = "Pred"
        # Si no se cargaron los datos específicos, se usan los predeterminados

    # Extraigo los indices de las columnas
    G, T, *_ = datos.columns

    st.header("Datos de la instalación", divider="red")
    with st.expander("**Datos**", expanded=False,
                     icon=":material/description:"):
        with st.form("formulario", clear_on_submit=False, border=False):
            col1, col2 = st.columns(2)
            with col1:
                N = st.number_input(
                    "Cantidad de Paneles", min_value=0, value=12, step=1
                )
                Gstd = st.number_input(
                    "Gstd Irradiancia estándar en $ W $/$ {m^2} $",
                    min_value=0.00,
                    value=1000.00,
                    step=100.00,
                    format="%2.2f",
                )
                Tr = st.number_input(
                    "Temperatura de referencia en $ °C $",
                    min_value=0.00,
                    value=25.0,
                    step=0.5,
                    format="%1.1f",
                )
                Ppico = st.number_input(
                    "Potencia Pico de cada modulo en $ W $",
                    min_value=0.00,
                    value=240.00,
                    step=10.00,
                    format="%2.2f",
                )

            with col2:
                kp = st.number_input(
                    "Coeficiente de Temperatura-Potencia en $ °C^{-1} $",
                    max_value=0.0000,
                    value=-0.0044,
                    step=0.0001,
                    format="%4.4f",
                )
                rend = st.number_input(
                    "Rendimiento global de la instalación",
                    min_value=0.00,
                    max_value=1.00,
                    value=0.97,
                    step=0.10,
                    format="%2.2f",
                )
                Pinv = st.number_input(
                    "Potencia maxima/trabajo del inversor en $ kW $",
                    min_value=0.00,
                    value=2.50,
                    step=0.50,
                    format="%2.2f",
                )
                umbral_minimo = st.number_input(
                    "Umbral minimo en %",
                    min_value=0.00,
                    value=0.00,
                    max_value=100.00,
                    step=1.00,
                    format="%2.2f",
                )

            #  Configuración botón para entregar
            entregado = st.form_submit_button(
                "Guardar datos",
                help="""Presione aquí para enviar sus
                respuestas""",
            )
            if entregado:
                # Barra de carga
                mensaje_progreso = "Cargando..."
                barra_progreso = st.progress(0, text=mensaje_progreso)
                # Se crea la barra de carga inicializada en 0

                for porcentaje_completado in range(100):
                    time.sleep(0.001)
                    # Se hacen 100 iteraciones, retrasando en cada una la
                    # ejecución por 0.001 segundos
                    barra_progreso.progress(
                        porcentaje_completado + 1, text=mensaje_progreso
                    )
                    # Actualiza la barra de progreso con el porcentaje
                    # incrementado en un 1%
                time.sleep(1)  # Pausa adicional de 1 seg cuando ya cargó
                barra_progreso.empty()  # Elimino barra de progreso

                st.success(" Datos guardados", icon="✅")

    # Corrijo la temperatura de celda en funcion a la temperatura ambiente
    datos["Temperatura de Celda (°C)"] = datos[T] + 0.031 * datos[G]
    Tc = datos["Temperatura de Celda (°C)"]

    # Calculo la potencia y la guardo en una nueva columna
    datos["Potencia (kW)"] = (
        N * datos[G] / Gstd * Ppico * (1 + kp * (Tc - Tr)) * rend * 1e-3
    )

    # Analizo si los valores de potencia estan dentro de rango, de no ser así
    # los reemplazo por el correspondiente
    Pmin = umbral_minimo / 100 * Pinv
    datos["Potencia (kW)"] = datos["Potencia (kW)"].where(
        datos["Potencia (kW)"] < Pinv, Pinv
        # Los datos de potencia se reemplazan siempre que sean menor a la del
        # inversor, sino se reemplazan por Pinv
    )
    datos["Potencia (kW)"] = datos["Potencia (kW)"].where(
        datos["Potencia (kW)"] > Pmin, 0
        # Los datos de potencia se reemplazan siempre que sean mayor a la
        # Pmin, sino se reemplazan por 0
    )
    # Muestro la Tabla (de aquí a proximas lineas)
    st.markdown("## Tabla Obtenida")

    # Genero dos columnas donde la primera es la tabla y ocupa el 70% de la
    # ventana, mientras que la otra la uso para seleccionar fechas:
    col1, col2 = st.columns([0.7, 0.3])

    with col2:

        # Calculo los intervalos de tiempo:
        intervalos = datos.index.to_series().diff().dropna()
        # Tomo de datos, los indíces, los transformo a serie de pandas,
        # y calculo la diferencia entre los elementos consecutivos (diff),
        # eliminando los valores NaN.

        intervalos = intervalos[0]  # Tomo el primer intervalo (todos iguales)
        # Le pido al usuario que seleccione que datos quiere ver, de
        # predeterminado muestra toda la tabla:

        fecha_inicial = st.date_input(
            "Seleccione Fecha Inicial",
            min_value=datos.index[0],
            max_value=datos.index[-1],
            key="fecha_inicial",
        )

        fecha_final = st.date_input(
            "Seleccione Fecha Inicial",
            min_value=datos.index[0],
            max_value=datos.index[-1],
            key="fecha_final",
        )

        st.session_state["fecha_inicial_est"] = fecha_inicial
        st.session_state["fecha_final_est"] = fecha_final
        # Mantengo las fechas cargadas en "Datos" en "Estadísticas"

        # Se define tiempo inicial y final, a cargar por usuario:
        tiempo_inicial = st.time_input(
            "Tiempo inicial", step=intervalos,
            value=st.session_state["tiempo_inicial"]
        )

        tiempo_final = st.time_input(
            "Tiempo final", step=intervalos,
            value=st.session_state["tiempo_final"]
        )

        st.session_state["tiempo_inicial"] = tiempo_inicial
        st.session_state["tiempo_final"] = tiempo_final
        # Guardo en el session state los tiempos para que se mantengan al
        # salir y volver a la sección de datos. Si no hay tiempos inicialmente
        # se ponen los del session state definido al principio.

    with col1:
        # Junto en un solo string la fecha y hora seleccionada para pasarsela
        # a la tabla
        fecha_inicial_seleccionado = (
            fecha_inicial.__str__() + " " + tiempo_inicial.__str__()
        )
        fecha_final_seleccionado = (fecha_final.__str__() + " " +
                                    tiempo_final.__str__())

        # Agrego una variable donde están los datos filtrados por el usuario
        datos_filtrados = datos.loc[
            fecha_inicial_seleccionado:fecha_final_seleccionado, :
        ]
        # Muestro la tabla
        st.dataframe(datos_filtrados, use_container_width=True)

        # Botón de descarga para la Tabla:

        # Crear archivo Excel en memoria
        archivo_temporal = BytesIO()  # Se crea una rchivo temporal en memoria
        datos_filtrados.to_excel(archivo_temporal, index=True)  # Se transforma
        # a excel el df, incluyendo las fechas (índices), y se sobreescribe en
        # el archivo temporal.
        archivo_temporal.seek(0)  # Permite que el botón de descarga pueda leer
        # desde el comienzo el archivo

        # Botón de descarga
        st.download_button(
            label="Descargar tabla en formato excel",
            data=archivo_temporal,
            file_name="Tabla_con_potencias.xlsx",
            mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
            sheet"""
            # El mime permite asegurar que el archivo es de Excel.
        )

    #
    # A PARTIR DE ACÁ VAN LAS GRÁFICAS
    #

    st.write("# Gráficas")
    st.info("""Para descargar cualquiera de las gráficas, pulse los tres
    puntos de la esquina superior derecha y seleccione el formato deseado
    """, icon="ℹ️")

    if len(datos_filtrados) > 10000:
        st.warning(
            """El rango seleccionado contiene demasiados datos para graficar.
            Se recomienda reducir el rango para mejorar el rendimiento del
            programa.""",
            icon="⚠️"
        )
        Limite_puntos = st.toggle("Deshabilitar limite de datos", value=False)
    else:
        Limite_puntos = True

    # Defino pestañas de gráficas:
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Gráfica de Potencia",
            "Gráficas de Temperaturas",
            "Gráfica de Irradiancia",
            "Gráfico de dispersión G-T",
        ]
    )

    # Verifico si la cantidad de puntos supera el límite donde se
    # realentizaría mucho la página (10000 puntos), si sucede, se muestra un
    # warning diciendo que son muchos los puntos como para realizar un gráfico.

    if Limite_puntos:
        # Si límite de puntos es True, significa que, o bien no se superó el
        # límite, o bien se activo el toggle para graficar igualmente
        with tab1:

            st.markdown("### Gráfico de Potencia")
            st.line_chart(
                data=datos_filtrados,
                y="Potencia (kW)",
                x_label="Fecha/Tiempo",
                y_label="Potencia (kW)",
            )

        with tab2:
            st.markdown("### Gráfica de Temperaturas")
            st.line_chart(
                data=datos_filtrados,
                y=["Temperatura de Celda (°C)", T],
                x_label="Fecha/Tiempo",
                y_label="Temperatura (°C)",
            )
            st.markdown("### Mapa de calor de Temperatura")
            mapa_de_calor = datos_filtrados.pivot_table(
                index=datos_filtrados.index, values=T, aggfunc="mean"
            ).sort_index(ascending=False)
            # Se usa como índice las fechas, y como valores las temperaturas,
            # de las cuales se calcula el promedio por HORA

            df = mapa_de_calor.reset_index()  # Guarda el índice como columna
            df["Fecha Formateada"] = df["Fecha"].dt.strftime("%Y-%m-%d")
            # Formatea fechas en año-mes-día

            # Mapa de calor interactivo usando Altair

            heatmap = (
                alt.Chart(df)  # Crea gráfico con el dataframe df
                .mark_rect()  # Especifica que es un mapa de calor
                .encode(
                    alt.X("Fecha Formateada:O", title="Fecha"),
                    y=alt.Y("hours(Fecha):O", title="Hora", sort="descending"),
                    color=alt.Color(
                        "Temperatura (°C):Q",
                        scale=alt.Scale(scheme="magma"),
                        title="Temperatura (°C)",
                    ),  # Colores según temperatura
                )
                .properties(title="Mapa de Calor: Temperatura por Día y Hora")
                .interactive()
            )  # Habilitar interactividad (paneo y zoom)

            # Mostrar el mapa de calor en Streamlit
            st.altair_chart(heatmap, use_container_width=True)

        with tab3:

            st.markdown("### Gráfica de Irradiancia")
            st.line_chart(
                data=datos_filtrados,
                y=G,
                x_label="Fecha/Tiempo",
                y_label="Irradiancia (W/m²)",
                color="#ffc300",
            )

        with tab4:

            st.markdown("### Gráfico de dispersión Irradiancia-Temperatura")
            st.scatter_chart(
                data=datos_filtrados,
                y=T,
                x=G,
                y_label="Temperatura (°C)",
                x_label="Irradiancia (W/m²)",
            )


# --- Sección 2.2: Estadísticas ---
if seccion == "Estadísticas":
    if "datos" not in st.session_state:
        st.warning('⚠️ No se poseen datos .')
    else:
        if st.session_state["tabla_en_uso"] == "Pred":
            datos = st.session_state["datos"]
            # Si usa la tabla pred, también los datos pred.
        else:
            datos = st.session_state["datos_bien_cargados"]
            # Sino, se usan los datos cargados como dataframe

        intervalos = datos.index.to_series().diff().dropna()
        intervalos = intervalos[0]
        # intervalo de tiempo entre índices consecutivos

        st.image(
            "Archivos//Imagenes//banner_est.jpg",
            use_container_width=True
            )
        st.header("Gráficas", divider="blue")
        st.info("""Para descargar cualquiera de las gráficas, pulse los tres
        puntos de la esquina superior derecha y seleccione el formato deseado
        """, icon="ℹ️")
        # El usuario elige si quiere los datos en días o semanas:
        option = st.selectbox(
            "Seleccione el período de tiempo deseado",
            ("Semanal", "Diario"),
        )

        col1, col2 = st.columns([0.7, 0.3])

        with col2:
            st.write("")
            st.write("")
            fecha_inicial_est = st.date_input(
                "Seleccione fecha inicial",
                min_value=datos.index[0],
                max_value=datos.index[-1],
                key="fecha_inicial_est",
            )
            fecha_final_est = st.date_input(
                "Seleccione fecha final",
                min_value=datos.index[0],
                max_value=datos.index[-1],
                key="fecha_final_est",
            )

            st.session_state["fecha_inicial"] = fecha_inicial_est
            st.session_state["fecha_final"] = fecha_final_est
            # Para que si se cambia o selecciona la fecha desde estadísticas,
            # también se tome esta fecha en la sección de datos.

            st.info(
                """Se toman de base las fechas cargadas en datos, pero si desea
                puede cambiarlas.""",
                icon="ℹ️"
            )

        with col1:
            tab1, tab2 = st.tabs(["Gráficas de Potencia",
                                  "Gráficas de Energía"])
            # Se establece el formato de las fechas iniciales y finales:
            fecha_inicial_seleccionado = (
                fecha_inicial_est.__str__()
                + " "
                + datetime.time.fromisoformat("00:00:00").__str__()
            )
            fecha_final_seleccionado = (
                fecha_final_est.__str__()
                + " "
                + datetime.time.fromisoformat("23:59:59").__str__()
            )

            chart_pot = datos[fecha_inicial_seleccionado:
                              fecha_final_seleccionado].drop(
                columns=[
                    "Temperatura (°C)",
                    "Irradiancia (W/m²)",
                    "Temperatura de Celda",
                ],
                errors="ignore",  # Evita error si la col eliminada no existe
            )  # Filtro fechas y le saco las columnas que no se necesitan
            with tab1:
                # Todo sobre POTENCIA en tab1

                if option == "Semanal":

                    # Calculos para potencia SEMANAL
                    if len(chart_pot.resample("W")) > 1:
                        potencia_media_SE = chart_pot.resample(
                            "W"
                        ).mean()  # Uso el resample para  tomar las
                        # semanas y el mean para calcular la media.
                        # SE significa Sin Editar, es decir, antes de realizar
                        # un formateo de indice (de igual forma termino
                        # utilizandolo modificado)

                        fechas_semanal = potencia_media_SE.index.to_list()
                        # Convierte el índice en una lista

                        if fechas_semanal[-1] != fecha_final_est:
                            fechas_semanal[-1] = fecha_final_est
                            # Si el último valor de la fechas en forma semanal,
                            # no es igual al final de la fecha seleccionada, se
                            # hacen coincidir

                        potencia_media_SE.index = fechas_semanal
                        # Ahora se reemplaza el indice de potencias (fechas),
                        # por las fechas corregidas (que coinciden con
                        # seleccionadas)

                        new_index = [
                            f"Week {fecha.year}-{fecha.month}-{fecha.day}"
                            for fecha in potencia_media_SE.index
                        ]
                        # Se define nuevo índice en el formato indicado
                        indice_no_string = new_index
                        new_index = pd.DataFrame(new_index, columns=["Fecha"])
                        # Se transforma la lista de índices a una sola columna
                        # de un dataframe
                        potencia_media_SE.index = indice_no_string
                        potencia_media_SE = potencia_media_SE.reset_index()
                        # Esto resetea el índice (1,2,...), y convierte el
                        # índice actual en una columna del df, llamada 'index'
                        potencia_media_SE["Fecha Formateada"] = (
                            potencia_media_SE["index"])
                        # Se le cambia el nombre a 'index' por 'fecha
                        # formateada'
                        grafico = (
                            alt.Chart(potencia_media_SE)
                            .mark_bar()  # Gráfico de barras
                            .encode(
                                x=alt.X(
                                    "index:N",
                                    sort=new_index,
                                    title="Fecha"),
                                y=alt.Y("Potencia (kW):Q"),
                            )
                            .interactive()
                        )
                        st.altair_chart(grafico, use_container_width=True)

                        potencia_media = potencia_media_SE.set_index(
                            "Fecha Formateada")
                        # Se convierte nuevamente el índice a fecha formateada.
                        C1P, C2P, C3P, *_ = potencia_media.columns
                        potencia_media = potencia_media.drop(C1P, axis=1).drop(
                            C2P, axis=1)
                        # Elimino dos columnas: C1P y C2P
                        st.subheader("Potencia", help="""Tabla de valores de la
                        gráfica anterior""")

                        st.write("**Potencia obtenida por semana**")
                        Nombres_col = {
                            "Fecha Formateada": "Fecha",
                            "Potencia (kW)": "Potencia [KW]",
                        }
                        st.dataframe(
                            potencia_media,
                            column_config=Nombres_col,
                            use_container_width=True,
                        )

                        potencia_media.rename_axis('Fecha', inplace=True)

                        # Crear archivo Excel en memoria
                        archivo_temporal_ps = BytesIO()
                        potencia_media.to_excel(
                            archivo_temporal_ps,
                            index=True
                            )
                        archivo_temporal_ps.seek(0)

                        # Botón de descarga
                        st.download_button(
                            label="Descargar tabla en formato excel",
                            data=archivo_temporal_ps,
                            file_name="Tabla_con_potencias_semanales.xlsx",
                            mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                            sheet"""
                        )
                    else:
                        st.warning("""Proporcione un intervalo de tiempo mayor
                        a una semana""", icon="⚠️")

                if option == "Diario":

                    # Calculos para potencia diaria
                    if len(chart_pot.resample("D")) > 1:
                        potencia_media_SE = chart_pot.resample("D").mean()
                        # Ahora se calcula la media tomando los días

                        potencia_media_SE = potencia_media_SE.reset_index()
                        potencia_media_SE[
                            "Fecha Formateada"] = potencia_media_SE[
                                "Fecha"].dt.strftime("%Y-%m-%d")

                        grafico = (
                            alt.Chart(potencia_media_SE)
                            .mark_bar()
                            .encode(
                                x=alt.X("Fecha Formateada:O", title="Fecha"),
                                y=alt.Y("Potencia (kW):Q"),
                            )
                            .interactive()
                        )

                        st.altair_chart(grafico, use_container_width=True)

                        # Aca va la tabla
                        potencia_media = potencia_media_SE.set_index(
                            "Fecha Formateada")
                        C1P, C2P, C3P, *_ = potencia_media.columns
                        potencia_media = potencia_media.drop(C1P, axis=1).drop(
                            C2P, axis=1)

                        st.subheader("Potencia", help="""Tabla de valores de la
                        gráfica anterior""")

                        st.write("**Potencia obtenida por día**")
                        Nombres_col = {
                            "Fecha Formateada": "Fecha",
                            "Potencia (kW)": "Potencia (KW)",
                        }
                        st.dataframe(
                            potencia_media,
                            column_config=Nombres_col,
                            use_container_width=True,
                        )

                        potencia_media.rename_axis('Fecha', inplace=True)

                        # Crear archivo Excel en memoria
                        archivo_temporal_pd = BytesIO()
                        potencia_media.to_excel(
                            archivo_temporal_pd,
                            index=True
                            )
                        archivo_temporal_pd.seek(0)

                        # Botón de descarga
                        st.download_button(
                            label="Descargar tabla en formato excel",
                            data=archivo_temporal_pd,
                            file_name="Tabla_con_potencias_diarias.xlsx",
                            mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                            sheet"""
                        )
                    else:
                        st.warning("""Proporcione un intervalo de tiempo mayor
                        a un día""", icon="⚠️")

            with tab2:

                # Todo sobre ENERGIA en tab2

                if option == "Semanal":
                    if len(chart_pot.resample("W")) > 1:

                        Energia_SE = chart_pot.resample(
                            "W"
                        ).mean()  # Uso el resample para tomar las
                        # semanas y el mean para calcular la media
                        contador_datos = chart_pot.resample("W").count()
                        # Cuenta la cantidad de datos por cada semana
                        contador_datos["contador_datos"] = (
                            contador_datos["Potencia (kW)"] * intervalos
                            # A la cantidad de datos de potencia la multiplica
                            # por el intervalo de tiempo al que corresponde
                            # cada dato
                        )
                        contador_datos = contador_datos.drop(
                            columns=[
                                "Temperatura de Celda (°C)",
                                "Potencia (kW)"],
                            errors="ignore",
                        )
                        # Se quitan columnas innecesarias
                        contador_datos = contador_datos.squeeze()
                        contador_datos = contador_datos.dt.days * 24
                        Energia_SE["Potencia (kW)"] = (
                            Energia_SE["Potencia (kW)"] * contador_datos
                        )

                        fechas_semanal = Energia_SE.index.to_list()
                        # Se hacen coincidir las fechas:
                        if fechas_semanal[-1] != fecha_final_est:
                            fechas_semanal[-1] = fecha_final_est

                        Energia_SE.index = fechas_semanal

                        new_index = [
                            f"Week {fecha.year}-{fecha.month}-{fecha.day}"
                            for fecha in Energia_SE.index
                        ]
                        indice_no_string = new_index
                        new_index = pd.DataFrame(new_index, columns=["Fecha"])

                        Energia_SE.index = indice_no_string
                        Energia_SE = Energia_SE.reset_index()
                        Energia_SE["Fecha Formateada"] = Energia_SE["index"]
                        grafico = (
                            alt.Chart(Energia_SE)
                            .mark_bar(color="yellowgreen")
                            .encode(
                                x=alt.X(
                                    "index:N",
                                    sort=new_index,
                                    title="Fecha"),
                                y=alt.Y(
                                    "Potencia (kW):Q",
                                    title="Energía (kWh)"),
                            )
                            .interactive()
                        )
                        st.altair_chart(grafico, use_container_width=True)

                        Energia = Energia_SE.set_index("Fecha Formateada")
                        C1E, C2E, C3E, *_ = Energia.columns
                        Energia = Energia.drop(C1E, axis=1).drop(C2E, axis=1)

                        st.subheader("Energía", help="""Tabla de valores de la
                        gráfica anterior""")

                        st.write("**Energía obtenida por semana**")
                        Nombres_col = {
                            "Fecha Formateada": "Fecha",
                            "Potencia (kW)": "Energía (kWh)",
                        }
                        st.dataframe(
                            Energia, column_config=Nombres_col,
                            use_container_width=True
                        )

                        Energia.rename(
                            columns={'Potencia (kW)': 'Energía (kWh)'},
                            inplace=True)
                        Energia.rename_axis('Fecha', inplace=True)

                        # Crear archivo Excel en memoria
                        archivo_temporal_es = BytesIO()
                        Energia.to_excel(archivo_temporal_es, index=True)
                        archivo_temporal_es.seek(0)

                        # Botón de descarga
                        st.download_button(
                            label="Descargar tabla en formato excel",
                            data=archivo_temporal_es,
                            file_name="Tabla_con_energía_semanal.xlsx",
                            mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                            sheet"""
                        )
                    else:
                        st.warning("""Proporcione un intervalo de tiempo mayor
                        a una semana""", icon="⚠️")

                if option == "Diario":
                    if len(chart_pot.resample("D")) > 1:
                        Energia_SE = chart_pot.resample(
                            "D"
                        ).mean()  # Uso el resample para tomar los dias y
                        # el mean para calcular la media
                        Energia_SE["Potencia (kW)"] = Energia_SE[
                            "Potencia (kW)"] * 24
                        Energia_SE = Energia_SE.reset_index()
                        Energia_SE["Fecha Formateada"] = Energia_SE[
                            "Fecha"].dt.strftime(
                            "%Y-%m-%d"
                        )

                        grafico = (
                            alt.Chart(Energia_SE)
                            .mark_bar(color="yellowgreen")
                            .encode(
                                x=alt.X(
                                    "Fecha Formateada:O",
                                    title="Fecha"),
                                y=alt.Y(
                                    "Potencia (kW):Q",
                                    title="Energía (kWh)"),
                            )
                            .interactive()
                        )

                        st.altair_chart(grafico, use_container_width=True)

                        Energia = Energia_SE.set_index("Fecha Formateada")
                        C1E, C2E, C3E, *_ = Energia.columns
                        Energia = Energia.drop(C1E, axis=1).drop(C2E, axis=1)

                        st.subheader("Energía", help="""Tabla de valores de la
                        gráfica anterior""")

                        Top_Energia = Energia.sort_values(
                            by="Potencia (kW)", ascending=False
                        )
                        st.markdown("**Energía obtenida por día**")
                        Nombres_col = {
                            "Fecha Formateada": "Fecha",
                            "Potencia (kW)": "Energía (kWh)",
                        }
                        st.dataframe(
                            Energia, column_config=Nombres_col,
                            use_container_width=True
                        )

                        Energia.rename(
                            columns={'Potencia (kW)': 'Energía (kWh)'},
                            inplace=True)
                        Energia.rename_axis('Fecha', inplace=True)

                        # Crear archivo Excel en memoria
                        archivo_temporal_ed = BytesIO()
                        Energia.to_excel(archivo_temporal_ed, index=True)
                        archivo_temporal_ed.seek(0)

                        # Botón de descarga
                        st.download_button(
                            label="Descargar tabla en formato excel",
                            data=archivo_temporal_ed,
                            file_name="Tabla_con_energía_diaria.xlsx",
                            mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                            sheet"""
                        )
                    else:
                        st.warning("""Proporcione un intervalo de tiempo mayor
                        a un día""", icon="⚠️")
        #
        # Todo sobre Datos caracteristicos
        #

        st.header("Datos característicos", divider="red")
        if option == "Diario":
            if len(chart_pot.resample("D")) > 1:
                Energia = Energia_SE.set_index("Fecha Formateada")
                C1E, C2E, C3E, *_ = Energia.columns
                Energia = Energia.drop(C1E, axis=1).drop(C2E, axis=1)
                potencia_media = potencia_media_SE.set_index(
                    "Fecha Formateada")
                C1P, C2P, C3P, *_ = potencia_media.columns
                potencia_media = potencia_media.drop(C1P, axis=1).drop(
                    C2P,
                    axis=1)
        if option == "Semanal":
            if len(chart_pot.resample("w")) > 1:
                Energia = Energia_SE.set_index("Fecha Formateada")
                C1E, C2E, C3E, *_ = Energia.columns
                Energia = Energia.drop(C1E, axis=1).drop(C2E, axis=1)
                potencia_media = potencia_media_SE.set_index(
                    "Fecha Formateada")
                C1P, C2P, C3P, *_ = potencia_media.columns
                potencia_media = potencia_media.drop(C1P, axis=1).drop(
                    C2P,
                    axis=1)

        col1, col2 = st.columns([0.5, 0.5], gap="large")
        with col1:
            # Potencias en col1

            st.markdown("### Potencia")
            if option == "Diario":
                if len(chart_pot.resample("D")) > 1:
                    Top_potencias = potencia_media.sort_values(
                        by="Potencia (kW)", ascending=False
                    ).head(10)
                    st.write("**Días de mayor Potencia obtenida**")
                    Nombres_col = {
                        "Fecha Formateada": "Fecha",
                        "Potencia (kW)": "Potencia (KW)",
                    }
                    st.dataframe(
                        Top_potencias, column_config=Nombres_col,
                        use_container_width=True
                    )

                    Top_potencias.rename_axis('Fecha', inplace=True)

                    # Crear archivo Excel en memoria
                    archivo_temporal_tpd = BytesIO()
                    Top_potencias.to_excel(archivo_temporal_tpd, index=True)
                    archivo_temporal_tpd.seek(0)

                    # Botón de descarga
                    st.download_button(
                        label="Descargar tabla en formato excel",
                        data=archivo_temporal_tpd,
                        file_name="Tabla_con_mayores_potencias_diarias.xlsx",
                        mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                        sheet"""
                    )

            if option == "Semanal":
                if len(chart_pot.resample("W")) > 1:
                    Top_potencias = potencia_media.sort_values(
                        by="Potencia (kW)", ascending=False
                    ).head(10)
                    st.write("**Semanas de mayor Potencia obtenida**")
                    Nombres_col = {
                        "Fecha Formateada": "Fecha",
                        "Potencia (kW)": "Potencia [KW]",
                    }
                    st.dataframe(
                        Top_potencias, column_config=Nombres_col,
                        use_container_width=True
                    )

                    Top_potencias.rename_axis('Fecha', inplace=True)

                    # Crear archivo Excel en memoria
                    archivo_temporal_tps = BytesIO()
                    Top_potencias.to_excel(archivo_temporal_tps, index=True)
                    archivo_temporal_tps.seek(0)

                    # Botón de descarga
                    st.download_button(
                        label="Descargar tabla en formato excel",
                        data=archivo_temporal_tps,
                        file_name="Tabla_con_mayores_potencias_semanales.xlsx",
                        mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                        sheet"""
                    )

        with col2:

            # Energia en col2
            st.markdown("### Energía")
            if option == "Diario":
                if len(chart_pot.resample("D")) > 1:
                    Top_Energia = Energia.sort_values(
                        by="Potencia (kW)", ascending=False
                    ).head(10)
                    st.markdown("**Días de mayor Energía obtenida**")
                    Nombres_col = {
                        "Fecha Formateada": "Fecha",
                        "Potencia (kW)": "Energía (kWh)",
                    }
                    st.dataframe(
                        Top_Energia, column_config=Nombres_col,
                        use_container_width=True
                    )

                    Top_Energia.rename_axis('Fecha', inplace=True)
                    Top_Energia.rename(
                        columns={'Potencia (kW)': 'Energía (kWh)'},
                        inplace=True
                        )

                    # Crear archivo Excel en memoria
                    archivo_temporal_ted = BytesIO()
                    Top_Energia.to_excel(archivo_temporal_ted, index=True)
                    archivo_temporal_ted.seek(0)

                    # Botón de descarga
                    st.download_button(
                        label="Descargar tabla en formato excel",
                        data=archivo_temporal_ted,
                        file_name="Tabla_con_mayores_energías_diarias.xlsx",
                        mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                        sheet"""
                    )

            if option == "Semanal":
                if len(chart_pot.resample("W")) > 1:
                    Top_Energia = Energia.sort_values(
                        by="Potencia (kW)", ascending=False
                    ).head(10)
                    st.write("**Semanas de mayor Energía obtenida**")
                    Nombres_col = {
                        "Fecha Formateada": "Fecha",
                        "Potencia (kW)": "Energía (kWh)",
                    }
                    st.dataframe(
                        Top_Energia, column_config=Nombres_col,
                        use_container_width=True
                    )

                    Top_Energia.rename_axis('Fecha', inplace=True)
                    Top_Energia.rename(
                        columns={'Potencia (kW)': 'Energía (kWh)'},
                        inplace=True
                        )

                    # Crear archivo Excel en memoria
                    archivo_temporal_tes = BytesIO()
                    Top_Energia.to_excel(archivo_temporal_tes, index=True)
                    archivo_temporal_tes.seek(0)

                    # Botón de descarga
                    st.download_button(
                        label="Descargar tabla en formato excel",
                        data=archivo_temporal_tes,
                        file_name="Tabla_con_mayores_enerías_semanales.xlsx",
                        mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                        sheet"""
                    )

        # Apartado de maximos y minimos

        st.header("Valores extremos", divider="green")
        datfil = datos[fecha_inicial_seleccionado:fecha_final_seleccionado]
        col1, col2 = st.columns(2)
        st.info(
            """En caso de que existan varios mínimos o máximos absolutos,
            en la tabla se muestra la fecha del primero de ellos.""",
            icon="ℹ️"
        )

        if option == "Semanal":
            if len(chart_pot.resample("W")) > 1:
                with col1:
                    # Col 1 para maximos (semanal)

                    st.subheader("Máximos")

                    tabla_max = pd.DataFrame(
                        {
                            "Fecha": [
                                datfil["Temperatura (°C)"].idxmax(),
                                datfil["Irradiancia (W/m²)"].idxmax(),
                                datfil["Potencia (kW)"].idxmax(),
                                potencia_media["Potencia (kW)"].idxmax(),
                                Energia["Potencia (kW)"].idxmax(),
                            ],
                            "Máximo": [
                                datfil["Temperatura (°C)"].max(),
                                datfil["Irradiancia (W/m²)"].max(),
                                datfil["Potencia (kW)"].max(),
                                potencia_media["Potencia (kW)"].max(),
                                Energia["Potencia (kW)"].max(),
                            ],
                        }
                    )
                    tabla_max.index = [
                        "Temperatura (°C)",
                        "Irradiancia (W/m²)",
                        "Potencia (kW)",
                        "Potencia Media Semanal (kW)",
                        "Energía Media Semanal (kWh)",
                    ]
                    st.dataframe(tabla_max)

                    # Crear archivo Excel en memoria
                    archivo_temporal_maxs = BytesIO()
                    tabla_max.to_excel(archivo_temporal_maxs, index=True)
                    archivo_temporal_maxs.seek(0)

                    # Botón de descarga
                    st.download_button(
                        label="Descargar tabla en formato excel",
                        data=archivo_temporal_maxs,
                        file_name="Tabla_con_máximos_semanales.xlsx",
                        mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                        sheet"""
                    )

                with col2:
                    # Col 2 minimos (semanal)

                    st.subheader("Mínimos")

                    tabla_min = pd.DataFrame(
                        {
                            "Fecha": [
                                datfil["Temperatura (°C)"].idxmin(),
                                datfil["Irradiancia (W/m²)"].idxmin(),
                                datfil["Potencia (kW)"].idxmin(),
                                potencia_media["Potencia (kW)"].idxmin(),
                                Energia["Potencia (kW)"].idxmin(),
                            ],
                            "Mínimo": [
                                datfil["Temperatura (°C)"].min(),
                                datfil["Irradiancia (W/m²)"].min(),
                                datfil["Potencia (kW)"].min(),
                                potencia_media["Potencia (kW)"].min(),
                                Energia["Potencia (kW)"].min(),
                            ],
                        }
                    )
                    tabla_min.index = [
                        "Temperatura (°C)",
                        "Irradiancia (W/m²)",
                        "Potencia (kW)",
                        "Potencia Media Semanal (kW)",
                        "Energía Media Semanal (kWh)",
                    ]
                    st.dataframe(tabla_min)

                    # Crear archivo Excel en memoria
                    archivo_temporal_mins = BytesIO()
                    tabla_min.to_excel(archivo_temporal_mins, index=True)
                    archivo_temporal_mins.seek(0)

                    # Botón de descarga
                    st.download_button(
                        label="Descargar tabla en formato excel",
                        data=archivo_temporal_mins,
                        file_name="Tabla_con_mínimos_semanales.xlsx",
                        mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                        sheet"""
                    )

        if option == "Diario":
            if len(chart_pot.resample("D")) > 1:
                with col1:

                    # Col 1 para maximos (diarios)

                    st.subheader("Máximos")

                    tabla_max = pd.DataFrame(
                        {
                            "Fecha": [
                                datfil["Temperatura (°C)"].idxmax(),
                                datfil["Irradiancia (W/m²)"].idxmax(),
                                datfil["Potencia (kW)"].idxmax(),
                                potencia_media["Potencia (kW)"].idxmax(),
                                Energia["Potencia (kW)"].idxmax(),
                            ],
                            "Máximo": [
                                datfil["Temperatura (°C)"].max(),
                                datfil["Irradiancia (W/m²)"].max(),
                                datfil["Potencia (kW)"].max(),
                                potencia_media["Potencia (kW)"].max(),
                                Energia["Potencia (kW)"].max(),
                            ],
                        }
                    )
                    tabla_max.index = [
                        "Temperatura (°C)",
                        "Irradiancia (W/m²)",
                        "Potencia (kW)",
                        "Potencia Media Diaria (kW)",
                        "Energía Media Diaria (kWh)",
                    ]
                    st.dataframe(tabla_max)

                    # Crear archivo Excel en memoria
                    archivo_temporal_maxd = BytesIO()
                    tabla_max.to_excel(archivo_temporal_maxd, index=True)
                    archivo_temporal_maxd.seek(0)

                    # Botón de descarga
                    st.download_button(
                        label="Descargar tabla en formato excel",
                        data=archivo_temporal_maxd,
                        file_name="Tabla_con_máximos_diarios.xlsx",
                        mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                        sheet"""
                    )

                with col2:

                    # Col 2 para minimos (diarios)

                    st.subheader("Mínimos")

                    tabla_min = pd.DataFrame(
                        {
                            "Fecha": [
                                datfil["Temperatura (°C)"].idxmin(),
                                datfil["Irradiancia (W/m²)"].idxmin(),
                                datfil["Potencia (kW)"].idxmin(),
                                potencia_media["Potencia (kW)"].idxmin(),
                                Energia["Potencia (kW)"].idxmin(),
                            ],
                            "Mínimo": [
                                datfil["Temperatura (°C)"].min(),
                                datfil["Irradiancia (W/m²)"].min(),
                                datfil["Potencia (kW)"].min(),
                                potencia_media["Potencia (kW)"].min(),
                                Energia["Potencia (kW)"].min(),
                            ],
                        }
                    )
                    tabla_min.index = [
                        "Temperatura (°C)",
                        "Irradiancia (W/m²)",
                        "Potencia (kW)",
                        "Potencia Media Diaria (kW)",
                        "Energía Media Diaria (kWh)",
                    ]
                    st.dataframe(tabla_min)

                    # Crear archivo Excel en memoria
                    archivo_temporal_mind = BytesIO()
                    tabla_min.to_excel(archivo_temporal_mind, index=True)
                    archivo_temporal_mind.seek(0)

                    # Botón de descarga
                    st.download_button(
                        label="Descargar tabla en formato excel",
                        data=archivo_temporal_mind,
                        file_name="Tabla_con_mínimos_diarios.xlsx",
                        mime="""application/vnd.openxmlformats-officedocument.spreadsheetml.
                        sheet"""
                    )


# --- Sección 2.3: Mapas ---
if seccion == "Mapas":
    st.image("Archivos//Imagenes//banner_mapa.jpg", use_container_width=True)
    st.info(
        """Cargue la ubicación del GFV analizado, si no ingresa ningún
            valor se mostrará por defecto la ubicación de los paneles de la
            UTN-FRSF.
            """,
        icon="ℹ️",
    )
    with st.expander(
        "**Ubicación del generador fotovoltaico**",
        icon=":material/location_on:"
    ):
        latitud = st.number_input(
            "Latitud",
            min_value=-90.00000000000000,
            max_value=90.00000000000000,
            value=-31.616681297694267,
            format="%.14f",
            step=1.00000000000000,
        )
        longitud = st.number_input(
            "Longitud",
            min_value=-180.00000000000000,
            max_value=180.00000000000000,
            value=-60.67543483706093,
            format="%.14f",
            step=1.00000000000000,
        )
    tab1, tab2, tab3 = st.tabs(
        ["Exploración geográfica", "Mapa de irradiancias",
         "Mapa de temperaturas"]
    )
    with tab1:
        opciones = st.selectbox(
            "Seleccione el mapa que desea para ver la ubicación de su GFV:",
            ["Mapa político", "Mapa satelital"],
        )
        if opciones == "Mapa político":
            st.subheader("Mapa Político")
            # mapa
            mapa = folium.Map(location=[latitud, longitud], zoom_start=18)
            # Las coordenadas de location indican el centro del mapa

            # Ahora se hace el marcador puntual
            folium.Marker(
                [latitud, longitud],
                popup="Ubicación generador fotovoltaico",
            ).add_to(mapa)

            # Mostrar el mapa:
            st_folium(mapa, use_container_width=True)

        elif opciones == "Mapa satelital":
            st.subheader("Mapa Satelital")
            # Se usa el iframe y con código en html se muestra el mapa
            components.html(
                f"""
                    <iframe
                        src="https://www.google.com/maps?q={latitud},{longitud}&t=k&hl=es&z=15&output=embed"
                        width="1400"
                        zoom="16"
                        height="700"
                        style="border:0;"
                        allowfullscreen=""
                        loading="lazy">
                    </iframe>
                """,
                height=700,
            )

        st.write("---")
        st.info(
            """Todos los mapas mostrados en esta página fueron extraídos de
            *Google Maps*, para consultar la web oficial, acceder desde *links
            de interés* (en el menú lateral)
            """,
            icon="ℹ️",
        )

    with tab2:
        st.subheader(
            "Mapa interactivo de irradiancia solar",
            help="""Obtenido de *Windy*""",
        )
        st.info(
            """Para utilizar el mapa puede mover el puntero que muestra la
            irradiancia. Además, al presionar sobre cualquier región o
            localidad, podrá ver un pronóstico del clima durante la semana
            actual"""
        )
        components.html(
            f"""<iframe width="1400" height="700" src="https://embed.windy.com/
            embed.html?type=map&location=coordinates&metricRain=default&
            metricTemp=default&metricWind=default&zoom=5&overlay=solarpower&
            product=ecmwf&level=surface&lat={latitud}&lon={longitud}&detailLat=
            {latitud}&detailLon={longitud}&marker=True" frameborder="0"></
            iframe>
            """,
            height=700,
        )
        st.write("---")
        st.info(
            """Si desea obtener un mapa de cualquier característica climática,
            pulse el botón de la esquina superior derecha donde indica 'Energía
            Solar' y podrá cambiar al mapa que busque. Para más mapas de
            irradiación interactivos consultar *Windy*, *Global Solar
            Atlas* o *NASA POWER* (links en menú lateral)""",
            icon="ℹ️",
        )

    with tab3:
        st.subheader(
            "Mapa interactivo de temperaturas medias",
            help="Obtenido de *Windy*",
        )
        st.info(
            """Para utilizar el mapa puede mover el puntero que muestra la
            temperatura. Además, al presionar sobre cualquier región o
            localidad, podrá ver un pronóstico del clima durante la semana
            actual
            """
        )
        components.html(
            f"""<iframe width="1400" height="700" src="https://embed.windy.com/
            embed.html?type=map&location=coordinates&metricRain=default&
            metricTemp=default&metricWind=default&zoom=5&overlay=temp&product=
            ecmwf&level=surface&lat={latitud}&lon={longitud}&detailLat=
            {latitud}&detailLon={longitud}&marker=true" frameborder="0"></
            iframe>
            """,
            height=700,
        )
        st.write("---")
        st.info(
            """Si desea obtener un mapa de cualquier característica climática,
            pulse el botón de la esquina superior derecha donde indica
            'Temperatura' y podrá cambiar al mapa que busque. Para más mapas
            de temperatura consultar *Windy* o *Servicio Meteorológico
            Nacional* (links en menú lateral)
            """,
            icon="ℹ️",
        )


# --- Sección 3: Ayuda ---
if seccion == "Ayuda":
    st.header("Ayuda y soporte de la página", divider="orange")
    with st.expander("**Importante**", icon="⚠️"):
        st.write(
            """Esta página aún se encuentra en un estado primitivo, para usar
            el chat por favor ingrese solamente el **número** de la opción que
            elija."""
        )
    with st.chat_message("assistant"):
        st.write("Hola! Escribí la opción sobre la que deseas obtener ayuda: ")
        """
            1. *Guía de la página*
            2. *Definiciones y glosario de términos*
            3. *Preguntas frecuentes (FAQs)*
            4. *Otro*
            """
    texto = st.chat_input("Escriba aquí...")
    if texto == "1":
        with st.chat_message("assistant"):
            texto = """
            *Guía de la página* \n
            La página cuenta con cuatro secciones principales:
            * ***Acerca de***, donde podrás encontrar una breve descripción de
            la página, información de los desarrolladores y la explicación del
            modelo matemático utilizado.
            * ***Generador***, es la sección
            principal y se encuentra, a su vez, subdividida en tres categorías,
            "*Datos*", donde pueden cargarse los datos del generador que se
            desea calcular, o usar los datos por defecto del generador de la
            FRSF-UTN; "*Estadísticas*", donde podrá encontrar valores
            representativos del generador, en las mismas fechas que las
            cargadas en Datos; y "*Mapas*", donde podrá visualizar una imagen
            satelital de la ubicación del generador, habiendo ingresado
            coordenadas de latitud y longitud, además de tener mapas estáticos
            de irradiancias y temperaturas de Argentina.
            * ***Ayuda***, sección en la que se haya actualmente.
            * ***Feedback***, donde podrá encontrar un breve cuestionario
            acerca de su experiencia con la página, lo que nos permitirá
            incorporar mejoras a futuro.

            Si necesitas ver la ayuda de otra opción, ingresa el número debajo
            nuevamente!
            """

            # Crear un contenedor vacío
            texto_placeholder = st.empty()

            # Escribir el texto gradualmente
            texto_parcial = ""
            for word in texto.split(" "):  # Split divide el texto en palabras
                texto_parcial = (
                    texto_parcial + word + " "
                )  # En cada iteración se agrega una palabra y un espacio,
                # y se va guardando en texto parcial.
                texto_placeholder.markdown(
                    texto_parcial
                )  # Actualizo el contenedor con el texto parcial, usando
                # markdown para mantener formatos.
                time.sleep(0.013)  # Tiempo para dar dinamismo al chat

    if texto == "2":
        with st.chat_message("assistant"):
            texto = """
            *Definiciones generales*

            * **GFV**: Generador Fotovoltaico. Un generador fotovoltaico es un
            sistema que convierte la energía del sol en electricidad. Los
            generadores solares funcionan mediante paneles fotovoltaicos,
            también conocidos como paneles solares, que absorben la luz del
            sol y la transforman en electricidad.

            * **Inversor**: Un inversor fotovoltaico, también conocido como
            inversor solar, es un dispositivo que transforma la corriente
            continua (CC) que generan los paneles solares en corriente alterna
            (CA), la cual es la utilizada en las instalaciones.

            * **Regulador**: Un regulador de carga, también conocido como
            controlador de carga, es un dispositivo electrónico que se utiliza
            en un sistema fotovoltaico para controlar el flujo de energía
            entre los paneles solares y las baterías.

            *Glosario de términos* \n
            A continuación encontrarás una lista con las abreviaturas y una
            explicación más detallada de todos los parámetros utilizados en el
            modelo matemático:

            * $ N $: es el número de paneles fotovoltaicos con los que cuenta
            el generador, tanto en serie como en paralelo.
            Resulta de la multiplicación del número de módulos en serie por el
            número de módulos en paralelo o, de forma matemática:
            $ N = N_{serie} \\cdot N_{paralelo} $.

            * $ G $: Irradiancia global incidente en forma normal a los
            módulos $ W $/$ m^{2} $. La irradiancia mide el flujo de energía
            proveniente de la radiación solar (sea de forma directa o
            indirecta) por unidad de superficie incidente.

            * $ G_{std} $: Irradiancia estándar, comúnmente en $ W $/$ m^{2} $.
            Es un valor de irradiancia que utilizan los fabricantes de los
            módulos para referenciar ciertas características técnicas.
            Normalmente $ G_{std} = 1000 $ $ W $/$ m^{2} $.

            * $ P_{pico} $: Potencia pico de cada módulo en $ W $. Se
            interpreta como la potencia eléctrica que entrega un módulo cuando
            $ G $ coincide con $ G_{std} $ y cuando $ T_{c} $ coincide con
            $ T_{r} $, en ausencia de viento y sin que el panel se vincule a
            otros componentes eléctricos que afecten el desempeño de la
            instalación. Constituye la potencia nominal bajo la cual los
            módulos son comercializados.

            * $ k_{p} $: Coeficiente de temperatura-potencia en $ °C^{-1} $.Es
            un parámetro negativo que refleja cómo incide la temperatura de la
            celda en el rendimiento del GFV. Se observa que incrementos
            (disminuciones) de $ T_{c} $ producen, en consecuencia,
            disminuciones (incrementos) de $ P $.

            * $ T_{c} $: Temperatura de la celda. Temperatura de la celda, en
            $ °C $. Es la temperatura de los componentes semiconductores que
            conforman cada módulo fotovoltaico.

            * $ T_{r} $: Temperatura de referencia, en Celsius. Es una
            temperatura utilizada por los fabricantes de los módulos para
            referenciar ciertos parámetros que dependen de la temperatura.
            Normalmente $ Tr =( 25 °C ) $.

            * $ \\eta $: Rendimiento global del sistema. Rendimiento global de
            la instalación “por unidad” (valor ideal: 1). Se utiliza para
            considerar el efecto de sombras parciales sobre el GFV, suciedad
            sobre la superficie de los módulos y, fundamentalmente, el
            rendimiento del equipo controlador-inversor. Los inversores
            contemplados por el modelo de la también incluyen el sistema de
            control para maximizar la potencia de salida.

            Si necesitas ver la ayuda de otra opción, ingresa el número debajo
            nuevamente!
            """

            # Crear un contenedor vacío
            texto_placeholder = st.empty()

            # Escribir el texto gradualmente
            texto_parcial = ""
            for word in texto.split(" "):
                texto_parcial = texto_parcial + word + " "
                texto_placeholder.markdown(texto_parcial)
                time.sleep(0.013)

    if texto == "3":
        with st.chat_message("assistant"):
            st.write("Descripción opción 3")
            """
            Aquí encontrarás preguntas frecuentes que pueden ayudarte en la
            utilización de la app web:
            """
            st.info(
                """¿Puedo descargar los resultados de los cálculos y los
                    gráficos?"""
            )
            with st.expander("Respuesta", icon=":material/add_circle:"):
                """
                Sí! Puedes descargar los resultados y gráficos en el formato
                que desees, encuentra los botones de descargas al final de
                cada análisis!
                """

            st.info("¿Qué sucede si ingreso datos incorrectos?")
            with st.expander("Respuesta", icon=":material/add_circle:"):
                """
                La aplicación está desarrollada automaticamente para validar
                los datos que han sido cargados, si detecta valores valores
                inconsistentes o fuera del rango que corresponde, se mostrará
                un mensaje de error con instrucciones para
                corregirlo.
                """

            st.info(
                """Puedo usar esta herramienta para un generador distinto al de
                la UTN-FRSF?"""
            )
            with st.expander("Respuesta", icon=":material/add_circle:"):
                """
                Por supuesto! Si bien esta aplicación fue desarrollada
                incialmente para analizar los datos del GFV de la UTN - FRSF,
                puedes cargar los datos de cualquier generador **(siempre en
                el formato adecuado)** y extraer los resultados.
                """

            st.info(
                """Que pasa si quiero analizar un período prolongado de
                    datos?"""
            )
            with st.expander("Respuesta", icon=":material/add_circle:"):
                """
                Podrás hacerlo, de todas formas la página te otorgorá
                advertencias, ya que no es recomendable debido a la
                disminución del rendimiento y aumento en el tiempo de
                ejecución.
                """

        """
       Si necesitas ver la ayuda de otra opción, ingresa el número debajo
       nuevamente!
       """

    if texto == "4":
        with st.chat_message("assistant"):
            texto = """
            Si todavía tienes dudas o inconvenientes con la página, te
            recomendamos realizar el formulario disponible en **Feedback** o
            contactar alguna de las siguientes direcciones de correo
            electrónico: \n
            :material/mail: storres@frsf.utn.edu.ar \n
            :material/mail: magarelik@frsf.utn.edu.ar \n
            :material/mail: lruizdiaz@frsf.utn.edu.ar \n
            """

            # Crear un contenedor vacío
            texto_placeholder = st.empty()

            # Escribir el texto gradualmente
            texto_parcial = ""
            for word in texto.split(" "):
                texto_parcial = texto_parcial + word + " "
                texto_placeholder.markdown(texto_parcial)
                time.sleep(0.013)
    if texto == 'pascuas':
        st.link_button("Trust me", "https://matias.me/nsfw/", icon='🥚')

# --- Sección 4: Feedback ---
if seccion == "Feedback":
    st.header("Dejá tu comentario!", divider="blue")
    with st.form("formulario", clear_on_submit=True):
        #  Datos del encuestado
        st.text_input("Introduzca su nombre", placeholder="Nombre Apellido")
        st.text_input(
            "Introduzca su correo electrónico", placeholder="correo@gmail.com"
        )
        notificaciones = st.checkbox(
            """¿Desea recibir respuesta a su feedback y notificaciones sobre
            próximos cambios en la página?"""
        )
        st.write("---")

        #  Puntuaciones de la página
        st.write(
            """Puntúe su experiencia con la aplicación en las siguientes
            categorías:"""
        )
        st.info(
            """Elija entre Insuficiente (menor puntuación) y Excelente (mayor
            puntuación).""",
            icon="ℹ️",
        )
        opciones = ["Insuficiente", "Regular", "Bueno", "Muy bueno",
                    "Excelente"]
        st.select_slider(
            "¿Que tan sencillo le fue utilizar esta aplicación?",
            options=opciones,
            value="Bueno",
        )  # VER SI USAMOS DEFINIR ESTO PARA ALGO
        st.select_slider(
            "¿Que tan útiles fueron las funciones ofrecidas?",
            options=opciones,
            value="Bueno",
        )
        st.select_slider(
            "¿Que tan actractiva visualmente encontró la aplicación?",
            options=opciones,
            value="Bueno",
        )
        st.write("---")
        st.write("Dale una puntuación general a la aplicación")
        st.info(
            """Elija entre 1 estrella (menor puntuación) y 5 estrellas (mayor
            puntuación).""",
            icon="ℹ️",
        )
        st.feedback("stars")
        st.write("---")

        #  Comentarios adicionales
        st.text_area(
            "Agregue cualquier otro comentario que desee",
            placeholder="Escriba aquí...",
            max_chars=500,
        )

        #  Configuración botón para entregar
        entregado = st.form_submit_button(
            "Enviar", help="Presione aquí para enviar sus respuestas"
        )
        if entregado:
            # Barra de carga
            mensaje_progreso = "Cargando..."
            barra_progreso = st.progress(0, text=mensaje_progreso)

            for porcentaje_completado in range(100):
                time.sleep(0.001)
                barra_progreso.progress(
                    porcentaje_completado + 1, text=mensaje_progreso
                )
            time.sleep(1)
            barra_progreso.empty()

            st.success(" Enviado con éxito!", icon="✅")
