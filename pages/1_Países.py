import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import numpy as np

df = pd.read_csv('zomato.csv',index_col=0)

st.set_page_config(page_title= 'Países',page_icon= '🌎',layout= 'wide' )


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


st.sidebar.markdown("""---""")

st.sidebar.markdown('##### Powered by Débora Freitas 👩🏻‍💻')
                    

# Layout no Streamlit _________________________________________________________________________


st.markdown('### Visão dos países cadastrados')


#Gráfico 1 - Restaurates registrados por país__________________________________________________

    
df2 = df.loc[:, ['restaurant_id', 'country_name']].groupby('country_name').count().reset_index().sort_values(by='restaurant_id', ascending= False)
df2.columns = ['Países', 'Quantidade de restaurantes']

fig2 = (px.bar(df2, x='Países', y='Quantidade de restaurantes',
          title= 'Quantidade de restaurantes registrados por país', color='Países',opacity=0.6))

st.plotly_chart(fig2, use_container_width= True)

    
    
# Gráfico 2 - Cidades registradas por país_________________________________________________________

df1 = df.loc[:,['city', 'country_name']].groupby('country_name').nunique().reset_index().sort_values(by='city', ascending=False)
df1.columns = ['Países', 'Quantidade de cidades']

fig1 = (px.bar(df1, x='Países', y='Quantidade de cidades',
              title= 'Quantidade de cidades registradas por país', color='Países',opacity=0.6))

st.plotly_chart(fig1, use_container_width= True)


# Gráfico 3 - Avaliações médias por país___________________________________________________________
    
df4 = df.loc[:,['aggregate_rating', 'country_name']].groupby('country_name').mean().sort_values(by='aggregate_rating',ascending=False).reset_index()

df4['aggregate_rating'] = df4['aggregate_rating'].apply(lambda x: np.round (x,1))

df4.columns = ['Países','Avaliações médias']

fig4 = (px.bar(df4, x='Países', y='Avaliações médias',
              title= 'Avaliações médias por país',color='Avaliações médias',
               opacity=0.5,text_auto=True, color_continuous_scale=px.colors.sequential.Viridis))

st.plotly_chart(fig4, use_container_width= True)