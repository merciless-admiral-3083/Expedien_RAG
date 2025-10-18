from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.output_parsers import StrOutputParser
from tools.react_prompt_template import get_prompt_template
from tools.pdf_query_tools import indian_constitution_pdf_query, indian_laws_pdf_query
import warnings
import os
import streamlit as st

@st.cache_resource  # caches once per app session
def load_pdf_tools():
    from tools.pdf_query_tools import (
        indian_constitution_pdf_query_with_qa,
        indian_laws_pdf_query_with_qa,
    )
    return [indian_constitution_pdf_query_with_qa, indian_laws_pdf_query_with_qa]

@st.cache_resource(show_spinner=False)
def get_agent_executor(use_ollama: bool, ollama_model: str = "llama3.1:8b"):
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)

    if use_ollama:
        os.environ["USE_OLLAMA"] = "true"
        os.environ["OLLAMA_MODEL"] = ollama_model
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        LLM = ChatOllama(
            model=ollama_model,
            base_url=base_url,
            temperature=0.1,
            timeout=120,
        )
    else:
        os.environ["USE_OLLAMA"] = "false"
        LLM = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            timeout=30,
            max_tokens=1000,
        )

    tools = load_pdf_tools()
    prompt_template = get_prompt_template()

    agent_instance = create_react_agent(LLM, tools, prompt_template)

    agent_executor = AgentExecutor(
        agent=agent_instance,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3,  # lower to reduce response time
        early_stopping_method="generate",
        max_execution_time=60,
        return_intermediate_steps=True,
    )

    return agent_executor

def agent(query: str, use_ollama: bool = False, ollama_model: str = "llama3.1:8b"):
    try:
        agent_executor = get_agent_executor(use_ollama, ollama_model)
        result = agent_executor.invoke({"input": query})
        return result["output"]
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        # Fallback to simple call
        try:
            if use_ollama:
                base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
                LLM = ChatOllama(model=ollama_model, base_url=base_url, temperature=0.1, timeout=120)
            else:
                LLM = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1, timeout=30, max_tokens=1000)
            simple_response = LLM.invoke(f"Answer this legal question about Indian law: {query}")
            return simple_response.content
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            return f"Sorry, I encountered an error while processing your query: {str(e)}. Please try rephrasing your question."


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