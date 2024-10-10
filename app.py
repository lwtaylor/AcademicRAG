import streamlit as st
import openai
import os
import sys

# Get the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path of the 'backend' directory
backend_dir = os.path.join(current_dir, 'backend')

# Add the 'backend' directory to sys.path
sys.path.append(backend_dir)

# Import the module from the 'backend' directory
from retriever import llm_answer


st.title("Alama AI")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = llm_answer(prompt)
    print(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)