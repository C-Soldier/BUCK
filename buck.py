# Importing the necessary libraries
# The LLM we'll be using
import google.generativeai as genai
# To be able to load the API key from the '.env' file
from dotenv import load_dotenv as lenv
# To be able to load the API key from the '.env' file
import os
# To be able to use streamlit
import streamlit as st
# For customization for the chatbot's prompt tuning
import json
# For customization of using the st.markdown
import base64

# --- APP CUSTOMIZATION SECTION ---
# App titles
st.markdown("""
    <h1 style= 
    'text-align: center;'
    color: #90C383;
    ><strong><i>💸BUCK💸</i></strong></h1>
            
    <style>
    position: sticky;
    top: 0;
    </style>
    """,
    unsafe_allow_html=True)

st.markdown(
    "<h4 style='text-align: center;' " 
    "color: #FFFFFF;" 
    "'><strong>ASK ME BEFORE YOU GO BROKE</strong></h4>",
    unsafe_allow_html=True)


# Background
# Load and encode the image
image_path = "buck_wallpaper.jpg"

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
        background-repea#Thisisto   t: no-repeat;
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

# Streamlit App Tab Customization
st.set_page_config(
    page_title="BUCK",
    page_icon="💸",
    layout="centered"
)

lenv()  # To load the api variable from .env file
secret_key = os.getenv("CHAT_API") #A assign the api to a variable

try:
    # Configurethe the generative model 
    genai.configure(api_key=secret_key)
except Exception as e:
    # If failed to find api, the app will stop
    st.error(f"Error configuring API key: {e}")
    st.stop()

# Configure/set up the generative model
# There are two differnet variables for the model to minimize the tokens used for the chatbot
casual_model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"}) #Using Gemini 2.5 Flash model
professional_model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"}) #Using Gemini 2.5 Flash model

# session state initialization for the chatbot
if "chat_session" not in st.session_state:
    st.session_state.chat_session = casual_model.start_chat(history=[])

# Session State variables
# A place to hold the messages
if "chats" not in st.session_state:
    st.session_state.chats = []

# To store the conversations made between the user and chabot
if "recentChats" not in st.session_state:
    st.session_state.recentChats = {}

# This varible was created to let the program know when to create a new conversation
if "store_chat" not in st.session_state:
    st.session_state.store_chat = True


# This is to store the title of the conversation created by the chatbot
if "chat_title" not in st.session_state:
    st.session_state.chat_title = None

# To initialze a 'default' persona varible in the session state
if 'persona' not in st.session_state:
    st.session_state.persona = 'casual.txt'

# To initialize a 'default' user avatar varible in the session state
if 'user_avatar' not in st.session_state:
    st.session_state.user_avatar = "😀"

# To initialize a 'default' chatbot avatar varible in the session state
if 'assistant_avatar' not in st.session_state:
    st.session_state.assistant_avatar = "🤖"

# Other variables for the chatbot's functions
# To create a global text variable
text = ''

# Functions
# This function is created to be ablt to talk to the chatbot
def askGemini(prompt, chat_session):
    try:
        response = chat_session.send_message(prompt)
        json_string = response.text
        start = json_string.find("{")
        end = json_string.find("}") + 1
        json_data = json.loads(json_string[start: end])
        st.session_state.chat_title = json_data.get("chat_title", "No chat_title found")
        reply = json_data.get("response", "No response found")
        return reply
    except Exception as e:
        st.error(f"Error generating response: {e}")
        st.stop()
        return None

# THis function is used to send images to the chabot
def showGemini(image_data, chat_session):
    try:
        image = {'mime_type': 'image/jpeg', 'data': image_data}
        response = chat_session.send_message(image)
        json_string = response.text
        start = json_string.find("{")
        end = json_string.find("}") + 1
        json_data = json.loads(json_string[start: end])
        st.session_state.chat_title = json_data.get("chat_title", "No chat_title found")
        reply = json_data.get("response", "No response found")
        return reply
    except Exception as e:
        st.error(f"Error processing image: {e}")
        st.stop()
        return None

#This function is a of the function 'askGemeini' and 'showGemini'
def chatGemini(prompt, image_data, chat_session):
    try:
        image = {'mime_type': 'image/jpeg', 'data': image_data}
        response = chat_session.send_message([image, prompt])
        json_string = response.text
        start = json_string.find("{")
        end = json_string.find("}") + 1
        json_data = json.loads(json_string[start: end])
        st.session_state.chat_title = json_data.get("chat_title", "No chat_title found")
        reply = json_data.get("response", "No response found")
        return reply
    except Exception as e:
        st.error(f"Error with response: {e}")
        st.stop()
        return None

# If the user wishes to delete any of the conversations as their choosing
@st.dialog("Which talk(s) would you like to delete?")
def delete():
    checked_key = None
    for key in st.session_state.recentChats.keys():
        if st.checkbox(key):
            checked_key = key
    try:
        if st.button("Delete"):
            st.session_state.recentChats.pop(checked_key)
            st.session_state.chats = []
            st.session_state.store_chat = True
            st.rerun()
    except KeyError:
        pass

