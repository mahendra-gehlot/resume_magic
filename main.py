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

# Custom modules for specific functionality
from data_processing.fetch_tex import read_latex_file
from scarp_job_description.scarping_method import get_job_text
from data_processing.save_results import save_tex
from data_processing.output_parser import LaTeXResumeParser
from prompt_templates import current_prompt_v3 as resume_template_latest
from prompt_templates import cover_letter_template

# LangGraph components for workflow management
from langgraph.graph import END, StateGraph
# Use the SQLite-based persistent checkpointer for state persistence
from langgraph.checkpoint.sqlite import SqliteSaver

# Load environment variables from .env file
load_dotenv()


def read_json_file(file_path: str) -> str:
    """
    Reads a JSON file and returns its content as a string.
    
    Args:
        file_path (str): Path to the JSON file to be read
        
    Returns:
        str: Content of the JSON file as a string
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        IOError: If there's an error reading the file
    """
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
    """
    State dictionary for the resume generation process.
    Stores all data needed throughout the workflow.
    """
    company_name: str
    current_latex_resume: str
    comprehensive_profile: str
    company_job_description: str
    generated_resume: str = None
    cover_letter: str = None
    error: str = None
    metrics: Dict = None


def initialize_metrics() -> Dict:
    """
    Initialize tracking metrics for the resume generation process.
    
    Returns:
        Dict: Dictionary with initialized metrics for tracking performance
    """
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
    """
    Process and validate input data for resume generation.
    
    Args:
        state (ResumeState): Current state with input data
        
    Returns:
        ResumeState: Updated state with validation results and initialized metrics
    """
    new_state = state.copy()
    
    # Validate required inputs
    if not new_state.get("company_name"):
        new_state["error"] = "Company name is required"
        return new_state
    
    if not new_state.get("company_job_description"):
        new_state["error"] = "Job description is required"
        return new_state
    
    # Initialize metrics if not already present
    if not new_state.get("metrics"):
        new_state["metrics"] = initialize_metrics()
        
    new_state["metrics"]["status"] = "inputs_processed"
    return new_state


def generate_tailored_resume(state: ResumeState) -> ResumeState:
    """
    Generate a tailored resume based on the job description.
    
    Args:
        state (ResumeState): Current state with processed inputs
        
    Returns:
        ResumeState: Updated state with generated resume and performance metrics
    """
    import time
    new_state = state.copy()
    
    # Skip if there were earlier errors
    if new_state.get("error"):
        return new_state
    
    start_time = time.time()
    
    try:
        # Initialize the language model
        llm = ChatOpenAI(
            temperature=0.25,
            model_name="gpt-4o-mini",
            api_key=os.environ["OPENAI_API_KEY"],
        )
        
        # Set up the prompt template for resume generation
        prompt = PromptTemplate(
            template=resume_template_latest,
            input_variables=[
                "company_name",
                "current_latex_resume",
                "comprehensive_profile_json",
                "company_job_description",
            ],
        )
        
        # Configure output parsing
        parser = LaTeXResumeParser()
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        from langchain.callbacks import get_openai_callback
        
        # Build the LangChain pipeline
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
        
        # Execute chain with token usage tracking
        with get_openai_callback() as cb:
            customized_resume = chain.invoke({
                "company_name": new_state["company_name"],
                "current_latex_resume": new_state["current_latex_resume"],
                "comprehensive_profile_json": new_state["comprehensive_profile"],
                "company_job_description": new_state["company_job_description"],
            })
            # Update metrics with token usage
            new_state["metrics"]["total_tokens_used"] += cb.total_tokens
            new_state["metrics"]["completion_tokens"] += cb.completion_tokens
            new_state["metrics"]["prompt_tokens"] += cb.prompt_tokens
            new_state["metrics"]["model_name"] = "gpt-4o-mini"
            
        new_state["generated_resume"] = customized_resume
        new_state["metrics"]["status"] = "resume_generated"
        
    except Exception as e:
        new_state["error"] = f"Resume generation error: {str(e)}"
        new_state["metrics"]["status"] = "resume_generation_failed"
    
    # Calculate and record generation time
    end_time = time.time()
    new_state["metrics"]["resume_generation_time"] = end_time - start_time
    return new_state


