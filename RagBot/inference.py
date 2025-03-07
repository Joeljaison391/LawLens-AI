import json
import chromadb
import requests
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./db")
collection = client.get_collection("industrial-documents")

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load Industrial Approval Application JSON
with open("industrial_application.json", "r") as file:
    application_details = json.load(file)

# Convert JSON to a structured text prompt for vector retrieval
query_text = f"""
Industry Name: {application_details['industry_name']}
Square Feet: {application_details['square_feet']}
Water Source: {application_details['water_source']}
Drainage: {application_details['drainage']}
Air Pollution: {application_details['air_pollution']}
Waste Management: {application_details['waste_management']}
Nearby Homes: {application_details['nearby_homes']}
Water Level Depth: {application_details['water_level_depth']}
"""

# Convert to vector embedding
query_embedding = model.encode(query_text).tolist()

# Query ChromaDB for the most relevant compliance rules
results = collection.query(query_embeddings=[query_embedding], n_results=5)

# Extract retrieved compliance rules
relevant_rules = results["documents"][0] if results["documents"] else []

print("\n🔹 **Top Relevant Compliance Rules from ChromaDB:**\n")
for rule in relevant_rules:
    print(f"- {rule}")

# Generate Compliance Report using Mistral-7B
def generate_compliance_report(application_details, rules):
    messages = [
        {"role": "system", "content": "You are an AI expert in industrial compliance. Analyze the given industrial application."},
        {"role": "user", "content": f"""
        Industrial Compliance Report:

        - **Industry Name:** {application_details['industry_name']}
        - **Square Footage:** {application_details['square_feet']} sq. ft.
        - **Water Source:** {application_details['water_source']}
        - **Drainage System:** {application_details['drainage']}
        - **Air Pollution:** {application_details['air_pollution']}
        - **Waste Management:** {application_details['waste_management']}
        - **Nearby Homes:** {application_details['nearby_homes']}
        - **Water Level Depth:** {application_details['water_level_depth']}

        **Top Relevant Compliance Rules from ChromaDB:**
        {rules}

        **Task:**  
        1. Analyze whether the industrial application follows these compliance rules.
        2. Identify any potential violations.
        3. Highlight environmental concerns.
        4. Recommend corrective actions if necessary.
        5. Provide a final approval decision (Approve/Reject/Needs Review).

        **Provide a structured and concise response.**
        """}
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
        print(f"❌ Error parsing AI response: {e}")
        return "⚠️ AI Response Error."

# Call AI Model for Compliance Report
report = generate_compliance_report(application_details, relevant_rules)

print("\n🔹 **Generated Compliance Report:**\n", report)