# sidebar controls
with st.sidebar:
    # To show the user which conversation they are currently in
    if len(st.session_state.recentChats) == 0:
        st.write("Current Talk: - -")
    else:
        for key, value in st.session_state.recentChats.items():
            if st.session_state.chats == value:
                st.write(f"Current Talk: {key}")
    
    # To start a new conversation with the chatbot
    if st.button("💲New Money Talk", width=220):
        st.session_state.chats = []
        if st.session_state.chat_session == casual_model.start_chat():
            st.session_state.chat_session = casual_model.start_chat()
        else:
            st.session_state.chat_session = professional_model.start_chat(history=[])
        st.session_state.store_chat = True
        st.rerun()
    
    # To properly seperate the different section of the sidebar
    st.divider()

    # To display each conversation made between the user and the chatbot
    with st.container():
        "Recent Money Talks💰:"
        for key, value in st.session_state.recentChats.items():
            if st.button(key, width=220):
                st.session_state.chats = value
                st.session_state.store_chat = False
                st.rerun()
  
    st.divider()

    # This is used to activate the delete chats function
    if st.button("Delete Talks💀", width=220):
        if len(st.session_state.recentChats) > 0:
            delete()
        else:
            st.toast("There are no talks to delete")
    
    # This is used to delete ALL the conversations
    if st.button("Delete All Talks☠", width=220):
        if len(st.session_state.recentChats) > 0:
            st.session_state.recentChats.clear()
            st.session_state.chats.clear()
            st.session_state.store_chat = True
            st.rerun()
        else:
            st.toast("There are no talks to delete")

for chat in st.session_state.chats:
    # Avatar customizations from the session state
    avatar = chat.get("avatar", st.session_state.assistant_avatar if chat.get('role') == 'assistant' else st.session_state.user_avatar)
    # Display all the historical messages
    st.chat_message(chat['role'], avatar=avatar).markdown(chat['content'])

# Input area for the user to type their message or upload a file for the chatbot
prompt = st.chat_input("Now, Let's Talk Finance 🤑",
accept_file=True,  # Allow file uploads
file_type=["jpg", "jpeg", "png", "webp", "gif"]#To specify which file types are accepted
)

# To send the text file of the chatbot's persona to prompt tune the chabot
try:
    with open(st.session_state.persona) as file:
        text = file.read()
except Exception as e:
    st.error(f"ERROR: {e}")

# If the file from the settings page is read successfully, we can use its content as a prompt
askGemini(text, st.session_state.chat_session)

if prompt and prompt.text and prompt["files"]:
    # To display the messages from the user in the Streamlit app
    st.chat_message("user", avatar=st.session_state.user_avatar).image(prompt["files"][0])
    st.chat_message("user", avatar=st.session_state.user_avatar).markdown(prompt.text)
    
    # To store each of the messages
    st.session_state.chats.append({'role': 'user', 'content': prompt["files"][0]})
    st.session_state.chats.append({'role': 'user', 'content': prompt.text})
    
    chat = chatGemini(prompt.text, prompt["files"][0].read(), st.session_state.chat_session)

    # Display the response from the chatbot about the image
    st.chat_message("assistant", avatar=st.session_state.assistant_avatar).markdown(chat)
    
    # To store the chatbot responses in the session state
    st.session_state.chats.append({'role': 'assistant', 'content': chat})    

elif prompt and prompt.text:
    # To display the messages from the user in the Streamlit app
    st.chat_message("user", avatar=st.session_state.user_avatar).markdown(prompt.text)
    
    # To store each of the messages
    st.session_state.chats.append({'role': 'user', 'content': prompt.text})
    
    # send the prompt to the chatmodel
    chat = askGemini(prompt.text, st.session_state.chat_session)
    
    # Show chatbot responses
    st.chat_message("assistant", avatar=st.session_state.assistant_avatar).markdown(chat)
    
    # To store the chatbot responses in the session state
    st.session_state.chats.append({'role': 'assistant', 'content': chat})

# If the user has uploaded an image file, process it
elif prompt and prompt["files"]:
    # To display the image uploaded by the user
    st.chat_message("user", avatar=st.session_state.user_avatar).image(prompt["files"][0])
    
    # To store each of the messages
    st.session_state.chats.append({'role': 'user', 'content': prompt["files"][0]})
    
    # send the image data to the chatmodel
    chat = showGemini(prompt["files"][0].read(), st.session_state.chat_session)
    
    # Display the response from the chatbot about the image
    st.chat_message("assistant", avatar=st.session_state.assistant_avatar).markdown(chat)
    
    # To store the chatbot responses in the session state
    st.session_state.chats.append({'role': 'assistant', 'content': chat})

# To store each conversation in the recent chats dict
if st.session_state.store_chat and prompt:
    st.session_state.recentChats.update({st.session_state.chat_title: st.session_state.chats})
    st.session_state.store_chat = False
    st.rerun()
