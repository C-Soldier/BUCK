import streamlit as st

#Pages in Streamlit
#The chatbot/main page
Chatbot = st.Page(
    page="buck.py",
    title="BUCK",
    icon="💸",
    default= True,
)

#The Bill Tracker Page
BillTracker = st.Page(
    page="stbill.py",
    title="📜📌Bill & Subscription Tracker",
)

#Financial News Page

#Logo
st.logo("Buck.png", size="large", link="https://buckfinance.streamlit.app/")

pg = st.navigation([Chatbot, BillTracker], position='top')
pg.run()
