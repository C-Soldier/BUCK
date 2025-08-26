import streamlit as st
from supabase import create_client, Client
import base64

supabase_url = st.secrets["supa"]["SUPABASE_URL"]
supabase_key = st.secrets["supa"]["SUPABASE_KEY"]
supabase: Client = create_client(supabase_url, supabase_key)

#Background Image
#Load and encode the image
image_path = "settings_wallpaper.jpg"

with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Use st.markdown to set the background image via CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        position: relative;
        min-height: 100vh;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


def sign_up(email, password, username):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password, "username": username})
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")

def main_app(user_email):
    st.title("🎉 Welcome Page")
    st.success(f"Welcome, {user_email}! 👋")
    if st.button("Logout"):
        sign_out()

def auth_screen():
    st.title(":green[🔐 Welcome to BUCK!]")
    option = st.selectbox("Choose an action:", ["Login", "Sign Up"])
    email = st.text_input("Enter your Email")
    user = st.text_input("Enter your Username")
    password = st.text_input("Password", type="password")

    if option == "Sign Up" and st.button("Register"):
        user = sign_up(email, password, username=user)
        if user and user.user:
            st.success("Registration successful. Please log in.")

    if option == "Login" and st.button("Login"):
        user = sign_in(email, password)
        if user and user.user:
            st.session_state.user_email = user.user.email
            st.success(f"Welcome back, {email}!")
            st.rerun()

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if st.session_state.user_email:
    main_app(st.session_state.user_email)
else:
    auth_screen()
