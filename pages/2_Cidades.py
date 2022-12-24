import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import numpy as np

df = pd.read_csv('zomato.csv',index_col=0)

st.set_page_config(page_title= 'Cidades',page_icon= '🏙️',layout= 'wide' )


# Centralizar e adicionar imagem __________________________________________________________________________________________________________


st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)


image = Image.open('logo.png')

st.sidebar.image(image, width=140)

st.sidebar.markdown("""---""")


# Textos da barra lateral __________________________________________________________________________________________________________


st.sidebar.markdown('# Boas vindas! 🍽️')

#filro para a escolha de países
countries = st.sidebar.multiselect(
    'Selecione o país que você deseja acompanhar 👇',
    ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India','Indonesia', 'New Zeland', 'England', 'Qatar','South Africa','Sri Lanka'],default= ['India', 'Brazil', 'Australia', 'United States of America', 'Canada','England', 'Qatar','South Africa'])

st.sidebar.markdown("""---""") #linha divisória

linhas_selecionadas = df['country_name'].isin(countries) #traffic_options assume o valor que o usuario clicar
df = df.loc[linhas_selecionadas,:]



#filtro para o tipo de preço/restaurante
price = st.sidebar.multiselect(
    'Selecione a categoria de restaurante 💰',
    ['expensive', 'gourmet', 'normal', 'cheap'],default= ['expensive', 'gourmet', 'normal', 'cheap'])

linhas_selecionadas = df['price_range'].isin(price)
df = df.loc[linhas_selecionadas,:]


st.sidebar.markdown("""---""") #linha divisória

st.sidebar.markdown('##### Powered by Débora Freitas 👩🏻‍💻')
                    

# Layout no Streamlit _________________________________________________________________________

    
st.markdown('### Visão das cidades cadastradas')

with st.container():
    
    col1, col2, col3 = st.columns(3)
    
    with col1:

    #TOP 15 cidades com mais restaurantes cadastrado __________________________________________

        st.markdown('###### TOP 15 cidades com mais restaurantes cadastrados')

        maiores = (df.loc[:, ['restaurant_id', 'city']].groupby(['city'])
                   .nunique().sort_values(by='restaurant_id', ascending=False).reset_index())

        maiores.columns = ['Cidades','Nº de restaurantes']

        maiores.iloc[0:15,:]

    with col2:

    #TOP 15 cidades com restaurantes que possuem média de avaliação acima de 4.5__________________
        
        st.markdown('###### TOP 15 cidades com restaurantes acima de 4.5')

        melhores_restaurantes = (df.loc[df['aggregate_rating'] > 4.5, ['restaurant_id', 'city']].groupby('city')
                                 .count().sort_values(by='restaurant_id', ascending=False).reset_index())

        melhores_restaurantes.columns = ['Cidades', 'Nº de restaurantes']

        melhores_restaurantes.iloc[0:15,:]
        
    with col3:
        
        #TOP 15 cidades com restaurantes que possuem média de avaliação menor que 2.5________________

        st.markdown('###### TOP 15 cidades com restaurantes abaixo de 2.5')
                    
        piores_restaurantes = (df.loc[df['aggregate_rating'] < 2.5, ['restaurant_id','city']].groupby('city')
                               .count().sort_values(by= 'restaurant_id', ascending=False).reset_index())

        piores_restaurantes.columns = ['Cidade', 'Nº de restaurantes']

        piores_restaurantes.iloc[0:15,:]
        
    
#Gráficos

#TOP 15 cidades com restaurantes mais caros'

with st.container():

    filtro1 = df['price_range'] == 'expensive'

    cidades_caras = (df.loc[filtro1,['city']]).value_counts()

    cidades_caras = cidades_caras.to_frame()
    
    cidades_caras = cidades_caras.reset_index()
    
    cidades_caras.columns = ['Cidade', 'Nº de restaurantes']

    cidades_caras = cidades_caras.iloc[0:15,:]

    fig8 = (px.bar(cidades_caras, x='Cidade', y= 'Nº de restaurantes',
                   title= 'TOP 15 cidades com restaurantes mais caros', color='Cidade',opacity=0.6,
                   text_auto=True))

    st.plotly_chart(fig8, use_container_width= True)
    
    
#TOP 15 cidades com restaurantes mais baratos
    
with st.container():   
    
    filtro2 = df['price_range'] == 'cheap'

    cidades_baratas = (df.loc[filtro2,['city']]).value_counts()

    cidades_baratas = cidades_baratas.to_frame()

    cidades_baratas = cidades_baratas.reset_index()

    cidades_baratas.columns = ['Cidade', 'Nº de restaurantes']

    cidades_baratas = cidades_baratas.iloc[0:15,:]

    fig9 = (px.bar(cidades_baratas, x='Cidade', y= 'Nº de restaurantes',
                   title= 'TOP 15 cidades com restaurantes mais baratos', color='Cidade',opacity=0.6,
                   text_auto=True))
    
    st.plotly_chart(fig9, use_container_width= True)