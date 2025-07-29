from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from PyPDF2 import PdfReader
import tempfile

def summarizer(pdf_file):
    # Save the uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_path = tmp_file.name

    # Step 1: Load PDF
    reader = PdfReader(tmp_path)
    raw_text = ''
    for page in reader.pages:
        raw_text += page.extract_text() or ''

    # Step 2: Split into chunks
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    texts = text_splitter.split_text(raw_text)

    # Step 3: Embedding
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    docsearch = FAISS.from_texts(texts, embeddings)
    docs = docsearch.similarity_search("Summarize the document", k=3)

    # Step 4: Chat LLM via OpenRouter (GPT-3.5 / GPT-4)
    llm = ChatOpenAI(
        model_name="openai/gpt-3.5-turbo",
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )

    # Step 5: Chain for QA/Summarization
    chain = load_qa_chain(llm, chain_type="stuff")
    result = chain.invoke({
    "input_documents": docs,
    "question": "Please summarize this PDF document in detail."
})
    
    return result
