import os
from PIL import Image as PILImage
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage
import streamlit as st

# Set your API Key (Replace with your actual key)
GOOGLE_API_KEY = "AIzaSyCr35hxFrpVsbNWgqOwU6PwmkpwLmO2dJA"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Ensure API Key is provided
if not GOOGLE_API_KEY:
    raise ValueError("⚠️ Please set your Google API Key in GOOGLE_API_KEY")

# Initialize the Medical Agent
medical_agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools()],
    markdown=True
)

# Medical Analysis Query
query = """
You are an elite-level board-certified radiologist with fellowship training in diagnostic imaging and 15+ years of clinical experience. Analyze this medical image with the precision of a specialist consultation:

### 1. Technical Assessment
- Identify specific imaging modality including technique parameters (e.g., projection view for X-rays, sequence type for MRI, window settings for CT)
- Evaluate anatomical region with proper anatomical landmarks and positioning
- Assess image quality (contrast, resolution, noise, artifacts) using standard radiological criteria
- Note any technical limitations affecting interpretation

### 2. Systematic Findings Analysis
- Conduct structured regional assessment following standard radiological examination patterns
- Document all visible structures with precise anatomical terminology
- Quantify abnormalities with appropriate measurements (dimensions, angles, Hounsfield units, signal intensities)
- Evaluate symmetry, borders, densities, and tissue characteristics using field-standard descriptors

### 3. Clinical Impression and Differential
- Formulate primary diagnosis with confidence level (definite, highly probable, possible, indeterminate)
- Present differential diagnoses in descending probability with evidence-based reasoning
- Incorporate relevant clinical correlation factors that would influence interpretation
- Flag critical findings requiring urgent attention according to ACR guidelines
- Include pertinent negatives that help narrow the differential

### 4. Patient Communication Framework
- Translate technical findings into accessible explanations using the teach-back method
- Provide clear visual metaphors appropriate to patient education level
- Include contextual information about the significance of findings
- Address likely patient concerns based on the identified condition

### 5. Evidence-Based Context
- Utilize DuckDuckGo to identify current literature (prioritize meta-analyses, systematic reviews)
- Reference applicable clinical guidelines and standard of care protocols
- Cite 2-3 high-impact publications supporting key aspects of the analysis
- Note any recent advances in imaging or treatment for the identified condition

Format your response with professional medical report structure, including appropriate headers, subheaders, and conclusion. Maintain proper medical terminology while ensuring clarity and precision.
"""

# Function to analyze medical image
def analyze_medical_image(image_path):
    """Processes and analyzes a medical image using AI."""
    
    # Open and resize image
    image = PILImage.open(image_path)
    width, height = image.size
    aspect_ratio = width / height
    new_width = 500
    new_height = int(new_width / aspect_ratio)
    resized_image = image.resize((new_width, new_height))

    # Save resized image
    temp_path = "temp_resized_image.png"
    resized_image.save(temp_path)

    # Create AgnoImage object
    agno_image = AgnoImage(filepath=temp_path)

    # Run AI analysis
    try:
        response = medical_agent.run(query, images=[agno_image])
        return response.content
    except Exception as e:
        return f"⚠️ Analysis error: {e}"
    finally:
        # Clean up temporary file
        os.remove(temp_path)

# Streamlit UI setup
st.set_page_config(page_title="Medical Image Analysis", layout="centered")
st.title("🩺 Medical Image Analysis Tool 🔬")
st.markdown(
    """
    Welcome to the **Medical Image Analysis** tool! 📸
    Upload a medical image (X-ray, MRI, CT, Ultrasound, etc.), and our AI-powered system will analyze it, providing detailed findings, diagnosis, and research insights.
    Let's get started!
    """
)

# Upload image section
st.sidebar.header("Upload Your Medical Image:")
uploaded_file = st.sidebar.file_uploader("Choose a medical image file", type=["jpg", "jpeg", "png", "bmp", "gif"])

# Button to trigger analysis
if uploaded_file is not None:
    # Display the uploaded image in Streamlit
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    if st.sidebar.button("Analyze Image"):
        with st.spinner("🔍 Analyzing the image... Please wait."):
            # Save the uploaded image to a temporary file
            image_path = f"temp_image.{uploaded_file.type.split('/')[1]}"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Run analysis on the uploaded image
            report = analyze_medical_image(image_path)
            
            # Display the report
            st.subheader("📋 Analysis Report")
            st.markdown(report, unsafe_allow_html=True)
            
            # Clean up the saved image file
            os.remove(image_path)
else:
    st.warning("⚠️ Please upload a medical image to begin analysis.")
