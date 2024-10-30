import streamlit as st
import os
from src import RAG

if "Next step" not in st.session_state:
    st.session_state["Next step"] = False  

if "Submit" not in st.session_state:
    st.session_state["Submit"] = False  
    

st.title('Documents chat')
st.write('You add to your chat a file PDF, a YouTube video (which will be transcribed) or a webpage link.')
source = st.selectbox('Pick your source',["PDF", "PDF_on_web","YouTube","Web"])
if source == "PDF":
    uploaded_file  = st.file_uploader("Upload your PDF", type="pdf")

        
else:  
    doc = st.text_input("Paste your Link")

if st.button("Next step"):
    st.session_state["Next step"] = True   

if st.session_state["Next step"]:
    if "doc" not in st.session_state and "source" not in st.session_state:
        st.session_state["doc"]=[]
        st.session_state["source"]=[]
    if source == "PDF" and uploaded_file is not None:
    # Define the directory where you want to save the file
        directory = "./temp-dir"
        
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Define the full file path
        file_path = os.path.join(directory, uploaded_file.name)
        
        # Write the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        doc = file_path
    st.session_state["doc"].append(doc)
    st.session_state["source"].append(source)
    if "rag" not in st.session_state:
        st.session_state["rag"] = RAG(doc, source)
    else:
        st.session_state["rag"].add_documents_to_embedding(doc,source)

    
    #  Prompt section
    st.header('Chatbot based on your info')
    prompt = st.text_input("Input your questions here")
    if st.button("Submit"):
        st.session_state["Submit"] = True   
    if st.session_state["Submit"]:
        if "user_prompt_history" not in st.session_state:
            st.session_state["user_prompt_history"]=[]
        if "chat_answers_history" not in st.session_state:
            st.session_state["chat_answers_history"]=[]
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"]=[]

        with st.spinner("Generating......"):
            # Storing the questions, answers and chat history
            if source == 'PDF':
            # After you're done with the file, you can delete it
                os.remove(file_path)
            print('RAG created!')
            history = st.session_state["chat_history"]
            answer = st.session_state["rag"].qa(prompt, chat_history=history)

            st.session_state["chat_answers_history"].append(answer)
            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_history"].append((prompt,answer))

        if st.session_state["chat_answers_history"]:
            for i, j in zip(st.session_state["chat_answers_history"],st.session_state["user_prompt_history"]):
                message1 = st.chat_message("user")
                message1.write(j)
                message2 = st.chat_message("assistant")
                message2.write(i)