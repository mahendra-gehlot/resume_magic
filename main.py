import os
import json
import datetime
from dotenv import load_dotenv
from typing import Dict, Any
import streamlit as st

from langchain.chains import LLMChain, TransformChain
from langchain.output_parsers import OutputFixingParser
from langchain.schema import BaseOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Your custom modules
from data_processing.fetch_tex import read_latex_file
from scarp_job_description.scarping_method import get_job_text
from data_processing.save_results import save_tex
from data_processing.output_parser import LaTeXResumeParser
from prompt_templates import current_prompt_v3 as resume_template_latest
from prompt_templates import cover_letter_template

# Import LangGraph components
from langgraph.graph import END, StateGraph
# Use the SQLite-based persistent checkpointer:
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

def read_json_file(file_path: str) -> str:
    """Reads a JSON file and returns its content as a string."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except IOError as e:
        raise IOError(f"Error reading the file at {file_path}: {str(e)}")

# Define state type for our graph
class ResumeState(dict):
    """State for the resume generation process."""
    company_name: str
    current_latex_resume: str
    comprehensive_profile: str
    company_job_description: str
    generated_resume: str = None
    cover_letter: str = None
    error: str = None
    metrics: Dict = None

# Initialize tracking metrics
def initialize_metrics() -> Dict:
    return {
        "resume_generation_time": None,
        "cover_letter_generation_time": None,
        "total_tokens_used": 0,
        "completion_tokens": 0,
        "prompt_tokens": 0,
        "model_name": None,
        "status": "initialized"
    }

# Graph Nodes
def process_inputs(state: ResumeState) -> ResumeState:
    """Process and validate input data."""
    new_state = state.copy()
    
    if not new_state.get("company_name"):
        new_state["error"] = "Company name is required"
        return new_state
    
    if not new_state.get("company_job_description"):
        new_state["error"] = "Job description is required"
        return new_state
    
    if not new_state.get("metrics"):
        new_state["metrics"] = initialize_metrics()
        
    new_state["metrics"]["status"] = "inputs_processed"
    return new_state

def generate_tailored_resume(state: ResumeState) -> ResumeState:
    """Generate a tailored resume based on the job description."""
    import time
    new_state = state.copy()
    
    if new_state.get("error"):
        return new_state
    
    start_time = time.time()
    
    try:
        llm = ChatOpenAI(
            temperature=0.25,
            model_name="gpt-4o-mini",
            api_key=os.environ["OPENAI_API_KEY"],
        )
        prompt = PromptTemplate(
            template=resume_template_latest,
            input_variables=[
                "company_name",
                "current_latex_resume",
                "comprehensive_profile_json",
                "company_job_description",
            ],
        )
        parser = LaTeXResumeParser()
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        from langchain.callbacks import get_openai_callback
        
        chain = (
            {
                "company_name": RunnablePassthrough(),
                "current_latex_resume": RunnablePassthrough(),
                "comprehensive_profile_json": RunnablePassthrough(),
                "company_job_description": RunnablePassthrough(),
            }
            | prompt
            | llm
            | fixing_parser
        )
        with get_openai_callback() as cb:
            customized_resume = chain.invoke({
                "company_name": new_state["company_name"],
                "current_latex_resume": new_state["current_latex_resume"],
                "comprehensive_profile_json": new_state["comprehensive_profile"],
                "company_job_description": new_state["company_job_description"],
            })
            new_state["metrics"]["total_tokens_used"] += cb.total_tokens
            new_state["metrics"]["completion_tokens"] += cb.completion_tokens
            new_state["metrics"]["prompt_tokens"] += cb.prompt_tokens
            new_state["metrics"]["model_name"] = "gpt-4o-mini"
        new_state["generated_resume"] = customized_resume
        new_state["metrics"]["status"] = "resume_generated"
    except Exception as e:
        new_state["error"] = f"Resume generation error: {str(e)}"
        new_state["metrics"]["status"] = "resume_generation_failed"
    
    end_time = time.time()
    new_state["metrics"]["resume_generation_time"] = end_time - start_time
    return new_state

def generate_tailored_cover_letter(state: ResumeState) -> ResumeState:
    """Generate a tailored cover letter based on the resume and job description."""
    import time
    new_state = state.copy()
    
    if new_state.get("error") or not new_state.get("generated_resume"):
        return new_state
    
    start_time = time.time()
    
    try:
        llm = ChatOpenAI(
            temperature=0.3,
            model_name="gpt-4o-mini",
            api_key=os.environ["OPENAI_API_KEY"],
        )
        prompt = PromptTemplate(
            template=cover_letter_template,
            input_variables=[
                "company_name",
                "current_latex_resume",
                "company_job_description",
                "generated_resume",
            ],
        )
        parser = LaTeXResumeParser()
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        from langchain.callbacks import get_openai_callback
        
        chain = (
            {
                "company_name": RunnablePassthrough(),
                "current_latex_resume": RunnablePassthrough(),
                "company_job_description": RunnablePassthrough(),
                "generated_resume": RunnablePassthrough(),
            }
            | prompt
            | llm
            | fixing_parser
        )
        with get_openai_callback() as cb:
            cover_letter = chain.invoke({
                "company_name": new_state["company_name"],
                "current_latex_resume": new_state["current_latex_resume"],
                "company_job_description": new_state["company_job_description"],
                "generated_resume": new_state["generated_resume"],
            })
            new_state["metrics"]["total_tokens_used"] += cb.total_tokens
            new_state["metrics"]["completion_tokens"] += cb.completion_tokens
            new_state["metrics"]["prompt_tokens"] += cb.prompt_tokens
        new_state["cover_letter"] = cover_letter
        new_state["metrics"]["status"] = "cover_letter_generated"
    except Exception as e:
        new_state["error"] = f"Cover letter generation error: {str(e)}"
        new_state["metrics"]["status"] = "cover_letter_generation_failed"
    
    end_time = time.time()
    new_state["metrics"]["cover_letter_generation_time"] = end_time - start_time
    return new_state

def should_generate_cover_letter(state: ResumeState) -> str:
    """Router node to decide if cover letter should be generated."""
    if state.get("error"):
        return "end"
    if state.get("generated_resume") and state.get("generate_cover_letter", False):
        return "generate_cover_letter"
    else:
        return "end"

# --- Persistent Checkpointer Wrapper ---
# Create a wrapper class that never calls __exit__
class PersistentSqliteSaver:
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._cp_context = SqliteSaver.from_conn_string(db_path)
        self._instance = self._cp_context.__enter__()
    def __getattr__(self, attr):
        return getattr(self._instance, attr)

@st.cache_resource(show_spinner=False)
def get_persistent_checkpointer(db_path: str):
    return PersistentSqliteSaver(db_path)

# Build the Graph using a persistent SQLite checkpointer.
def build_resume_graph(checkpoint_directory="./checkpoints"):
    """Build the LangGraph for resume generation with persistent checkpoints."""
    os.makedirs(checkpoint_directory, exist_ok=True)
    db_path = os.path.join(checkpoint_directory, "resume_generation.db")
    checkpointer = get_persistent_checkpointer(db_path)
    
    workflow = StateGraph(ResumeState)
    workflow.add_node("process_inputs", process_inputs)
    workflow.add_node("generate_resume", generate_tailored_resume)
    workflow.add_node("generate_cover_letter", generate_tailored_cover_letter)
    
    workflow.add_edge("process_inputs", "generate_resume")
    workflow.add_conditional_edges(
        "generate_resume",
        should_generate_cover_letter,
        {"generate_cover_letter": "generate_cover_letter", "end": END}
    )
    workflow.add_edge("generate_cover_letter", END)
    workflow.set_entry_point("process_inputs")
    
    return workflow.compile(checkpointer=checkpointer)

# Wrapper functions for the main application.
def generate_resume_with_tracking(
    company_name: str, 
    current_latex_resume: str, 
    comprehensive_profile: str,
    company_job_description: str,
    generate_cover_letter: bool = False
) -> Dict:
    """Generate a resume with tracking via LangGraph using persistent checkpoints."""
    graph = build_resume_graph()
    
    # Create a configuration with a thread_id to satisfy the checkpointer requirements.
    default_config = {
        "configurable": {
            "thread_id": datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        }
    }
    
    initial_state = ResumeState({
        "company_name": company_name,
        "current_latex_resume": current_latex_resume,
        "comprehensive_profile": comprehensive_profile,
        "company_job_description": company_job_description,
        "generate_cover_letter": generate_cover_letter,
        "metrics": initialize_metrics()
    })
    
    # Invoke the graph with the configuration.
    final_state = graph.invoke(initial_state, config=default_config)
    
    result = {
        "generated_resume": final_state.get("generated_resume"),
        "cover_letter": final_state.get("cover_letter"),
        "error": final_state.get("error"),
        "metrics": final_state.get("metrics")
    }
    
    try:
        metrics_dir = "./metrics"
        os.makedirs(metrics_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        metrics_file = os.path.join(metrics_dir, f"generation_metrics_{timestamp}.json")
        with open(metrics_file, "w") as f:
            json.dump(final_state.get("metrics", {}), f, indent=2)
    except Exception as e:
        print(f"Error saving metrics: {str(e)}")
    
    return result

# Legacy wrapper functions for backward compatibility.
def generate_resume(
    company_name: str, current_latex_resume: str, comprehensive_profile: str, company_job_description: str
) -> str:
    """Legacy wrapper for resume generation."""
    result = generate_resume_with_tracking(
        company_name=company_name,
        current_latex_resume=current_latex_resume,
        comprehensive_profile=comprehensive_profile,
        company_job_description=company_job_description,
        generate_cover_letter=False
    )
    if result.get("error"):
        raise Exception(result["error"])
    return result["generated_resume"]

def generate_cover_letter(
    company_name: str,
    current_latex_resume: str,
    company_job_description: str,
    generated_resume: str,
) -> str:
    """Legacy wrapper for cover letter generation."""
    result = generate_resume_with_tracking(
        company_name=company_name,
        current_latex_resume=current_latex_resume,
        comprehensive_profile="{}",  # Not needed for cover letter
        company_job_description=company_job_description,
        generate_cover_letter=True
    )
    if result.get("error"):
        raise Exception(result["error"])
    return result["cover_letter"]
