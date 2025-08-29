# This is the customization page for the app
# It allows the user to customize the chatbot's persona and avatars for both the user and the chatbot
# Importing the necessary libraries
# Import the streamlit module
import streamlit as st
# Import the genai llm
import google.generativeai as genai
# Import base64 for customization of app
import base64
# To import the emojis library
import emoji

# --- APP CUSTOMIZATION SECTION ---
# App titles
st.markdown("""
    <h1 style=
    color: #90C383;
    ><strong><i>⚙ Customize Buck</i></strong></h1>
            
    <style>
    position: sticky;
    top: 0;
    </style>
    """,
    unsafe_allow_html=True)

# Background
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

# Injecting CSS for the theme - mostly green
st.markdown(
    """
    <style>
        /* Text Font - Sans-Serif */
        * {
            font-family: "Verdana", "Sans-Serif";
        }

        /* Use patterns over the gradient behind the text */
        .stApp::before, .stApp::after, {
            content: "";
            position: absolute;
            border-radius: 50%;
            background: #578C35; 
            pointer-events: auto;
            filter: drop-shadow(10px);
            z-index: 0;
            border-color: #FFFFFF;
        }

        /* Sidebar background - lighter than background */
        section[data-testid="stSidebar"] {
            border-right: 2px solid #8FC087;
            padding-top: 1rem;
        }

        /* --- BUTTONS --- */
        div.stButton > button {
            background-color: #191B18 ;
            color: #f0fff0 ;
            font-weight: bold;
            border-radius: 8px;
            border: 1px solid #FFFFFF ;
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:hover {
            background-color: #4cb152;
            transform: translateY(-2px) scale(1.03);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            color: #76ca76;
            position: relative;
            z-index: 20;
        }

        /* General text */
        .stMarkdown, .stText {
            color: #76ca76;
            position: relative;
            z-index: 20;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# The variable is here too, so when the user decides to change the chatbot's persona, the 'model' will change as well. This is to reduce token from the chatbot 
casual_model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"}) #Using Gemini 2.5 Flash model
professional_model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"}) #Using Gemini 2.5 Flash model

# Session State Variables
# To initialze the persona varible in the session state so that the session state can be overidden on this page
if 'persona' not in st.session_state:
    st.session_state.peronsa = 'casual.txt'

# To initialze the index parameter for the radio to change the chatbot's personality in the session state
if 'persona_index' not in st.session_state:
    st.session_state.persona_index = 0
    
# session state initialization for the chatbot
if "chat_session" not in st.session_state:
    st.session_state.chat_session = casual_model.start_chat(history=[])

# To initialize a 'default' avatar varible in the session state
if 'user_avatar' not in st.session_state:
    st.session_state.user_avatar = "😀"

# To initialize a list user avatars varible in the session state
if 'user_avatars_list' not in st.session_state:
    st.session_state.user_avatars_list = ["😀", "🤓", 
                                          "😂", "🥰", 
                                          "🤔", "🤩", 
                                          "😮", "🤫", 
                                          "😴", "😔", 
                                          "😠", "🥳", 
                                          "😎", "🤑"]

# To initialize a 'default' chatbot avatar varible in the session state
if 'buck_avatar' not in st.session_state:
    st.session_state.buck_avatar = "🤖"

# To initialize a list chatbot avatars varible in the session state
if 'buck_avatars_list' not in st.session_state:
    st.session_state.buck_avatars_list = ["🤖", "👾",
                                          "💰", "🏦",
                                          "💵", "💸", 
                                          "💲"]

# Functions
# This function is if the user wishes to add more icons for the user
@st.dialog("Choose Your Avatar")
def user_avatars():
    st.markdown(f"## Your Current Avatar: {st.session_state.user_avatar}")
    # To organize the avatars in the middle of the screen
    col1, col2, col3 = st.columns([1, 7, 1])
    # To let the user choose which icon they want
    with col2.container(border=False, height=180):
        # To let the user choose which icon they want
        for user_avatar in range(0, len(st.session_state.user_avatars_list), 4):
            # To organize the avatars in rows of 4
            col_avatars = st.columns(4)
            # To display the avatars in rows of 4
            for i, user_avatar in enumerate(st.session_state.user_avatars_list[user_avatar:user_avatar+4]): # Loop through a slice of 4 avatars
                with col_avatars[i]:
                    # If the user clicks on the avatar, it will be set as their avatar
                    if st.button(user_avatar):
                        st.session_state.user_avatar = user_avatar
                        st.rerun()

    # To add an avatar to the list
    input_emoji = st.text_input("*", placeholder="Emojis Only e.g., 😀")
    if input_emoji: 
        # To check to see if it's an emoji the user entered
        if not emoji.is_emoji(input_emoji):
            st.error("Invalid Avatar. Emojis Only e.g., 😀")
        # To check if the avatar already exists
        elif input_emoji in st.session_state.user_avatars_list:
            st.error("Avatar already exists. Please enter a different one.")
        # To add the avatar if it passes the checks
        else:
            st.session_state.user_avatars_list.append(input_emoji)

# This function is if the user wishes to add more icons for the chatbot
@st.dialog("Add Your Avatar")
def add_buck_avatar():
    st.markdown(f"## Buck's Current Avatar: {st.session_state.buck_avatar}")
    col1, col2, col3 = st.columns([1, 7, 1])
    # To let the user choose which icon they want
    with col2.container(border=False, height=180):
        # To let the user choose which icon they want
        for buck_avatar in range(0, len(st.session_state.buck_avatars_list), 4):
            # To organize the avatars in rows of 4
            col_avatars = st.columns(4)
            # To display the avatars in rows of 4
            for i, buck_avatar in enumerate(st.session_state.buck_avatars_list[buck_avatar:buck_avatar+4]): # Loop through a slice of 4 avatars
                with col_avatars[i]:
                    # If the user clicks on the avatar, it will be set as their avatar
                    if st.button(buck_avatar):
                        st.session_state.buck_avatar = buck_avatar
                        st.rerun()
    
    # To add an avatar to the list
    input_emoji = st.text_input("Add An Avatar", placeholder="Emojis Only e.g., 😀")
    if input_emoji: 
        # To check to see if it's an emoji theuse r entered
        if not emoji.is_emoji(input_emoji):
            st.error("Invalid Avatar. Emojis Only e.g., 😀")
        # To check if the avatar already exists
        elif input_emoji in st.session_state.buck_avatars_list:
            st.error("Avatar already exists. Please enter a different one.")
        # To add the avatar if it passes the checks
        else:
            st.session_state.buck_avatars_list.append(input_emoji)

    st.divider()
    
# To let the user choose the chatbot's personality
st.markdown("## Buck's Personality")
tone = st.radio("", ["Casual😄", "Professional💼"], index=st.session_state.persona_index)
# Depending on what the user chooses, the chatbot's persona and model will change
if tone == "Casual😄":
    st.session_state.persona = 'casual.txt'
    st.session_state.chat_session = casual_model.start_chat(history=[])
    st.session_state.persona_index = 0
else:
    st.session_state.persona = 'professional.txt'
    st.session_state.chat_session = professional_model.start_chat(history=[])
    st.session_state.persona_index = 1

# To divide the different sections of the page
st.divider()

st.markdown("## Avatars")
# These variables are for orgainization of the settings
col1, col2 = st.columns(2)
# To let the user choose which icon they want
with col1.container():
    st.markdown(f"##### Your Current Avatar: {st.session_state.user_avatar}")
    
    # To invoke the user_add_avatar function
    if st.button("Change Your Avatar"):
        user_avatars()
    
with col2.container():
    st.markdown(f"##### Buck's Current Avatar: {st.session_state.buck_avatar}")

    # To invoke the user_add_avatar function
    if st.button("Change Buck's Avatar"):
        add_buck_avatar()