def generate_tailored_cover_letter(state: ResumeState) -> ResumeState:
    """
    Generate a tailored cover letter based on the resume and job description.
    
    Args:
        state (ResumeState): Current state with generated resume
        
    Returns:
        ResumeState: Updated state with generated cover letter and performance metrics
    """
    import time
    new_state = state.copy()
    
    # Skip if there were errors or no resume was generated
    if new_state.get("error") or not new_state.get("generated_resume"):
        return new_state
    
    start_time = time.time()
    
    try:
        # Initialize the language model
        llm = ChatOpenAI(
            temperature=0.3,
            model_name="gpt-4o-mini",
            api_key=os.environ["OPENAI_API_KEY"],
        )
        
        # Set up the prompt template for cover letter generation
        prompt = PromptTemplate(
            template=cover_letter_template,
            input_variables=[
                "company_name",
                "current_latex_resume",
                "company_job_description",
                "generated_resume",
            ],
        )
        
        # Configure output parsing
        parser = LaTeXResumeParser()
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        from langchain.callbacks import get_openai_callback
        
        # Build the LangChain pipeline
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
        
        # Execute chain with token usage tracking
        with get_openai_callback() as cb:
            cover_letter = chain.invoke({
                "company_name": new_state["company_name"],
                "current_latex_resume": new_state["current_latex_resume"],
                "company_job_description": new_state["company_job_description"],
                "generated_resume": new_state["generated_resume"],
            })
            # Update metrics with token usage
            new_state["metrics"]["total_tokens_used"] += cb.total_tokens
            new_state["metrics"]["completion_tokens"] += cb.completion_tokens
            new_state["metrics"]["prompt_tokens"] += cb.prompt_tokens
            
        new_state["cover_letter"] = cover_letter
        new_state["metrics"]["status"] = "cover_letter_generated"
        
    except Exception as e:
        new_state["error"] = f"Cover letter generation error: {str(e)}"
        new_state["metrics"]["status"] = "cover_letter_generation_failed"
    
    # Calculate and record generation time
    end_time = time.time()
    new_state["metrics"]["cover_letter_generation_time"] = end_time - start_time
    return new_state


def should_generate_cover_letter(state: ResumeState) -> str:
    """
    Router node to decide if cover letter should be generated.
    
    Args:
        state (ResumeState): Current state after resume generation
        
    Returns:
        str: Next node to execute ("generate_cover_letter" or "end")
    """
    if state.get("error"):
        return "end"
    if state.get("generated_resume") and state.get("generate_cover_letter", False):
        return "generate_cover_letter"
    else:
        return "end"


