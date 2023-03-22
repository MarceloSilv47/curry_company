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
    page_title="Visão Empresa",
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

def order_metric(df1):
    colunas = ['ID', 'Order_Date']
    df_aux = df1.loc[: , colunas].groupby('Order_Date').count().reset_index()
    df_aux.head()
    fig = px.bar( df_aux, x='Order_Date', y='ID')
    return fig

def traffic_order_share(df1):
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby( 'Road_traffic_density' ).count().reset_index()
    df_aux['perc_ID'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum())
    fig = px.pie( df_aux, values='perc_ID', names='Road_traffic_density' )
    return fig

def traffic_order_city(df1):   
    df_aux = (df1.loc[:, ['ID', 'Road_traffic_density','City']].groupby(['City', 'Road_traffic_density']).count().reset_index())
    fig = px.scatter(df_aux, x = 'City', y='Road_traffic_density', size = 'ID', color = 'City')
    return fig

def order_by_week(df1):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    colunas = ['ID', 'week_of_year']
    df_aux = df1.loc[: , colunas].groupby('week_of_year').count().reset_index()
    df_aux.head()
    fig = px.line( df_aux, x='week_of_year', y='ID')
    return fig

def order_share_by_week(df1):
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )
    return fig

def country_maps(df1):
    colunas = ['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']
    df_aux = data_plot = df1.loc[:, colunas].groupby( ['City', 'Road_traffic_density']).median().reset_index()
    map_ = folium.Map( zoom_start=11 )
    for index, location_info in data_plot.iterrows():
      folium.Marker( [location_info['Delivery_location_latitude'],
                      location_info['Delivery_location_longitude']],
                      popup=location_info[['City', 'Road_traffic_density']] ).add_to( map_ )
    folium_static(map_ , width=1024 , height=600)

#===================== Inicio da Estrutura lógica do código ============================

#Import Dataset
df = pd.read_csv( 'dataset/train.csv')

#Limpando os dados
df1 = clean_code(df)

#==========================================
#Barra Lateral no Streamlit
#==========================================

st.header('Marketplace - Visão Empresa')

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

tab1 , tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    
    with st.container():
        #Quantidade de pedidos por dia
        st.markdown('# Orders by Day')
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        #Distribuição dos pedidos por tipo de tráfego
        with col1:
            st.header('Traffic Order Share')
            fig = traffic_order_share(df1)
            st.plotly_chart(fig, use_container_width=True)
                
        with col2:
            st.header('Traffic Order City')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)        

with tab2:
    with st.container():
        # Quantidade de pedidos por semana.
        st.markdown('# Order by week')
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        # A quantidade de pedidos por entregador por semana.
        st.markdown('# Order share by week')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
        

with tab3:    
    #A localização central de cada cidade por tipo de tráfego.
    st.markdown('# Country Maps')
    country_maps(df1)
   