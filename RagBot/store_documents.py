import os
import chromadb
import fitz  # PyMuPDF for PDFs
import docx
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("industrial-documents")

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Get the absolute path of the documents directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")

# Supported document types
SUPPORTED_EXTENSIONS = (".pdf", ".docx", ".txt")


# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text() + "\n"
    except Exception as e:
        print(f"❌ Error reading PDF {pdf_path}: {e}")
    return text.strip()


# Extract text from DOCX
def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"❌ Error reading DOCX {docx_path}: {e}")
    return text.strip()


# Extract text from TXT
def extract_text_from_txt(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        print(f"❌ Error reading TXT {txt_path}: {e}")
        return ""


# Process all files in the documents directory
def process_documents(directory):
    if not os.path.exists(directory):
        print(f"❌ Error: Directory '{directory}' does not exist.")
        return

    files = [f for f in os.listdir(directory) if f.endswith(SUPPORTED_EXTENSIONS)]

    if not files:
        print("⚠️ No valid documents found in the directory.")
        return

    processed_count = 0

    for filename in files:
        file_path = os.path.join(directory, filename)

        print(f"📂 Processing: {filename}")

        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(file_path)
        elif filename.endswith(".txt"):
            text = extract_text_from_txt(file_path)
        else:
            continue

        if not text:
            print(f"⚠️ Skipping {filename}: No valid text found.")
            continue

        # Generate embeddings
        embedding = model.encode(text).tolist()

        # Store in ChromaDB (Avoid duplicate IDs)
        existing_docs = collection.get(ids=[filename])
        if existing_docs['ids']:
            print(f"⚠️ Skipping {filename}: Already exists in ChromaDB.")
        else:
            collection.add(documents=[text], embeddings=[embedding], ids=[filename])
            print(f"✅ {filename} added to ChromaDB.")

        processed_count += 1

    print(f"\n✅ {processed_count}/{len(files)} documents stored successfully in ChromaDB!")


# Run the document processing
process_documents(DOCUMENTS_DIR)
