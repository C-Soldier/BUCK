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

# Customize Buck page
Buck_Settings =  st.Page(
    page="buck_customization.py",
    title="Customize Buck",
    icon="⚙"
)

#The Account Settings Page
Account = st.Page(
    page="account.py",
    title="Account Settings",
    icon="📝",
)

#Logo
st.logo("buck_logo.png", size="large")

pg = st.navigation([Chatbot, BillTracker, Buck_Settings, Account], position='top')
pg.run()
