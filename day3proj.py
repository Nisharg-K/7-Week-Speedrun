import os
import time

# LangChain Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
# ==========================================
# PHASE 1: INGESTION PIPELINE
# ==========================================
def ingest_document(pdf_path: str, persist_dir: str = "./enterprise_db"):
    """Loads a PDF, splits it, and saves it to a local Vector Database."""
    print(f"\nLoading {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    print(f"Splitting {len(docs)} pages into secure chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(docs)
    
    print(f"Embedding {len(chunks)} chunks into ChromaDB (This takes a moment)...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    return vectorstore


#RETRIEVAL & GENERATION

def setup_rag_chain(vectorstore):
    """Wires the database to the LLM with a strict prompt."""
    
  
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    llm = ChatOllama(model="qwen2.5:1.5b", temperature=0)
    
    system_prompt = (
        "You are a highly secure Enterprise Knowledge Assistant. "
        "You must answer the user's question using ONLY the provided context. "
        "If the answer is not contained in the context, you must reply: 'I cannot find the answer in the provided documents.' "
        "Do not guess. Do not use outside knowledge. Keep your answers clear and professional."
        "\n\nContext:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    qa_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, qa_chain)

# INTERACTIVE CHAT LOOP
def main():
    print("=" * 60)
    print("🛡️ SECURE ENTERPRISE KNOWLEDGE BOT (LOCAL RAG)")
    print("=" * 60)
    
    pdf_filename = "sample.pdf"
    db_folder = "./enterprise_db"
    
    if not os.path.exists(pdf_filename):
        print(f"Error: Cannot find '{pdf_filename}'. Please place it in the current folder.")
        return

    # Build or Load the Database
    # (In a real app, you wouldn't ingest the PDF every single time, but we will for this test)
    vectorstore = ingest_document(pdf_filename, db_folder)
    rag_chain = setup_rag_chain(vectorstore)
    
    print("\nSystem Ready. (Type 'quit' to exit)")
    print("-" * 60)
    
    # The Chat Loop
    while True:
        user_query = input("\n🧑‍💻 You: ")
        if user_query.lower() in ['quit', 'exit']:
            print("Shutting down secure session. Goodbye! 👋")
            break
            
        if not user_query.strip():
            continue
            
        print("Bot is searching secure documents...")
        start_time = time.time()
        
        # Invoke the pipeline
        try:
            response = rag_chain.invoke({"input": user_query})
            answer = response["answer"]
            sources = response["context"]
            
            # Print the Answer
            print(f"\n Answer: {answer}")
            
            # Print the Strict Citations
            print("\nSources Cited:")
            # Use a set to remove duplicate page numbers if multiple chunks came from the same page
            pages_used = set(doc.metadata.get('page', 'Unknown') for doc in sources)
            for page in sorted(pages_used):
                print(f"  - Document: {pdf_filename} | Page {page}")
                
            print(f"(Query took {round(time.time() - start_time, 2)} seconds)")
            print("-" * 60)
            
        except Exception as e:
            print(f"\nPipeline Error: {e}")

if __name__ == "__main__":
    main()