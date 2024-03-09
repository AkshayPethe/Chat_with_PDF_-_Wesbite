from langchain_community.chat_models import ChatOpenAI
import streamlit as st
from DS_Modules.pdf_reader import Pdf_Reader
from langchain_core.messages import AIMessage, HumanMessage
from DS_Modules.websiteparse import  get_text_for_url
from DS_Modules.vectorstore import vectorstore_pdf, vectorstore_url
from dotenv import load_env






def get_response(user_input):
    return "I dont Know"

def main():
    load_env()
    # App config
    st.set_page_config(page_title="Chat with PDF and Websites")
    st.title("Chat with Websites and PDFs")
   
   

    choice = st.sidebar.selectbox("Choose your option:", ("Upload PDF", "Website URL"))
    
    # Sidebar
    with st.sidebar:
        if choice == "Upload PDF":
            pdf_docs = st.file_uploader("Choose a PDF file", type="pdf")
            st.write("Successfully uploaded PDF!")
            process_pdf = st.button("Process PDF")
            if process_pdf:
                with st.spinner("Processing.Please Wait..."):
                    vector_store_pdf = vectorstore_pdf(pdf_docs)
                    st.success(vector_store_pdf)
                    st.button("Processing Done.Please Ask Question Now (Click to hide)", key="processed_button")
                    

        elif choice == "Website URL":
            website_url = st.text_input("Enter Website URL")
            process_url = st.button("Extract from Website")
            if process_url:
                with st.spinner("Processing.Please Wait..."):
                    vector_store_url = vectorstore_url(website_url)
                    st.success(vector_store_url)
                    st.button("Processing Done.Please Ask Question Now (Click to hide)", key="processed_button")
                    

            elif website_url is None or website_url=="":
                st.info("Please Enter Website URL")
                # Use libraries like requests and beautifulsoup4 to access website content

    
    user_query = st.chat_input("Please Enter your Question Here")
    if user_query is not None and user_query!="":
        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

    #Basically when not in session we will roll back to AI Initial Message
    if "chat_history" not in st.session_state:
        st.session_state.chat_history= [
            AIMessage(content="Hello,How can I help you?")
        ]
    
    #Conversation Chain    
    for message in st.session_state.chat_history:
        if isinstance(message,AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)

        elif isinstance(message,HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

     
           
if __name__ == "__main__":
    main()




                 


