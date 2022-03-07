import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

page=st.sidebar.selectbox('Explorar Data o Predicción Sueldo', ('Predicción','Data'))

with st.container():
    st.image('logo.png')
    st.write("[< Volver a Machine Learning](https://web-casgroup-capacitacion.herokuapp.com/py-ml)")

if page=='Predicción':
    show_predict_page()
else:
    show_explore_page()