import os
import json  
import google.generativeai as genai


working_directory= os.path.dirname(os.path.abspath(__file__))

config_file_path=f"{working_directory}/config.json"
config_data=json.load(open(config_file_path))
#loadig api key
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]
print(GOOGLE_API_KEY)


#Conguguring google gen ai with api key
genai.configure(api_key=GOOGLE_API_KEY)

#function to load geminin pro model for the chatbot
def load_gemini_pro_model():
    gemini_pro_model=genai.GenerativeModel("gemini-pro")
    return gemini_pro_model


# Function to load Gemini Pro model for image captioning
def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-1.5-flash")
    response = gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result

#function to get text
def embedding_model_reponse(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model=embedding_model,
                                     content = input_text,
                                     task_type = "retrieval_document",
                                     )
    embedding_list = embedding['embedding']
    return embedding_list


#Function te get respomse from gemini pro 
def gemini_pro_response(user_prompt):
    gemini_pro_model=genai.GenerativeModel("gemini-pro")
    response =gemini_pro_model.generate_content(user_prompt)
    result =  response.text 
    return result

