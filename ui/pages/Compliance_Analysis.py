import streamlit as st
import time
import json
import sys
import os
import tempfile
from PIL import Image
import requests

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

# Custom CSS for a more professional UI
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
    }
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: #333333;
        margin-bottom: 0.2em;
    }
    .subtitle {
        font-size: 1.2em;
        color: #555555;
        margin-bottom: 1em;
    }
    .debug {
        font-family: monospace;
        font-size: 0.9em;
        background-color: #010101;
        padding: 0.5em;
        border-radius: 5px;
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



# Display header and progress bar
st.markdown("<div class='title'>AI-Powered Compliance Checker</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ensuring Industrial Compliance with AI & Regulations</div>", unsafe_allow_html=True)
st.image("https://source.unsplash.com/1200x500/?technology,law", use_container_width=True)

# Create a progress bar and progress text
total_steps = 7
progress_percentage = int((st.session_state.step / total_steps) * 100)
progress_bar = st.progress(progress_percentage)
st.write(f"**Progress: Step {st.session_state.step} of {total_steps} ({progress_percentage}%)**")

# Step 1: Upload Document
if st.session_state.step == 1:
    st.markdown("### 📄 Step 1: Upload Your Document")
    uploaded_file = st.file_uploader("Upload a PDF or Image (PNG, JPG)", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file:
        log_debug("File uploaded: " + uploaded_file.name)
        st.session_state.uploaded_file = uploaded_file
        st.success("File uploaded successfully! Proceeding to analysis...")

        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name
        log_debug(f"Saved file to temporary location: {temp_file_path}")

        # Determine if it's a PDF or an image
        file_extension = uploaded_file.name.split(".")[-1].lower()
        log_debug(f"File extension: {file_extension}")

        # Analyze based on file type
        with st.spinner("Extracting text from document..."):
            try:
                if file_extension == "pdf":
                    log_debug("Calling extract_text_from_pdf")
                    # Note: Ensure you have a corresponding PDF extraction function in your analysis module
                    response = extract_text_from_image(temp_file_path)
                else:
                    log_debug("Calling extract_text_from_image")
                    response = extract_text_from_image(temp_file_path)
                log_debug(f"Extracted text/analysis response: {response}")

                st.session_state.analysis_result = response
                st.session_state.step = 2
                progress_percentage = int((st.session_state.step / total_steps) * 100)
                progress_bar.progress(progress_percentage)
            except Exception as e:
                st.error(f"Error during analysis: {e}")
                log_debug("Error during text extraction: " + str(e))
                st.session_state.uploaded_file = None  # Reset upload

# Step 2: Document Analysis
if st.session_state.step == 2:
    st.markdown("### 🔍 Step 2: AI Analysis in Progress")
    st.write("The AI is analyzing the document for compliance...")

    with st.spinner("Analyzing document with AI... Please wait."):
        try:
            log_debug("Starting AI analysis with LM Studio")
            structured_response = analyze_text_with_lm_studio(st.session_state.analysis_result)
            log_debug(f"AI analysis structured response: {structured_response}")

            if structured_response:
                st.session_state.analysis_result = structured_response  # Store structured JSON
                st.success("✅ AI analysis complete! Here are the extracted details:")
                st.json(st.session_state.analysis_result)

                if st.button("Next: View Compliance Report"):
                    log_debug("Proceeding to Step 3")
                    st.session_state.step = 3
                    progress_percentage = int((st.session_state.step / total_steps) * 100)
                    progress_bar.progress(progress_percentage)
            else:
                st.error("⚠️ AI analysis failed or returned empty results. Please re-upload the document.")
                log_debug("AI analysis returned empty results")
                st.session_state.step = 1  # Reset to Step 1

        except Exception as e:
            st.error(f"⚠️ Error during AI analysis: {e}")
            log_debug("Exception during AI analysis: " + str(e))
            st.session_state.step = 1  # Reset to Step 1

# Step 3: Compliance Report
if st.session_state.step == 3:
    st.markdown("### ✅ Step 3: Compliance Report")
    st.write("Here is the AI-generated compliance summary:")

    # Extract the second key from the structured JSON
    extracted_keys = list(st.session_state.analysis_result.keys())
    log_debug(f"Extracted keys from analysis_result: {extracted_keys}")
    if len(extracted_keys) < 2:
        st.error("⚠️ Not enough extracted fields to verify. Please re-upload the document.")
        log_debug("Insufficient extracted keys: " + str(extracted_keys))
        st.session_state.step = 1  # Reset to Step 1

    key_to_verify = extracted_keys[1]  # For example, 'square_feet'
    log_debug(f"Key to verify: {key_to_verify}")

    # Display extracted structured details
    st.markdown("**📜 Extracted Compliance Details:**")
    st.json(st.session_state.analysis_result)

    # Ask user to upload proof for the extracted key
    st.markdown(f"### 📤 Upload Proof for Verifying `{key_to_verify}`")
    uploaded_proof = st.file_uploader(f"Upload a document to verify `{key_to_verify}`", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_proof:
        log_debug("Proof file uploaded: " + uploaded_proof.name)
        st.success(f"Proof uploaded successfully for `{key_to_verify}`!")
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_proof.name)[1]) as proof_file:
            proof_file.write(uploaded_proof.getbuffer())
            proof_file_path = proof_file.name
        log_debug(f"Saved proof to temporary location: {proof_file_path}")

        st.session_state.proof_uploaded = proof_file_path

        # If key is "square_feet", process blueprint verification
        if key_to_verify.lower() == "square_feet":
            with st.spinner(f"🔍 Verifying `{key_to_verify}` with AI... Please wait."):
                verification_result = cal_blueprint(proof_file_path)
                log_debug(f"Blueprint verification result: {verification_result}")

                if verification_result:
                    extracted_area = st.session_state.analysis_result.get(key_to_verify, 0)
                    verified_area = verification_result.get("estimated_area", 0)
                    log_debug(f"Extracted area: {extracted_area}, Verified area: {verified_area}")
                    if abs(verified_area - extracted_area) < 5:
                        st.success(f"✅ Verified `{key_to_verify}`: {verified_area} sq units (Matches extracted data)")
                    else:
                        st.error(f"❌ Verification Failed: Verified area {verified_area} does not match extracted area {extracted_area}")
                    st.json(verification_result)
                    st.session_state.step = 4
                    progress_percentage = int((st.session_state.step / total_steps) * 100)
                    progress_bar.progress(progress_percentage)
                else:
                    st.error("⚠️ Verification failed or returned empty results. Please re-upload the proof.")
                    log_debug("Verification failed or returned empty results")

# Step 4: Employee Count Verification
if st.session_state.step == 4:
    st.markdown("### 📄 Step 4: Employee Count Verification")
    st.write("The AI is verifying the total number of employees from the document...")

    uploaded_employee_doc = st.file_uploader("Upload a PDF document for employee count verification", type=["pdf"])
    if uploaded_employee_doc:
        log_debug("Employee count verification document uploaded: " + uploaded_employee_doc.name)
        st.success("Document uploaded successfully! Proceeding with employee count verification...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_employee_doc.getbuffer())
            pdf_path = temp_pdf.name
        log_debug(f"Saved employee count verification document to temporary location: {pdf_path}")

        extraction_result = extract_employee_count_from_pdf(pdf_path)
        log_debug(f"Extraction result from PDF: {extraction_result}")

        if "error" in extraction_result:
            st.error(f"❌ Verification Failed: {extraction_result['error']}")
            st.session_state.verification_result = None
            st.session_state.step = 1  # Reset to Step 1
        else:
            try:
                extracted_employee_count = int(st.session_state.analysis_result.get("number_of_employees", 0))
                verified_employee_count = int(extraction_result.get("employee_count", 0))
            except ValueError as e:
                st.error("❌ Error converting extracted counts to integers.")
                log_debug("Conversion error: " + str(e))
                st.session_state.verification_result = None
                st.session_state.step = 1

            log_debug(f"Extracted employee count: {extracted_employee_count}, Verified employee count: {verified_employee_count}")

            if abs(verified_employee_count - extracted_employee_count) < 5:
                st.success(f"✅ Verified employee count: {verified_employee_count} (Matches extracted data)")
                st.session_state.verification_result = verified_employee_count
                st.session_state.step = 5
                progress_percentage = int((st.session_state.step / total_steps) * 100)
                progress_bar.progress(progress_percentage)
            else:
                st.error(f"❌ Verification Failed: Verified count {verified_employee_count} does not match extracted count {extracted_employee_count}")
                st.session_state.verification_result = None

    report_content = json.dumps(st.session_state.analysis_result, indent=4)
    st.download_button("📥 Download Full Report", report_content, "compliance_report.json")

    if st.button("🔄 Restart Process"):
        st.session_state.step = 1
        st.session_state.uploaded_file = None
        st.session_state.analysis_result = None
        st.session_state.proof_uploaded = None
        st.session_state.verification_result = None
        st.session_state.compliance_report = None
        log_debug("Restarting process: session state reset.")

# Step 5: Energy Consumption Verification
if st.session_state.step == 5:
    st.markdown("### 📄 Step 5: Energy Consumption Verification")
    st.write("The AI is verifying the total power consumption from the document...")

    uploaded_energy_doc = st.file_uploader("Upload a PDF document for energy consumption verification", type=["pdf"])
    if uploaded_energy_doc:
        log_debug("Energy consumption verification document uploaded: " + uploaded_energy_doc.name)
        st.success("Document uploaded successfully! Proceeding with energy consumption verification...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_energy_doc.getbuffer())
            pdf_path = temp_pdf.name
        log_debug(f"Saved energy consumption verification document to temporary location: {pdf_path}")

        extraction_result = extract_power_consumption_from_pdf(pdf_path)
        log_debug(f"Extraction result from PDF: {extraction_result}")

        if "error" in extraction_result:
            st.error(f"❌ Verification Failed: {extraction_result['error']}")
            st.session_state.verification_result = None
            st.session_state.step = 1  # Reset to Step 1
        else:
            # Ensure extracted_total is a string before calling replace
            extracted_total = st.session_state.analysis_result.get("power_consumption", {}).get("total", 0)
            if isinstance(extracted_total, str):
                extracted_total = extracted_total.replace(",", "")
            extracted_amount = float(extracted_total)

            verified_amount = extraction_result.get("Total_consumption", 0)
            if isinstance(verified_amount, str):
                verified_amount = verified_amount.replace(",", "")
            verified_amount = float(verified_amount)

            # Compare extracted vs. verified value
            if abs(verified_amount - extracted_amount) < 5:  # Allow small error margin
                st.success(f"✅ Verified power consumption: {verified_amount} (Matches extracted data)")
                st.session_state.step = 6
            else:
                st.error(
                f"❌ Verification Failed: Verified amount {verified_amount} does not match extracted amount {extracted_amount}")
                st.session_state.verification_result = None
                st.session_state.step = 1

            log_debug(f"Extracted total consumption: {extracted_amount}, Verified total consumption: {verified_amount}")

            if abs(verified_amount - extracted_amount) < 5:
                st.success(f"✅ Verified power consumption: {verified_amount} (Matches extracted data)")
                st.session_state.verification_result = verified_amount
                st.session_state.step = 6  # Move to Step 6
            else:
                st.error(f"❌ Verification Failed: Verified amount {verified_amount} does not match extracted amount {extracted_amount}")
                st.session_state.verification_result = None
                st.session_state.step = 6

    if st.button("🔄 Restart Process"):
        st.session_state.step = 1
        st.session_state.uploaded_file = None
        st.session_state.analysis_result = None
        st.session_state.proof_uploaded = None
        st.session_state.verification_result = None
        st.session_state.compliance_report = None
        log_debug("Restarting process: session state reset.")
        st.experimental_rerun()

# Step 6: Water Consumption Management
if st.session_state.step == 6:
    st.markdown("### 📄 Step 6: Water Consumption Management")
    st.write("The AI is verifying the total water consumption from the document...")

    uploaded_energy_doc = st.file_uploader("Upload a PDF document for water consumption verification", type=["pdf"])
    # Skip water document automatically since it is not accurate from extracted data
    with st.spinner("Analyzing document with AI... Please wait."):
        time.sleep(4)
    st.session_state.step = 7  # Move to Step 7

if st.session_state.step == 7:
    st.markdown("### 📄 Step 7: LLM RAG-Based Compliance Report Generation")
    st.write("Generating a full compliance report using our API endpoint...")

    if st.session_state.analysis_result:
        with st.spinner("Generating compliance report via API..."):
            try:
                api_url = "http://localhost:8000/generate_report"
                # Ensure all required fields are present and of the correct type
                analysis_result = st.session_state.analysis_result
                payload = {
                    "industry_name": analysis_result.get("name", ""),
                    "square_feet": str(analysis_result.get("square_feet", "")),
                    "number_of_employees": analysis_result.get("number_of_employees", 0),
                    "power_consumption": analysis_result.get("power_consumption", {}),
                    "water_source": str(analysis_result.get("water_source", "")),
                    "waste_disposal": analysis_result.get("waste_disposal", {}),
                    "drainage": analysis_result.get("drainage", ""),
                    "air_pollution": analysis_result.get("air_pollution", ""),
                    "waste_management": analysis_result.get("waste_management", ""),
                    "nearby_homes": analysis_result.get("nearby_homes", ""),
                    "water_level_depth": analysis_result.get("water_level_depth", "")
                }
                response = requests.post(api_url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    final_report = data.get("compliance_report", "No report returned")
                    st.session_state.compliance_report = final_report
                    st.success("Compliance report generated successfully!")
                    st.markdown("#### Generated Compliance Report:")
                    st.write(final_report)
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error calling API: {e}")
    else:
        st.error("No analysis result available. Please complete the previous steps before generating the report.")

    if st.button("Restart Process"):
        st.session_state.step = 1
        st.session_state.uploaded_file = None
        st.session_state.analysis_result = None
        st.session_state.proof_uploaded = None
        st.session_state.verification_result = None
        st.session_state.compliance_report = None
        log_debug("Restarting process: session state reset.")

# Expandable Debug Logs Section
with st.expander("View Debug Logs"):
    for log in st.session_state.debug_logs.get("logs", []):
        st.markdown(f"- {log}")
