import streamlit as st
import google.generativeai as genai
import os
import time
import tempfile

# --- UI Configuration ---
st.set_page_config(page_title="AI Peer Review Assistant", page_icon="📄", layout="wide")
st.title("📄 Automated Academic Peer-Review Assistant")
st.write("Upload a manuscript to generate a structured review, then ask follow-up questions.")

# --- API Configuration ---
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY environment variable not found. Please set it in your environment or Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# --- Session State Initialization ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "review_generated" not in st.session_state:
    st.session_state.review_generated = False
if "manuscript_name" not in st.session_state:
    st.session_state.manuscript_name = None

# --- Main App Execution ---
uploaded_file = st.file_uploader("Drop your PDF manuscript here", type=["pdf"])

if uploaded_file is not None and not st.session_state.review_generated:
    if st.button("Generate Peer Review"):
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            st.sidebar.info("Uploading PDF to Gemini...")
            manuscript = genai.upload_file(path=tmp_file_path, display_name="Uploaded_Manuscript")
            st.session_state.manuscript_name = manuscript.name
            
            with st.spinner("Processing document on Google's servers..."):
                while manuscript.state.name == 'PROCESSING':
                    time.sleep(2)
                    manuscript = genai.get_file(manuscript.name)

            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            
            st.session_state.chat_session = model.start_chat(
                history=[
                    {"role": "user", "parts": [manuscript]},
                ]
            )

            prompt = """
            You are an expert, rigorous academic peer reviewer for a high-impact engineering journal (e.g., Expert Systems with Applications).
            Thoroughly evaluate this manuscript, paying close attention to deep learning architectures, methodology, and data acquisition.
            Provide a highly structured review using exactly this format:
            ## 1. Executive Summary
            ## 2. Methodological Strengths
            ## 3. Major Concerns & Limitations
            ## 4. Minor Issues
            ## 5. Recommendation [Accept, Minor Revisions, Major Revisions, Reject]
            """
            
            st.sidebar.info("Generating expert review...")
            response = st.session_state.chat_session.send_message(prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.session_state.review_generated = True
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

# --- Interactive Chat UI ---
if st.session_state.review_generated:
    st.success("Document analyzed successfully! You can now ask highly specific technical questions about the methodology or data.")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("E.g., Does their AI model address the class imbalance in the dataset?"):
        st.chat_message("user").markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chat_session.send_message(user_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    if st.sidebar.button("Clear Memory & Upload New File"):
        if st.session_state.manuscript_name:
             genai.delete_file(st.session_state.manuscript_name)
        st.session_state.clear()
        st.rerun()
