import streamlit as st
import time
import base64
from ui.assets.logo import get_logo, get_logo_base64

# Set page config
st.set_page_config(
    page_title="AI Compliance Checker - Home",
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

# Custom Styling with modern design elements - dark theme
st.markdown(
    """
    <style>
        /* Base styles - Dark Theme */
        body {
            background-color: #1a1a1a;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #f0f0f0;
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
        
        /* Hero section */
        .hero {
            position: relative;
            margin-bottom: 40px;
            text-align: center;
        }
        
        .hero-image {
            width: 100%;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            max-height: 450px;
            object-fit: cover;
        }
        
        .hero-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(0deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.4) 100%);
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 40px;
        }
        
        .hero-title {
            color: white;
            font-size: 50px;
            font-weight: 800;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .hero-description {
            color: #e6e6e6;
            font-size: 22px;
            max-width: 700px;
            margin: 0 auto 30px auto;
            line-height: 1.5;
        }
        
        /* Cards and sections */
        .card {
            background-color: #2a2a2a;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
        }
        
        .card-icon {
            font-size: 42px;
            margin-bottom: 20px;
            color: #3f96e8;
            text-align: center;
        }
        
        .card-title {
            font-size: 24px;
            font-weight: 600;
            color: #f0f0f0;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .card-content {
            color: #b0b0b0;
            font-size: 16px;
            flex-grow: 1;
            text-align: center;
        }
        
        /* Features section */
        .feature-container {
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            background-color: #2a2a2a;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        }
        
        .feature-icon {
            font-size: 30px;
            color: #3f96e8;
            margin-right: 15px;
            vertical-align: middle;
        }
        
        .feature-title {
            font-size: 20px;
            font-weight: 600;
            color: #f0f0f0;
            vertical-align: middle;
        }
        
        .feature-description {
            margin-top: 10px;
            color: #b0b0b0;
        }
        
        /* Buttons */
        .cta-button {
            background: linear-gradient(90deg, #3f96e8, #67c0ff);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            display: inline-block;
            box-shadow: 0 4px 10px rgba(30, 136, 229, 0.3);
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(30, 136, 229, 0.4);
        }
        
        /* Section formatting */
        .section-title {
            font-size: 32px;
            font-weight: 700;
            color: #f0f0f0;
            margin-bottom: 25px;
            text-align: center;
        }
        
        .section-description {
            font-size: 18px;
            color: #b0b0b0;
            margin-bottom: 40px;
            text-align: center;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Stats counter */
        .stat-container {
            text-align: center;
            padding: 20px;
            background-color: #2a2a2a;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            height: 100%;
        }
        
        .stat-number {
            font-size: 46px;
            font-weight: 800;
            color: #3f96e8;
            margin-bottom: 10px;
        }
        
        .stat-label {
            font-size: 18px;
            color: #b0b0b0;
        }
        
        /* Testimonial */
        .testimonial {
            background-color: #1f2937;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            position: relative;
        }
        
        .testimonial-text {
            font-size: 18px;
            font-style: italic;
            color: #f0f0f0;
            margin-bottom: 20px;
        }
        
        .testimonial-author {
            font-weight: 600;
            color: #3f96e8;
        }
        
        .testimonial-company {
            color: #b0b0b0;
            font-size: 14px;
        }
        
        .testimonial:before {
            content: '"';
            font-size: 80px;
            color: #3f96e8;
            opacity: 0.2;
            position: absolute;
            top: 10px;
            left: 20px;
            font-family: serif;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding-top: 30px;
            margin-top: 60px;
            border-top: 1px solid #333;
            color: #777;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate {
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Separator */
        .separator {
            height: 3px;
            background: linear-gradient(90deg, #1a1a1a, #3f96e8, #1a1a1a);
            margin: 60px 0;
            border-radius: 2px;
        }
        
        /* Sidebar customization */
        .css-1d391kg, .css-163ttbj, [data-testid="stSidebar"] {
            background-color: #121212;
        }
        
        .css-1d391kg p, .css-163ttbj p, [data-testid="stSidebar"] p {
            color: #f0f0f0;
        }
        
        /* Fix for overlapping elements */
        .row-widget > div {
            width: 100%;
        }
        
        /* Button styling */
        .stButton button {
            background: linear-gradient(90deg, #3f96e8, #67c0ff);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 30px;
            font-weight: 600;
            box-shadow: 0 4px 10px rgba(30, 136, 229, 0.3);
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton button:hover {
            box-shadow: 0 6px 15px rgba(30, 136, 229, 0.4);
            transform: translateY(-2px);
        }
        
        /* Main container */
        .block-container {
            max-width: 100%;
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        /* Make all elements fully visible */
        .main {
            background-color: #1a1a1a;
        }
    </style>
    """,
    unsafe_allow_html=True
)



# Our Impact - Statistics
st.markdown('<h2 class="section-title animate">Our Impact</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-description animate">Transforming the regulatory landscape with AI-powered solutions.</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="stat-container animate">
            <div class="stat-number">70%</div>
            <div class="stat-label">Processing Time Reduced</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col2:
    st.markdown(
        """
        <div class="stat-container animate">
            <div class="stat-number">92%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col3:
    st.markdown(
        """
        <div class="stat-container animate">
            <div class="stat-number">500+</div>
            <div class="stat-label">Applications Processed</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col4:
    st.markdown(
        """
        <div class="stat-container animate">
            <div class="stat-number">20+</div>
            <div class="stat-label">Regulatory Frameworks</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Separator
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Key Features
st.markdown('<h2 class="section-title animate" id="features">Key Features</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-description animate">Advanced technology to streamline regulatory compliance.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="card animate">
            <div class="card-icon">📄</div>
            <div class="card-title">Document Analysis</div>
            <div class="card-content">
                Our AI system can process and analyze complex industrial application documents in various formats including PDFs, images, and text files. Extract crucial information with high accuracy.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col2:
    st.markdown(
        """
        <div class="card animate">
            <div class="card-icon">🔍</div>
            <div class="card-title">Compliance Verification</div>
            <div class="card-content">
                Automatically cross-reference extracted information with relevant regulatory requirements and standards to identify compliance issues and gaps.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

col3, col4 = st.columns(2)

with col3:
    st.markdown(
        """
        <div class="card animate">
            <div class="card-icon">📊</div>
            <div class="card-title">Detailed Reporting</div>
            <div class="card-content">
                Generate comprehensive compliance reports with actionable insights, recommendations for improvements, and clear explanations of regulatory requirements.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col4:
    st.markdown(
        """
        <div class="card animate">
            <div class="card-icon">🤖</div>
            <div class="card-title">AI Chatbot Assistance</div>
            <div class="card-content">
                Get instant answers to compliance questions through our AI-powered chatbot that understands regulatory frameworks and can provide guidance on specific requirements.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Separator
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# How It Works Section
st.markdown('<h2 class="section-title animate">How It Works</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-description animate">A simple, efficient process powered by advanced AI.</p>', unsafe_allow_html=True)

# Process Steps
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-container animate">
            <span class="feature-icon">1️⃣</span>
            <span class="feature-title">Upload Documents</span>
            <p class="feature-description">
                Upload your industrial application documents in PDF, image, or text format through our secure platform.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col2:
    st.markdown(
        """
        <div class="feature-container animate">
            <span class="feature-icon">2️⃣</span>
            <span class="feature-title">AI Analysis</span>
            <p class="feature-description">
                Our advanced AI system analyzes the documents, extracts key information, and verifies compliance with regulatory frameworks.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col3:
    st.markdown(
        """
        <div class="feature-container animate">
            <span class="feature-icon">3️⃣</span>
            <span class="feature-title">Get Results</span>
            <p class="feature-description">
                Receive a comprehensive compliance report with actionable insights and recommendations for improvement.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Separator
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Testimonials
st.markdown('<h2 class="section-title animate">What Our Clients Say</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="testimonial animate">
            <p class="testimonial-text">
                The AI Compliance Checker has revolutionized how we process industrial applications. What used to take weeks now takes hours, with even greater accuracy.
            </p>
            <div class="testimonial-author">Sarah Johnson</div>
            <div class="testimonial-company">Department of Environmental Protection</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col2:
    st.markdown(
        """
        <div class="testimonial animate">
            <p class="testimonial-text">
                This tool has significantly reduced our administrative burden while improving our accuracy in catching non-compliant applications. The ROI has been incredible.
            </p>
            <div class="testimonial-author">Michael Chen</div>
            <div class="testimonial-company">Industrial Regulatory Commission</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Call to Action Section
st.markdown(
    """
    <div style="text-align: center; margin: 60px 0 40px 0;" class="animate" id="get-started">
        <h2 class="section-title">Ready to Transform Your Compliance Process?</h2>
        <p class="section-description">Start using our AI-powered solution today and experience the difference.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# CTA Buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("Start Compliance Analysis", key="main_cta"):
        with st.spinner("Preparing compliance analysis tool..."):
            time.sleep(1)
        st.success("Redirecting to compliance analysis page...")
        st.switch_page("pages/Compliance_Analysis.py")

# Footer
st.markdown(
    """
    <div class="footer animate">
        <p>© 2023 AI Compliance Checker | Powered by SoulSync</p>
        <p style="font-size: 14px; margin-top: 10px;">
            Contact: support@aisoulcheck.com | Privacy Policy | Terms of Service
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
