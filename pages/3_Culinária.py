import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import numpy as np

df = pd.read_csv('zomato.csv',index_col=0)

st.set_page_config(page_title= 'Culinárias',page_icon= '🍲',layout= 'wide' )

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


st.markdown('### Visão das culinárias cadastradas')

with st.container():

        #TOP 15 culinárias mais bem avaliadas

        st.markdown('###### TOP 15 culinárias mais bem avaliadas')

        bem_avaliadas = (df.loc[:,['cuisines_null', 'aggregate_rating']]
                         .groupby('cuisines_null')
                         .mean().sort_values(by='aggregate_rating', ascending=False)
                         .reset_index())

        bem_avaliadas['aggregate_rating'] = bem_avaliadas['aggregate_rating'].apply(lambda x: np.round (x,1))

        bem_avaliadas.columns = ['Tipos de culinária','Avaliações médias']

        bem_avaliadas = bem_avaliadas.iloc[0:15,:]
        
        bem_avaliadas = np.round(bem_avaliadas,1)

        fig5 = (px.bar(bem_avaliadas, x='Tipos de culinária', y='Avaliações médias',
                       color='Avaliações médias',opacity=0.5,text_auto=True))

        st.plotly_chart(fig5, use_container_width= True)

with st.container():
    
    col1, col2= st.columns(2)
    
    with col1:
        #TOP 15 cidades com mais tipos de culinárias distintos

        st.markdown('###### TOP 15 cidades com mais tipos de culinária distinto')

        culinarias = (df.loc[:, ['cuisines_null', 'city']].groupby('city')
                      .nunique().sort_values(by='cuisines_null', ascending=False).reset_index())

        culinarias.columns= ['Cidades','Tipos de culinária']

        culinarias = culinarias.iloc[0:15,:]
        
        st.dataframe(culinarias)
        

    with col2:

        #TOP 15 restaurantes mais bem avaliados

        st.markdown('###### TOP 15 restaurantes mais bem avaliados')

        restaurantes = (df.loc[:, ['aggregate_rating', 'restaurant_name','cuisines_null']].drop_duplicates()
                        .groupby(['restaurant_name'])
                        .max()
                        .sort_values(by= 'aggregate_rating', ascending=False)
                        .reset_index())

        restaurantes.columns = ['Restaurantes', 'Avaliações', 'Culinária']
        
        #restaurantes['Avaliações'] = restaurantes['Avaliações'].apply(lambda x: x**2)
        
        restaurantes['Avaliações'] = restaurantes['Avaliações'].apply(lambda x: f'{x}')

        restaurantes = restaurantes.iloc[0:15,:]
        
        st.dataframe(restaurantes)