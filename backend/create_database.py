from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader

import os
from dotenv import load_dotenv, dotenv_values

# Load the environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv('OPEN_AI_KEY')

# Load the Documents
loader = DirectoryLoader('../text_files/', glob="./*.txt", loader_cls=TextLoader)
documents = loader.load()

# Split the text
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk
persist_directory = 'vector_db'

# OpenAI Embeddings to embed the words
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Create vector database
vectordb = Chroma.from_documents(documents=texts, 
                                 embedding=embedding,
                                 persist_directory=persist_directory)

#vectordb.persist() persist is deprecated, automatically persists now
vectordb = None