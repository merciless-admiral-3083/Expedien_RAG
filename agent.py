from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.output_parsers import StrOutputParser
from tools.react_prompt_template import get_prompt_template
from tools.pdf_query_tools import indian_constitution_pdf_query, indian_laws_pdf_query
import warnings
import os


def agent(query: str, use_ollama: bool = False, ollama_model: str = "llama3.1:8b"):
    """
    Create and run an agent with either Groq or OLLAMA LLM
    
    Args:
        query (str): The user's query
        use_ollama (bool): Whether to use OLLAMA instead of Groq
        ollama_model (str): OLLAMA model to use (default: llama3.1:8b)
    """
    warnings.filterwarnings("ignore", category=FutureWarning)

    # Set environment variables for PDF tools to use the same LLM choice
    if use_ollama:
        os.environ["USE_OLLAMA"] = "true"
        os.environ["OLLAMA_MODEL"] = ollama_model
        # Support Docker OLLAMA or local OLLAMA
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        # Use OLLAMA for local LLM
        LLM = ChatOllama(
            model=ollama_model,
            base_url=base_url,
            temperature=0.1,
            timeout=120,  # Increase timeout for local models
        )
        print(f"Using OLLAMA model: {ollama_model} at {base_url}")
    else:
        os.environ["USE_OLLAMA"] = "false"
        # Use Groq for cloud LLM
        LLM = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            timeout=30,  # Add timeout for Groq
            max_tokens=1000  # Limit response length
        )
        print("Using Groq model: llama-3.3-70b-versatile")

    # Import tools with error handling
    try:
        from tools.pdf_query_tools import (
            indian_constitution_pdf_query_with_qa,
            indian_laws_pdf_query_with_qa,
        )
        tools = [indian_constitution_pdf_query_with_qa, indian_laws_pdf_query_with_qa]
    except ImportError as e:
        print(f"Warning: Could not import QA tools: {e}")
        # Fallback to basic tools
        tools = [indian_constitution_pdf_query, indian_laws_pdf_query]

    prompt_template = get_prompt_template()

    agent = create_react_agent(
        LLM,
        tools,
        prompt_template
    )

    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,  # Enable verbose for debugging
        handle_parsing_errors=True,
        max_iterations=5,  # Reduce iterations to prevent infinite loops
        early_stopping_method="generate",
        max_execution_time=60,  # Add 60-second timeout
        return_intermediate_steps=True
    )

    try:
        result = agent_executor.invoke({"input": query})
        return result["output"]
    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        print(error_msg)
        
        # Fallback: try simple LLM call without tools
        try:
            print("Attempting fallback with simple LLM call...")
            simple_response = LLM.invoke(f"Answer this legal question about Indian law: {query}")
            return simple_response.content
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            return f"Sorry, I encountered an error while processing your query: {str(e)}. Please try rephrasing your question or check your internet connection."


def get_available_ollama_models():
    """
    Get list of available OLLAMA models
    """
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        else:
            return []
    except Exception as e:
        print(f"Could not connect to OLLAMA: {e}")
        return []


def check_ollama_connection():
    """
    Check if OLLAMA is running and accessible
    """
    try:
        import requests
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        return response.status_code == 200
    except:
        return False