# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 12:18:48 2021

@author: Pipe San Martín
"""

import requests
import json
import pandas as pd
import numpy as np
import streamlit as st
import time
import datetime as d
import base64
from datetime import datetime

data_load_state = st.text("Cargando datos.....")


url = 'https://api.nasa.gov/planetary/apod'
apikey = "qOVfMfqCIs0VVahdaMdWIUWWOHiJAFOSB9g6Xb8w"
hoy = datetime.today().strftime('%Y-%m-%d')

@st.cache
def get_nasa_info(url, apikey):
    querystring = {
        "start_date":'2020-01-01',
        "end_date": hoy,
        "api_key": apikey
    }
    
    headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
            }
    data_load_state.text("Consultando a la nasa.....")
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        lista = json.loads(response.text)
        
    except:
        
        print("Error")

    fechas = []
    titulos = []
    explicacion = []
    urls = []
    for e in lista:
    
        fechas.append(e['date'])
        titulos.append(e['title'])
        explicacion.append(e['explanation'])
        urls.append(e['url'])
        
    
    df = pd.DataFrame({
        'Fecha': fechas,
        'Titulo': titulos,
        'Explicacion': explicacion,
        'Url': urls
    })
    
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Fecha'] = df['Fecha'].dt.strftime('%Y-%m-%d')
    
    return df


data = get_nasa_info(url, apikey)

data_load_state.text("¡Datos listos!")


def download_csv(df, name='APOD_NASA'):
    
    csv = df.to_csv(index=False)
    base = base64.b64encode(csv.encode()).decode()
    file = (f'<a href="data:file/csv;base64,{base}" download="%s.csv">Descargar datos con AVOD de la NASA</a>' % (name))
    
    return file


st.header('Astronomy Picture of the Day (APOD)')

st.sidebar.title("¿De qué día quieres ver el APOD?")



today = datetime.today()
yesterday = today - d.timedelta(days=1)
start_date = st.sidebar.date_input('Día seleccionado', yesterday)


j = 0

for fecha in data['Fecha']:

    if str(fecha) == str(start_date):
        

            
        if 'jpg' in data['Url'][j]:
                
            st.image(data['Url'][j], caption=data['Titulo'][j] + ' (' + datetime.strptime(fecha, '%Y-%m-%d').strftime('%b %d, %Y') + ')')
                
        else:
                
            st.video(data['Url'][j])
            st.subheader(data['Titulo'][j] + ' (' + datetime.strptime(fecha, '%Y-%m-%d').strftime('%b %d, %Y') + ')')
        

            
        st.write(data['Explicacion'][j])

    j += 1
    
if j == (len(data)-1):
    
    st.error('Error: no se encontró APOD para esa fecha')
   
st.sidebar.markdown(download_csv(data),unsafe_allow_html=True)