# --- Persistent Checkpointer Wrapper ---
class PersistentSqliteSaver:
    """
    Wrapper for SqliteSaver that maintains an open connection.
    Prevents the context manager from closing the database connection.
    """
    def __init__(self, db_path: str):
        """
        Initialize the persistent saver with a database path.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self._db_path = db_path
        self._cp_context = SqliteSaver.from_conn_string(db_path)
        self._instance = self._cp_context.__enter__()
        
    def __getattr__(self, attr):
        """
        Delegate attribute access to the underlying SqliteSaver instance.
        
        Args:
            attr: Attribute name to access
            
        Returns:
            The requested attribute from the SqliteSaver instance
        """
        return getattr(self._instance, attr)


@st.cache_resource(show_spinner=False)
def get_persistent_checkpointer(db_path: str):
    """
    Get or create a persistent checkpointer instance.
    Uses Streamlit's caching to maintain a single instance.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        PersistentSqliteSaver: A persistent SQLite checkpointer
    """
    return PersistentSqliteSaver(db_path)


def build_resume_graph(checkpoint_directory="./checkpoints"):
    """
    Build the LangGraph for resume generation with persistent checkpoints.
    
    Args:
        checkpoint_directory (str): Directory to store checkpoint database
        
    Returns:
        Compiled StateGraph: Ready-to-use workflow graph with checkpointing
    """
    # Ensure checkpoint directory exists
    os.makedirs(checkpoint_directory, exist_ok=True)
    db_path = os.path.join(checkpoint_directory, "resume_generation.db")
    checkpointer = get_persistent_checkpointer(db_path)
    
    # Create the workflow graph
    workflow = StateGraph(ResumeState)
    
    # Add nodes (processing steps)
    workflow.add_node("process_inputs", process_inputs)
    workflow.add_node("generate_resume", generate_tailored_resume)
    workflow.add_node("generate_cover_letter", generate_tailored_cover_letter)
    
    # Add edges (connections between steps)
    workflow.add_edge("process_inputs", "generate_resume")
    workflow.add_conditional_edges(
        "generate_resume",
        should_generate_cover_letter,
        {"generate_cover_letter": "generate_cover_letter", "end": END}
    )
    workflow.add_edge("generate_cover_letter", END)
    
    # Set the entry point
    workflow.set_entry_point("process_inputs")
    
    # Compile and return the graph with checkpointing
    return workflow.compile(checkpointer=checkpointer)


def generate_resume_with_tracking(
    company_name: str, 
    current_latex_resume: str, 
    comprehensive_profile: str,
    company_job_description: str,
    generate_cover_letter: bool = False
) -> Dict:
    """
    Generate a resume with tracking via LangGraph using persistent checkpoints.
    
    Args:
        company_name (str): Name of the target company
        current_latex_resume (str): Current LaTeX resume content
        comprehensive_profile (str): JSON string with comprehensive profile information
        company_job_description (str): Job description text
        generate_cover_letter (bool): Whether to generate a cover letter
        
    Returns:
        Dict: Results including generated content, errors, and performance metrics
    """
    # Build the workflow graph
    graph = build_resume_graph()
    
    # Create a configuration with a unique thread_id for checkpointing
    default_config = {
        "configurable": {
            "thread_id": datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        }
    }
    
    # Prepare the initial state
    initial_state = ResumeState({
        "company_name": company_name,
        "current_latex_resume": current_latex_resume,
        "comprehensive_profile": comprehensive_profile,
        "company_job_description": company_job_description,
        "generate_cover_letter": generate_cover_letter,
        "metrics": initialize_metrics()
    })
    
    # Execute the graph with the configuration
    final_state = graph.invoke(initial_state, config=default_config)
    
    # Prepare the result dictionary
    result = {
        "generated_resume": final_state.get("generated_resume"),
        "cover_letter": final_state.get("cover_letter"),
        "error": final_state.get("error"),
        "metrics": final_state.get("metrics")
    }
    
    # Save metrics to file for analysis
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


def generate_resume(
    company_name: str, 
    current_latex_resume: str, 
    comprehensive_profile: str, 
    company_job_description: str
) -> str:
    """
    Legacy wrapper for resume generation.
    Maintains backward compatibility with older code.
    
    Args:
        company_name (str): Name of the target company
        current_latex_resume (str): Current LaTeX resume content
        comprehensive_profile (str): JSON string with comprehensive profile information
        company_job_description (str): Job description text
        
    Returns:
        str: Generated LaTeX resume content
        
    Raises:
        Exception: If an error occurs during generation
    """
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
    """
    Legacy wrapper for cover letter generation.
    Maintains backward compatibility with older code.
    
    Args:
        company_name (str): Name of the target company
        current_latex_resume (str): Current LaTeX resume content
        company_job_description (str): Job description text
        generated_resume (str): Generated resume content
        
    Returns:
        str: Generated cover letter content
        
    Raises:
        Exception: If an error occurs during generation
    """
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