import os
from dotenv import load_dotenv

import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_TENANT", "default_tenant")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE", "default_database")

# --- Embeddings (Google, no local model — keeps memory usage low) ---
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY,
)

# --- ChromaDB Cloud client (official CloudClient — matches server protocol) ---
chroma_client = chromadb.CloudClient(
    tenant=CHROMA_TENANT,
    database=CHROMA_DATABASE,
    api_key=CHROMA_API_KEY,
)

collection = chroma_client.get_or_create_collection(name="rag_collection")

# --- LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
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

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    ids = [f"{os.path.basename(file_path)}-{i}" for i in range(len(chunks))]

    vectors = embeddings.embed_documents(texts)

    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=texts,
        metadatas=metadatas,
    )
    return len(chunks)


def retrieve_context(query: str, k: int = 4) -> str:
    """Similarity search — returns top-k chunks as a single string."""
    query_vector = embeddings.embed_query(query)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k,
    )
    documents = results.get("documents", [[]])[0]
    return "\n\n".join(documents)


def docu_chat(query: str) -> str:
    """Retrieve context and generate a grounded answer."""
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