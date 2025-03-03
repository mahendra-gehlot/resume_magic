import os
import streamlit as st
from dotenv import load_dotenv
import subprocess
import base64
from pathlib import Path
import json
import time
import pandas as pd
import plotly.express as px

from data_processing.fetch_tex import read_latex_file

# Import the LangGraph-enabled functions from the main module
from main import generate_resume_with_tracking, read_json_file

# Load environment variables from .env file
load_dotenv()


def ensure_directory(directory: str):
    """
    Create directory if it doesn't exist.
    
    Args:
        directory (str): Path to the directory to create
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


@st.cache_data(show_spinner=False)
def get_current_latex_resume():
    """
    Cache the LaTeX resume template to avoid repeated disk I/O.
    
    Returns:
        str: The LaTeX resume template content
    """
    return read_latex_file()


def convert_latex_to_pdf(latex_content: str, output_path: str) -> Path:
    """
    Convert LaTeX content to PDF using pdflatex with error checking.
    
    Args:
        latex_content (str): LaTeX document content as a string
        output_path (str): Path where the PDF should be saved
        
    Returns:
        Path: Path to the generated PDF file, or None if generation failed
    """
    try:
        output_path = Path(output_path)
        # Ensure the output directory exists
        ensure_directory(output_path.parent)
        
        # Create a temporary .tex file
        temp_tex_path = output_path.with_suffix('.tex')
        with open(temp_tex_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # Run pdflatex to convert the .tex file to PDF
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', str(temp_tex_path)],
            cwd=temp_tex_path.parent,
            capture_output=True,
            text=True
        )
        
        # Check for errors
        if result.returncode != 0:
            st.error("pdflatex error:\n" + result.stdout + "\n" + result.stderr)
            return None
            
        return output_path.with_suffix('.pdf')
    except Exception as e:
        st.error(f"Error converting LaTeX to PDF: {str(e)}")
        return None


def display_pdf(pdf_path: Path):
    """
    Display PDF in Streamlit using an HTML iframe.
    
    Args:
        pdf_path (Path): Path to the PDF file to display
    """
    # Read the PDF file and encode it in base64
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Create an iframe to display the PDF
    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="800px"
            type="application/pdf">
        </iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)


def reset_app():
    """
    Reset session state variables to clear the application state.
    Removes all generated content and user inputs.
    """
    keys_to_reset = [
        "generation_result", 
        "current_latex_resume", 
        "company_name", 
        "job_description", 
        "show_metrics"
    ]
    for key in keys_to_reset:
        st.session_state.pop(key, None)


def display_metrics(metrics: dict):
    """
    Display generation metrics in an organized way with visual charts.
    
    Args:
        metrics (dict): Dictionary containing performance metrics
    """
    if not metrics:
        return
        
    st.subheader("📊 Generation Metrics")
    
    # Display key metrics in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Resume Generation Time", f"{metrics.get('resume_generation_time', 0):.2f}s")
        if metrics.get('cover_letter_generation_time'):
            st.metric("Cover Letter Generation Time", f"{metrics.get('cover_letter_generation_time', 0):.2f}s")
        st.metric("Status", metrics.get('status', 'Unknown'))
    with col2:
        st.metric("Total Tokens Used", metrics.get('total_tokens_used', 0))
        st.metric("Completion Tokens", metrics.get('completion_tokens', 0))
        st.metric("Prompt Tokens", metrics.get('prompt_tokens', 0))
        st.metric("Model", metrics.get('model_name', 'Unknown'))
    
    # Create a bar chart of token usage
    token_data = {
        'Category': ['Prompt Tokens', 'Completion Tokens'],
        'Count': [metrics.get('prompt_tokens', 0), metrics.get('completion_tokens', 0)]
    }
    token_df = pd.DataFrame(token_data)
    fig = px.bar(
        token_df, 
        x='Category', 
        y='Count',
        title='Token Usage Breakdown',
        color='Category', 
        color_discrete_map={
            'Prompt Tokens': '#3498db',
            'Completion Tokens': '#2ecc71'
        }
    )
    st.plotly_chart(fig, use_container_width=True)


def display_historical_metrics():
    """
    Display historical metrics from previous generations with trend charts.
    Reads and processes all metric JSON files from the metrics directory.
    """
    metrics_dir = "./metrics"
    
    # Check if metrics directory exists
    if not os.path.exists(metrics_dir):
        st.info("No historical metrics available yet")
        return
        
    # Get all JSON files in the metrics directory
    metrics_files = [os.path.join(metrics_dir, f) for f in os.listdir(metrics_dir) if f.endswith('.json')]
    if not metrics_files:
        st.info("No historical metrics available yet")
        return
    
    # Load all metrics files into a list of dictionaries
    all_metrics = []
    for file_path in metrics_files:
        try:
            with open(file_path, 'r') as f:
                metrics = json.load(f)
            # Extract timestamp from filename
            filename = os.path.basename(file_path)
            timestamp = filename.replace('generation_metrics_', '').replace('.json', '')
            metrics['timestamp'] = timestamp
            all_metrics.append(metrics)
        except Exception:
            continue
            
    if not all_metrics:
        st.info("No valid metrics data found")
        return
    
    # Convert to DataFrame for visualization
    metrics_df = pd.DataFrame(all_metrics)
    metrics_df['timestamp'] = pd.to_datetime(metrics_df['timestamp'], format='%Y%m%d_%H%M%S')
    metrics_df = metrics_df.sort_values('timestamp')
    
    st.subheader("📈 Historical Performance")
    
    # Plot token usage over time
    if 'total_tokens_used' in metrics_df.columns:
        fig = px.line(
            metrics_df, 
            x='timestamp', 
            y='total_tokens_used',
            title='Token Usage Over Time',
            labels={'total_tokens_used': 'Total Tokens', 'timestamp': 'Date'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Plot generation time over time
    if 'resume_generation_time' in metrics_df.columns:
        time_df = metrics_df[['timestamp', 'resume_generation_time']].copy()
        time_df.columns = ['timestamp', 'Generation Time (s)']
        fig = px.line(
            time_df,
            x='timestamp', 
            y='Generation Time (s)',
            title='Generation Time Over Time',
            labels={'timestamp': 'Date'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Show raw data in an expandable section
    with st.expander("View Raw Metrics Data"):
        st.dataframe(metrics_df)


def main():
    """
    Main application function for the Streamlit interface.
    Handles UI layout, form submission, and results display.
    """
    # Configure the page
    st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="wide")
    
    # Header section with reset button
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("Mahendra's AI Resume Builder")
        st.markdown("*Now with LangGraph tracking*")
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            reset_app()
            st.experimental_rerun()
    st.markdown("---")
    
    # Initialize session state variables
    st.session_state.setdefault("generation_result", None)
    st.session_state.setdefault("current_latex_resume", None)
    st.session_state.setdefault("company_name", "")
    st.session_state.setdefault("job_description", "")
    st.session_state.setdefault("show_metrics", False)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ OpenAI API key not found. Please set it in your .env file.")
        return
    
    # Input form section
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.form("resume_form"):
            company_name = st.text_input(
                "🏢 Enter Company Name",
                value=st.session_state.company_name,
                placeholder="e.g., Microsoft"
            )
            job_description = st.text_area(
                "📝 Paste Job Description",
                value=st.session_state.job_description,
                height=300,
                placeholder="Paste the job description here..."
            )
            generate_cl = st.checkbox("Generate Cover Letter too")
            
            # Buttons for generating resume and toggling metrics
            col_a, col_b = st.columns(2)
            with col_a:
                submitted_resume = st.form_submit_button("Generate Resume")
            with col_b:
                toggle_metrics = st.form_submit_button("Toggle Metrics View")
    
    # Handle metrics toggle
    if toggle_metrics:
        st.session_state.show_metrics = not st.session_state.show_metrics
        st.experimental_rerun()
    
    # Handle resume generation form submission
    if submitted_resume:
        if not company_name or not job_description:
            st.error("Please fill in all required fields!")
            return
            
        # Save inputs to session state
        st.session_state.company_name = company_name
        st.session_state.job_description = job_description
        
        try:
            # Read the current resume template
            with st.spinner("Reading current resume template..."):
                st.session_state.current_latex_resume = get_current_latex_resume()
                
            # Generate the customized resume
            with st.spinner("🎯 Customizing your resume..."):
                generation_start = time.time()
                result = generate_resume_with_tracking(
                    company_name=company_name,
                    current_latex_resume=st.session_state.current_latex_resume,
                    comprehensive_profile=read_json_file('./data/detailed_resume.json'),
                    company_job_description=job_description,
                    generate_cover_letter=generate_cl
                )
                generation_end = time.time()
                
                # Check for errors
                if result.get("error"):
                    st.error(f"Generation error: {result['error']}")
                    return
                    
                # Save results to session state
                st.session_state.generation_result = result
                st.success("✅ Documents generated successfully!")
                
                # Display resume LaTeX source
                if result.get("generated_resume"):
                    with st.expander("View Resume LaTeX Source"):
                        st.code(result["generated_resume"], language="tex")
                
                # Display cover letter if generated
                if result.get("cover_letter"):
                    st.markdown("---")
                    st.subheader("Cover Letter")
                    cl_pdf_path = convert_latex_to_pdf(result["cover_letter"], "./pdfs/temp_cl_output.pdf")
                    if cl_pdf_path:
                        st.subheader("Cover Letter Preview")
                        display_pdf(cl_pdf_path)
                    with st.expander("View Cover Letter LaTeX Source"):
                        st.code(result["cover_letter"], language="tex")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please check your inputs and try again.")
            return
            
    # Display existing results if available (for when the page is refreshed)
    elif st.session_state.generation_result is not None:
        result = st.session_state.generation_result
        
        # Display resume LaTeX source
        if result.get("generated_resume"):
            with st.expander("View Resume LaTeX Source"):
                st.code(result["generated_resume"], language="tex")
        
        # Display cover letter if it exists
        if result.get("cover_letter"):
            st.markdown("---")
            st.subheader("Cover Letter")
            cl_pdf_path = convert_latex_to_pdf(result["cover_letter"], "./pdfs/temp_cl_output.pdf")
            if cl_pdf_path:
                st.subheader("Cover Letter Preview")
                display_pdf(cl_pdf_path)
            with st.expander("View Cover Letter LaTeX Source"):
                st.code(result["cover_letter"], language="tex")
    
    # Display metrics if enabled
    if st.session_state.show_metrics:
        st.markdown("---")
        tabs = st.tabs(["Current Generation", "Historical Metrics"])
        with tabs[0]:
            if st.session_state.generation_result and st.session_state.generation_result.get("metrics"):
                display_metrics(st.session_state.generation_result["metrics"])
            else:
                st.info("No metrics available for the current generation")
        with tabs[1]:
            display_historical_metrics()


if __name__ == "__main__":
    main()