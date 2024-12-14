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
from datetime import date
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
        'About': "# This is a header. This is an *extremely* cool app!"
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
            sac.MenuItem('Mapas interactivos', icon='map-fill'),
        ]),
        sac.MenuItem('Ayuda', icon='question-circle-fill'),
        sac.MenuItem('Feedback', icon='chat-right-heart-fill'),
        sac.MenuItem(type='divider'),
        sac.MenuItem('links de interés', type='group', children=[
            sac.MenuItem('Global Solar Atlas', icon='link-45deg',
                         href='https://globalsolaratlas.info/map'),
            sac.MenuItem('NASA POWER', icon='link-45deg',
                         href='https://power.larc.nasa.gov/'),
        ]),
    ], open_all=True, color='#2aa7e1')

#  Secciones

if seccion == 'Acerca de':
    st.header('Acerca de esta aplicación', divider='grey')
    st.image('Archivos\\Imagenes\\banner_panelessolares.jpg', use_container_width=True)
    st.subheader('Descripción')
    """
    Esta aplicación, desarrollada como proyecto final en la asignatura "*Introducción a la programación
    científica con MATLAB y PYTHON*" en el marco de la Facultad Regional Santa Fe - UTN, se centra en 
    el análisis de distintos datos de un generador fotovotaico (GFV) para el cálculo de la potencia que
    éste es capaz de entregar. Además, de acuerdo a los datos cargados de temperaturas, irradiancias y
    tiempo, se calculan otros datos estadísticos de interés, así como gráficas y mapas interactivos. Se
    toma como base incial el generador de la Facultad Regional Santa Fe de la Universidad Tecnológica 
    Nacional.
    """
    st.subheader('Objetivos del proyecto')
    """
    * **Permitir al usuario cargar los datos de su propio generador** y otorgarle los resultados del análisis en 
    tiempos específicos que desee.
    * **Analizar el comportamiento del generador fotovoltaico de la Facultad Regional Santa Fe - UTN.** 
    * Utilizar sintaxis *Python* y la librería *Streamlit* para crear la aplicación web interactiva. 
    * Usar la librería *Pandas* para el manejo de *dataframes*. 
    """
    st.subheader('¿Cómo funciona?', help='En este apartado se describen las ecuaciones utilizadas para realizar los cálculos del GFV')
    """
    1. **Estimación de potencia generada**
    
    """

    # Agregar aca toda la explicación del funcionamiento del generador.

    st.subheader('Integrantes del grupo')
    col1, col2, col3 = st.columns([0.35, 1/3, 1/3])

    with col1:
        with st.expander('**Santiago Ernesto Torres**', expanded=True, icon=":material/engineering:"):
            # Agregar foto
            st.markdown('*UTN - Facultad Regional Santa Fe*')
            st.markdown(':material/mail: storres@frsf.utn.edu.ar')
            st.markdown(':material/call: 342-516-1517')

    with col2:
        with st.expander('**Leandro Ruíz Díaz**', expanded=True, icon=":material/engineering:"):
            # Agregar foto
            st.markdown('*UTN - Facultad Regional Santa Fe*')
            st.markdown(':material/mail: lruizdiaz@frsf.utn.edu.ar')
            st.markdown(':material/call: 340-452-2507')

    with col3:
        with st.expander('**Manuel Garelik**', expanded=True, icon=":material/engineering:"):
            # st.image('Archivos//Imagenes//FOTOMANU.png')
            st.markdown('*UTN - Facultad Regional Santa Fe*')
            st.markdown(':material/mail: magarelik@frsf.utn.edu.ar')
            st.markdown(':material/call: 342-554-7236')



