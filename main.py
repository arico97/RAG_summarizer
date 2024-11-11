import streamlit as st
import os

import requests

from src import ChatTextGenerator

API_URL = "http://127.0.0.1:8000/"

sources = ["pdf", "epub", "PDF from web","YouTube","Web"]

# Define the directory where you want to save the file
temp_dir = "./temp-dir"

if "Add source" not in st.session_state:
    st.session_state["Add source"] = False  
    

st.title('Documents chat')
st.write('You can add to your chat a file PDF, an epub file, a YouTube video (which will be transcribed) or a webpage link.')
source = st.selectbox('Pick your source', sources)
if source in {"pdf","epub"}:
    uploaded_file  = st.file_uploader("Upload your file", type=source)    
else:  
    doc = st.text_input("Paste your Link")

if st.button("Add source"): #try to set n_sources
    st.session_state["Add source"] = True   

if st.session_state["Add source"]: 
    if source in {"pdf","epub"} and uploaded_file is not None:
        
        # Create the directory if it doesn't exist
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # Define the full file path
        file_path = os.path.join(temp_dir, uploaded_file.name)
        st.session_state["file_path"] = file_path
        # Write the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        doc = file_path

    if "rag" not in st.session_state:
        endpoint = 'initialize-rag/'
        st.session_state["rag"] = True
        url = API_URL+endpoint
        payload = {"source_type":source, "documents":doc}
        requests.post(url=url, json = payload)
        st.session_state["Add source"] = False  
        st.session_state["source"] = source
    else:
        endpoint = 'add-documents/'
        url = API_URL + endpoint
        payload = {"source_type": source, "documents": doc}
        requests.post(url=url, json = payload)
        st.session_state["Add source"] = False  
        st.session_state["source"] = source

if "rag" in st.session_state:
    #  Prompt section
    st.header('Chatbot based on your info')
    prompt = st.chat_input("Input your questions here")
    if prompt:
        if "user_prompt_history" not in st.session_state:
            st.session_state["user_prompt_history"]=[]
        if "chat_answers_history" not in st.session_state:
            st.session_state["chat_answers_history"]=[]
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"]=[{"prompt":"","answer":""}]

        with st.spinner("Generating......"):
            # Storing the questions, answers and chat history
            if st.session_state["source"] in {"pdf","epub"}:
            # After you're done with the file, you can delete it
                os.remove(st.session_state["file_path"])
                st.session_state["source"] = None
                st.session_state["file_path"] = None
            history = st.session_state["chat_history"]
            endpoint = 'answer/'
            url = API_URL + endpoint
            payload = {"query": prompt, "chat_history": history}
            answer = requests.post(url=url, json = payload).json()
            st.session_state["chat_answers_history"].append(answer["answer"])
            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_history"].append({"prompt":prompt,"answer":answer["answer"]})

        if st.session_state["chat_answers_history"]:
            for i, j in zip(st.session_state["chat_answers_history"],st.session_state["user_prompt_history"]):
                message1 = st.chat_message("user")
                message1.write(j)
                message2 = st.chat_message("assistant")
                message2.write(i)

    st.header('Download conversation')
    if st.button("Generate and download chat"):
        generator = ChatTextGenerator()
        text_data = generator.generate_chat_text(st.session_state["chat_history"])
        st.write('You can download in .txt the chat conversation that you have already had.')
        # Descarga del PDF
        st.download_button(
            label="Download conversation in txt",
            data=text_data,
            file_name="chat_conversation.txt"
        )
