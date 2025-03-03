# AI Resume Builder - README  

## 📌 Project Overview  
AI Resume Builder is a Streamlit-based application that generates ATS-friendly resumes and cover letters tailored to specific job descriptions. It leverages OpenAI's LLM models, **LangChain**, and **LangGraph** for enhanced tracking, customization, and structured reasoning.  

## 🎯 Features  
- **Automated Resume Generation**: Customizes LaTeX-based resumes for different companies and job descriptions.  
- **Cover Letter Generation**: Optionally generates a cover letter alongside the resume.  
- **Performance Tracking**: Displays metrics like token usage and generation time.  
- **Historical Analysis**: Tracks and visualizes past resume generations.  

## 🏗️ Tech Stack  
- **Python** (Streamlit, Pandas, Plotly, Subprocess)  
- **OpenAI API** (LLM for content generation)  
- **LangChain & LangGraph** (Enhanced reasoning and tracking)  
- **LaTeX** (Resume and Cover Letter formatting)  

## 🚀 Installation  
1. Clone the repository:  
   ```bash
   git clone <repository_url>
   cd ai-resume-builder
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:  
   - Create a `.env` file with:  
     ```
     OPENAI_API_KEY=<your_openai_api_key>
     ```
4. Run the application:  
   ```bash
   streamlit run app.py
   ```

## 📜 Usage  
1. Enter the **company name** and **job description**.  
2. Click **"Generate Resume"**.  
3. Optionally, enable **Cover Letter Generation**.  
4. View the generated **LaTeX source** or download the **PDF**.  

## 📈 Metrics & Analytics  
- Displays **current token usage**, **generation time**, and **model details**.  
- Tracks **historical metrics** for performance insights.  

## 📧 Contact  
For any issues or contributions, reach out to **Mahendra Gehlot**.