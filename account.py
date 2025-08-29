# Importing libraries for the page:
# To be able to use streamlit 
import streamlit as st
# Using Supabase to manage the backend of the chatbot with a User Authentication System in a database
from supabase import create_client, Client
# For cutomization using the st.markdown
import base64
from dotenv import load_dotenv
# To be able to access environment variables
import os
# To be able to use the main chatbot functions
import buck

# Load environment variables from a .env file
load_dotenv()
# Retrieving a Supabase URL and Supabase Key to create a Client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# ---Background Image---
# Load and encode the image
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

# ---Functions using Supabase Authentication:---
# Defining a Sign Up function - registers a 'Signed Up' user 
def sign_up(email, password, username):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password, "username": username})
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")

# Defining a Sign In function which similarly allows users to log into their created accounts
def sign_in(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")

# Defining a Sign Out function responsible for logging out users
def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.rerun() #This function ensures that the chatbot reloads properly after logging out
    except Exception as e:
        st.error(f"Logout failed: {e}")

# Defines the main chatbot screen for successfully authenticated users
def main_app(user_email):
    st.title("🎉 Welcome Page") # Includes a 'Welcome' message
    st.success(f"Welcome, {user_email}! 👋")
    if st.button("Logout"): # Includes a button to Sign Out if preferred
        sign_out()

# The Authentication Screen displays the login and sign up user interface
def auth_screen():
    st.title(":green[🔐 Welcome to BUCK!]") # Shows a title
    option = st.selectbox("Choose an action:", ["Login", "Sign Up"]) # Includes a drop-down menu for users to pick an option between logging in or signing up
    email = st.text_input("Enter your Email") # Includes an input field for 'Email', 
    user = st.text_input("Enter your Username") # Input field for 'Username'
    password = st.text_input("Password", type="password") # And an input field for 'Password'

    # If the user selects 'Sign Up' and clicks the 'Register' button, the Sign Up function will be executed
    if option == "Sign Up" and st.button("Register"): 
        user = sign_up(email, password, username=user)
        if user and user.user:
            st.success("Registration successful. Please log in.")

    # If the user chooses 'Login' and clicks the 'Login' button instead, the Sign In function will be executed
    if option == "Login" and st.button("Login"):
        user = sign_in(email, password)
        if user and user.user:
            st.session_state.user_email = user.user.email  # Upon successful login, the user's email is stored in the st.session_state
            st.success(f"Welcome back, {email}!") # A welcome message displays
            buck.askGemini("LOGGED IN STOP TALK")
            st.rerun() # And the chatbot will rerun once again to update the interface

# This is to check is the user email exists in the st.session_state
if "user_email" not in st.session_state:
    st.session_state.user_email = None
    
# If the user is logged in, the main_app function is displayed
if st.session_state.user_email:
    main_app(st.session_state.user_email)
else: # Otherwise, the Authentication screen is shown
    auth_screen()

# This ensures a smooth experience where users only see the appropriate screen based on their authentication status.
