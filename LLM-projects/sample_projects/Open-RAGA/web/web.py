import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components
import uuid
from config import firebaseConfig
import pyrebase




# Only load once
if "config_loaded" not in st.session_state:
    # Load environment variables
    load_dotenv()
    # get url endpoint
    st.session_state.URL = os.getenv('URL')




if "firebase" not in st.session_state:
    firebase = pyrebase.initialize_app(firebaseConfig)
    st.session_state.database = firebase.database()


if "unique_id" not in st.session_state:
    st.session_state.unique_id = str(uuid.uuid4())




    
# Define dialog using the decorator
@st.dialog("ℹ️ Connection Error..")
def no_internet(text):
    st.markdown(f"""
         {text}
           """)
  


# Function to make post request
def get_reponse(prompt:str,messages:list,url:str):


    payload = {'query': prompt.strip(), 'last_3_turn': messages}

    try:

        response = requests.post(url= url, data=json.dumps(payload))

        if(response.status_code==200):

           return response.json()['response']


    except requests.exceptions.RequestException as e:
        # This will catch all types of request-related exceptions

        no_internet("""EVA is currently unable to reach its server.

               This might be due to:
               - Temporary server maintenance
               - Network issues
               - Incorrect backend URL

               Please try again later or contact support.""")



# Define dialog using the decorator
@st.dialog("ℹ️ EVA Usage policy..")
def eva_policy():


    st.markdown("""
        **1. 🔒 Privacy**: Your questions are stored anonymously to improve our services.  
        **2. ⚠️ No Guarantees**: The assistant may not always provide accurate or official responses.  
        **3. 🪪 No Sensitive Info**: Please avoid entering personal, sensitive, or financial information.  
        **4. 🎓Educational Purpose**: This bot is for helping with university-related queries only.

        ✔️ By continuing, you agree to these terms.
        """)

    col1,col2,col3 = st.columns([1,2,1])
    with col2:

     if st.button("AGREE AND CONTINUE",icon="✅"):

            st.session_state.accepted_policy = True
            st.rerun()





def ChatUI():

    # Show dialog automatically on first load
    if "accepted_policy" not in st.session_state:
        eva_policy()
        st.stop()

    st.info("☑️ This is a official Virtual assistant for Eklavya University , Damoh.")
    st.info("💬 Welcome! I can help with courses,admissions and more.")

    with st.container(border=True):
    
        col1, col2, col3, col4 = st.columns([2, 7, 2, 2])
    
        with col1:
    
            st.empty()
    
            st.image("app/assets/icon/eklavaya_university_logo.png", width=40)
            st.image("app/assets/icon/google-gemini-icon.png", width=40)
    
        with col2:

            st.markdown(
                """
                <h1 style='color: #1f77b4; font-size: 45px;'>
                    EVA <span style='color: #d54747 ; font-size: 20px;'>Eklavya</span> <span style='font-size: 20px;'>Virtual Assistant</span>
                </h1>
                """,
                unsafe_allow_html=True
            )
    
        with col4:
            st.markdown("")
            st.image("app/assets/icon/icons8-google-assistant-120.png", width=80)
    
    
    # Initialize chat history
    if "messages" not in st.session_state:
    
        st.session_state.messages = []
    
    
    # Initialize history variable
    if 'history' not in st.session_state:
        st.session_state.history = [{"role": "user", "content": ''},{"role": "assistant", "content": ''}]


    for message in st.session_state.messages:

        role = message["role"]
        avatar = ":material/person:" if role == "user" else "✨"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])
    
    
    
    # Accept user input
    if prompt := st.chat_input("Write message..?"):

        # Add user message to history with avatar
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "avatar": ":material/person:"
        })



        # Display user message in chat message container
        with st.chat_message("user",avatar=":material/person:"):
            st.markdown(prompt)
    
        # Empty placeholder
        placeholder = st.empty()
    
        # Display user message in chat message container
        with placeholder.chat_message("assistant",avatar=":material/lightbulb:"):
    
            st.markdown('Thinking...')
    
    
    
        # Get the response
        response = get_reponse(prompt.strip(), st.session_state.history[-6:], st.session_state.URL+"/chat")
    
    
        if (response):


            placeholder.empty()
    
            with st.chat_message("assistant",avatar="✨"):
    
                st.markdown(response)



            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

            QA_data = {"user":prompt, "assistant":response}

            st.session_state.database.child("Q_A_EVA").child(st.session_state.unique_id).push(QA_data)


    
        placeholder.empty()

        # Add anchor at the end of page (outside loop)
    st.markdown('<div id="bottom-anchor"></div>', unsafe_allow_html=True)

    components.html(
        """
        <script>
            var element = window.parent.document.getElementById("bottom-anchor");
            if (element) {
                element.scrollIntoView({behavior: "smooth"});
            }
        </script>
        """,
        height=0,
    )




def check_internet():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.RequestException:
        return False



if "server_ok" not in st.session_state:
    try:
        response = requests.get(url=st.session_state.URL.strip(), timeout=5)
        st.session_state.server_ok = response.status_code == 200
    except requests.exceptions.RequestException:
        st.session_state.server_ok = False






if not st.session_state.URL:
  
  print("URL is empty in environment variable")
  
else:

      if not check_internet():

        no_internet("""**⚠️ No Internet Connection Detected**

**EVA** requires an active internet connection to fetch real-time responses and updates.""")
        st.stop()

      else:


            if st.session_state.server_ok:


                ChatUI()


            else:

                no_internet("""EVA is currently unable to reach its server.

               This might be due to:
               - Temporary server maintenance
               - Network issues
               - Incorrect backend URL

               Please try again later or contact support.""")





    
