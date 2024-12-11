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
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Titulos para la pagina principal y para la barra lateral
st.markdown("# Página Principal 🎈")
st.sidebar.markdown("# Página Principal 🎈")
"""
# Calculo Generador Fotovoltaico
"""
            #Le pido al usuario que cargue una tabla
Datos = st.file_uploader(
    'Ingresá el archivo', help='Arrastrá el archivo acá o subilo mediante el botón', accept_multiple_files=False)

# En caso de que el usuario no cargue ninguna tabla, se utiliza como ejemplo la proporcionada por UTN
if Datos is None:
    st.markdown("## Ejemplo con Tabla de Datos Climatologicos de Santa Fe 2019")
    Datos = pd.read_excel(
        'Archivos\Datos_climatologicos_Santa_Fe_2019.xlsx', index_col=0)
else:
    Datos = pd.read_excel(Datos, index_col=0)

# Extraigo los indices de las columnas
G, T = Datos.columns

# Todos los datos que tiene que cargar el usuario, utiliza como predeterminados los de la UTN

"""
## **Proporcionar datos de la instalación**
"""
col1, col2=st.columns(2)
with col1:
    N = st.number_input('Cantidad de Paneles', min_value=0, value=12, step=1)
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
Tc = Datos[T] + 0.031*Datos[G]

# Calculo la potencia y la guardo en una nueva columna
P = N*Datos[G]/Gstd*Ppico*(1+kp*(Tc-Tr))*rend*1e-3
Datos['Potencia'] = P

# Analizo si los valores de potencia estan dentro de rango, de no ser así los reemplazo por el correspondiente
Datos['Potencia'] = Datos['Potencia'].where(Datos['Potencia'] < Pinv, Pinv)
Datos['Potencia'] = Datos['Potencia'].where(Datos['Potencia'] > Pmininv, 0)

# Muestro la Tabla (de aca a proximas lineas)
st.markdown('## Tabla Cargada')

# Genero dos columnas donde la primera es la tabla y ocupa el 70% de la ventana, mientras que la otra la uso para seleccionar fechas
col1, col2 = st.columns([0.7, 0.3])


