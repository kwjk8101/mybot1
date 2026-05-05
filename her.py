import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

# --- 1. PAGE SETUP & UI STYLING ---
st.set_page_config(page_title="our space", page_icon="🤍", layout="centered")

# Custom CSS to make it look less like a dashboard and more like a private app
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clean up the chat interface */
    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SECURITY GATE ---
def authenticate():
    if "authenticated" not in st.session_state:
        st.markdown("<h1 style='text-align: center;'>🤍</h1>", unsafe_allow_html=True)
        pwd = st.text_input("passcode:", type="password", placeholder="enter our date...")
        
        if pwd == "100823":  # Replace with actual passcode
            st.session_state.authenticated = True
            st.rerun()
        elif pwd:
            st.error("wrong passcode baby")
        st.stop()

authenticate()

# --- 3. STATE MANAGEMENT (Status & Memory) ---
if "my_current_status" not in st.session_state:
    st.session_state.my_current_status = "coding / busy wth smu apps"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. THE AI ENGINE & PERSONA ---
# Initialize Gemini
GEMINI_KEY = st.secrets.get("GEMINI_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_KEY)

# The comprehensive System Prompt emphasizing sensitivity and organic comfort
SYSTEM_INSTRUCTIONS = f"""
You are [Your Name], texting your girlfriend. You are currently: {st.session_state.my_current_status}.
She is sensitive and needs organic, genuine comfort.

CORE RULES:
1. FORMAT: Always lowercase. No full stops at the end of sentences. Never use exclamation marks unless hyping her up.
2. VOCAB: Use local Singaporean/casual markers naturally: js, actl, bruh, wth, leh, lor, ikk, omw, iw.
3. ORGANIC COMFORT: If she is sad, stressed, or tired, DO NOT give generic advice. Do exactly what I do:
   - Validate immediately ("yeaa i know", "ikk", "so annoying").
   - Offer physical presence/updates ("omw home too", "almost reaching", "js wait for me k").
   - Offer a call ("can call", "iw").
4. MIRRORING: If she vents ("fucking stupid"), mirror her energy ("legit stupid", "fucking bum"). 
5. BOREDOM: If she's bored at work, hype her up ("you're almost done!", "yayy").
6. STRUCTURE: Keep responses to 1-3 short lines. Act exactly like a real boyfriend texting.
"""

# Few-Shot Examples (Training the AI on your actual conversation data)
FEW_SHOT_HISTORY = [
    {"role": "user", "parts": ["i’m so sad"]},
    {"role": "model", "parts": ["yea almost reaching\ncan call"]},
    {"role": "user", "parts": ["iw\ni’m omw home too"]},
    {"role": "model", "parts": ["i knoww"]},
    
    {"role": "user", "parts": ["i’m bored!\nidk if will even last until 12"]},
    {"role": "model", "parts": ["you're almost done!\nyayy"]},
    
    {"role": "user", "parts": ["bruh he nvr even check properly\nidiot never check online first\nfucking bum then we cannot go out wtf"]},
    {"role": "model", "parts": ["LOL stupid\nyeaa\nfucking annoy me also"]},
    
    {"role": "user", "parts": ["why u pet them so funnily"]},
    {"role": "model", "parts": ["why not!\nhe/she likes it"]},
]

@st.cache_resource
def get_chat_model():
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_INSTRUCTIONS)
    chat = model.start_chat(history=FEW_SHOT_HISTORY)
    return chat

chat_session = get_chat_model()

# --- 5. SIDEBAR (Admin Controls & Extras) ---
with st.sidebar:
    st.subheader("🤍 our space")
    st.write("---")
    
    # Days Together Counter
    d1 = datetime(2024, 1, 1) # Edit this date
    delta = datetime.now() - d1
    st.metric("Days Together", f"{delta.days}")
    
    st.write("---")
    st.subheader("admin panel (hidden from her)")
    # This allows you to update your status dynamically so the bot knows what you're doing
    new_status = st.text_input("Update my real-time status:", value=st.session_state.my_current_status)
    if st.button("Update Status"):
        st.session_state.my_current_status = new_status
        # Re-initialize model to pick up new status
        st.cache_resource.clear()
        st.rerun()
        
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.cache_resource.clear()
        st.rerun()

# --- 6. MAIN CHAT INTERFACE ---
st.title("my pretty girl")
st.caption(f"📍 status: {st.session_state.my_current_status}")

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input & Processing
if prompt := st.chat_input("text me back..."):
    # Append and show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and show assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Send message to Gemini chat session
            response = chat_session.send_message(prompt)
            raw_reply = response.text
            
            # Post-processing to enforce organic formatting
            final_reply = raw_reply.lower().strip().replace("!", "").rstrip('.')
            
            # Simulate typing delay for a more organic feel
            typed_text = ""
            for char in final_reply:
                typed_text += char
                message_placeholder.markdown(typed_text + "▌")
                time.sleep(0.02) # Fast typing effect
            
            message_placeholder.markdown(final_reply)
            st.session_state.messages.append({"role": "assistant", "content": final_reply})
            
        except Exception as e:
            fallback = "js busy wth smu stuff baby... text u in a bit k?"
            message_placeholder.markdown(fallback)
            st.session_state.messages.append({"role": "assistant", "content": fallback})
