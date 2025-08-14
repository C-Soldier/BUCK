#USING GEMINI

# Import necessary libraries
import google.generativeai as genai
from dotenv import load_dotenv as lenv
import os
import streamlit as st
import json
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
    "<h4 style='text-align: center; " 
    "color: #FFFFFF;" 
    "'><strong>Ask me before you go broke.</strong></h4>",
    unsafe_allow_html=True)


#Background
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


lenv()  # Load environment variables from .env file
secret_key = os.getenv("API")

#Configurethe the generative model 
try:
    genai.configure(api_key=secret_key)
except Exception as e:
    st.error(f"Error configuring API key: {e}")
    st.stop()

# Configure the generative model
model1 = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"}) #Using Gemini 2.5 Flash model
model2 = genai.GenerativeModel('gemini-2.5-pro', generation_config={"response_mime_type": "application/json"}) #Using Gemini 2.5 Pro model

#session state initialization
if "chat_session1" not in st.session_state:
    st.session_state.chat_session1 = model1.start_chat(history=[])

#Session State variables
if "chat_session2" not in st.session_state:
    st.session_state.chat_session2 = model2.start_chat(history=[])

#A place to hold the messages
if "requests" not in st.session_state:
    st.session_state.requests = []

if "recentChats" not in st.session_state:
    st.session_state.recentChats = {}

if "store" not in st.session_state:
    st.session_state.store = True
    
if "title" not in st.session_state:
    st.session_state.title = None

#Other variables for the chatbot's functions
file_path = "prompts.txt"
text = ""


#Functions
def askGemini(question, chat_session1):
    try:
        response = chat_session1.send_message(question)
        json_string = response.text
        start = json_string.find("{")
        end = json_string.find("}") + 1
        json_data = json.loads(json_string[start: end])
        st.session_state.title = json_data.get("chat_title", "No chat_title found")
        reply = json_data.get("response", "No response found")
        return reply
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

def showGemini(image_data, chat_session1):
    try:
        image = {'mime_type': 'image/jpeg', 'data': image_data}
        response = chat_session1.send_message([image])
        json_string = response.text
        start = json_string.find("{")
        end = json_string.find("}") + 1
        json_data = json.loads(json_string[start: end])
        st.session_state.title = json_data.get("chat_title", "No chat_title found")
        reply = json_data.get("response", "No response found")
        return reply
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None
 
#If the user wishes to delete mulitple chats at their choosing   
@st.dialog("Delete Multiple Talks")
def delete():
    checked_key = None
    for key in st.session_state.recentChats.keys():
        if st.checkbox(key):
            checked_key = key
    try:
        if st.button("Delete"):
            st.session_state.recentChats.pop(checked_key)
            st.session_state.requests = []
            st.session_state.store = True
            st.rerun()
    except KeyError:
        pass


#Streamlit Customization
st.set_page_config(
    page_title="BUCK",
    page_icon="💸",
    layout="centered"
)

#sidebar controls
with st.sidebar:
    #New chat button 
    if st.button("💲New Money Talk"):
        st.session_state.requests = []
        st.session_state.chat_session1 = model1.start_chat()
        st.session_state.store = True
        st.rerun()
    
    with st.container():
        "Recent Money Talks💰:"
        for key, value in st.session_state.recentChats.items():
            if st.button(key):
                st.session_state.requests = value
                st.session_state.store = False
                st.rerun()

    #This is used to activate the delete multiple chats function
    if st.button("Delete Talks💀"):
        if len(st.session_state.recentChats) > 0:
            delete()
        else:
            st.toast("There are no talks to delete")
    
    #This is used to delete all the chats
    if st.button("Delete All Talks☠"):
        if len(st.session_state.recentChats) > 0:
            st.session_state.recentChats.clear()
            st.session_state.requests.clear()
            st.session_state.store = True
            st.rerun()
        else:
            st.toast("There are no talks to delete")
            

#Display all the historical messages
for request in st.session_state.requests:
    #Avatar customizations
    avatar = request.get("avatar", "💲" if request.get('role') == 'assistant' else "🤑")
    #Display all the historical messages
    st.chat_message(request['role'], avatar=avatar).markdown(request['content'])

#Input area for the user to type their message or upload a file
prompt = st.chat_input("Now, Let's Talk Finance 🤑",
accept_file=True,  # Allow file uploads
file_type=["jpg", "jpeg", "png", "webp", "gif"]#Specify allowed file types
)

try:
    with open(file_path) as file:
        text = file.read()
except Exception as e:
    st.error(f"ERROR: {e}")

# If the file is read successfully, we can use its content as a prompt
askGemini(text, st.session_state.chat_session1)

if prompt and prompt.text:
    #To display the messages from the user in the Streamlit app
    st.chat_message("user", avatar="🤑").markdown(prompt.text)
    
    #To store each of the messages
    st.session_state.requests.append({'role': 'user', 'content': prompt.text})
    
    #send the prompt to the chatmodel
    request = askGemini(prompt.text, st.session_state.chat_session1)
    
    #Show chatbot responses
    st.chat_message("assistant", avatar="💲").markdown(request)
    
    #To store the chatbot responses in the session state
    st.session_state.requests.append({'role': 'assistant', 'content': request})

#If the user has uploaded an image file, process it
if prompt and prompt["files"]:
    #To display the image uploaded by the user
    st.chat_message("user").image(prompt["files"][0])
    
    #To store each of the messages
    st.session_state.requests.append({'role': 'user', 'content': prompt["files"][0]})
    
    #send the image data to the chatmodel
    request = showGemini(prompt["files"][0].read(), st.session_state.chat_session1)
    
    #Display the response from the chatbot about the image
    st.chat_message("assistant", avatar="🤑").markdown(request)
    
    #To store the chatbot responses in the session state
    st.session_state.requests.append({'role': 'assistant', 'content': request})

#To store each conversation in the recent chats dict
if st.session_state.store and (prompt and prompt.text) or (prompt and prompt["files"]):
    st.session_state.recentChats.update({st.session_state.title: st.session_state.requests})
    st.session_state.store = False
    st.rerun()
