"""
Cosas obligatorias:
    Barra lateral
    Pestañas
    Datos
    Graficos
    Hora interactiva con calendario

"""
#Librerias que se utilizan o pueden llegar a ser necesarias
import datetime
from datetime import date
import numpy as np
import streamlit as st
import pandas as pd

#Titulos para la pagina principal y para la barra lateral
st.markdown("# Página Principal 🎈")
st.sidebar.markdown("# Página Principal 🎈")

"""
# Calculo Generador Fotovoltaico
"""
#Le pido al usuario que cargue una tabla
Datos=st.file_uploader('Ingresá el archivo', help='Arrastrá el archivo acá o subilo mediante el botón' ,accept_multiple_files=False)

#En caso de que el usuario no cargue ninguna tabla, se utiliza como ejemplo la proporcionada por UTN 
if Datos is None:
    st.markdown("## Ejemplo con Tabla de Datos Climatologicos de Santa Fe 2019")
    Datos=pd.read_excel('Archivos\Datos_climatologicos_Santa_Fe_2019.xlsx', index_col=0)   
else:
    Datos=pd.read_excel(Datos, index_col=0)

#Extraigo los indices de las columnas
G, T= Datos.columns

#Todos los datos que tiene que cargar el usuario, utiliza como predeterminados los de la UTN
with st.sidebar:
    """
    ## **Proporcionar datos de la instalación**
    """
    N=st.number_input('Cantidad de Paneles', min_value=0, value=12, step=1 )
    # st.markdown('Gstd Irradiancia estándar en $\cfrac {W}{m^2}$')
    Gstd=st.number_input('Gstd Irradiancia estándar en $\cfrac {W}{m^2}$', min_value=0.00, value=1000.00, step=100.00, format='%2.2f' )
    Tr=st.number_input('Temperatura de referencia', min_value=0.00, value=25.0, step=0.5, format='%1.1f' )
    Ppico=st.number_input('Potencia Pico de cada modulo [W]', min_value=0.00, value=240.00, step=10.00, format='%2.2f' )
    kp=st.number_input('Coeficiente de Temperatura-Potencia', max_value=0.0000,value=-0.0044, step=0.0001, format='%4.4f' )
    rend=st.number_input('Rendimiento global de la instalación', min_value=0.00 ,max_value=1.00, value=0.97, step=0.10, format='%2.2f' )
    Pinv=st.number_input('Potencia maxima/trabajo del inversor [Kw]', min_value=0.00, value=2.50, step=10.00, format='%2.2f' )
    Pmininv=st.number_input('Potencia minima del inversor [Kw]', min_value=0.00, value=0.00, max_value=Pinv, step=10.00, format='%2.2f' )


#Corrijo la temperatura de celda en funcion a la temperatura ambiente
Tc= Datos[T] + 0.031*Datos[G]

#Calculo la potencia y la guardo en una nueva columna
P=N*Datos[G]/Gstd*Ppico*(1+kp*(Tc-Tr))*rend*1e-3
Datos['Potencia']=P

#Analizo si los valores de potencia estan dentro de rango, de no ser así los reemplazo por el correspondiente
Datos['Potencia']=Datos['Potencia'].where(Datos['Potencia']<Pinv, Pinv)
Datos['Potencia']=Datos['Potencia'].where(Datos['Potencia']>Pmininv, 0)

#Muestro la Tabla (de aca a proximas lineas)
st.markdown('## Tabla Cargada')

#Genero dos columnas donde la primera es la tabla y ocupa el 70% de la ventana, mientras que la otra la uso para seleccionar fechas
col1,col2=st.columns([0.7,0.3])


with col2:
    #Le pido al usuario que seleccione que datos quiere ver, de predeterminado muestra toda la tabla
    Fecha_inicial=st.date_input('Seleccione Fecha Inicial', value=Datos.index[0], min_value=Datos.index[0] ,max_value=Datos.index[-1]).__str__()
    Fecha_final=st.date_input('Seleccione Fecha Final', value=Datos.index[-1], min_value=Datos.index[0] ,max_value=Datos.index[-1]).__str__()
    Tiempo_inicial=st.time_input('Tiempo inicial', datetime.time(0,0), step=600).__str__()
    Tiempo_final=st.time_input('Tiempo final', datetime.time(23,50), step=600).__str__()
with col1:
    #Junto en un solo string la fecha y hora seleccionada para pasarsela a la tabla
    Fecha_inicial_seleccionado=Fecha_inicial+ ' ' + Tiempo_inicial
    Fecha_final_seleccionado=Fecha_final+ ' ' + Tiempo_final
    
    #Muestro la tabla
    Datos.loc[Fecha_inicial_seleccionado:Fecha_final_seleccionado,:]

