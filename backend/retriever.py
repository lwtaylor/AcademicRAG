from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI # from langchain_openai import OpenAI  
from langchain.chains import RetrievalQA

import os
from dotenv import load_dotenv, dotenv_values

# Load the environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv('OPEN_AI_KEY')

persist_directory =  'backend/vector_db'
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Load the persisted database from disk. 
# chroma will create a new empty database if the directory does not exist!
vectordb = Chroma(persist_directory=persist_directory, 
                  embedding_function=embedding)

# Make a retriever for
retriever = vectordb.as_retriever()


# trying out chat openai
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2, 
    api_key= OPENAI_API_KEY  # if you prefer to pass api key in directly instaed of using env vars
    # base_url="...",
    # organization="...",
    # other params...
)
# create the chain to answer questions 
# include verbose=True for more information on what the chain is doing
qa_chain = RetrievalQA.from_chain_type(llm=llm, 
                                  chain_type="stuff", 
                                  retriever=retriever, 
                                  return_source_documents=True,
                                  verbose=True)

## Process LLM response and cite sources
def process_llm_response(llm_response):
    final_response = llm_response['result']
    final_response += '\n\nSources:'
    print(llm_response)
    for source in llm_response["source_documents"]:
        final_response += f"\n {source.metadata['source']}"
    return final_response
        
# Final Response
def llm_answer(query):
    llm_response = qa_chain(query)
    final_response = process_llm_response(llm_response)
    return final_response

# test llm answer directly
#llm_answer("What are some linguistics introductory courses?")