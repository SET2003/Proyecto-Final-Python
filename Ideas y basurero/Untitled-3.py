import streamlit as st
import streamlit_antd_components as sac
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


with st.sidebar:
    st.image('Imagenes\\logo-utn.png')
    st.logo('Imagenes\\home-header.png', size = "large", link="https://www.frsf.utn.edu.ar/", icon_image = 'Imagenes\\UTN-FRSF.jpg')
    st.write('---')
    a=sac.menu([
        sac.MenuItem('Acerca de', icon='house-fill'),
        sac.MenuItem('Generador', icon='sun-fill', children=[
            sac.MenuItem('Datos', icon='clipboard-data-fill'),
            sac.MenuItem('Estadísticas', icon='bar-chart-line-fill'),
            sac.MenuItem('Mapa interactivo', icon='map-fill'),
        ]),

        sac.MenuItem('disabled', disabled=True),
        sac.MenuItem(type='divider'),
        sac.MenuItem('links de interés', type='group', children=[
            sac.MenuItem('antd-menu', icon='heart-fill', href='https://ant.design/components/menu#menu'),
            sac.MenuItem('bootstrap-icon', icon='bootstrap-fill', href='https://icons.getbootstrap.com/'),
        ]),
    ], open_all=True, color='#2aa7e1')

if a=='home':
    st.write('messsiiii')