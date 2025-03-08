from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import chromadb
import requests
from sentence_transformers import SentenceTransformer

app = FastAPI()

# ----------------------------
# ChromaDB and Model Setup
# ----------------------------

# Initialize ChromaDB client and retrieve (or create) the collection
client = chromadb.PersistentClient(path="./db")
try:
    collection = client.get_collection("industrial-documents")
except Exception:
    # If collection doesn't exist, create it
    collection = client.create_collection("industrial-documents")
print("Collection 'industrial-documents' is available.")

# Load the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# Pydantic Model for Report Request
# ----------------------------
class IndustrialApplication(BaseModel):
    industry_name: str
    square_feet: str
    water_source: str
    drainage: str
    air_pollution: str
    waste_management: str
    nearby_homes: str
    water_level_depth: str

# ----------------------------
# Pydantic Models for Chat
# ----------------------------
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# ----------------------------
# Compliance Report Generation Functions
# ----------------------------
def generate_compliance_report_inner(application_details: dict, rules: list) -> str:
    """
    Generate a compliance report using the Mistral-7B model based on the provided industrial
    application details and retrieved compliance rules.
    """
    messages = [
        {
            "role": "system",
            "content": "You are an AI expert in industrial compliance. Analyze the given industrial application."
        },
        {
            "role": "user",
            "content": f"""
Industrial Compliance Report:

- **Industry Name:** {application_details.get('industry_name', 'N/A')}
- **Square Footage:** {application_details.get('square_feet', 'N/A')} sq. ft.
- **Water Source:** {application_details.get('water_source', 'N/A')}
- **Drainage System:** {application_details.get('drainage', 'N/A')}
- **Air Pollution:** {application_details.get('air_pollution', 'N/A')}
- **Waste Management:** {application_details.get('waste_management', 'N/A')}
- **Nearby Homes:** {application_details.get('nearby_homes', 'N/A')}
- **Water Level Depth:** {application_details.get('water_level_depth', 'N/A')}

**Top Relevant Compliance Rules from ChromaDB:**
{rules}

**Task:**  
1. Analyze whether the industrial application follows these compliance rules.
2. Identify any potential violations.
3. Highlight environmental concerns.
4. Recommend corrective actions if necessary.
5. Provide a final approval decision (Approve/Reject/Needs Review).

**Provide a structured and concise response.**
"""
        }
    ]
    payload = {
        "model": "amethyst-13b-mistral",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",  # Mistral-7B API endpoint
        headers=headers,
        json=payload
    )
    try:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "⚠️ AI Response Error.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing AI response: {e}")

def generate_industrial_compliance_report(industry_details: dict) -> str:
    """
    Given industrial application details, perform retrieval to find relevant compliance rules
    from ChromaDB and generate a compliance report using the Mistral-7B model.
    """
    query_text = f"""
Industry Name: {industry_details.get('industry_name', 'N/A')}
Square Feet: {industry_details.get('square_feet', 'N/A')}
Water Source: {industry_details.get('water_source', 'N/A')}
Drainage: {industry_details.get('drainage', 'N/A')}
Air Pollution: {industry_details.get('air_pollution', 'N/A')}
Waste Management: {industry_details.get('waste_management', 'N/A')}
Nearby Homes: {industry_details.get('nearby_homes', 'N/A')}
Water Level Depth: {industry_details.get('water_level_depth', 'N/A')}
"""
    query_embedding = model.encode(query_text).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    relevant_rules = results.get("documents", [[]])[0]
    print("\n🔹 **Top Relevant Compliance Rules from ChromaDB:**\n")
    for rule in relevant_rules:
        print(f"- {rule}")
    report = generate_compliance_report_inner(industry_details, relevant_rules)
    return report

# ----------------------------
# FastAPI Endpoints
# ----------------------------

@app.post("/generate_report")
def generate_report(app_details: IndustrialApplication):
    """
    Expects an industrial application JSON in the request body and returns a compliance report.
    """
    try:
        industry_details = app_details.dict()
        report = generate_industrial_compliance_report(industry_details)
        return {"compliance_report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
def chat_endpoint(chat_req: ChatRequest):
    """
    Expects a JSON request with a list of chat messages (conversation history)
    and returns the AI's reply. The conversation history is used as context.
    """
    payload = {
        "model": "amethyst-13b-mistral",
        "messages": [msg.dict() for msg in chat_req.messages],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post("http://localhost:1234/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            chat_reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No reply received.")
            return {"message": chat_reply}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling chat API: {e}")

# ----------------------------
# Auto-run Server When File is Executed
# ----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
