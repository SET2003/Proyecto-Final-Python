"""
Cosas obligatorias:
    Barra lateral
    Pestañas
    Datos
    Graficos
    Hora interactiva con calendario

"""
# Librerias que se utilizan o pueden llegar a ser necesarias
import datetime
from datetime import datetime as dt
import numpy as np
import streamlit as st
import streamlit_antd_components as sac
from streamlit_folium import st_folium
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import requests
import folium
import altair as alt

# Configuración de la página

st.set_page_config(
    page_title="Proyecto Generador Fotovoltaico",
    page_icon=":material/solar_power:",
    layout="wide",
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Página del Proyecto de Generador Fotovoltaico"
        #VER DE MODIFICAR ESTE MENU
    }
)

# Configuración sidebar

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
    st.image('Archivos\\Imagenes\\logo-utn.png')
    st.logo('Archivos\\Imagenes\\home-header.png', size="large",
            link="https://www.frsf.utn.edu.ar/", icon_image='Archivos\\Imagenes\\UTN-FRSF.jpg')
    st.write('---')
    seccion = sac.menu([
        sac.MenuItem('Acerca de', icon='house-fill'),
        sac.MenuItem('Generador', icon='sun-fill', children=[
            sac.MenuItem('Datos', icon='clipboard-data-fill'),
            sac.MenuItem('Estadísticas', icon='bar-chart-line-fill'),
            sac.MenuItem('Mapas', icon='map-fill'),
        ]),
        sac.MenuItem('Ayuda', icon='question-circle-fill'),
        sac.MenuItem('Feedback', icon='chat-right-heart-fill'),
        sac.MenuItem(type='divider'),
        sac.MenuItem('links de interés', type='group', children=[
            sac.MenuItem('Global Solar Atlas', icon='link-45deg',
                         href='https://globalsolaratlas.info/map'),
            sac.MenuItem('NASA POWER', icon='link-45deg',
                         href='https://power.larc.nasa.gov/'),
            sac.MenuItem('Servicio Meteorológico Nacional', icon='link-45deg',
                         href='https://www.smn.gob.ar/clima/vigilancia-mapas'),
            sac.MenuItem('The Weather Channel', icon='link-45deg',
                         href='https://weather.com/es-CR/tiempo/mapas/interactive/l/Santa+Fe+de+la+Vera+Cruz+SF+ARXX4963:1:AR'),
        ]),
    ], open_all=True, color='#2aa7e1')

#  Secciones

