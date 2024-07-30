import os
import streamlit as st 
from streamlit_option_menu import option_menu


from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_vision_response,
                            embedding_model_reponse,
                            gemini_pro_response)
from PIL import Image

working_directory= os.path.dirname(os.path.abspath(__file__))
print(working_directory)
#page configuration

st.set_page_config(
    page_title = "Gemini AI",
    page_icon = "🧠",
    layout='centered'
)
with st.sidebar:
    selected = option_menu(menu_title='Gemini AI',
                           options=['ChatBot',
                           'Image Captioning',
                           'Embed Text',
                           'Ask me anything'],
                           menu_icon = 'robot',
                           icons=['chats-dot-fill','image-fill','textarea-t','patch-question-fill'],
                           default_index=0)
    
#function to translate terminolgy between gemini pro and streamlit

def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role

if selected == 'ChatBot':
    model = load_gemini_pro_model()
    #initalize chat session in streamlit if not allready present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    #streamlit page title
    st.title('🤖ChatBot')

    #TO DISPLAY CHAT HISTORY
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    #input filed for user meassage
    user_prompt=st.chat_input("Ask Gemin Pro..")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response =st.session_state.chat_session.send_message(user_prompt)

        #display gemini response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


#Image Captioning 
if selected == 'Image Captioning':
    st.title("📸Snap Narate")

    uploaded_image = st.file_uploader("Upload an image...",type=["jpg","jpeg","png"])
    if st.button("Generate Caption"):
        # Open the image
        image = Image.open(uploaded_image)

        col1,col2 = st.columns(2)
        with col1:
            resized_image = image.resize((800,500))
            st.image(resized_image)
        defualt_prompt = "Write a short caption for this image"

        # Get the caption output from model 
        caption = gemini_pro_vision_response(defualt_prompt, image)
        with col2:
            st.info(caption)


#text embedding text
if selected == 'Embed Text':
    st.title("🔠Embed Text")
    #input text box
    input_text=st.text_area(label="",placeholder="Enter the text to get embeddings")

    if st.button("Get Embedding"):
        response= embedding_model_reponse(input_text)
        st.markdown(response)

#ask me question
if selected == 'Ask me anything':
    st.title("❓Ask me Question")
    #textbox to enter the prompt
    user_prompt = st.text_area(label="",placeholder="Ask me Anything !")
    if st.button("Get an Answer"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)