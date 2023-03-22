import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    layout = "wide"
)

#image_path = 'Imagem/logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write('# Curry Company Growth Dashboard')