if seccion == 'Acerca de':
    st.header('Acerca de esta aplicación', divider='grey')
    st.image('Archivos\\Imagenes\\banner_panelessolares.jpg', use_container_width=True)
    st.subheader('Descripción')

    st.markdown("""<div style='text-align: justify;'>
    Esta aplicación, desarrollada como proyecto final en la asignatura "Introducción a la programación
    científica con MATLAB y PYTHON" en el marco de la Facultad Regional Santa Fe - UTN, se centra en 
    el análisis de distintos datos de un generador fotovotaico (GFV) para el cálculo de la potencia que
    éste es capaz de entregar. Además, de acuerdo a la información cargada de temperaturas, irradiancias y
    tiempo, se calculan otros datos estadísticos de interés, así como gráficas y mapas interactivos. Se
    toma como base incial el generador de la Facultad Regional Santa Fe de la Universidad Tecnológica 
    Nacional.
    </div> """, unsafe_allow_html=True)

    st.subheader('Objetivos del proyecto')
    """
    * **Permitir al usuario cargar los datos de su propio generador** y otorgarle los resultados del análisis en 
    tiempos específicos que desee.
    * **Analizar el comportamiento del generador fotovoltaico de la Facultad Regional Santa Fe - UTN.** 
    * Utilizar sintaxis *Python* y la librería *Streamlit* para crear la aplicación web interactiva. 
    * Usar la librería *Pandas* para el manejo de *dataframes*. 
    """
    st.subheader('¿Cómo funciona?', help='En este apartado se describe el funcionamiento del GFV, así como el modelo matemático utilizado. Extraído de *Guía del Proyecto*')
    
    st.markdown("""<div style='text-align: justify;'>
    Un generador fotovoltaico (GFV) convierte parte de la energía proveniente de la radicación solar en
    la forma eléctrica. La instalación se ejecuta en forma modular; una cantidad N de paneles (o módulos)
    se vinculan a través de sus terminales de salida en una configuración mixta serie-paralelo. El conexionado
    serie se utiliza cuando se pretende incrementar la potencia de salida elevando el nivel de tensión eléctrica
    (diferencia de potencial total del conjunto). El conexionado paralelo, por su parte, se realiza cuando el
    incremento de potencia se logra elevando el nivel de la corriente entregada. En la práctica, un GFV puede
    utilizar una combinación de módulos conectados en serie, los que a su vez se vinculan en paralelo con otros
    conjuntos de conexionados serie. 
    La tensión eléctrica provista por un GFV es del tipo continua, es decir, que se mantiene constante siempre que lo hagan las condiciones de radiación solar y temperatura. No obstante, dado que esto último no es
    posible, se requiere de un equipo electrónico que funciona como controlador, que busca estabilizar las condiciones de operación siempre que sea posible. Una variante muy difundida altera convenientemente dicha
    tensión para que la potencia erogada sea la máxima posible de acuerdo con las condiciones meteorológicas
    del momento. Asimismo, en virtud de que las redes eléctricas no suelen operar con tensión continua, sino
    en forma alterna (con una variación sinusoidal en el tiempo), un circuito electrónico “inversor” es requerido
    para realizar la conversión. Es habitual que un único equipamiento cumpla
    simultáneamente las funciones de controlador e inversor. </div> """, unsafe_allow_html=True)
    """

    """
    """
    **1. Estimación de potencia generada**
    """
    
    st.markdown("""<div style='text-align: justify;'>
    Existen numerosos modelos matemáticos para representar el funcionamiento de un GFV. La configuración de las conexiones entre módulos es relevante si se pretende que el modelo obtenga la tensión y corriente
    de operación. En otras circunstancias, cuando interese fundamentalmente la potencia eléctrica entregada,
    pueden emplearse modelos simplificados. Por caso, la siguiente expresión obtiene la potencia eléctrica P
    (en kilo-Watt) obtenida por un GFV, siempre que todos los módulos sean idénticos y cuando se utiliza un
    controlador de potencia que altera la condición de tensión de trabajo para maximizar el rendimiento.
    </div> """, unsafe_allow_html=True)  

    st.latex("""
    P = N\\cdot \\frac{G}{G_{std}}\\cdot P_{pico}\\cdot\\left[1+k_{p}\\cdot (T_{c}-T_{r})\\right ]\\cdot\\eta\\cdot 10^{-3}
    """)

    """
    Donde:  
    $ N $: Número de módulos fotovoltaicos.  
    $ G $: Irradiancia global incidente en forma normal a los módulos $ W $/$ m^{2} $.  
    $ G_{std} $: Irradiancia estándar, comúnmente en $ W $/$ m^{2} $.  
    $ P_{pico} $: Potencia pico de cada módulo en $ W $.  
    $ k_{p} $: Coeficiente de temperatura-potencia en $ °C^{-1} $.  
    $ T_{c} $: Temperatura de la celda.  
    $ T_{r} $: Temperatura de referencia ($ 25 °C $).  
    $ \eta $: Rendimiento global del sistema.  
    
    **2. Corrección de temperatura de celda**
  
    La temperatura de la celda difiere de la temperatura ambiente $ T $. En la literatura se disponen decenas
    de modelos matemáticos que permiten estimar $ T_{c} $  a partir de mediciones de $ T $. El modelo más sencillo,
    válido únicamente en ausencia de viento, indica que la relación se puede aproximar según:  
    """

    st.latex(""" T_{c}= T + 0.031\\left [ °C \\cdot m^{2}/W \\right ] \\cdot G""")

    st.markdown(""" <div style='text-align: justify;'>
    Se destaca, por otra parte, que las mediciones de irradiancia que se toman a partir de una estación
    meteorológica, normalmente no coinciden con G, puesto que se realizan sobre una superficie de prueba
    horizontal, y no en relación a la disposición real de los módulos. La obtención de G a partir de las mediciones
    es compleja y depende, entre otras cosas, de las coordenadas geográficas del GFV (latitud y longitud), de
    la disposición espacial de los módulos (incluidas las inclinaciones), del momento preciso de análisis (año,
    mes, día, hora y zona horaria de implantación de la instalación), de la humedad relativa y temperatura del
    ambiente, y de las características de lo que se encuentra en los alrededores, en relación a su capacidad para
    reflejar en forma directa o difusa la radiación. No obstante, a los efectos de esta práctica, se
    utilizarán mediciones de irradiancia asumiendo, por simplicidad, que sus valores corresponden a G.            
    </div> """,unsafe_allow_html=True) 
    """
    
    """
    """  
    **3. Límites de generación**  

    Los circuitos inversores funcionan adecuadamente siempre que la producción, en términos de potencia,
    supere un umbral mínimo $ \mu $, habitualmente expresado en forma porcentual, en relación a la potencia nominal
    $ P_{inv} $ del equipo. Si este umbral no es superado, la instalación no entrega potencia eléctrica. Asimismo, el
    valor $ P_{inv} $ (en kilo-Watt) opera como límite superior del GFV. En consecuencia, la potencia real $ P_{r} $ que
    entrega la instalación se puede calcular como:   
    """

    st.latex("""P_{min} = \\cfrac{\\mu (\\%)}{100} \\cdot P_{inv}""")

    st.latex("""\\begin{cases}
    0 & \\text{si} \,\,P\\leq P_{min} \\\\
    P & \\text{si}  \,\, P_{min}\\leq P_{inv} \\\\
    P_{inv} & \\text{si} \,\, P> P_{inv} 
    \end{cases} """)
    
    st.info('Para información acerca de la carga y extracción de datos, así como un glosario de términos, consulte la sección *Ayuda* del menú lateral.', icon="ℹ️")

    st.subheader('Integrantes del equipo',divider='violet')
    col1, col2, col3 = st.columns([0.33, 0.33, 0.33])

    with col1:
        with st.expander('**Santiago Ernesto Torres**', expanded=True, icon=":material/engineering:"):
            
            st.markdown('*UTN - Facultad Regional Santa Fe*')
            st.markdown(':material/mail: storres@frsf.utn.edu.ar')
            st.markdown(':material/call: 342-516-1517')
            st.image('Archivos//Imagenes//Diseño sin título.png', use_container_width=True)

    with col2:
        with st.expander('**Leandro Ruíz Díaz**', expanded=True, icon=":material/engineering:"):
            
            st.markdown('*UTN - Facultad Regional Santa Fe*')
            st.markdown(':material/mail: lruizdiaz@frsf.utn.edu.ar')
            st.markdown(':material/call: 340-452-2507')
            st.image('Archivos//Imagenes//FOTOLEO.png', use_container_width=True)

    with col3:
        with st.expander('**Manuel Garelik**', expanded=True, icon=":material/engineering:"):
            st.markdown('*UTN - Facultad Regional Santa Fe*')
            st.markdown(':material/mail: magarelik@frsf.utn.edu.ar')
            st.markdown(':material/call: 342-554-7236')
            st.image('Archivos//Imagenes//FOTOMANU.png', use_container_width=True)



