import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


with st.container():
    st.image('logo.png')
    st.write("[< Volver a Machine Learning](https://web-casgroup-capacitacion.herokuapp.com/py-ml)")


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  '3-5 years':
        return 4
    if x == '6-8 years':
        return 7
    if x == '9-11 years':
        return 10
    if x == '0-2 years':
        return 1
    if x == '15-17 years':
        return 16
    if x == '18-20 years':
        return 19
    if x == '30 or more years':
        return 30
    if x == '12-14 years':
        return 13
    if x == '24-26 years':
        return 25
    if x == '21-23 years':
        return 22
    if x == '27-29 years':
        return 28
    return int(x)

def clean_education(x):
    if 'Bachelor’s degree (BA, BS, B.Eng., etc.)' in x:
        return 'Grado Universitario'
    if 'Master’s degree (MA, MS, M.Eng., MBA, etc.)' in x:
        return 'Post grado'
    if 'Professional degree (JD, MD, etc.)' in x or 'Other doctoral degree (Ph.D, Ed.D., etc.)' in x:
        return 'Doctorado'
    return 'Sin grado universitario'

@st.cache
def load_data():
    df= pd.read_csv('survey_results_public18.csv', sep=';')
    df=df[['Country','FormalEducation','YearsCoding','Employment','Salary']]
    df=df[df['Salary'].notnull()]
    df=df.dropna()
    df=df[df['Employment']=='Employed full-time']
    df=df.drop('Employment',axis=1)
    
    country_map = shorten_categories(df.Country.value_counts(), 300)
    df['Country'] = df['Country'].map(country_map)
    df['Salary']=pd.to_numeric(df['Salary'],errors='coerce')
    df = df[df["Salary"] <= 250000] #filtra los mayores a 250000
    df = df[df["Salary"] >= 10000] #filtra los menores a 10000
    df = df[df['Country'] != 'Other'] #filtra los otros eliminándolos

    df['YearsCoding'] = df['YearsCoding'].apply(clean_experience)
    df['FormalEducation'] = df['FormalEducation'].apply(clean_education)
    return df

df=load_data()

def show_explore_page():
    st.title('Exploración Data Modelo')

    st.write("""### Información Stack Overflow Developer Survey 2018""")

    data=df['Country'].value_counts()

    fig1, ax1=plt.subplots()
    ax1.pie(data, labels=data.index, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    st.write("""### Participación por País""")
    st.pyplot(fig1)

    st.write("""### Sueldo Promedio por País""")
    data=df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""### Sueldo Promedio por Años de Experiencia""")
    data=df.groupby(['YearsCoding'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)