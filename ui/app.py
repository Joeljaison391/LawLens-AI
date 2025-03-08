import streamlit as st
from streamlit_extras.app_logo import add_logo
import time
import base64
from ui.assets.logo import get_logo, get_logo_base64

# Set page config
st.set_page_config(
    page_title="AI Compliance Checker",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to add logo to sidebar
def add_custom_logo():
    # Try to load the image file first
    logo_image = get_logo()
    
    if logo_image is not None:
        # If image file found, display it directly
        st.sidebar.image(logo_image, width=80)
    else:
        # Fallback to the base64 version if image file not found
        logo_base64 = get_logo_base64()
        logo_html = f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{logo_base64}" alt="SoulSync Logo" width="80">
        </div>
        """
        st.sidebar.markdown(logo_html, unsafe_allow_html=True)

# Add logo to sidebar
add_custom_logo()

# Custom Styling with dark theme
st.markdown(
    """
    <style>
        /* Base styles - Dark Theme */
        body {
            background-color: #1a1a1a;
            color: #f0f0f0;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        .main {
            background-color: #1a1a1a;
            padding: 1.5rem;
            border-radius: 10px;
            color: #f0f0f0;
        }
        
        .block-container {
            max-width: 100%;
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        /* Typography */
        .title {
            font-size: 46px;
            font-weight: 800;
            background: linear-gradient(90deg, #3f96e8, #67c0ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .subtitle {
            font-size: 24px;
            color: #b0b0b0;
            margin-bottom: 30px;
            text-align: center;
            font-weight: 400;
        }
        
        /* Buttons */
        .cta-btn {
            background: linear-gradient(90deg, #3f96e8, #67c0ff);
            color: white;
            padding: 15px 30px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 10px rgba(30, 136, 229, 0.3);
            transition: all 0.3s ease;
        }
        
        .cta-btn:hover {
            box-shadow: 0 6px 15px rgba(30, 136, 229, 0.4);
            transform: translateY(-2px);
        }
        
        /* Sections */
        .section {
            background-color: #2a2a2a;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
            border-left: 5px solid #3f96e8;
        }
        
        .section-title {
            font-size: 24px;
            font-weight: 600;
            color: #3f96e8;
            margin-bottom: 15px;
        }
        
        /* Cards for tech stack and features */
        .card-container {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
        }
        
        .card {
            background-color: #2a2a2a;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            flex: 1;
            min-width: 200px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.25);
        }
        
        .card-icon {
            font-size: 30px;
            margin-bottom: 10px;
            color: #3f96e8;
        }
        
        /* Sidebar styling */
        .css-1d391kg, .css-163ttbj, [data-testid="stSidebar"] {
            background-color: #121212;
        }
        
        .css-1d391kg p, .css-163ttbj p, [data-testid="stSidebar"] p {
            color: #f0f0f0;
        }
        
        .css-hxt7ib {
            padding-top: 2rem;
        }
        
        /* Streamlit default element overrides */
        div[data-testid="stToolbar"] {
            display: none;
        }
        
        .stButton button {
            width: 100%;
            background-color: #3f96e8;
            color: white;
            border: none;
        }
        
        .stButton button:hover {
            background-color: #67c0ff;
            color: white;
        }
        
        /* Override standard elements */
        h1, h2, h3, h4, h5, h6 {
            color: #f0f0f0;
        }
        
        p, li, ol, ul {
            color: #d0d0d0;
        }
        
        a {
            color: #3f96e8;
        }
        
        a:hover {
            color: #67c0ff;
        }
        
        /* Dark theme tweaks */
        .stMarkdown {
            color: #d0d0d0;
        }
        
        .css-1kyxreq, .css-12oz5g7 {
            background-color: #2a2a2a;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        
        /* Make column gaps consistent */
        .row-widget {
            padding: 0 5px;
        }
        
        /* Fix for overlapping elements */
        .row-widget > div {
            width: 100%;
        }
        
        .stImage img {
            border-radius: 10px;
            object-fit: cover;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header with enhanced visual appeal
st.markdown('<div class="title">AI-Powered Compliance Checker</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ensuring Industrial Compliance with AI & Regulations</div>', unsafe_allow_html=True)



# About Section with improved styling
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🚀 Project Overview</div>', unsafe_allow_html=True)
st.write(
    "Our platform enables governments to **analyze industrial applications** for compliance with **environmental and regulatory frameworks** using AI-powered technology. We combine advanced AI models with intuitive interfaces to streamline the approval process."
)
st.markdown('</div>', unsafe_allow_html=True)

# Tech Stack Section with cards
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🛠 Tech Stack</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🧠</div>
        <h3>AI Models</h3>
        <p>Mistral-7B, RAG for document retrieval, Fine-tuned for compliance analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">⚙️</div>
        <h3>Backend</h3>
        <p>FastAPI, Python, RESTful services, Async processing</p>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">💾</div>
        <h3>Infrastructure</h3>
        <p>PostgreSQL, Elasticsearch, Docker, Kubernetes</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# How It Works with visual process flow
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔍 How It Works</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <div style="font-size: 36px; color: #3f96e8;">1️⃣</div>
        <p style="font-weight: 600; color: #f0f0f0;">Upload Documents</p>
        <p style="font-size: 14px; color: #b0b0b0;">Upload industrial application documents in PDF or image format</p>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <div style="font-size: 36px; color: #3f96e8;">2️⃣</div>
        <p style="font-weight: 600; color: #f0f0f0;">AI Analysis</p>
        <p style="font-size: 14px; color: #b0b0b0;">Advanced AI models analyze content and extract key compliance data</p>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <div style="font-size: 36px; color: #3f96e8;">3️⃣</div>
        <p style="font-weight: 600; color: #f0f0f0;">Compliance Check</p>
        <p style="font-size: 14px; color: #b0b0b0;">Automated verification against regulatory frameworks</p>
    </div>
    """, unsafe_allow_html=True)
    
with col4:
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <div style="font-size: 36px; color: #3f96e8;">4️⃣</div>
        <p style="font-weight: 600; color: #f0f0f0;">Report Generation</p>
        <p style="font-size: 14px; color: #b0b0b0;">Comprehensive compliance report with actionable insights</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Goals & Impact Section with visual elements
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎯 Goals & Impact</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style="background-color: #1a3a5a; padding: 20px; border-radius: 8px;">
        <h4 style="color: #3f96e8; margin-top: 0;">For Governments</h4>
        <ul style="color: #d0d0d0;">
            <li>Reduce processing time by up to 70%</li>
            <li>Increase accuracy in compliance verification</li>
            <li>Standardize approval processes</li>
            <li>Create transparent audit trails</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div style="background-color: #1a3a32; padding: 20px; border-radius: 8px;">
        <h4 style="color: #4caf50; margin-top: 0;">For Environment</h4>
        <ul style="color: #d0d0d0;">
            <li>Ensure proper environmental standards</li>
            <li>Reduce carbon footprint through efficiency</li>
            <li>Promote sustainable industrial practices</li>
            <li>Enforce regulatory compliance</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Call to Action with enhanced button
st.markdown('<div class="section" style="text-align: center;">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🚀 Experience the Power of AI Compliance</div>', unsafe_allow_html=True)
st.write("Ready to revolutionize how you handle compliance verification?")

# Animated button with hover effect
st.markdown("""
<div style="display: flex; justify-content: center; margin: 30px 0;">
    <button id="cta-button" onclick="document.getElementById('cta-button').classList.add('clicked')" class="cta-btn">
        🔥 Try Now
    </button>
</div>
<script>
    document.getElementById('cta-button').addEventListener('click', function() {
        this.innerHTML = '⏳ Loading...';
    });
</script>
""", unsafe_allow_html=True)

cta = st.button("Start Compliance Analysis", key="demo_button", help="Click to go to the compliance analysis page")
if cta:
    with st.spinner("Launching compliance analyzer..."):
        time.sleep(1)
    st.success("Redirecting to the compliance checker...")
    st.switch_page("pages/Compliance_Analysis.py")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #333;">
    <p style="color: #777; font-size: 14px;">© 2023 AI Compliance Checker | Powered by SoulSync</p>
</div>
""", unsafe_allow_html=True)
