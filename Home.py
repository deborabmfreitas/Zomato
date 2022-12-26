import pandas as pd
import numpy as np
import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
from PIL import Image
import plotly.express as px

df = pd.read_csv('zomato.csv',index_col=0)

df1 = df.copy()

st.set_page_config(page_title= 'Zomato',page_icon= '📊',layout= 'wide' )


# Adicionando imagem __________________________________________________________________________________________________________

images = Image.open('zomato1.png')
st.image(images)


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

st.sidebar.markdown("""---""") #linha divisória


# Textos da barra lateral ______________________________________________________________________________________________________________


st.sidebar.markdown('# Boas vindas! 🍽️')

#filro para a escolha de países
countries = st.sidebar.multiselect(
    'Selecione o país que você deseja acompanhar 👇',
    ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India','Indonesia', 'New Zeland', 'England', 'Qatar','South Africa','Sri Lanka'],default= ['India', 'Brazil', 'Australia', 'United States of America', 'Canada','England', 'Qatar','South Africa'])

st.sidebar.markdown("""---""")

linhas_selecionadas = df['country_name'].isin(countries) #traffic_options assume o valor que o usuario clicar
df = df.loc[linhas_selecionadas,:]



#filtro para o tipo de preço/restaurante
price = st.sidebar.multiselect(
    'Selecione a categoria de restaurante 💰',
    ['expensive', 'gourmet', 'normal', 'cheap'],default= ['expensive', 'gourmet', 'normal', 'cheap'])

linhas_selecionadas = df['price_range'].isin(price)
df = df.loc[linhas_selecionadas,:]


st.sidebar.markdown("""---""")

st.sidebar.markdown('##### Powered by Débora Freitas 👩🏻‍💻')
                    

# Métricas gerais ______________________________________________________________________________________________________________________


with st.container():
        
    col1, col2, col3, col4, col5 = st.columns(5)
    
    
    with col1:
       
        countries_list = list(df1['country_name'].unique())
        countries_list = len(countries_list)
        
        col1.metric('Países registrados', countries_list)
     
    
    with col2:
        cities_list = list(df1['city'].unique())
        cities_list = len(cities_list)
        
        col2.metric('Cidades registradas', cities_list)
    
    with col3:
        
        restaurants_list = list(df1['restaurant_id'].unique())
        restaurants_list = len(restaurants_list)

        col3.metric('Restaurantes registrados', restaurants_list)

    with col4:
        
        cuisines_unique = df1['cuisines_null'].unique()
        cuisines_unique = len(cuisines_unique)
        
        col4.metric('Tipos de culinária',cuisines_unique)
    
    with col5:
        total_avaliacoes = df1['aggregate_rating'].count()
        
        col5.metric('Total de avaliações', total_avaliacoes)

        
#tabs
        
tab1, tab2 = st.tabs(['Visão geográfica', 'Categorias de restaurante'])


# TAB 1 Mapa ____________________________________________________________________________________________________________________________

with tab1:
    

    st.markdown('### Visão geográfica')

    locais = df[['latitude','longitude']].values.tolist()
    popups = df[['city','restaurant_name','aggregate_rating']].values.tolist()

    mapa = folium.Map()

    MarkerCluster(locations=locais, popups=popups).add_to(mapa)

    folium_static(mapa, width=1024, height=600)
    
# TAB 2 Gráficos _________________________________________________________________________________________________________________________

with tab2:

    #Avaliações por tipo de restaurante
    
    st.markdown('#### Avaliações por categoria de restaurante')


    avaliacao_tipo = (df.loc[:,['price_range','aggregate_rating']].groupby('price_range')
                      .mean().reset_index().sort_values(by= 'aggregate_rating', ascending=False))

    avaliacao_tipo['aggregate_rating'] = avaliacao_tipo['aggregate_rating'].apply(lambda x: np.round (x,1))

    avaliacao_tipo.columns = ['Tipo de restaurante','Avaliação média']

    fig6 = (px.bar(avaliacao_tipo, x='Tipo de restaurante', y= 'Avaliação média', color='Tipo de restaurante',opacity=0.6, text_auto=True))

    st.plotly_chart(fig6, use_container_width= True)



    #Quantidade de restaurantes por categoria
    
    st.markdown('#### Quantidade de restaurantes por categoria')

    restaurantes_tipo = (df.loc[:,['price_range','restaurant_id']].groupby('price_range')
                      .count().reset_index().sort_values(by= 'restaurant_id', ascending=False))


    restaurantes_tipo.columns = ['Tipo de restaurante','Nº de restaurantes']

    fig7 = (px.bar(restaurantes_tipo, x='Tipo de restaurante', y= 'Nº de restaurantes', color='Tipo de restaurante',opacity=0.6, text_auto=True))

    st.plotly_chart(fig7, use_container_width= True)