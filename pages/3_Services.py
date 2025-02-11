import streamlit as st
# import firebase_admin
# from firebase_admin import credentials #pip install firebase_admin
# from firebase_admin import auth
import io
from PIL import Image
import base64
# import pandas as pd
# from st_aggrid import AgGrid, GridOptionsBuilder  #add import for GridOptionsBuilder
# import psycopg2
 

# ---- HEADER SECTION ----
st.set_page_config(
    page_title="Services",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Make your dream a reality!"
    }
)

# Load the images
youtube_img = base64.b64encode(open("pages/images/youtube.png", "rb").read()).decode()
instagram_img = base64.b64encode(open("pages/images/instagram.png", "rb").read()).decode()

# Create columns in the sidebar with less spacing
col1, col2, col3, col4, col5 , col6  = st.sidebar.columns([1, 1, 1, 1, 1, 1])

with col1:
    st.markdown(
        """<a href="https://www.youtube.com/@djtayzer">
        <img src="data:image/png;base64,{}" width="30">
        </a>""".format(youtube_img),
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """<a href="https://www.instagram.com/tayzer/">
        <img src="data:image/png;base64,{}" width="30">
        </a>""".format(instagram_img),
        unsafe_allow_html=True
    )

# Use local CSS
with open("pages/style/style.css") as source_style:
    st.markdown(f"<style>{source_style.read()}</style>", unsafe_allow_html=True)

with open("pages/style/style.css") as source_style:
    st.markdown(f"<style>{source_style.read()}</style>", unsafe_allow_html=True)
st.image("pages/images/services.png", width=1750) 

# Inject CSS for background color
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)





 





# # Uses st.cache_resource to only run once.
# @st.cache_resource
# def init_connection():
#     return psycopg2.connect(**st.secrets["postgres"])

# conn = init_connection()

 
# # Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()

 

# st.sidebar.write("Products")
# _property_type = ""; _occupancy = ""; _credit_score_est_result = ""; _refi_purpose = ""; _property_value = ""; _borrow_amount = ""; _property_balance = ""; 
 
# _loan_type = st.sidebar.selectbox('What services?', ['Purchase','Refinance','Home Equity'])
# if _loan_type == "Refinance" or _loan_type == "Home Equity":
#     _property_type = st.sidebar.radio( "What type of property do you own?",('Single Family Home','Townhome', 'Condominium','Multi Family Home', 'Manufactured or Mobile Home'))
#     _occupancy = st.sidebar.radio( "What is the property use?",('Primary Home', 'Secondary Home', 'Rental Property'))
#     _credit_score_est_result = st.sidebar.selectbox('What is your fico score?', ['Excellent > 719','Good 680 - 719', 'Fair 640 - 679', 'Poor 620 - 639', 'Bad 580 - 619'])
#     _refi_purpose = st.sidebar.radio("What is the loan purpose?",('Home Improvement', 'Retirement Income', 'Debt Consolidation', 'Investment Purposes' ,'Other'))
#     _property_value = st.sidebar.slider('What is the property estimated value?', 0, 10000000, 600000)
#     _borrow_amount = st.sidebar.slider('How much do you want to borrow?', 0, 10000000, 500000)
#     _property_balance = st.sidebar.slider('What is the current balance?', 0, 10000000, 300000)
#     _ltv = int((int(_borrow_amount)) / int(_property_value) * 100)
# elif _loan_type == "Purchase":
#    _property_type = st.sidebar.radio( "What type of property are you looking to purchase?",('Single Family Home','Townhome', 'Condominium','Multi Family Home', 'Manufactured or Mobile Home'))
#    _occupancy = st.sidebar.radio( "What is the property use?",('Primary Home', 'Secondary Home', 'Rental Property'))
#    _credit_score_est_result = st.sidebar.selectbox('What is your fico score?', ['Excellent > 719','Good 680 - 719', 'Fair 640 - 679', 'Poor 620 - 639', 'Bad 580 - 619'])
#    _sale_amount = st.sidebar.slider('What is the sales price?', 0, 10000000, 600000)
#    _borrow_amount = st.sidebar.slider('How much do you want to borrow?', 0, 10000000, 500000)
#    _ltv = int(((_borrow_amount) / (_sale_amount)) * 100)

# _temp_list = []
# _temp_list.append(_property_type)
# _temp_list.append(_occupancy)
# _temp_list.append(_loan_type)

# if _credit_score_est_result == "Excellent > 719":
#     _fico = 720
# elif _credit_score_est_result == "Good 680 - 719":
#     _fico = 680
# elif _credit_score_est_result == "Fair 640 - 679":
#     _fico = 640
# elif _credit_score_est_result == "Poor 620 - 639":
#     _fico = 620
# elif _credit_score_est_result == "Bad 580 - 619":
#     _fico = 580
 
# rows = run_query("select lender, trunc(int_rate,2) as int_rate, trunc(base,2) as base, trunc(adj,2) as adj from lwn_qualify_company_rates(_fico:="+ str(_fico) + ",_ltv:="+ str(_ltv) + ",_attribute_names:=array" + str(_temp_list) + ");")

# data=pd.DataFrame(rows)
# if len(data.columns) == 0:
#     st.write("Product not available")
# else:
#     data.columns=['Lender','Int Rate','Base','Adjustment']
#     st.table(data)

 
