import streamlit as st
import pickle
import numpy as np

with st.container():
    st.image('logo.png')
    st.write("[< Volver a Machine Learning](https://web-casgroup-capacitacion.herokuapp.com/py-ml)")


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data=load_model()
regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]


def show_predict_page():
    st.title('Predictor Sueldo Software Developer')

    st.write("""### Información Requerida para Predicción Sueldo""")


    countries=(
        'United States',
        'India',
        'United Kingdom',
        'Germany',
        'Canada',
        'France',
        'Russian Federation'
    )

    education_level=(
        'Grado Universitario', 
        'Sin grado universitario', 
        'Post grado',
        'Doctorado'
    )

    country=st.selectbox('Pais', countries)
    education=st.selectbox('Educacion', education_level)

    experience=st.slider('Años de Experiencia',0,30,3)

    ok=st.button('Calcular Sueldo')

    if ok:
        X = np.array([[country, education, experience ]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)

        salary=regressor.predict(X)
        st.subheader(f'Sueldo estimado: ${salary[0]:,.2f}')
