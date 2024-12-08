"""
Barra lateral
Pestañas
Datos
Graficos
Hora interactiva con calendario

"""
import numpy as np
import streamlit as st
import pandas as pd

"""
# Calculo Generador Fotovoltaico


"""

st.markdown("# Página Principal 🎈")
st.sidebar.markdown("# Página Principal 🎈")

Datos=st.file_uploader('Ingresá el archivo', help='Arrastrá el archivo acá o subilo mediante el botón' ,accept_multiple_files=False)

if Datos is None:
    st.markdown("## Ejemplo con Tabla de Datos Climatologicos de Santa Fe 2019")
    Datos=pd.read_excel('Archivos\Datos_climatologicos_Santa_Fe_2019.xlsx', index_col=0)   
else:
    Datos=pd.read_excel(Datos, index_col=0)

"""
## **Proporcionar datos de la instalación**

"""

with st.sidebar:
    N=st.number_input('Cantidad de Paneles', min_value=0, value=12, step=1 )
    # st.markdown('Gstd Irradiancia estándar en $\cfrac {W}{m^2}$')
    Gstd=st.number_input('Gstd Irradiancia estándar en $\cfrac {W}{m^2}$', min_value=0.00, value=1000.00, step=100.00, format='%2.2f' )
    Tr=st.number_input('Temperatura de referencia', min_value=0.00, value=25.0, step=0.5, format='%1.1f' )
    Ppico=st.number_input('Potencia Pico de cada modulo', min_value=0.00, value=240.00, step=10.00, format='%2.2f' )
    kp=st.number_input('Coeficiente de Temperatura-Potencia', max_value=0.0000,value=-0.0044, step=0.0001, format='%4.4f' )
    rend=st.number_input('Rendimiento global de la instalación', min_value=0.00 ,max_value=1.00, value=0.97, step=0.10, format='%2.2f' )

st.markdown('## Tabla Cargada')
Datos