if seccion == 'Datos':
    st.title ('Cálculo generador fotovoltaico')
    # Le pido al usuario que cargue una tabla
    st.header ('Carga de datos climatológicos', divider='blue')

    datos_especificos = st.toggle ('Cargar nueva tabla')
    st.info('Los datos ingresados en forma de tabla deben estar completos, respetando intervalos de tiempo constantes. Si no se ingresan, se realizará el cálculo con los datos climatológicos de Santa Fe de 2019.', icon="ℹ️")

    if datos_especificos:
        Datos = st.file_uploader(
        'Ingresá el archivo', help='Arrastra el archivo aquí o subelo mediante el botón', accept_multiple_files=False)
        Datos = pd.read_excel(Datos, index_col=0)

    else:
    # En caso de que el usuario no cargue ninguna tabla, se utiliza como ejemplo la del generador de la UTN-FRSF
        Datos = pd.read_excel(
            'Archivos\Datos_climatologicos_Santa_Fe_2019.xlsx', index_col=0)


    st.session_state["Datos"]=Datos
    
    # Extraigo los indices de las columnas
    G, T = Datos.columns

    # Todos los datos que tiene que cargar el usuario, utiliza como predeterminados los de la UTN

    st.header ('Datos de la instalación', divider='red')
    with st.expander('**Datos**', expanded=False, icon=":material/description:"):
            with st.form ('formulario', clear_on_submit=True, border=False):
                col1, col2 = st.columns(2)
                with col1:
                    N = st.number_input('Cantidad de Paneles',
                                        min_value=0, value=12, step=1)
                    # st.markdown('Gstd Irradiancia estándar en $\cfrac {W}{m^2}$')
                    Gstd = st.number_input(
                        'Gstd Irradiancia estándar en $ W $/$ {m^2} $', min_value=0.00, value=1000.00, step=100.00, format='%2.2f')
                    Tr = st.number_input('Temperatura de referencia en $ °C $',
                                        min_value=0.00, value=25.0, step=0.5, format='%1.1f')
                    Ppico = st.number_input(
                        'Potencia Pico de cada modulo en $ W $', min_value=0.00, value=240.00, step=10.00, format='%2.2f')

                with col2:
                    kp = st.number_input('Coeficiente de Temperatura-Potencia en $ °C^{-1} $',
                                        max_value=0.0000, value=-0.0044, step=0.0001, format='%4.4f')
                    rend = st.number_input('Rendimiento global de la instalación',
                                        min_value=0.00, max_value=1.00, value=0.97, step=0.10, format='%2.2f')
                    Pinv = st.number_input(
                        'Potencia maxima/trabajo del inversor en $ kW $', min_value=0.00, value=2.50, step=0.50, format='%2.2f')
                    umbral_minimo = st.number_input(
                        'Umbral minimo en %', min_value=0.00, value=0.00, max_value=1.00, step=0.10, format='%2.2f')
                
                #  Configuración botón para entregar
                entregado = st.form_submit_button ('Guardar datos', help='Presione aquí para enviar sus respuestas')
                if entregado: 
                    #Barra de carga
                    mensaje_progreso = "Cargando..."
                    barra_progreso = st.progress(0, text=mensaje_progreso)

                    for porcentaje_completado in range(100):
                        time.sleep(0.001)
                        barra_progreso.progress(porcentaje_completado + 1, text=mensaje_progreso)
                    time.sleep(3)
                    barra_progreso.empty()

                    st.success(' Datos guardados', icon="✅")
    
    # Corrijo la temperatura de celda en funcion a la temperatura ambiente
    Datos['Temperatura de Celda (°C)']= Datos[T] + 0.031*Datos[G]
    Tc=Datos['Temperatura de Celda (°C)']

    # Calculo la potencia y la guardo en una nueva columna
    Datos['Potencia (kW)']= N*Datos[G]/Gstd*Ppico*(1+kp*(Tc-Tr))*rend*1e-3
   
    # Analizo si los valores de potencia estan dentro de rango, de no ser así los reemplazo por el correspondiente
    Pmin=umbral_minimo*Pinv
    Datos['Potencia (kW)'] = Datos['Potencia (kW)'].where(Datos['Potencia (kW)'] < Pinv, Pinv)
    Datos['Potencia (kW)'] = Datos['Potencia (kW)'].where(Datos['Potencia (kW)'] > Pmin, 0)

    # Muestro la Tabla (de aca a proximas lineas)
    st.markdown('## Tabla Cargada')

    # Genero dos columnas donde la primera es la tabla y ocupa el 70% de la ventana, mientras que la otra la uso para seleccionar fechas
    col1, col2 = st.columns([0.7, 0.3])

    with col2:
        
        # Calculo los intervalos de tiempo
        intervalos = Datos.index.to_series().diff().dropna()
        intervalos = intervalos[0]
        # Le pido al usuario que seleccione que datos quiere ver, de predeterminado muestra toda la tabla
        
        
        
        # if ('Fecha_inicial' or 'Fecha_final') not in st.session_state:
        #     st.session_state['Fecha_inicial']=Datos.index[0]
        #     st.session_state['Fecha_final']=Datos.index[-1]
        
        # Fecha_inicial_anterior= st.session_state["Fecha_inicial"]
        # Fecha_inicial_anterior=dt.strptime(Fecha_inicial_anterior, '%Y-%m-%d')
        # Fecha_final_anterior = st.session_state["Fecha_final"]
        # Fecha_final_anterior=dt.strptime(Fecha_final_anterior, '%Y-%m-%d')

        # st.session_state['Fecha_inicial'] = st.date_input(
        #         'Seleccione Fecha Inicial', value=Fecha_inicial_anterior, min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
        # st.session_state['Fecha_final']= st.date_input(
        #         'Seleccione Fecha Final', value=Fecha_final_anterior, min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
        
        # Fecha_inicial=st.session_state['Fecha_inicial']
        # Fecha_final=st.session_state['Fecha_final']




        # if Fecha_inicial_anterior != Fecha_inicial:
        #     st.session_state['Fecha_inicial']=Fecha_inicial
        # if Fecha_final_anterior != Fecha_final:
        #     st.session_state['Fecha_final']=Fecha_final

        if ('Fecha_inicial' or 'Fecha_final') not in st.session_state:
            Fecha_inicial = st.date_input(
                'Seleccione Fecha Inicial', value=Datos.index[0], min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
            Fecha_final = st.date_input(
                'Seleccione Fecha Final', value=Datos.index[-1], min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
        else:
            
            Fecha_inicial= st.session_state["Fecha_inicial"]
            Fecha_inicial=dt.strptime(Fecha_inicial, '%Y-%m-%d')
            Fecha_final = st.session_state["Fecha_final"]
            Fecha_final=dt.strptime(Fecha_final, '%Y-%m-%d')

            Fecha_inicial = st.date_input(
                'Seleccione Fecha Inicial', value=Fecha_inicial, min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
           
            
            Fecha_final = st.date_input(
                'Seleccione Fecha Final', value=Fecha_final, min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
            
        # if 'Fecha_inicial' not in st.session_state:
        #     st.write('La fecha inicial no está guardada')
        #     Fecha_inicial = st.date_input(
        #         'Seleccione Fecha Inicial', value=Datos.index[0], min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
        
        # else:
        #     st.write('La fecha si está guardada')
        #     Fecha_inicial= st.session_state["Fecha_inicial"]
        #     Fecha_inicial=dt.strptime(Fecha_inicial, '%Y-%m-%d')

        #     Fecha_inicial = st.date_input(
        #         'Seleccione Fecha Inicial', value=Fecha_inicial, min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()

        # if 'Fecha_final' not in st.session_state:
            
        #     Fecha_final = st.date_input(
        #         'Seleccione Fecha Final', value=Datos.index[-1], min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
        
        # else:
        #     Fecha_final = st.session_state["Fecha_final"]
        #     Fecha_final=dt.strptime(Fecha_final, '%Y-%m-%d')
            
        #     Fecha_final = st.date_input(
        #         'Seleccione Fecha Final', value=Fecha_final, min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()


        if ('Tiempo_inicial' or 'Tiempo_final') not in st.session_state:    
            Tiempo_inicial = st.time_input(
                'Tiempo inicial', value=Datos.index[0], step=intervalos)
            Tiempo_final = st.time_input(
                'Tiempo final', value=Datos.index[-1], step=intervalos)
        else:
            Tiempo_inicial=st.session_state['Tiempo_inicial']
            Tiempo_final=st.session_state['Tiempo_final']
            Tiempo_inicial = st.time_input(
                'Tiempo inicial', value=Tiempo_inicial, step=intervalos)
            Tiempo_final = st.time_input(
                'Tiempo final', value=Tiempo_final, step=intervalos)
        
        # st.session_state.pop("Tiempo_inicial")
        # st.session_state.pop("Tiempo_final") 
        # st.session_state.pop("Fecha_inicial") 
        # st.session_state.pop("Fecha_final")     

        st.session_state["Tiempo_inicial"]=Tiempo_inicial
        st.session_state["Tiempo_final"]=Tiempo_final
        st.session_state["Fecha_inicial"]=Fecha_inicial
        st.session_state["Fecha_final"]=Fecha_final
        
    with col1:
        # Junto en un solo string la fecha y hora seleccionada para pasarsela a la tabla
        Fecha_inicial_seleccionado = Fecha_inicial + ' ' + Tiempo_inicial.__str__()
        Fecha_final_seleccionado = Fecha_final + ' ' + Tiempo_final.__str__()
        # Agregué una variable donde están los datos filtrados por el usuario
        Datos_filtrados = Datos.loc[Fecha_inicial_seleccionado:Fecha_final_seleccionado, :]
       
        # Muestro la tabla  
        st.dataframe(Datos_filtrados, use_container_width=True)
        
#
#
# A PARTIR DE ACÁ VAN LAS GRÁFICAS
#
#

    st.write('# Gráficas')
    
    if len(Datos_filtrados) > 10000:
        st.warning(
            "El rango seleccionado contiene demasiados datos para graficar. Se recomienda reducir el rango para mejorar el rendimiento del programa.", icon="⚠️")
        Limite_puntos=st.toggle('Deshabilitar limite de datos', value=False)
    else:
        Limite_puntos=True
    
    tab1, tab2, tab3, tab4 = st.tabs(
        ['Gráfica de Potencia', 'Graficas de Temperatura', 'Grafica de Irradiancia' ,'Gráfico de dispersión G-T'])

    # Verifico si la cantidad de puntos supera un límite donde se realentizaría mucho la página (10000 puntos), si lo es muestro un warning diciendo que son muchos los puntos
    # como para realizar un gráfico.
    
    if Limite_puntos:
        with tab1:

            st.markdown('### Gráfico de Potencia')
            st.line_chart(data=Datos_filtrados, y="Potencia (kW)",
                          x_label='Fecha/Tiempo', y_label='Potencia (kW)')

        with tab2:
                st.markdown('### Gráfico de Temperatura')
                st.line_chart(data=Datos_filtrados, y=["Temperatura de Celda (°C)",T],
                          x_label='Fecha/Tiempo', y_label='Temperatura (°C)')
                st.markdown('### Mapa de calor de Temperatura')
                # st.pyplot(fig)
                mapa_de_calor = Datos_filtrados.pivot_table(
                    index=Datos_filtrados.index,
                    values=T, 
                    aggfunc='mean'
                ).sort_index(ascending=False)

                df=mapa_de_calor.reset_index()
                df["Fecha Formateada"]=df["Fecha"].dt.strftime("%Y-%m-%d")

                # # Mapa de calor interactivo usando Altair

                heatmap = alt.Chart(df).mark_rect().encode(
                    alt.X("Fecha Formateada:O", title="Fecha"),
                    y=alt.Y("hours(Fecha):O", title="Hora",sort="descending"),
                    color=alt.Color('Temperatura (°C):Q', scale=alt.Scale(scheme="magma"), title="Temperatura (°C)")  # Colores según temperatura
                ).properties(   
                    title="Mapa de Calor: Temperatura por Día y Hora"
                ).interactive()  # Habilitar interactividad (paneo y zoom)

                # Mostrar el mapa de calor en Streamlit
                st.altair_chart(heatmap, use_container_width=True)

        with tab3:
            
            st.markdown('### Gráfico de Irradiancia')
            st.line_chart(data=Datos_filtrados, y=G, x_label='Fecha/Tiempo',
                          y_label='Irradiancia (W/m²)', color="#ffc300")
            
        with tab4:

            st.markdown('### Gráfico de dispersión Irradiancia-Temperatura')
            st.scatter_chart(data=Datos_filtrados, y=T, x=G, y_label="Temperatura (°C)", x_label="Irradiancia (W/m²)")


if seccion == 'Estadísticas':
    if 'Datos' not in st.session_state:
        st.warning('⚠️ Ingrese los datos a través de la pestaña datos.')
    else:
        st.header ('Estadísticas')
        st.write('### Gráfica de la Potencia Media')
        #El usuario elige si quiere la media en días o semanas
        option = st.selectbox(
        "Seleccione un periodo de tiempo para el cálculo de la media:",
        ("En semanas", "En días"),
        )

        Datos=st.session_state["Datos"]
        Fecha_inicial = st.session_state["Fecha_inicial"]
        Fecha_final = st.session_state["Fecha_final"]
        Fecha_inicial=dt.strptime(Fecha_inicial, '%Y-%m-%d')
        Fecha_final=dt.strptime(Fecha_final, '%Y-%m-%d')

        col4, col5 = st.columns([0.7, 0.3])
        with col5:
            Fecha_inicial = st.date_input( 
                'Seleccione Fecha inicial', value=Fecha_inicial, min_value=Datos.index[0], max_value=Datos.index[-1])
            Fecha_final = st.date_input(
                'Seleccione Fecha Final', value=Fecha_final, min_value=Datos.index[0], max_value=Datos.index[-1])
            
            st.session_state["Fecha_inicial"]=Fecha_inicial.__str__()
            st.session_state["Fecha_final"]=Fecha_final.__str__()

        with col4:
            tab1, tab2=st.tabs(['Potencia', 'Energia'])
            Fecha_inicial_seleccionado=Fecha_inicial.__str__()+ ' '+ datetime.time.fromisoformat('00:00:00').__str__()
            Fecha_final_seleccionado=Fecha_final.__str__()+ ' '+ datetime.time.fromisoformat('23:59:59').__str__()
            
            chart_pot = Datos[(Datos.index >= Fecha_inicial.__str__()) & (Datos.index <= Fecha_final_seleccionado.__str__())].drop(columns=['Temperatura (°C)', 'Irradiancia (W/m²)', 'Temperatura de Celda'], errors='ignore') #Filtro la tabla y le saco las columnas excedentes
            
            with tab1:
                if option == "En semanas" :
                    
                    potencia_media_SE = chart_pot.resample('W').mean() #Uso el resample para calcular tomar las semanas y el mean para calcular la media
                    
                    potencia_media=potencia_media_SE.reset_index()
                    potencia_media["Fecha Formateada"]=potencia_media["Fecha"].dt.strftime("%Y-%m-%d")
                    
                    # lista=potencia_media['Fecha Formateada'].values.tolist()
                    
                    grafico=alt.Chart(potencia_media).mark_bar().encode(
                        x=alt.X("Fecha Formateada:O", title="Fecha"),
                        y=alt.Y("Potencia:Q", title="Potencia"),
                    ).interactive()

                    st.altair_chart(grafico, use_container_width=True)

                if option == "En días" :
                    potencia_media_SE = chart_pot.resample('D').mean() #Uso el resample para calcular tomar los dias y el mean para calcular la media
                    
                    potencia_media = potencia_media_SE.reset_index()
                    potencia_media["Fecha Formateada"]=potencia_media["Fecha"].dt.strftime("%Y-%m-%d")
                    
                    grafico=alt.Chart(potencia_media).mark_bar().encode(
                        x=alt.X("Fecha Formateada:O", title="Fecha"),
                        y=alt.Y("Potencia:Q", title="Potencia"),
                    ).interactive()

                    st.altair_chart(grafico, use_container_width=True)

            with tab2:
                if option == "En semanas" :
                    
                    Energia_SE = chart_pot.resample('W').mean() #Uso el resample para calcular tomar las semanas y el mean para calcular la media
                    Energia_SE['Potencia']=Energia_SE['Potencia']*168

                    Energia=Energia_SE.reset_index()
                    Energia["Fecha Formateada"]=Energia["Fecha"].dt.strftime("%Y-%m-%d")
                    
                    # lista=potencia_media['Fecha Formateada'].values.tolist()
                    
                    grafico=alt.Chart(Energia).mark_bar().encode(
                        x=alt.X("Fecha Formateada:O", title="Fecha"),
                        y=alt.Y("Potencia:Q", title="Energia"),
                    ).interactive()

                    st.altair_chart(grafico, use_container_width=True)

                if option == "En días" :
                    
                    Energia_SE = chart_pot.resample('D').mean() #Uso el resample para calcular tomar los dias y el mean para calcular la media
                    Energia_SE['Potencia']=Energia_SE['Potencia']*24
                    Energia = Energia_SE.reset_index()
                    Energia["Fecha Formateada"]=Energia["Fecha"].dt.strftime("%Y-%m-%d")
                    

                    grafico=alt.Chart(Energia).mark_bar().encode(
                        x=alt.X("Fecha Formateada:O", title="Fecha"),
                        y=alt.Y("Potencia:Q", title="Energia"),
                    ).interactive()

                    st.altair_chart(grafico, use_container_width=True)
       
        st.write('### Días principales')

        col6, col7 = st.columns([0.5, 0.5])
        Energia=Energia.set_index('Fecha Formateada')
        C1E, C2E = Energia.columns
        Energia=Energia.drop(C1E,axis=1)
        potencia_media=potencia_media.set_index('Fecha Formateada')
        C1P, C2P=potencia_media.columns
        potencia_media=potencia_media.drop(C1P, axis=1)
        with col6:
            #Ordeno las potencias de mayor a menor
            if option =="En días" :
                
                Top_potencias = potencia_media.sort_values(by="Potencia", ascending = False).head(10)
                st.write('Los diez (10) días con mayor potencia en el intervalo elegido son:')
                st.write(Top_potencias)
                
            if option == "En semanas" :
                
                Top_potencias = potencia_media.sort_values(by="Potencia", ascending = False).head(10)
                st.write('Las diez (10) semanas con mayor potencia en el intervalo elegido son:')
                st.write(Top_potencias)

        with col7:
            #ACÁ VA LO DE ENERGÍA
            
            if option =="En días" :
                
                Top_Energia=Energia.sort_values(by="Potencia", ascending = False).head(10)
                st.write('Los diez (10) días con mayor energia en el intervalo elegido son:')
                st.write(Top_Energia)

            if option == "En semanas" :
                
                Top_Energia=Energia.sort_values(by="Potencia", ascending = False).head(10)
                st.write('Las diez (10) semanas con mayor energia en el intervalo elegido son:')
                st.write(Top_Energia)

        
        st.write('### Máximos y mínimos')

        st.write('La temperatura máxima fue de ', Datos['Temperatura (°C)'].max(), '°C, el día ', Datos['Temperatura (°C)'].idxmax())
        st.write('La irradiancia máxima fue de ', Datos['Irradiancia (W/m²)'].max(), 'W/m², el día ', Datos['Irradiancia (W/m²)'].idxmax())



if seccion == 'Mapas': 
    st.title ('Mapas')
    tab1, tab2, tab3 = st.tabs(['Mapa Satelital', 'Mapa de irradiancas', 'Mapa de temperaturas'])
    with tab1: 
        st.subheader("Mapa Satelital")
        col1, col2 = st.columns([0.3, 0.7])
        with col1:
            st.image('Archivos\\Imagenes\\ubicacion2.jpg', use_container_width=True)
            st.info('Cargue la ubicación del GFV analizado, si no ingresa ningún valor se mostrará la ubicación de los paneles de la UTN-FRSF', icon="ℹ️")
            latitud = st.number_input('Latitud', min_value=-90.00000000000000, max_value=90.00000000000000, value=-31.616681297694267, format='%.14f', step=1.00000000000000)
            longitud = st.number_input ('Longitud', min_value=-180.00000000000000, max_value=180.00000000000000, value=-60.67543483706093, format='%.14f', step=1.00000000000000)
        with col2:
            # mapa
            mapa = folium.Map(location=[latitud, longitud], zoom_start=18)
            # Las coordenadas de location indican el centro del mapa

            #Ahora se hace el marcador puntual
            folium.Marker(
                    [latitud, longitud], 
                    popup="Ubicación generador fotovoltaico",
                    ).add_to(mapa)

            # Mostrar el mapa:
            st_folium(mapa, use_container_width=True)

    with tab2: 
       st.subheader("Mapa de irradiación del mundo", help='Obtenido de Global Solar Atlas, muestra la irradiación directa normal')
       st.image('Archivos\\Imagenes\\mapa_irradiancia_mundo.png', use_container_width=True)
       st.write('---')
       st.subheader("Mapa de irradiación de Latinoamérica", help='Obtenido de Global Solar Atlas, muestra la irradiación directa normal')
       st.image('Archivos\\Imagenes\\mapa_irradiancia_latinoamerica.png', use_container_width=True)
       st.info('Para mapas de irradiación interactivos consultar *Global Solar Atlas* y *NASA POWER* (link en menú lateral)', icon="ℹ️")

    with tab3: 
        st.subheader("Mapa de temperaturas medias de Argentina", help='Obtenido de Servicio Meteorológico Nacional')
        st.image('Archivos\\Imagenes\\111.jpg', use_container_width=True)
        st.info('Para más mapas de temperatura consultar *Servicio Meteorológico Nacional* y *The Weather Channel* (link en menú lateral)', icon="ℹ️")


  
if seccion == 'Ayuda':
    st.header('Ayuda y soporte de la página', divider='orange')
    with st.expander ('**Importante**', icon="⚠️"): 
        st.write(' Esta página aún se encuentra en un estado primitivo, para usar el chat por favor ingrese solamente el **número** de la opción que elija.')
    with st.chat_message('assistant'):
            st.write('Hola! Escribí la opción sobre la que deseas obtener ayuda: ')
            """
            1. *Guía de la página*    
            2. *Definiciones y glosario de términos*  
            3. *Preguntas frecuentes (FAQ's)*  
            4. *Otro*
            """
    texto = st.chat_input("Escriba aquí...")
    if texto=='1':
        with st.chat_message('assistant'):
            """
            *Guía de la página*   
            La página cuenta con cuatro secciones principales:
            * ***Acerca de***, donde podrás encontrar una breve descripción de la página, 
            información de los desarrolladores y la explicación del modelo matemático utilizado. 
            * ***Generador***, es la sección principal y se encuentra, a su vez, subdividida en tres categorías,
            "*Datos*", donde pueden cargarse los datos del generador que se desea calcular, o usar los datos por
            defecto del generador de la FRSF-UTN; "*Estadísticas*", donde podrá encontrar valores representativos 
            del generador, en las mismas fechas que las cargadas en Datos; y "*Mapas*", donde podrá visualizar 
            una imagen satelital de la ubicación del generador, habiendo ingresado coordenadas de latitud y 
            longitud, además de tener mapas estáticos de irradiancias y temperaturas de Argentina. 
            * ***Ayuda***, sección en la que se haya actualmente.
            * ***Feedback***, donde podrá encontrar un breve cuestionario acerca de su experiencia con la página,
            lo que nos permitirá incorporar mejoras a futuro.

            Si necesitas ver la ayuda de otra opción, ingresa el número debajo nuevamente!
            """


    if texto=='2':
        with st.chat_message('assistant'):
            """
            *Definiciones generales*

            * **GFV**: Generador Fotovoltaico. Un generador fotovoltaico es un sistema que convierte la energía del sol en electricidad.
            Los generadores solares funcionan mediante paneles fotovoltaicos, también conocidos como paneles solares, que absorben la
            luz del sol y la transforman en electricidad.

            * **Inversor**: Un inversor fotovoltaico, también conocido como inversor solar, es un dispositivo que transforma la corriente
            continua (CC) que generan los paneles solares en corriente alterna (CA), la cual es la utilizada en las instalaciones.

            * **Regulador**: Un regulador de carga, también conocido como controlador de carga, es un dispositivo electrónico que se utiliza
            en un sistema fotovoltaico para controlar el flujo de energía entre los paneles solares y las baterías.

            *Glosario de términos*   
            A continuación encontrarás una lista con las abreviaturas y una explicación más detallada de todos los
            parámetros utilizados en el modelo matemático:  

            * $ N $: es el número de paneles fotovoltaicos con los que cuenta el generador, tanto en serie como en paralelo.
            Resulta de la multiplicación del número de módulos en serie por el número de módulos en paralelo o, de forma 
            matemática: $ N = N_{serie} \\cdot N_{paralelo} $.

            * $ G $: Irradiancia global incidente en forma normal a los módulos $ W $/$ m^{2} $. La irradiancia
            mide el flujo de energía proveniente de la radiación solar (sea de forma directa o indirecta) por unidad
            de superficie incidente.  

            * $ G_{std} $: Irradiancia estándar, comúnmente en $ W $/$ m^{2} $. Es un valor de irradiancia que utilizan los
            fabricantes de los módulos para referenciar ciertas características técnicas. Normalmente $ G_{std} = 1000 $ $ W $/$ m^{2} $.

            * $ P_{pico} $: Potencia pico de cada módulo en $ W $. Se interpreta como la potencia eléctrica que entrega
            un módulo cuando $ G $ coincide con $ G_{std} $ y cuando $ T_{c} $ coincide con $ T_{r} $, en ausencia de viento y sin
            que el panel se vincule a otros componentes eléctricos que afecten el desempeño de la instalación.
            Constituye la potencia nominal bajo la cual los módulos son comercializados. 

            * $ k_{p} $: Coeficiente de temperatura-potencia en $ °C^{-1} $.Es un parámetro negativo que refleja cómo incide
            la temperatura de la celda en el rendimiento del GFV. Se observa que incrementos (disminuciones)
            de $ T_{c} $ producen, en consecuencia, disminuciones (incrementos) de $ P $.

            * $ T_{c} $: Temperatura de la celda. Temperatura de la celda, en $ °C $. Es la temperatura de los componentes semiconductores que
            conforman cada módulo fotovoltaico.

            * $ T_{r} $: Temperatura de referencia, en Celsius. Es una temperatura utilizada por los fabricantes de los
            módulos para referenciar ciertos parámetros que dependen de la temperatura. Normalmente $ Tr =( 25 °C ) $. 

            * $ \eta $: Rendimiento global del sistema. Rendimiento global de la instalación “por unidad” (valor ideal: 1). Se utiliza para considerar el efecto
            de sombras parciales sobre el GFV, suciedad sobre la superficie de los módulos y, fundamentalmente,
            el rendimiento del equipo controlador-inversor. Los inversores contemplados por el modelo de la también incluyen el sistema de control para maximizar
            la potencia de salida.

            Si necesitas ver la ayuda de otra opción, ingresa el número debajo nuevamente!
            """
    

    if texto=='3':
       with st.chat_message('assistant'):
            st.write('Descripción opción 3') 
            """
            Aquí encontrarás preguntas frecuentes que pueden ayudarte en la utilización de la app web: 
            """
            st.info('¿Puedo descargar los resultados de los cálculos y los gráficos?')
            with st.expander ('Respuesta', icon=":material/add_circle:"): 
                """
                Sí! Puedes descargar los resultados y gráficos en el formato que desees, encuentra los botones de descargas
                al final de cada análisis!
                """

            st.info('¿Qué sucede si ingreso datos incorrectos?')
            with st.expander ('Respuesta', icon=":material/add_circle:"): 
                """
                La aplicación está desarrollada automaticamente para validar los datos que han sido cargados, si detecta valores
                valores inconsistentes o fuera del rango que corresponde, se mostrará un mensaje de error con instrucciones para
                corregirlo.
                """

            st.info('Puedo usar esta herramienta para un generador distinto al de la UTN-FRSF?')
            with st.expander ('Respuesta', icon=":material/add_circle:"): 
                """
                Por supuesto! Si bien esta aplicación fue desarrollada incialmente para analizar los datos del GFV de la UTN - FRSF, 
                puedes cargar los datos de cualquier generador **(siempre en el formato adecuado)** y extraer los resultados.
                """

            st.info('Que pasa si quiero analizar un período prolongado de datos?')
            with st.expander ('Respuesta', icon=":material/add_circle:"): 
                """
                Podrás hacerlo, de todas formas la página te otorgorá advertencias, ya que no es recomendable debido a la disminución del
                rendimiento y aumento en el tiempo de ejecución.
                """
    
       """
       Si necesitas ver la ayuda de otra opción, ingresa el número debajo nuevamente!
       """
    
    if texto=='4':
       with st.chat_message('assistant'):
            """
            Si todavía tienes dudas o inconvenientes con la página, te recomendamos realizar el formulario disponible en **Feedback** o contactar
            alguna de las siguientes direcciones de correo electrónico:
            """
            st.markdown(':material/mail: storres@frsf.utn.edu.ar')
            st.markdown(':material/mail: magarelik@frsf.utn.edu.ar')
            st.markdown(':material/mail: lruizdiaz@frsf.utn.edu.ar')



if seccion == 'Feedback': 
    st.header ('Dejá tu comentario!', divider='blue')
    with st.form ('formulario', clear_on_submit=True):
        #  Datos del encuestado
        st.text_input('Introduzca su nombre', placeholder='Nombre Apellido')
        st.text_input('Introduzca su correo electrónico', placeholder='correo@gmail.com')
        notificaciones = st.checkbox ('¿Desea recibir respuesta a su feedback y notificaciones sobre próximos cambios en la página?')
        st.write('---')
        
        #  Puntuaciones de la página
        st.write('Puntúe su experiencia con la aplicación en las siguientes categorías: ')
        st.info(' Elija entre Insuficiente (menor puntuación) y Excelente (mayor puntuación).', icon="ℹ️")
        opciones = ['Insuficiente', 'Regular', 'Bueno', 'Muy bueno', 'Excelente']
        st.select_slider ('¿Que tan sencillo le fue utilizar esta aplicación?', options=opciones, value='Bueno')  # VER SI USAMOS DEFINIR ESTO PARA ALGO
        st.select_slider ('¿Que tan útiles fueron las funciones ofrecidas?', options=opciones, value='Bueno')
        st.select_slider ('¿Que tan actractiva visualmente encontró la aplicación?', options=opciones, value='Bueno')
        st.write('---')
        st.write ('Dale una puntuación general a la aplicación')
        st.info(' Elija entre 1 estrella (menor puntuación) y 5 estrellas (mayor puntuación).', icon="ℹ️")
        st.feedback('stars')
        st.write('---')
        
        #  Comentarios adicionales
        st.text_area('Agregue cualquier otro comentario que desee',placeholder='Escriba aquí...', max_chars=500)

        #  Configuración botón para entregar
        entregado = st.form_submit_button ('Enviar', help='Presione aquí para enviar sus respuestas')
        if entregado: 
            #Barra de carga
            mensaje_progreso = "Cargando..."
            barra_progreso = st.progress(0, text=mensaje_progreso)

            for porcentaje_completado in range(100):
                time.sleep(0.001)
                barra_progreso.progress(porcentaje_completado + 1, text=mensaje_progreso)
            time.sleep(3)
            barra_progreso.empty()

            st.success(' Enviado con éxito!', icon="✅")


