import streamlit as st
import google.generativeai as genai
import base64

# To import the emojis library
import emoji

# --- APP CUSTOMIZATION SECTION ---
# App titles
st.markdown("""
    <h1 style=
    color: #90C383;
    ><strong><i>⚙Customize Buck</i></strong></h1>
            
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
            color: #e7ffe7;
            position: relative;
            z-index: 20;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# The variable are here too, so when the user decides to change the chatbot's persona, the 'model' will change as well
casual_model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"}) #Using Gemini 2.5 Flash model
professional_model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"}) #Using Gemini 2.5 Flash model

# Session State Variables
# To initialze the persona varible in the session state so that the session state can be overidden on this page
if 'persona' not in st.session_state:
    st.session_state.peronsa = 'casual.txt'

# To initialze the index parameter for the radio in the session state
if 'index' not in st.session_state:
    st.session_state.index = {'index1': 0,
                              'index2': 0,
                              'index3': 0}
    
# session state initialization for the chatbot
if "chat_session" not in st.session_state:
    st.session_state.chat_session = casual_model.start_chat(history=[])

# To initialize a 'default' avatar varible in the session state
if 'user_avatar' not in st.session_state:
    st.session_state.user_avatar = ""

# To initialize a list user avatars varible in the session state
if 'user_avatars_list' not in st.session_state:
    st.session_state.user_avatars_list = ["😀", "🤑", "💸", "💲"]

# To initialize a 'default' chatbot avatar varible in the session state
if 'assistant_avatar' not in st.session_state:
    st.session_state.assistant_avatar = ""

# To initialize a list chatbot avatars varible in the session state
if 'assistant_avatars_list' not in st.session_state:
    st.session_state.assistant_avatars_list = ["🤖", "👾", "💸", "💲"]

# Functions
# This function is if the user wishes to add more icons for the user
@st.dialog("Add Your Cutom Avatar")
def add_user_avatar():
    input_emoji = st.text_input("*", placeholder="Emojis Only e.g., 😀")
    if input_emoji: 
        # To check to see if it's an emoji theuse r entered
        for char in input_emoji:
            if not emoji.is_emoji(char):
                st.error("Invalid Avatar. Emojis Only e.g., 😀")
            else:
                st.session_state.user_avatars_list.append(input_emoji) 
                st.rerun()

# This function is if the user wishes to add more icons for the chatbot
@st.dialog("Add Your Cutom Avatar")
def add_assistant_avatar():
    input_emoji = st.text_input("*", placeholder="Emojis Only e.g., 😀")
    if input_emoji: 
        # To check to see if it's an emoji theuse r entered
        for char in input_emoji:
            if not emoji.is_emoji(char):
                st.error("Invalid Avatar. Emojis Only e.g., 😀")
            else:
                st.session_state.assistant_avatars_list.append(input_emoji) 
                st.rerun()

# To let the user choose the chatbot's personality
tone = st.radio("Customize Buck's Personality", ["Casual😄", "Professional💼"], index=st.session_state.index['index1'])
if tone == "Casual😄":
    st.session_state.persona = 'casual.txt'
    st.session_state.chat_session = casual_model.start_chat(history=[])
    st.session_state.index['index1'] = 0
else:
    st.session_state.persona = 'professional.txt'
    st.session_state.chat_session = professional_model.start_chat(history=[])
    st.session_state.index['index1'] = 1

# To divide the different sections of the page
st.divider()

# These variables are for orgainization of the settings
col1, col2 = st.columns(2)
# To let the user choose which icon they want
with col1.container():
    user_avatar = st.radio("Choose your user avatar", st.session_state.user_avatars_list, index=st.session_state.index['index2'])
    if user_avatar:
        st.session_state.user_avatar = user_avatar
        # To set the index for the radio function
        st.session_state.index['index2'] = st.session_state.user_avatars_list.index(st.session_state.user_avatar)
    
    # To invoke the user_add_avatar function
    if st.button("Add User Avatar"):
        add_user_avatar()
    
with col2.container():
    # To let the user choose which icon they want for Buck
    assistant_avatar = st.radio("Choose Buck's avatar", st.session_state.assistant_avatars_list, index=st.session_state.index['index3'])
    if assistant_avatar:
        st.session_state.assistant_avatar = assistant_avatar
        # To set the index for the radio function
        st.session_state.index['index3'] = st.session_state.assistant_avatars_list.index(st.session_state.assistant_avatar)

    # To invoke the user_add_avatar function
    if st.button("Add Buck Avatar"):
        add_assistant_avatar()