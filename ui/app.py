import streamlit as st
from streamlit_extras.app_logo import add_logo
import time

# Set page config
st.set_page_config(
    page_title="AI Compliance Checker",
    page_icon="⚖️",
    layout="wide"
)

# Custom Styling
st.markdown(
    """
    <style>
        .main { text-align: center; }
        .title { font-size: 40px; font-weight: bold; color: #1E88E5; }
        .subtitle { font-size: 22px; color: #555; }
        .cta-btn { background-color: #1E88E5; color: white; padding: 15px 30px; border-radius: 10px; font-size: 18px; }
        .cta-btn:hover { background-color: #1565C0; }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("<div class='title'>AI-Powered Compliance Checker</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ensuring Industrial Compliance with AI & Regulations</div>", unsafe_allow_html=True)

st.image("https://source.unsplash.com/1200x500/?technology,law", use_column_width=True)

# About Section
st.markdown("### 🚀 Project Overview")
st.write(
    "Our platform enables governments to **analyze industrial applications** for compliance with **environmental and regulatory frameworks** using AI-powered technology."
)

# Tech Stack Section
st.markdown("### 🛠 Tech Stack")
st.write(
    "- **AI Models:** Mistral-7B, RAG for document retrieval"
    "\n- **Backend:** FastAPI, Python"
    "\n- **Frontend:** Streamlit, React (for future expansions)"
    "\n- **Database:** PostgreSQL, Elasticsearch"
    "\n- **Cloud & Hosting:** Docker, Kubernetes"
)

# How It Works
st.markdown("### 🔍 How It Works")
st.write(
    "1️⃣ **Upload an industrial application document** (PDF, text)."
    "\n2️⃣ AI **analyzes the document** and extracts relevant compliance laws."
    "\n3️⃣ **AI-powered chatbot** answers compliance queries."
    "\n4️⃣ Generate a **detailed compliance report**."
)

# Alignment with Goals
st.markdown("### 🎯 Goals & Impact")
st.write(
    "✅ Ensure **compliance with regulations** for industrial applications."
    "\n✅ Reduce **manual effort** with AI-powered automation."
    "\n✅ Help **governments streamline approval processes** efficiently."
)

# Call to Action
st.markdown("### 🚀 Try the Demo")
cta = st.button("🔥 Try Now", key="demo_button")
if cta:
    with st.spinner("Launching demo..."):
        time.sleep(1.5)
    st.success("Redirecting to the compliance checker...")
    st.switch_page("pages/2_📄_Compliance_Analysis.py")
