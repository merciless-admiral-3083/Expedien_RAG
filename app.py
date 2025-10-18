from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import dotenv_values
import streamlit as st
from agent import agent, check_ollama_connection, get_available_ollama_models
import streamlit as st

st.set_page_config(
    page_title="VerdictAI",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded",
)
# Load environment variables
try:
    # Try to get secrets from Streamlit Cloud
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY", "")
except Exception:
    # Fallback to .env locally
    envs = dotenv_values(".env")
    GROQ_API_KEY = envs.get("GROQ_API_KEY", "")
    HUGGINGFACE_API_KEY = envs.get("HUGGINGFACE_API_KEY", "")

# Set environment variables
if GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Configure Streamlit


st.title("VerdictAI⚖️")

# Sidebar for LLM selection
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Check OLLAMA connection
    ollama_available = check_ollama_connection()
    
    if ollama_available:
        st.success("🟢 OLLAMA is running")
        available_models = get_available_ollama_models()
        
        llm_provider = st.radio(
            "Choose LLM Provider:",
            ["Groq (Cloud)", "OLLAMA (Local)"],
            help="Select between cloud-based Groq or local OLLAMA"
        )
        
        if llm_provider == "OLLAMA (Local)":
            if available_models:
                selected_model = st.selectbox(
                    "Select OLLAMA Model:",
                    available_models,
                    help="Choose from your locally installed OLLAMA models"
                )
            else:
                st.warning("No OLLAMA models found. Please install models using: `ollama pull <model_name>`")
                selected_model = st.text_input(
                    "Enter model name manually:",
                    value="llama3.1:8b",
                    help="Enter the OLLAMA model name (e.g., llama3.1:8b, mistral:7b)"
                )
    else:
        st.error("🔴 OLLAMA not running")
        st.info("To use local models, start OLLAMA server:\n```\nollama serve\n```")
        llm_provider = "Groq (Cloud)"
        selected_model = None
    
    # Display current configuration
    st.subheader("Current Config:")
    if llm_provider == "OLLAMA (Local)" and ollama_available:
        st.write(f"**Provider:** OLLAMA (Local)")
        st.write(f"**Model:** {selected_model}")
    else:
        st.write(f"**Provider:** Groq (Cloud)")
        st.write(f"**Model:** llama-3.3-70b-versatile")

# Main content
initial_msg = """
#### A Chatbot for all your Legal Queries👩‍⚖️
#### You can ask anything regarding the laws or constitution of India
"""
st.markdown(initial_msg)

# Initialize session state
if "store" not in st.session_state:
    st.session_state.store = []

store = st.session_state.store

# Display chat history
for message in store:
    if message.type == "ai":
        avatar = "👩‍⚖️"
    else:
        avatar = "🗨️"
    with st.chat_message(message.type, avatar=avatar):
        st.markdown(message.content)

# Chat input
if prompt := st.chat_input("What's your query?"):
    # Display user message
    st.chat_message("user", avatar="🗨️").markdown(prompt)
    
    # Show thinking message
    thinking_placeholder = st.chat_message("assistant", avatar="⚖️")
    thinking_placeholder.markdown("Thinking...")
    
    # Add user message to store
    store.append(HumanMessage(content=prompt))
    
    try:
        # Determine which LLM to use
        use_ollama = (llm_provider == "OLLAMA (Local)" and ollama_available)
        
        if use_ollama:
            response_content = agent(prompt, use_ollama=True, ollama_model=selected_model)
        else:
            # Check if Groq API key is available
            if not GROQ_API_KEY:
                response_content = "Sorry, no API key found for Groq and OLLAMA is not available. Please set GROQ_API_KEY or start OLLAMA server."
            else:
                response_content = agent(prompt, use_ollama=False)
        
        response = AIMessage(content=response_content)
        
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        if "API" in str(e).upper():
            error_msg += "\n\nThis might be due to API limits. Try using OLLAMA for local processing."
        response = AIMessage(content=error_msg)
    
    # Add response to store
    store.append(response)
    
    # Update the thinking message with actual response
    thinking_placeholder.markdown(response.content)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
        💡 Thank you for using VerdictAI!
    </div>
    """, 
    unsafe_allow_html=True
)
