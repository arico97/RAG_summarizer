'''Frontend of the chatbot without backend integration'''

import streamlit as st
import os
from src import RAG
import logging 

logging.basicConfig(level=logging.INFO) 

directory = "./temp-dir"

if "Add source" not in st.session_state:
    st.session_state["Add source"] = False  
    

st.title('Documents chat')
st.write('You add to your chat a file PDF, a YouTube video (which will be transcribed) or a webpage link.')
source = st.selectbox('Pick your source',["pdf", "PDF_on_web","YouTube","Web"])
if source in {"pdf","epub"}:
    uploaded_file  = st.file_uploader("Upload your PDF", type="pdf")    
    logging.info("Uploaded file")
else:  
    doc = st.text_input("Paste your Link")

if st.button("Add source"): #try to set n_sources
    st.session_state["Add source"] = True   

if st.session_state["Add source"]: 
    if source in {"pdf","epub"} and uploaded_file is not None:
    # Define the directory where you want to save the file
        
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Define the full file path
        file_path = os.path.join(directory, uploaded_file.name)
        st.session_state["file_path"] = file_path
        # Write the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        doc = file_path
        logging.info(doc in globals())
    if doc in globals():
        if "rag" not in st.session_state: # falta que haya un doc en session state
            st.session_state["rag"] = RAG(document=doc, source=source)
            st.session_state["Add source"] = False  
            st.session_state["source"] = source
        else:
            st.session_state["rag"].add_documents_to_embedding(doc,source)
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
            st.session_state["chat_history"]=[]

        with st.spinner("Generating......"):
            # Storing the questions, answers and chat history
    #        logging.info("The current source is")
    #        logging.info(st.session_state["source"])
            if st.session_state["source"] == 'pdf':
            # After you're done with the file, you can delete it
                os.remove(st.session_state["file_path"])
                st.session_state["source"] = None
                st.session_state["file_path"] = None
     #           logging.info(st.session_state["source"])
      #      logging.info('RAG created!')
            history = st.session_state["chat_history"]
            answer =  st.session_state["rag"].invoke_answer(my_prompt=prompt, chat_history=history)

            st.session_state["chat_answers_history"].append(answer)
            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_history"].append((prompt,answer))

        if st.session_state["chat_answers_history"]:
            for i, j in zip(st.session_state["chat_answers_history"],st.session_state["user_prompt_history"]):
                message1 = st.chat_message("user")
                message1.write(j)
                message2 = st.chat_message("assistant")
                message2.write(i)
    