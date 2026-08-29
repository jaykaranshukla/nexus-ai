import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")       # if using ChromaDB Cloud
CHROMA_TENANT  = os.getenv("CHROMA_TENANT", "default_tenant")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE", "default_database")

# --- Embeddings ---
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)


# --- Vector Store (local persistent — swap for Cloud client if needed) ---

chroma_client = chromadb.HttpClient(
    ssl=True,
    host=os.getenv("CHROMA_HOST"),
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE"),
    headers={"x-chroma-token": os.getenv("CHROMA_API_KEY")}
)

vectorstore = Chroma(
    client=chroma_client,
    collection_name="rag_collection",
    embedding_function=embeddings,
)

# --- LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3,
    convert_system_message_to_human=True,
)

# --- Text Splitter ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

SYSTEM_PROMPT = """You are a helpful assistant that answers questions strictly based on the provided document context.
If the answer is not found in the context, say: "I could not find this information in the provided documents."
Do not use any outside knowledge. Be concise and accurate."""


def ingest_pdf(file_path: str) -> int:
    """Load a PDF, split it, embed and store in ChromaDB. Returns chunk count."""
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    chunks = text_splitter.split_documents(documents)
    vectorstore.add_documents(chunks)
    return len(chunks)


def retrieve_context(query: str, k: int = 4) -> str:
    """Similarity search — returns top-k chunks as a single string."""
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])


def docu_chat(query: str) -> str:
    context = retrieve_context(query)
    prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {query}"
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content
    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict) and "text" in block:
                text_parts.append(block["text"])
            elif isinstance(block, str):
                text_parts.append(block)
        return " ".join(text_parts)
    return str(content)