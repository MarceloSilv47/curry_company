#LIBRARIES
import pandas as pd
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Visão Entregadores",
    layout = "wide"
)

#=========================================
#Funções
#=========================================

def clean_code(df1):
    """
    Esta função tem a resposabilidade de limpar o dataframe
    Tipos de limpeza:
    1. Remoção dos dados NaN
    2. Mudança do tipo da coluna de dados
    3. Remoção dos espaços das variáveis de texto
    4. Formatação da coluna de datas
    5. Limpeza  da coluna de tempo (remoção do texto da variável numérica)
    
    Input: Dataframe
    Output: Dataframe
    """
    #1. Convertendo a coluna Delivery_person_Age de texto para int
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    #2. Convertendo Delivery_person_Ratings de texto para float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    #3.Convertendo a coluna Order_Date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    #4. Convertendo a coluna multiple_deliveries de texto para int
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    #5. Removendo os espaços dentro de strings/texto/object

    df1.loc[: , 'ID'] = df1.loc[: , 'ID'].str.strip()
    df1.loc[: , 'Road_traffic_density'] = df1.loc[: , 'Road_traffic_density'].str.strip()
    df1.loc[: , 'Type_of_order'] = df1.loc[: , 'Type_of_order'].str.strip()
    df1.loc[: , 'Type_of_vehicle'] = df1.loc[: , 'Type_of_vehicle'].str.strip()
    df1.loc[: , 'City'] = df1.loc[: , 'City'].str.strip()
    df1.loc[: , 'Festival'] = df1.loc[: , 'Festival'].str.strip()

    #6. Removendo Nan de Weatherconditions
    linhas_where = df1['Weatherconditions'] != 'conditions NaN'
    df1 = df1.loc[linhas_where, :].copy()

    #7. Removendo Nan de Festival	
    linhas_fest = df1['Festival'] != 'NaN'
    df1 = df1.loc[linhas_fest, :].copy()

    #8. Removendo Nan de City
    linhas_city = df1['City'] != 'NaN'
    df1 = df1.loc[linhas_city, :].copy()

    #9. Limpando a coluna de time taken

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ' )[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1

def top_delivery(df1, top_asc):
    colunas = ['Delivery_person_ID','Time_taken(min)', 'City']
    colunas2 = ['City','Time_taken(min)']
    df_aux = (df1.loc[:, colunas].groupby(colunas2).mean().sort_values(colunas2, ascending=top_asc).reset_index())
    df_aux01 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df_aux.loc[df_aux['City'] == 'Urban', :].head(10)
    df_aux03 = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].head(10)
    df_final = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df_final

#===================== Inicio da Estrutura lógica do código ============================

#Import Dataset
df = pd.read_csv( 'dataset/train.csv')

#Limpando os dados
df1 = clean_code(df)


#==========================================
#Barra Lateral no Streamlit
#==========================================

st.header('Marketplace - Visão Entregadores')

#image_path = '/Users/marce/Documents/repos/ftc_programacao_python/Imagem/logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value = pd.datetime( 2022, 4, 13),
    min_value = pd.datetime( 2022, 2, 11),
    max_value = pd.datetime( 2022, 4, 6),
    format='DD-MM-YYYY' )
st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown('### Power by Comunidade DS')

#Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de Trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#==========================================
#Layout no Streamlit
#==========================================

tab1 , tab2, tab3 = st.tabs(['Visão Gerencial', '', ''])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        
        col1 , col2, col3, col4 = st.columns(4 , gap = 'large')
        with col1:
            #Maior idade dos entregadores
            maior = df1['Delivery_person_Age'].max()
            col1.metric('Maior idade', maior)
            
        with col2:
            #Menor idade dos entregadores
            menor = df1['Delivery_person_Age'].min()
            col2.metric('Menor idade', menor)

        with col3:
            #Melhor condição de veículos
            melhor = df1['Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor)
            
        with col4:
            #Pior condição de veículos
            pior = df1['Vehicle_condition'].min()
            col4.metric('Pior condição', pior)
    
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown( '###### Avaliação média por entregador')
            df_medias = df1.loc[:,['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_medias)
            
        with col2:
            st.markdown( '###### Avaliação média por trânsito')
            df_avg_std = (df1.loc[: , ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density')
                            .agg({'Delivery_person_Ratings': ['mean','std']}))
            df_avg_std.columns = ['delivery_mean', 'delivery_std']
            st.dataframe(df_avg_std.reset_index())
            
            st.markdown( '###### Avaliação média por clima')
            df_avg_std = (df1.loc[: , ['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions')
                .agg({'Delivery_person_Ratings': ['mean','std']}))
            df_avg_std.columns = ['delivery_mean', 'delivery_std']
            st.dataframe(df_avg_std.reset_index())
            
    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Top entregadores mais rápidos')
            df3 = top_delivery(df1, top_asc=True)
            st.dataframe(df3)

        with col2:
            st.markdown('##### Top entregadores mais lentos')
            df3 = top_delivery(df1, top_asc=False)
            st.dataframe(df3)

        
        
        
