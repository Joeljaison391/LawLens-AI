import streamlit as st
import time
import json
import sys
import os
import tempfile
from PIL import Image
import requests
import base64
from ui.assets.logo import get_logo, get_logo_base64

# Ensure the root directory (SoulSync) is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Import the necessary functions
from ui.document_analysis.analysis import extract_text_from_image, analyze_text_with_lm_studio
from ui.document_analysis.area_calculator import cal_blueprint
from ui.document_analysis.employeeCount import extract_employee_count_from_pdf
from ui.document_analysis.energyConsumption import extract_power_consumption_from_pdf


# Set page config
st.set_page_config(
    page_title="AI Compliance Checker",
    page_icon="⚖️",
    layout="wide"
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

# Custom CSS for an enhanced modern dark UI
st.markdown("""
    <style>
    /* Base Styles */
    body {
        background-color: #1a1a1a;
        font-family: 'Segoe UI', Arial, sans-serif;
        color: #f0f0f0;
    }

    /* Typography */
    .title {
        font-size: 2.8em;
        font-weight: 800;
        background: linear-gradient(90deg, #3f96e8, #67c0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2em;
        text-align: center;
    }

    .subtitle {
        font-size: 1.3em;
        color: #b0b0b0;
        margin-bottom: 1.5em;
        text-align: center;
        font-weight: 400;
    }

    /* Cards and Containers */
    .card {
        background-color: #2a2a2a;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        margin-bottom: 20px;
        border-left: 5px solid #3f96e8;
    }

    .card-header {
        font-size: 1.4em;
        font-weight: 600;
        color: #3f96e8;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .card-header-icon {
        font-size: 1.6em;
        color: #3f96e8;
    }

    /* Process Steps */
    .step-container {
        position: relative;
        padding: 15px;
        background-color: #2a2a2a;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .step-container.active {
        border-left: 5px solid #4CAF50;
        background-color: #2a3a2a;
    }
    
    .step-container.inactive {
        opacity: 0.7;
    }
    
    .step-number {
        display: inline-block;
        width: 35px;
        height: 35px;
        line-height: 35px;
        text-align: center;
        background-color: #3f96e8;
        color: white;
        border-radius: 50%;
        font-weight: bold;
        margin-right: 10px;
    }
    
    .step-title {
        display: inline-block;
        font-size: 1.2em;
        font-weight: 600;
        color: #f0f0f0;
        vertical-align: middle;
    }
    
    /* File Upload Styling */
    [data-testid="stFileUploader"] {
        border: 2px dashed #3f96e8;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #1f2937;
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(90deg, #3f96e8, #67c0ff);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(30, 136, 229, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        box-shadow: 0 6px 15px rgba(30, 136, 229, 0.4);
        transform: translateY(-2px);
    }
    
    /* Progress Bar */
    .progress-container {
        margin: 30px 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
    
    .progress-description {
        font-weight: 600;
        color: #f0f0f0;
    }
    
    .progress-percentage {
        color: #3f96e8;
        font-weight: 600;
    }
    
    /* Debug Log */
    .debug {
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        background-color: #1a1a1a;
        color: #00ff00;
        padding: 12px;
        border-radius: 5px;
        white-space: pre-wrap;
        margin-top: 5px;
        border-left: 3px solid #00cc00;
    }
    
    /* Document Preview */
    .document-preview {
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        background-color: #1f2937;
    }
    
    /* Results display */
    .result-success {
        background-color: #1a3a2a;
        color: #4caf50;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #4caf50;
    }
    
    .result-warning {
        background-color: #3a3a1a;
        color: #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #ffc107;
    }
    
    .result-error {
        background-color: #3a1a1a;
        color: #f44336;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #f44336;
    }
    
    /* JSON Display */
    pre {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 5px;
        padding: 15px;
        white-space: pre-wrap;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        max-height: 300px;
        overflow-y: auto;
        color: #67c0ff;
    }
    
    /* Spinner Customization */
    .stSpinner > div > div {
        border-top-color: #3f96e8 !important;
    }
    
    /* Sidebar customization */
    .css-1d391kg, .css-163ttbj, [data-testid="stSidebar"] {
        background-color: #121212;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #2a2a2a;
        border-radius: 4px 4px 0 0;
        color: #b0b0b0;
        padding: 0 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #3f96e8;
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
    
    /* Fix for overlapping elements */
    .row-widget > div {
        width: 100%;
    }
    
    /* Table styles */
    .table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .table th, .table td {
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #333;
    }
    
    .table th {
        background-color: #1f2937;
        color: #3f96e8;
    }
    
    .table tr:hover {
        background-color: #1f2937;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2a2a2a;
        color: #f0f0f0;
        border-radius: 4px;
    }
    
    .streamlit-expanderContent {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-top: none;
        border-radius: 0 0 4px 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Define session state for step tracking and debugging
if "step" not in st.session_state:
    st.session_state.step = 1
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "proof_uploaded" not in st.session_state:
    st.session_state.proof_uploaded = None
if "verification_result" not in st.session_state:
    st.session_state.verification_result = None
if "debug_logs" not in st.session_state:
    st.session_state.debug_logs = {}
if "compliance_report" not in st.session_state:
    st.session_state.compliance_report = None

def log_debug(message):
    st.session_state.debug_logs.setdefault("logs", []).append(message)
    st.write(f"<div class='debug'>DEBUG: {message}</div>", unsafe_allow_html=True)

# Display header with improved design
st.markdown("<div class='title'>AI-Powered Compliance Checker</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ensuring Industrial Compliance with AI & Regulations</div>", unsafe_allow_html=True)



# Create an enhanced progress indicator
total_steps = 7
progress_percentage = int((st.session_state.step / total_steps) * 100)

st.markdown("""
    <div class="progress-container">
        <div class="progress-label">
            <div class="progress-description">Progress: Step {step} of {total}</div>
            <div class="progress-percentage">{percentage}%</div>
        </div>
    </div>
""".format(step=st.session_state.step, total=total_steps, percentage=progress_percentage), unsafe_allow_html=True)

progress_bar = st.progress(progress_percentage/100)

# Create tabs for main process, debug logs, and help
tab1, tab2, tab3 = st.tabs(["📋 Compliance Process", "🔍 Debug Logs", "❓ Help & Info"])

with tab1:
    # Step 1: Upload Document - enhanced with styling
    if st.session_state.step == 1:
        st.markdown("""
            <div class="card">
                <div class="card-header">
                    <span class="card-header-icon">📄</span>
                    <span>Step 1: Upload Your Document</span>
                </div>
                <p>Upload your industrial application document for compliance analysis. Our AI will analyze the content and extract relevant information.</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a PDF or Image file", type=["pdf", "png", "jpg", "jpeg"],
                                      help="Upload the industrial application document you want to analyze")
                                      
        st.markdown("""
            <div style="background-color: #1f2937; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <h4 style="color: #3f96e8; margin-top: 0;">📌 Document Requirements</h4>
                <ul>
                    <li>File must be in PDF, PNG, or JPG format</li>
                    <li>File size should be under 10MB</li>
                    <li>Document should contain legible text</li>
                    <li>Include blueprints or floor plans if available</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        if uploaded_file:
            log_debug("File uploaded: " + uploaded_file.name)
            st.session_state.uploaded_file = uploaded_file
            
            # Success message with enhanced styling
            st.markdown("""
                <div class="result-success">
                    <h4 style="margin-top: 0;">✅ Upload Successful</h4>
                    <p>Your file has been successfully uploaded. Proceeding to analysis...</p>
                </div>
            """, unsafe_allow_html=True)

            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                temp_file_path = temp_file.name
            log_debug(f"Saved file to temporary location: {temp_file_path}")

            # Determine file type and show a preview
            file_extension = uploaded_file.name.split(".")[-1].lower()
            log_debug(f"File extension: {file_extension}")
            
            # Show document preview
            st.markdown("<div class='card-header'>Document Preview</div>", unsafe_allow_html=True)
            if file_extension in ["jpg", "jpeg", "png"]:
                st.image(uploaded_file, width=400, caption="Uploaded Document")
            else:
                st.markdown("PDF preview not available. Processing the document...")

            # Analysis progress
            with st.spinner("Extracting text from document..."):
                try:
                    if file_extension == "pdf":
                        log_debug("Calling extract_text_from_pdf")
                        response = extract_text_from_image(temp_file_path)
                    else:
                        log_debug("Calling extract_text_from_image")
                        response = extract_text_from_image(temp_file_path)
                    log_debug(f"Extracted text/analysis response: {response}")

                    st.session_state.analysis_result = response
                    st.session_state.step = 2
                    progress_percentage = int((st.session_state.step / total_steps) * 100)
                    progress_bar.progress(progress_percentage/100)
                    
                    # Force rerun to show the next step
                    st.experimental_rerun()
                except Exception as e:
                    st.markdown(f"""
                        <div class="result-error">
                            <h4 style="margin-top: 0;">❌ Error During Analysis</h4>
                            <p>There was an error processing your document: {str(e)}</p>
                            <p>Please try uploading a different document or contact support.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    log_debug("Error during text extraction: " + str(e))
                    st.session_state.uploaded_file = None  # Reset upload

    # Step 2: Document Analysis - enhanced with card styling and progress indicators
    if st.session_state.step == 2:
        st.markdown("""
            <div class="card">
                <div class="card-header">
                    <span class="card-header-icon">🔍</span>
                    <span>Step 2: AI Analysis In Progress</span>
                </div>
                <p>Our AI is analyzing your document for compliance requirements and extracting key information.</p>
            </div>
        """, unsafe_allow_html=True)

        with st.spinner("Analyzing document with advanced AI..."):
            try:
                log_debug("Starting AI analysis with LM Studio")
                
                # Show animated processing indicator
                st.markdown("""
                    <div style="text-align: center; margin: 30px 0;">
                        <div style="display: inline-block; width: 50px; height: 50px; border: 5px solid #333; border-top: 5px solid #3f96e8; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                        <style>
                            @keyframes spin {
                                0% { transform: rotate(0deg); }
                                100% { transform: rotate(360deg); }
                            }
                        </style>
                        <p style="margin-top: 15px; color: #b0b0b0;">AI analysis in progress. This might take a minute...</p>
                    </div>
                """, unsafe_allow_html=True)
                
                structured_response = analyze_text_with_lm_studio(st.session_state.analysis_result)
                log_debug(f"AI analysis structured response: {structured_response}")

                if structured_response:
                    st.session_state.analysis_result = structured_response  # Store structured JSON
                    
                    # Success message with enhanced styling
                    st.markdown("""
                        <div class="result-success">
                            <h4 style="margin-top: 0;">✅ Analysis Complete</h4>
                            <p>The AI has successfully analyzed your document and extracted key information.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display results in a visually appealing way
                    st.markdown("<div class='card-header'>Extracted Information</div>", unsafe_allow_html=True)
                    
                    # Convert the JSON to a more readable format
                    if isinstance(structured_response, dict):
                        col1, col2 = st.columns(2)
                        
                        # Check for common keys in compliance documents
                        with col1:
                            st.markdown("<div style='background-color: #1f2937; padding: 15px; border-radius: 8px;'>", unsafe_allow_html=True)
                            st.markdown("#### 📋 Document Overview")
                            if "project_name" in structured_response:
                                st.markdown(f"**Project Name:** {structured_response.get('project_name', 'N/A')}")
                            if "company" in structured_response:
                                st.markdown(f"**Company:** {structured_response.get('company', 'N/A')}")
                            if "location" in structured_response:
                                st.markdown(f"**Location:** {structured_response.get('location', 'N/A')}")
                            if "document_type" in structured_response:
                                st.markdown(f"**Document Type:** {structured_response.get('document_type', 'N/A')}")
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                        with col2:
                            st.markdown("<div style='background-color: #1f2937; padding: 15px; border-radius: 8px;'>", unsafe_allow_html=True)
                            st.markdown("#### 📊 Key Metrics")
                            if "area" in structured_response:
                                st.markdown(f"**Floor Area:** {structured_response.get('area', 'N/A')} sq.m")
                            if "employee_count" in structured_response:
                                st.markdown(f"**Employee Count:** {structured_response.get('employee_count', 'N/A')}")
                            if "energy_consumption" in structured_response:
                                st.markdown(f"**Energy Consumption:** {structured_response.get('energy_consumption', 'N/A')} kWh")
                            if "waste_generation" in structured_response:
                                st.markdown(f"**Waste Generation:** {structured_response.get('waste_generation', 'N/A')} tons/year")
                            st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Display full JSON in a collapsible section
                    with st.expander("View Complete Analysis Data"):
                        st.json(st.session_state.analysis_result)

                    # Enhanced button styling
                    st.markdown("""
                        <div style="text-align: center; margin-top: 30px;">
                            <p style="margin-bottom: 10px; color: #b0b0b0;">Ready to proceed with the compliance assessment?</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Generate Compliance Report", key="proceed_btn"):
                        log_debug("Proceeding to Step 3")
                        st.session_state.step = 3
                        progress_percentage = int((st.session_state.step / total_steps) * 100)
                        progress_bar.progress(progress_percentage/100)
                        st.experimental_rerun()
                else:
                    st.markdown("""
                        <div class="result-error">
                            <h4 style="margin-top: 0;">❌ Analysis Failed</h4>
                            <p>The AI could not analyze the document successfully. Please try with a different document or format.</p>
                        </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error during analysis: {e}")
                log_debug("Error during AI analysis: " + str(e))
                
                # Show error with retry option
                st.markdown("""
                    <div class="result-error">
                        <h4 style="margin-top: 0;">❌ Analysis Error</h4>
                        <p>There was an error during the AI analysis process. This might be due to server load or document complexity.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("Retry Analysis"):
                    log_debug("Retrying AI analysis")
                    st.experimental_rerun()

with tab2:
    # Display debug logs in a formatted, collapsible area
    st.markdown("<div class='card-header'>Debug Logs</div>", unsafe_allow_html=True)
    
    if "logs" in st.session_state.debug_logs and st.session_state.debug_logs["logs"]:
        with st.expander("View All Debug Logs", expanded=False):
            for i, log in enumerate(st.session_state.debug_logs["logs"]):
                st.markdown(f"<div class='debug'>[{i+1}] {log}</div>", unsafe_allow_html=True)
    else:
        st.info("No debug logs available yet.")

with tab3:
    # Help and Information section
    st.markdown("<div class='card-header'>Help & Information</div>", unsafe_allow_html=True)
    
    # FAQ Accordion
    with st.expander("Frequently Asked Questions"):
        st.markdown("""
            #### What types of documents can I upload?
            You can upload industrial application documents in PDF, PNG, or JPG formats. The document should contain clear text for the AI to analyze.
            
            #### How accurate is the AI analysis?
            Our AI system uses advanced models trained on regulatory compliance data. While it achieves high accuracy, we recommend human verification of results.
            
            #### What information does the compliance check include?
            The system checks for adherence to environmental regulations, energy efficiency requirements, building codes, and workplace safety standards.
            
            #### How long does the analysis take?
            Most documents are analyzed within 1-2 minutes, but complex documents may take longer.
            
            #### Is my data secure?
            Yes, all uploaded documents are processed securely and are not stored permanently unless explicitly requested.
        """)
    
    # Contact Support
    with st.expander("Contact Support"):
        st.markdown("""
            If you encounter any issues or have questions, please contact our support team:
            
            - Email: support@aisoulcheck.com
            - Phone: +1 (800) 555-0123
            - Hours: Monday-Friday, 9 AM - 5 PM EST
        """)
    
    # Tutorial
    with st.expander("How to Use This Tool"):
        st.markdown("""
            #### Step 1: Upload Your Document
            Upload your industrial application document using the file uploader on the main page.
            
            #### Step 2: AI Analysis
            Wait while our AI analyzes the document and extracts key information about the project.
            
            #### Step 3: Review Extracted Data
            Review the data extracted by the AI and make corrections if necessary.
            
            #### Step 4: Compliance Check
            The system will check the extracted information against relevant regulations.
            
            #### Step 5: View Compliance Report
            Review the comprehensive compliance report with recommendations.
        """)
        
    # System Requirements
    with st.expander("System Requirements"):
        st.markdown("""
            - Browser: Chrome, Firefox, Safari, or Edge (latest versions)
            - Internet Connection: Minimum 5 Mbps
            - Maximum File Size: 10MB
        """)

# Add a footer
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #333;">
        <p style="color: #777; font-size: 14px;">© 2023 AI Compliance Checker | Powered by SoulSync</p>
    </div>
""", unsafe_allow_html=True)
