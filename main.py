import streamlit as st
import os
from src import RAG

if "Next step" not in st.session_state:
    st.session_state["Next step"] = False  

if "Go" not in st.session_state:
    st.session_state["Go"] = False  

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
    st.text('Now write your prompt.')
    prompt = st.text_input("Input your prompt here")
    if st.button("Go"):
        st.session_state["Go"] = True   
    if st.session_state["Go"]:
        rag = RAG(doc, source)
        if source == 'PDF':
        # After you're done with the file, you can delete it
            os.remove(file_path)
        print('RAG created!')
        answer = rag.qa(prompt)
        st.write(answer)
        