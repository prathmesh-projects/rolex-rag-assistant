#Importing the needed libraries
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import glob
import os

#RAGBot class 
class RAGBot:
    #Constructor for the same
    def __init__(self):
        #loading API key from .env file
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        os.environ["GOOGLE_API_KEY"] = self.api_key

        #pre-defining the folder path from which documents will be loaded
        self.folder_path = os.getenv("DOCS_FOLDER", "./data")  

        #collecting all files that end with .pdf and .docx
        pdfs = glob.glob(os.path.join(self.folder_path, "*.pdf"))
        docs = glob.glob(os.path.join(self.folder_path, "*.docx"))
        self.file_paths = pdfs + docs

        #Setting up our LLM, Embedding Model and Memory
        self.llm = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        self.embeds = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.memory = ConversationBufferMemory(k=3, return_messages=True, memory_key="chat_history") 
        # K=3 means the model remembers the last three user queries

        #Getting the documents and then spilling them into chunks
        self.docs = self.getting_documents()
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
        self.splitted_docs = self.splitter.split_documents(self.docs)

        print(f"Indexed {len(self.splitted_docs)} chunks from {len(self.docs)} raw documents.")

        #initializing the vector-database and the retriever to get the data
        self.store = Chroma.from_documents(self.splitted_docs, embedding=self.embeds)
        self.retriever = self.store.as_retriever(search_kwargs={"k": 15})

        #defining the prompt, with the fallback strategy
        system_template = """
        You are a helpful assistant answering questions about Rolex watches based on the provided documents.
        Only use information from the context. If unsure, reply: "I don't know. Please ask a relevant question."
        """
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("Context:\n{context}\n\nQuestion: {question}")
        ])

        # Build the conversational RAG chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=False,
            combine_docs_chain_kwargs={"prompt": self.prompt},
            get_chat_history=lambda h: h
        )

    #function to load the documents based on type/extension
    def getting_documents(self):
        docs = []
        for path in self.file_paths:
            if path.endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif path.endswith(".docx"):
                loader = Docx2txtLoader(path)
            else:
                print(f"Skipping unsupported file: {path}")
                continue
            try:
                loaded = loader.load()
                docs.extend(loaded)
            except Exception as e:
                print(f" Failed to load {path}: {e}")
        return docs

    #function to get the response 
    def get_answer(self, query):
        try:
            result = self.chain.invoke({"question": query})
            return result.get("answer", "Something went wrong.")
        except Exception as e:
            return f"Error: {str(e)}"