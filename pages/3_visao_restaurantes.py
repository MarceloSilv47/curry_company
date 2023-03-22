#LIBRARIES
import pandas as pd
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
import numpy as np

st.set_page_config(
    page_title="Visão Restaurantes",
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

def distance(df1, fig):
    if fig == False:
        colunas = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude','Delivery_location_longitude']
        df1['distance'] = df1.loc[:, colunas].apply( lambda x: haversine(
        (x['Restaurant_latitude'], x['Restaurant_longitude']), 
        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        dis_media = np.round(df1['distance'].mean(), 2)
        return dis_media
    else:
        colunas = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude','Delivery_location_longitude']
        df1['distance'] = df1.loc[:, colunas].apply( lambda x: haversine(
            (x['Restaurant_latitude'], x['Restaurant_longitude']), 
            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        dis_media = df1.loc[: , ['City' , 'distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data = [go.Pie (labels = dis_media['City'], values = dis_media['distance'], pull = [0, 0.1, 0])])
        return fig

def time_delivery(df1, festival, op):
    if op == 'avg':
        df_fes = df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').mean().reset_index()
        linhas = df_fes['Festival'] == festival
        df_aux = df_fes.loc[linhas,['Time_taken(min)'] ]
        df_aux = np.round(df_aux.iloc[0,0], 2)
    else:
        df_fes = df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').std().reset_index()
        linhas = df_fes['Festival'] == festival
        df_aux = df_fes.loc[linhas,['Time_taken(min)'] ]
        df_aux = np.round(df_aux.iloc[0,0], 2)
    return df_aux

def time_graph(df1):
    colunas = ['City', 'Time_taken(min)']
    df_aux = df1.loc[:, colunas].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['time_mean', 'time_std']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar( name = 'Control',
                             x = df_aux['City'],
                             y = df_aux['time_mean'],
                             error_y = dict (type = 'data', array = df_aux['time_std'])))
    fig.update_layout(barmode = 'group')
    return fig 

def time_on_traffic(df1):
    colunas = ['City', 'Time_taken(min)', 'Road_traffic_density']
    df_cal = df1.loc[:, colunas].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
    df_cal.columns = ['time_mean', 'time_std']
    df_cal = df_cal.reset_index()
    fig = px.sunburst(df_cal, path=['City', 'Road_traffic_density'], values='time_mean',
                      color = 'time_std',color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df_cal['time_std']))
    return fig
            


#===================== Inicio da Estrutura lógica do código ============================

#Import Dataset
df = pd.read_csv( 'dataset/train.csv')

#Limpando os dados
df1 = clean_code(df)


#==========================================
#Barra Lateral no Streamlit
#==========================================

st.header('Marketplace - Visão Restaurantes')

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
        st.title('Overal Metrics')
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            #Quantidade de entregadores
            qt_entregadores = df1['Delivery_person_ID'].nunique()
            st.metric('Entregadores únicos',qt_entregadores)
            
        with col2:
            dis_media = distance(df1, fig=False)
            st.metric('Distância média',dis_media)

        with col3:
            #Tempo médio de entrega durante os Festivais
            df_aux = time_delivery(df1, festival = 'Yes', op='avg')
            st.metric('Tempo médio de entrega c/festival',df_aux)
            
            
        with col4:
            #Desvio Padrão de entrega durante os Festivais
            df_aux = time_delivery(df1, festival = 'Yes',  op='std')
            st.metric('Tempo médio de entrega c/festival',df_aux)
            
        with col5:
            #Tempo médio de entrega sem os Festivais
            df_aux = time_delivery(df1, festival = 'No', op='avg')
            st.metric('Tempo médio de entrega s/festival',df_aux)
            
        with col6:
            #Desvio Padrão de entrega durante os Festivais
            df_aux = time_delivery(df1, festival = 'No',  op='std')
            st.metric('Desvio padrão de entrega s/festival',df_aux)
            
        
    with st.container():
        st.markdown("""---""")
        st.title('Tempo médio de entrega por cidade')
        fig = time_graph(df1)
        st.plotly_chart(fig)
    
    with st.container():
        st.markdown("""---""")
        st.title('Distribuição do tempo')
        
        col1, col2 = st.columns(2)
        with col1:
            fig = distance(df1, fig=True)
            st.plotly_chart(fig)
            
        with col2:
            fig = time_on_traffic(df1)
            st.plotly_chart(fig)
            
    with st.container():
        st.markdown("""---""")
        st.title('Distribuição da distância')
        colunas = ['City', 'Time_taken(min)', 'Type_of_order']
        df_cal = df1.loc[:, colunas].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})
        df_cal.reset_index()
        df_cal.columns = ['time_mean', 'time_std']
        st.dataframe(df_cal)