if seccion == 'Datos':
    """
    # Cálculo Generador Fotovoltaico
    """
    # Le pido al usuario que cargue una tabla
    Datos = st.file_uploader(
        'Ingresá el archivo', help='Arrastrá el archivo acá o subilo mediante el botón', accept_multiple_files=False)

    # En caso de que el usuario no cargue ninguna tabla, se utiliza como ejemplo la proporcionada por UTN
    if Datos is None:
        st.markdown(
            "## Ejemplo con Tabla de Datos Climatologicos de Santa Fe 2019")
        Datos = pd.read_excel(
            'Archivos\Datos_climatologicos_Santa_Fe_2019.xlsx', index_col=0)
    else:
        Datos = pd.read_excel(Datos, index_col=0)

    st.session_state['Datos']=Datos
    # Extraigo los indices de las columnas
    G, T = Datos.columns

    # Todos los datos que tiene que cargar el usuario, utiliza como predeterminados los de la UTN

    st.markdown("### Datos de la Instalación")
    with st.expander("## Datos"):

        col1, col2 = st.columns(2)
        with col1:
            N = st.number_input('Cantidad de Paneles',
                                min_value=0, value=12, step=1)
            # st.markdown('Gstd Irradiancia estándar en $\cfrac {W}{m^2}$')
            Gstd = st.number_input(
                'Gstd Irradiancia estándar en $\cfrac {W}{m^2}$', min_value=0.00, value=1000.00, step=100.00, format='%2.2f')
            Tr = st.number_input('Temperatura de referencia',
                                min_value=0.00, value=25.0, step=0.5, format='%1.1f')
            Ppico = st.number_input(
                'Potencia Pico de cada modulo [W]', min_value=0.00, value=240.00, step=10.00, format='%2.2f')

        with col2:
            kp = st.number_input('Coeficiente de Temperatura-Potencia',
                                max_value=0.0000, value=-0.0044, step=0.0001, format='%4.4f')
            rend = st.number_input('Rendimiento global de la instalación',
                                min_value=0.00, max_value=1.00, value=0.97, step=0.10, format='%2.2f')
            Pinv = st.number_input(
                'Potencia maxima/trabajo del inversor [Kw]', min_value=0.00, value=2.50, step=0.50, format='%2.2f')
            Pmininv = st.number_input(
                'Potencia minima del inversor [Kw]', min_value=0.00, value=0.00, max_value=Pinv, step=0.50, format='%2.2f')

    # Corrijo la temperatura de celda en funcion a la temperatura ambiente
    Datos['Temperatura de Celda']= Datos[T] + 0.031*Datos[G]
    Tc=Datos['Temperatura de Celda']

    # Calculo la potencia y la guardo en una nueva columna
    Datos['Potencia']= N*Datos[G]/Gstd*Ppico*(1+kp*(Tc-Tr))*rend*1e-3
   
    # Analizo si los valores de potencia estan dentro de rango, de no ser así los reemplazo por el correspondiente
    Datos['Potencia'] = Datos['Potencia'].where(Datos['Potencia'] < Pinv, Pinv)
    Datos['Potencia'] = Datos['Potencia'].where(Datos['Potencia'] > Pmininv, 0)

    # Muestro la Tabla (de aca a proximas lineas)
    st.markdown('## Tabla Cargada')

    # Genero dos columnas donde la primera es la tabla y ocupa el 70% de la ventana, mientras que la otra la uso para seleccionar fechas
    col1, col2 = st.columns([0.7, 0.3])

    with col2:
        
        # Calculo los intervalos de tiempo
        intervalos = Datos.index.to_series().diff().dropna()
        intervalos=intervalos[0]
        # Le pido al usuario que seleccione que datos quiere ver, de predeterminado muestra toda la tabla
        Fecha_inicial = st.date_input(
            'Seleccione Fecha Inicial', value=Datos.index[0], min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
        Fecha_final = st.date_input(
            'Seleccione Fecha Final', value=Datos.index[-1], min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
        Tiempo_inicial = st.time_input(
            'Tiempo inicial', datetime.time(0, 0), step=intervalos).__str__()
        Tiempo_final = st.time_input(
            'Tiempo final', datetime.time(23, 50), step=intervalos).__str__()
        
        st.session_state["Fecha_inicial"]=Fecha_inicial
        st.session_state["Fecha_final"]=Fecha_final
        
    with col1:
        # Junto en un solo string la fecha y hora seleccionada para pasarsela a la tabla
        Fecha_inicial_seleccionado = Fecha_inicial + ' ' + Tiempo_inicial
        Fecha_final_seleccionado = Fecha_final + ' ' + Tiempo_final
        # Agregué una variable donde están los datos filtrados por el usuario
        Datos_filtrados = Datos.loc[Fecha_inicial_seleccionado:Fecha_final_seleccionado, :]
       
        # Muestro la tabla
        Datos_filtrados

#
#
# A PARTIR DE ACÁ VAN LAS GRÁFICAS
#
#

    st.write('# Gráficas')
    
    if len(Datos_filtrados) > 10000:
        st.warning(
            "El rango seleccionado contiene demasiados datos para graficar. Reduce el rango para mejorar el rendimiento")
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
            st.line_chart(data=Datos_filtrados, y="Potencia",
                          x_label='Fecha/Tiempo', y_label='Potencia')

        with tab2:
                st.markdown('### Gráfico de Temperatura')
                st.line_chart(data=Datos_filtrados, y=["Temperatura de Celda",T],
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
        Fecha_inicial=datetime.datetime.strptime(Fecha_inicial, '%Y-%m-%d')
        Fecha_final=datetime.datetime.strptime(Fecha_final, '%Y-%m-%d')

        col4, col5 = st.columns([0.7, 0.3])
        with col5:
            Fecha_inicial = st.date_input( 
                'Seleccione Fecha inicial', value=Fecha_inicial, min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
            Fecha_final = st.date_input(
                'Seleccione Fecha Final', value=Fecha_final, min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
        with col4:
            chart_pot = Datos[(Datos.index >= Fecha_inicial) & (Datos.index <= Fecha_final)].drop(columns=['Temperatura (°C)', 'Irradiancia (W/m²)', 'Temperatura de Celda'], errors='ignore') #Filtro la tabla y le saco las columnas excedentes
            if option == "En semanas" :
                potencia_media = chart_pot.resample('W').mean() #Uso el resample para calcular la media
                st.bar_chart(potencia_media)
            if option == "En días" :
                potencia_media = chart_pot.resample('D').mean() #Uso el resample para calcular la media
                st.bar_chart(potencia_media)

        st.write('### Días principales')

        col6, col7 = st.columns([0.5, 0.5])
        with col6:
            #Ordeno las potencias de mayor a menor
            Top_potencias = potencia_media.sort_values(by="Potencia", ascending = False).head(10)

            st.write('Los diez (10) días con mayor potencia en el intervalo elegido son:')
            st.write(Top_potencias)
        with col7:
            #ACÁ VA LO DE ENERGÍA
            st.write('Los diez (10) días con mayor energía???? en el intervalo elegido son:')
        
        st.write('### Máximos y mínimos')

        st.write('La temperatura máxima fue de ', max(Datos['Temperatura (°C)']), '°C, el día ????')
        st.write('La irradiancia máxima fue de ', max(Datos['Irradiancia (W/m²)']), 'W/m², el día ????')

if seccion == 'Mapas interactivos': 
    st.header ('Mapas interactivos', divider='gray')
    st.info(' Esta sección recopila la información geográfica cargada en la pestaña de *Datos*.', icon="ℹ️")
    st.subheader("Mapa Satelital")
    # mapa
    mapa = folium.Map(location=[-31.616681297694267, -60.67543483706093], zoom_start=18)
    # Las coordenadas de location indican el centro del mapa

    #Ahora se hace el marcador puntual
    folium.Marker(
            [-31.616681297694267, -60.67543483706093], 
            popup="Ubicación generador fotovoltaico",
            tooltip="Facultad Regional Santa Fe - UTN"
            ).add_to(mapa)

    # Mostrar el mapa:
    st_folium(mapa, width=725)


  
if seccion == 'Ayuda':
    st.header('Ayuda y soporte de la página', divider='orange')
    with st.expander ('**Importante**', icon="⚠️"): 
        st.write(' Esta página aún se encuentra en un estado primitivo, para usar el chat por favor ingrese solamente el **número** de la opción que elija.')
    with st.chat_message('assistant'):
            st.write('Hola! Escribí la opción sobre la que deseas obtener ayuda: ')
            """
            1. *Guía de la página*  
            2. *Carga y extracción de datos del generador*  
            3. *Glosario de términos*  
            4. *Preguntas frecuentes*  
            5. *Otro*
            """
    texto = st.chat_input("Escriba aquí...")
    if texto=='1':
        with st.chat_message('assistant'):
            st.write('Descripción opción 1')

    if texto=='2':
        with st.chat_message('assistant'):
            st.write('Descripción opción 2')
    #  HACER ASI PARA CADA OPCION DEL CHATBOT


if seccion == 'Feedback': 
    st.header ('Dejá tu comentario!', divider='blue')
    with st.form ('formulario', clear_on_submit=True):
        #  Datos del encuestado
        st.text_input('Introduzca su nombre', placeholder='Juan Peréz')
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




