import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceInstructEmbeddings
from dotenv import load_dotenv


def get_pdf_text(pdf_documents):
  text = ""
  for pdf in pdf_documents:
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
      text += page.extract_text()
  return text


def get_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

  
def get_embeddings(text_chunks):

    embeddings = HuggingFaceInstructEmbeddings(model_name="WhereIsAI/UAE-Large-V1")
    # embeddings = OpenAIEmbeddings()
  
    vector_store = FAISS.from_texts(text_chunks, embeddings)
  
    return vector_store


def main():
  load_dotenv()
  st.set_page_config(page_title='Chat Multiple PDFs',page_icon=':books:')
  
  
  with st.sidebar:
    pdf_documents = st.file_uploader('Upload your PDF file', type=['pdf'], accept_multiple_files=True)
  
    if st.button('Process'):
      with st.spinner('Processing...'):
        pdf_text = get_pdf_text(pdf_documents)
        
        text_chunks = get_chunks(pdf_text)
        
        st.session_state.vector_store = get_embeddings(text_chunks)
        
        st.success('Done! You can now ask questions to your PDFs')


  st.title('Chat with Multiple PDFs :books:')
  st.text_input('Ask a question about the PDFs')


if __name__ == '__main__':
    main()