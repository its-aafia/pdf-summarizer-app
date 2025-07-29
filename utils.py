from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from PyPDF2 import PdfReader
import os
import tempfile

def summarizer(pdf_file):
    # Save uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_path = tmp_file.name

    # Step 1: Read PDF content
    reader = PdfReader(tmp_path)
    raw_text = ''.join(page.extract_text() or '' for page in reader.pages)

    # Step 2: Split into chunks
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(raw_text)

    # Step 3: Convert chunks into embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    docsearch = FAISS.from_texts(texts, embeddings)
    docs = docsearch.similarity_search("Summarize the document", k=3)

    # Step 4: Call GPT model via OpenRouter
    llm = ChatOpenAI(
        model_name="openai/gpt-3.5-turbo",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),  # Must be added in Streamlit secrets
    )

    # Step 5: Generate summary
    chain = load_qa_chain(llm, chain_type="stuff")
    result = chain.invoke({
        "input_documents": docs,
        "question": "Please summarize this PDF document in detail."
    })

    return result