with col2:
    # Le pido al usuario que seleccione que datos quiere ver, de predeterminado muestra toda la tabla
    Fecha_inicial = st.date_input(
        'Seleccione Fecha Inicial', value=Datos.index[0], min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
    Fecha_final = st.date_input(
        'Seleccione Fecha Final', value=Datos.index[-1], min_value=Datos.index[0], max_value=Datos.index[-1]).__str__()
    Tiempo_inicial = st.time_input(
        'Tiempo inicial', datetime.time(0, 0), step=600).__str__()
    Tiempo_final = st.time_input(
        'Tiempo final', datetime.time(23, 50), step=600).__str__()

with col1:
    # Junto en un solo string la fecha y hora seleccionada para pasarsela a la tabla
    Fecha_inicial_seleccionado = Fecha_inicial + ' ' + Tiempo_inicial
    Fecha_final_seleccionado = Fecha_final + ' ' + Tiempo_final
    #Agregué una variable donde están los datos filtrados por el usuario
    Datos_filtrados = Datos.loc[Fecha_inicial_seleccionado:Fecha_final_seleccionado, :]

    # Muestro la tabla
    Datos.loc[Fecha_inicial_seleccionado:Fecha_final_seleccionado, :]

#A PARTIR DE ACÁ VAN LAS GRÁFICAS 

st.write('# Gráficas')
tab1, tab2, tab3 = st.tabs(['Gráfico de líneas', 'Heatmap temporal', 'Gráfico de dispersión'])

#Verifico si la cantidad de puntos supera un límite donde se realentizaría mucho la página (10000 puntos), si lo es muestro un warning diciendo que son muchos los puntos
#como para realizar un gráfico.

if len(Datos_filtrados) > 10000: 
    st.warning("El rango seleccionado contiene demasiados puntos para graficar. Reduce el rango para mejorar el rendimiento.")
else:
    with tab1:
        st.markdown('### Gráfico de Irradiancia')
        st.line_chart(data=Datos_filtrados, y=G, x_label='Fecha/Tiempo', y_label='Irradiancia (W/m²)', color="#ffc300")
        st.markdown('### Gráfico de Temperatura')
        st.line_chart(data=Datos_filtrados, y=T, x_label='Fecha/Tiempo', y_label='Temperatura (°C)')

    with tab2:
        
        # Crear el heatmap
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Generar la tabla dinámica para el heatmap
        heatmap_data = Datos_filtrados.pivot_table(
            index=Datos_filtrados.index.hour, 
            columns=Datos_filtrados.index.dayofyear, 
            values=T, 
            aggfunc='mean'
        ).sort_index(ascending=False) #Esto hace que se ordenen las horas de forma descendente

        # Crear el heatmap
        sns.heatmap(
            heatmap_data,
            cmap="flare", #Paleta de colores
            ax=ax,
            cbar_kws={'label': 'Temperactura (°C)'}  # Etiqueta para la barra de color
        )

        # Etiquetas y título
        ax.set_xlabel('Día del año')
        ax.set_ylabel('Hora del día')
        ax.set_title('Heatmap de Temperatura Promedio por Hora y Día')
        
        # Mostrar el heatmap
        st.markdown('### Mapa de calor de Temperatura')
        st.pyplot(fig)

    with tab3:
        
        # Crear el scatter plot (Gráfico de dispersión)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(Datos_filtrados[G], Datos_filtrados[T], alpha=0.6, c=Datos_filtrados[G], cmap="viridis")

        # Agregar etiquetas y título
        ax.set_title("Relación entre Irradiancia y Temperatura", fontsize=16)
        ax.set_xlabel("Irradiancia (W/m²)", fontsize=12)
        ax.set_ylabel("Temperatura (°C)", fontsize=12)
        ax.grid(alpha=0.3)

        # Mostrar la figura en Streamlit
        st.markdown('### Gráfico de dispersión Irradiancia-Temperatura')
        st.pyplot(fig)



# import altair as alt

# # Datos de ejemplo
# data = {
#     "Tiempo": pd.date_range(start="2024-01-01", periods=10, freq="D"),
#     "Temperatura (°C)": [20, 21, 19, 23, 24, 22, 20, 21, 23, 25],
#     "Irradiancia (W/m²)": [400, 420, 410, 450, 470, 460, 430, 440, 480, 500],
# }

# # Convertir los datos a un DataFrame de pandas
# df = pd.DataFrame(data)

# # Escalas compartidas para mantener el zoom consistente
# x_scale = alt.Scale(domain=list(df["Tiempo"].dt.to_pydatetime()))  # Escala de tiempo compartida

# # Gráfico para la Temperatura con Tooltip
# temp_chart = alt.Chart(df).mark_line(color="blue").encode(
#     x=alt.X("Tiempo:T", scale=x_scale, title="Tiempo"),
#     y=alt.Y("Temperatura (°C):Q", title="Temperatura (°C)", axis=alt.Axis(titleColor="blue")),
#     tooltip=["Tiempo:T", "Temperatura (°C):Q"]  # Información al pasar el mouse
# )

# # Gráfico para la Irradiancia con Tooltip
# irr_chart = alt.Chart(df).mark_line(color="orange").encode(
#     x=alt.X("Tiempo:T", scale=x_scale),  # Reutiliza la escala de tiempo
#     y=alt.Y("Irradiancia (W/m²):Q", title="Irradiancia (W/m²)", axis=alt.Axis(titleColor="orange")),
#     tooltip=["Tiempo:T", "Irradiancia (W/m²):Q"]  # Información al pasar el mouse
# )

# # Combinar los gráficos con capas y ejes independientes
# combined_chart = alt.layer(
#     temp_chart,
#     irr_chart
# ).resolve_scale(
#     y="independent"  # Escalas independientes para los ejes Y
# ).properties(
#     width=700,
#     height=400,
#     title="Gráfico de Temperatura e Irradiancia"
# ).interactive()  # Habilitar interactividad (zoom y paneo)

# # Mostrar el gráfico en Streamlit
# st.altair_chart(combined_chart, use_container_width=True)



# # Generar datos de ejemplo
# n_days = 7  # Número de días
# n_hours = 24  # Número de horas en un día

# # Crear un DataFrame con días, horas y temperaturas aleatorias
# data = {
#     "Día": np.repeat(pd.date_range(start="2024-01-01", periods=n_days, freq="D").strftime('%Y-%m-%d'), n_hours),
#     "Hora": np.tile(range(n_hours), n_days),
#     "Temperatura (°C)": np.random.uniform(15, 35, n_days * n_hours),  # Temperaturas aleatorias
# }

# heatmap_data = Datos_filtrados.pivot_table(
#             index=Datos_filtrados.index.hour, 
#             columns=Datos_filtrados.index.dayofyear, 
#             values=T, 
#             aggfunc='mean'
#         ).sort_index(ascending=False)

# heatmap_data=heatmap_data.reset_index()
# heatmap_data
# # Mapa de calor interactivo usando Altair
# heatmap = alt.Chart(heatmap_data).mark_rect().encode(
#     x=alt.X('heatmap_data.columns', title="Día"),  # Eje X: Días
#     y=alt.Y('heatmap_data.index', title="Hora"),  # Eje Y: Horas
#     color=alt.Color('heatmap_data', scale=alt.Scale(scheme="viridis"), title="Temperatura (°C)")  # Colores según temperatura
#     #tooltip=[Datos_filtrados.index.dayofyear, Datos_filtrados.index.hour, Datos_filtrados[T]]  # Información interactiva
# ).properties(
#     width=700,
#     height=400,
#     title="Mapa de Calor: Temperatura por Día y Hora"
# ).interactive()  # Habilitar interactividad (paneo y zoom)

# # Mostrar el mapa de calor en Streamlit
# st.altair_chart(heatmap, use_container_width=True)


#
#
# 
# 
#  DE ACA EN ADELANTE SON PRUEBAS DE COMO HACER TABLA GENERICA EN FUNCION DE TIEMPOS GENERICOS, NO BORRAR
#
#
#
#
# Tiempo_uno_tabla=str(Datos.index[0])
# # Tiempo_uno_tabla=pd.to_datetime(Tiempo_uno_tabla)

# b=Tiempo_uno_tabla.split(' ')
# c=b[1].split(':')
# st.write(type(b))
# st.write(b)
# st.write(c)