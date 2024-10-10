'''test the chroma backend'''


# import
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter

# load the document and split it into chunks
loader = TextLoader("../text_files/Linguistics_Courses.txt")
documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# load it into Chroma
db = Chroma.from_documents(docs, embedding_function)

# query it
query = "What linguistics courses are about memes?"
docs = db.similarity_search(query)

# print results
print('CHUNK 0\n')
print(docs[0].page_content)
print('CHUNK 1\n')
print(docs[1].page_content)
print('CHUNK 2\n')
print(docs[2].page_content)
print('CHUNK 3\n')
print(docs[3].page_content)