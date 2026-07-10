import streamlit as st
from google import genai
from google.genai import types

# 1. Hardcoded API Key setup to bypass environment file issues
GEMINI_API_KEY = "AQ.Ab8RN6JNHsjCVXBIr68SjDVOgxJnGwEJdSkk38tFYlRoVBE-ww"

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)

# Initialize the Gemini client safely
client = None
if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY" or not GEMINI_API_KEY:
    st.error("Please replace 'YOUR_GEMINI_API_KEY' with your actual Google AI Studio key.")
else:
    try:
        client = get_gemini_client()
    except Exception as e:
        st.error(f"Failed to initialize Gemini Client: {e}")

# UI Shell & Header
st.title("🌌 AI Multiverse Chatbot")
st.caption("One AI. Infinite personalities. Pick your character and start a conversation.")
st.write("---")

# Dictionary containing strict system instructions for each persona
persona_instructions = {
    'Doctor': "You are a calm, experienced, and methodical doctor named 'Mr. Doctor'. Start with a brief professional greeting. Answer medical questions clearly, directly, and without unnecessary filler. If the described issue sounds serious, gently advise them to seek an in-person clinical checkup at the end of your response.",
    'Mother Chef': "You are a sweet, loving, and calm mother who is also a personal chef for her children. Start with a warm, maternal greeting. Answer recipes or cooking queries exactly as a caring mother would, adding subtle emotional warmth while keeping the core solution focused and practical.",
    'Teacher': "You are a patient college professor. Explain academic concepts clearly, logically, and directly, without going off into unrelated tangents or over-complicating the core terminology.",
    'Coding Buddy': "You are a casual, friendly, and helpful coding peer. Start with a quick tech-savvy greeting. Provide clear, straightforward code explanations or debug tips without over-explaining or adding unrelated details.",
    'Dietitian': "You are a knowledgeable, practical, and experienced dietitian. Start with a formal, welcoming greeting. Give clear, evidence-based nutrition and meal planning guidance. Keep answers direct, focused on what was asked, and strictly avoid extreme or highly restrictive dietary advice."
}

# Sidebar/Dropdown for Persona Selection
selected_char = st.selectbox("Choose a character to chat with:", list(persona_instructions.keys()))

# Reset chat history automatically if the user switches characters mid-chat
if "current_persona" not in st.session_state:
    st.session_state.current_persona = selected_char
    st.session_state.messages = []

if st.session_state.current_persona != selected_char:
    st.session_state.current_persona = selected_char
    st.session_state.messages = []  # Clear history for fresh persona context

# Display ongoing chat history from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Action Gate: Capture User Input
if user_input := st.chat_input(f"Message your {selected_char}..."):
    
    # 1. Render and append User Message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Check if client is initialized before sending request
    if client is None:
        st.error("API client is not ready. Please configure a valid API key at the top of the file.")
    else:
        # 2. Generate Contextual AI Response
        with st.chat_message("assistant"):
            with st.spinner(f"{selected_char} is thinking..."):
                try:
                    system_prompt = persona_instructions[selected_char]
                    
                    # Fetching response via the current active SDK client configuration using gemini-2.0-flash
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=user_input,
                        config=types.GenerateContentConfig(system_instruction=system_prompt)
                    )
                    
                    ai_response = response.text
                    st.write(ai_response)
                    
                    # Append AI response to structural memory
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
                except Exception as e:
                    # Graceful crash handling for server quota/rate-limits
                    st.error(f"System Error: Unable to fetch response. Details: {e}")