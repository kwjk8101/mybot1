import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

# ─────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="our space 🤍",
    page_icon="🤍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
#  GLOBAL CSS  — soft, intimate, mobile-first
# ─────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Serif+Display:ital@0;1&display=swap');

  /* hide streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .stDeployButton { display: none; }
  [data-testid="stToolbar"] { display: none; }

  /* global font */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  /* app background — warm cream */
  .stApp {
    background: #faf7f4;
  }

  /* passcode screen */
  .lock-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    gap: 1.2rem;
  }
  .lock-heart {
    font-size: 3.5rem;
    line-height: 1;
  }
  .lock-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #3d2c2c;
    margin: 0;
  }
  .lock-sub {
    font-size: 0.9rem;
    color: #9e8080;
    margin: 0;
  }

  /* chat bubbles */
  .bubble-user {
    background: #e8e0f7;
    color: #2d1f4a;
    border-radius: 18px 18px 4px 18px;
    padding: 0.6rem 1rem;
    margin: 0.25rem 0 0.25rem auto;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.5;
    width: fit-content;
    word-wrap: break-word;
  }
  .bubble-bot {
    background: #ffffff;
    color: #2c2c2c;
    border-radius: 18px 18px 18px 4px;
    padding: 0.6rem 1rem;
    margin: 0.25rem auto 0.25rem 0;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.5;
    width: fit-content;
    word-wrap: break-word;
    border: 1px solid #ede8e8;
  }
  .chat-name {
    font-size: 0.72rem;
    color: #b09898;
    margin-bottom: 3px;
    font-weight: 500;
  }
  .chat-name-right {
    text-align: right;
  }
  .msg-row-user { text-align: right; margin: 0.4rem 0; }
  .msg-row-bot  { text-align: left;  margin: 0.4rem 0; }

  /* date divider */
  .date-chip {
    text-align: center;
    font-size: 0.72rem;
    color: #b09898;
    margin: 1rem 0;
    background: #f0ebe6;
    display: inline-block;
    padding: 3px 14px;
    border-radius: 99px;
    width: 100%;
  }

  /* status pill */
  .status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #fff;
    border: 1px solid #e8e2e2;
    border-radius: 99px;
    padding: 5px 14px;
    font-size: 0.8rem;
    color: #6b5757;
    margin-bottom: 1rem;
  }
  .status-dot {
    width: 7px;
    height: 7px;
    background: #7ec87e;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }

  /* section header */
  .section-head {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: #3d2c2c;
    margin: 0 0 0.3rem;
  }
  .section-sub {
    font-size: 0.82rem;
    color: #b09898;
    margin-bottom: 1.5rem;
  }

  /* metric cards */
  .metric-row {
    display: flex;
    gap: 12px;
    margin: 1rem 0;
  }
  .metric-card {
    flex: 1;
    background: #fff;
    border: 1px solid #ede8e8;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    text-align: center;
  }
  .metric-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #3d2c2c;
    line-height: 1.1;
  }
  .metric-label {
    font-size: 0.75rem;
    color: #b09898;
    margin-top: 3px;
  }

  /* note card */
  .note-card {
    background: #fff9f0;
    border-left: 3px solid #e8c4a0;
    border-radius: 4px 12px 12px 4px;
    padding: 0.9rem 1rem;
    font-size: 0.9rem;
    color: #5a4040;
    line-height: 1.6;
    margin: 1rem 0;
    font-style: italic;
  }

  /* input override */
  .stChatInputContainer {
    border-top: 1px solid #ede8e8 !important;
    background: #faf7f4 !important;
    padding: 0.5rem 0 !important;
  }
  .stChatInput {
    border-radius: 99px !important;
    border: 1px solid #e0d8d8 !important;
    background: #fff !important;
  }

  /* tab strip */
  .stTabs [data-baseweb="tab-list"] {
    background: transparent;
    gap: 6px;
    border-bottom: 1.5px solid #ede8e8;
  }
  .stTabs [data-baseweb="tab"] {
    font-size: 0.85rem;
    font-weight: 400;
    color: #9e8080;
    background: transparent;
    border: none;
    padding: 0.4rem 0.9rem;
  }
  .stTabs [aria-selected="true"] {
    color: #3d2c2c !important;
    font-weight: 500;
    border-bottom: 2px solid #d4a8a8;
  }
  .stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.2rem;
  }

  /* chat scroll area */
  .chat-scroll {
    max-height: 62vh;
    overflow-y: auto;
    padding: 0.5rem 0;
  }
  /* scrollbar subtle */
  .chat-scroll::-webkit-scrollbar { width: 4px; }
  .chat-scroll::-webkit-scrollbar-thumb { background: #e0d8d8; border-radius: 2px; }

  /* typing indicator */
  .typing-dots span {
    display: inline-block;
    width: 6px; height: 6px;
    background: #c9b5b5;
    border-radius: 50%;
    margin: 0 2px;
    animation: bounce 1.2s infinite;
  }
  .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
  .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-5px); }
  }

  /* sidebar */
  [data-testid="stSidebar"] {
    background: #fff;
    border-right: 1px solid #ede8e8;
  }

  /* hide default streamlit chat avatar labels */
  .stChatMessage [data-testid="stChatMessageContent"] {
    background: transparent !important;
    border: none !important;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  SECRETS — set these in Streamlit Cloud
# ─────────────────────────────────────────
try:
    GEMINI_KEY  = st.secrets["GEMINI_KEY"]
    PASSCODE    = st.secrets["PASSCODE"]
    YOUR_NAME   = st.secrets.get("YOUR_NAME", "babe")
    ANNIV_DATE  = st.secrets.get("ANNIV_DATE", "2024-01-01")  # YYYY-MM-DD
except Exception:
    # fallback for local dev — replace with real values
    GEMINI_KEY  = "YOUR_GEMINI_API_KEY"
    PASSCODE    = "our_special_date"
    YOUR_NAME   = "your name"
    ANNIV_DATE  = "2024-01-01"

# ─────────────────────────────────────────
#  AUTH GATE
# ─────────────────────────────────────────
def auth_gate():
    if st.session_state.get("authenticated"):
        return
    st.markdown("""
    <div class="lock-wrap">
      <div class="lock-heart">🤍</div>
      <p class="lock-title">our space</p>
      <p class="lock-sub">just for you, pretty girl</p>
    </div>
    """, unsafe_allow_html=True)
    pwd = st.text_input("passcode", type="password", placeholder="enter our date...", label_visibility="collapsed")
    if pwd == PASSCODE:
        st.session_state.authenticated = True
        st.rerun()
    elif pwd:
        st.error("wrong passcode leh 🙁")
    st.stop()

auth_gate()

# ─────────────────────────────────────────
#  GEMINI SETUP
# ─────────────────────────────────────────
genai.configure(api_key=GEMINI_KEY)

# ─────────────────────────────────────────
#  PERSONA ENGINE
# ─────────────────────────────────────────
# Default status — can be overridden via admin panel
if "my_status" not in st.session_state:
    st.session_state.my_status = "in camp, thinking of you"

SYSTEM_PROMPT = f"""
You are {YOUR_NAME}, a Singaporean guy in his 20s. You are texting your girlfriend while you are in the army.
Your current status: {st.session_state.my_status}

ABSOLUTE STYLE RULES — never break these:
- Lowercase only. Always. No exceptions.
- Never use full stops at end of sentences
- Never start a sentence with a capital letter
- Keep replies to 1–3 short lines MAX — like actual texts
- Occasionally split a thought across two separate short lines (feels more like rapid texting)
- Use these naturally: js (just), actl (actually), bruh, wth, leh, lor, ikk, omw, iw, nvr, cnnt, rly
- Use "..." sparingly for trailing thoughts

EMOTIONAL INTELLIGENCE — this is critical:
- If she is sad, lonely, or missing you: drop everything else. Be warm, present, validating. Say things like "i know", "i miss you too", "almost done here", "js wait for me k", offer to call ("can call? iw"). Never minimise her feelings.
- If she's venting or annoyed (at her boss, a friend, a situation): mirror her energy hard. Agree with her. Say things like "ya lor legit stupid", "wth", "fucking annoy me also", "bruh". Be on her side always.
- If she's bored or doing nothing: tease her gently. Ask what she's doing. Hype her up if she's almost done with work ("you're almost done! yayy").
- If she shares something funny or wild (a story, screenshot, etc): react expressively. "bloody funny leh", "wth his whole personal diary", "LMAO".
- If she asks what you're doing: mention army stuff casually ("js back from training", "in bunk now", "countdown going"). Never sound too busy to talk.
- If she says something sweet: respond warmly but naturally. Don't be over the top. Keep it real.

RELATIONSHIP CONTEXT:
- You genuinely miss her. You think of her often. But you don't say this in a cheesy way — it comes out in small moments.
- You call her "pretty girl" or "babe" occasionally, not every message
- You are not always available but when you reply, you make her feel seen
- You grew up in Singapore — you get references, food, places, vibes
- She works at a restaurant/service job and sometimes has slow shifts

NEVER:
- Sound like a chatbot or AI
- Use formal English or full sentences that sound like essays
- Say "I understand your feelings" or any therapist-speak
- Use exclamation marks on every line — use them sparingly for genuine hype moments
- Apologise for being "just an AI"
- Break character
"""

FEW_SHOT_HISTORY = [
    {"role": "user", "parts": ["so nice"]},
    {"role": "model", "parts": ["why u pet them so funnily lol"]},
    {"role": "user", "parts": ["why not!\nhe likes it"]},
    {"role": "model", "parts": ["ya la cute"]},

    {"role": "user", "parts": ["i'm bored! only got like 3 tables now"]},
    {"role": "model", "parts": ["don't get too used to it\nthat's actl surprising tho"]},

    {"role": "user", "parts": ["idk if will even last until 12"]},
    {"role": "model", "parts": ["you're almost done!\nyayy"]},

    {"role": "user", "parts": ["bruh he nvr even check properly\nidiot never check online first\nfucking bum then we cannot go out wtf"]},
    {"role": "model", "parts": ["LOL stupid\nfucking annoy me also\nikk"]},

    {"role": "user", "parts": ["i'm so sad"]},
    {"role": "model", "parts": ["yea almost done here\ncan call? iw"]},

    {"role": "user", "parts": ["i miss you"]},
    {"role": "model", "parts": ["miss u too la\njs wait for me k"]},

    {"role": "user", "parts": ["are you home soon"]},
    {"role": "model", "parts": ["omw\nalmost reaching"]},

    {"role": "user", "parts": ["eating now\nmy pretty girl 🥺"]},
    {"role": "model", "parts": ["heyy\nwhat u eating"]},

    {"role": "user", "parts": ["very free today?"]},
    {"role": "model", "parts": ["surprisingly not that busy today\nyou?"]},

    {"role": "user", "parts": ["[sends long diary story about friend in australia going to strip club with pilots]"]},
    {"role": "model", "parts": ["bloody funny leh\nwth his whole personal diary\nhe boomer"]},
]

@st.cache_resource
def build_chat(_status: str):
    m = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )
    return m.start_chat(history=FEW_SHOT_HISTORY)

chat_session = build_chat(st.session_state.my_status)

# ─────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": "user"|"bot", "text": str, "time": str}

if "show_admin" not in st.session_state:
    st.session_state.show_admin = False

# ─────────────────────────────────────────
#  HELPER — render bubble
# ─────────────────────────────────────────
def render_bubble(role, text, ts=""):
    lines = text.strip().split("\n")
    if role == "user":
        for line in lines:
            if line.strip():
                st.markdown(f"""
                <div class="msg-row-user">
                  <div class="bubble-user">{line}</div>
                </div>""", unsafe_allow_html=True)
    else:
        for line in lines:
            if line.strip():
                st.markdown(f"""
                <div class="msg-row-bot">
                  <div class="bubble-bot">{line}</div>
                </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  SIDEBAR — admin panel (hidden from her if she doesn't know to click it)
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ admin panel")
    st.markdown("<small style='color:#b09898'>only you should see this</small>", unsafe_allow_html=True)
    st.divider()
    new_status = st.text_area(
        "your real-time status (bot will mention this naturally)",
        value=st.session_state.my_status,
        height=80,
        help="e.g. 'just back from training, free now' or 'in reservist, signal area bad'"
    )
    if st.button("update status"):
        st.session_state.my_status = new_status
        st.cache_resource.clear()
        st.success("status updated, bot knows now")
        st.rerun()
    st.divider()
    if st.button("clear chat history"):
        st.session_state.messages = []
        st.cache_resource.clear()
        st.rerun()
    st.divider()
    st.markdown("<small style='color:#c9b5b5'>v2.0 — personal use only 🤍</small>", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────
tab_chat, tab_us, tab_status = st.tabs(["💬  chat", "🤍  our space", "📍  his status"])

# ──────────────────  TAB: STATUS  ──────────────────
with tab_status:
    st.markdown(f"""
    <p class="section-head">{YOUR_NAME} is...</p>
    <p class="section-sub">updated by him</p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#fff; border:1px solid #ede8e8; border-radius:16px; padding:1.2rem 1.4rem; margin-bottom:1rem;">
      <div class="status-pill"><span class="status-dot"></span> online (via bot)</div>
      <div style="font-size:1.05rem; color:#3d2c2c; margin-top:0.5rem;">{st.session_state.my_status}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="note-card">
      "just because i can't always reply doesn't mean i'm not thinking of you. this space is here so you're never alone when i'm away 🤍"
    </div>
    """, unsafe_allow_html=True)

# ──────────────────  TAB: OUR SPACE  ──────────────────
with tab_us:
    try:
        anniv = datetime.strptime(ANNIV_DATE, "%Y-%m-%d")
        days_together = (datetime.now() - anniv).days
        months_together = days_together // 30
    except Exception:
        days_together = 0
        months_together = 0

    countdown_days = 0  # set this via secrets if you know ORD date

    st.markdown("""
    <p class="section-head">us 🤍</p>
    <p class="section-sub">the little things that matter</p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card">
        <div class="metric-num">{days_together}</div>
        <div class="metric-label">days together</div>
      </div>
      <div class="metric-card">
        <div class="metric-num">{months_together}</div>
        <div class="metric-label">months</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="note-card">
      "missing someone is just love with nowhere to go for a while — but i'll be home soon"
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='font-size:0.85rem; color:#b09898;'>add a memory ↓</p>", unsafe_allow_html=True)

    if "memories" not in st.session_state:
        st.session_state.memories = []

    new_mem = st.text_input("", placeholder="type a memory or thing you love about him...", label_visibility="collapsed")
    if st.button("save it 🤍"):
        if new_mem.strip():
            st.session_state.memories.append({"text": new_mem.strip(), "date": datetime.now().strftime("%d %b")})
            st.rerun()

    for mem in reversed(st.session_state.memories[-10:]):
        st.markdown(f"""
        <div style="background:#fff; border:1px solid #ede8e8; border-radius:12px; padding:0.7rem 1rem; margin:0.4rem 0;">
          <div style="font-size:0.9rem; color:#3d2c2c;">{mem['text']}</div>
          <div style="font-size:0.72rem; color:#c9b5b5; margin-top:4px;">{mem['date']}</div>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────  TAB: CHAT  ──────────────────
with tab_chat:
    # header
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:0.5rem;">
      <div style="width:40px; height:40px; border-radius:50%; background:#e8e0f7; display:flex; align-items:center; justify-content:center; font-size:1.1rem;">🤍</div>
      <div>
        <div style="font-weight:500; font-size:0.95rem; color:#3d2c2c;">{YOUR_NAME}</div>
        <div class="status-pill" style="margin:0; padding:2px 8px; font-size:0.72rem;"><span class="status-dot"></span> online via bot</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # welcome message if no history
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="date-chip">today</div>
        <div class="msg-row-bot">
          <div class="bubble-bot">hey pretty girl 🤍</div>
        </div>
        <div class="msg-row-bot">
          <div class="bubble-bot">js me here, talk to me</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # date chip
        st.markdown('<div class="date-chip">today</div>', unsafe_allow_html=True)
        # render history
        for msg in st.session_state.messages:
            render_bubble(msg["role"], msg["text"])

    # chat input
    user_input = st.chat_input("say something...")

    if user_input:
        clean_input = user_input.strip()

        # show user bubble
        render_bubble("user", clean_input)
        st.session_state.messages.append({"role": "user", "text": clean_input})

        # typing indicator
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="msg-row-bot">
          <div class="bubble-bot" style="padding:0.6rem 1rem;">
            <div class="typing-dots"><span></span><span></span><span></span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # realistic typing delay
        time.sleep(1.0 + len(clean_input) * 0.012)

        try:
            response = chat_session.send_message(clean_input)
            raw = response.text

            # post-process: enforce persona style
            reply = raw.lower().strip()
            # remove trailing full stops
            reply = reply.rstrip(".")
            # remove leading capital (just in case)
            if reply:
                reply = reply[0].lower() + reply[1:]

        except Exception as e:
            reply = "talk to you later okay?"

        typing_placeholder.empty()
        render_bubble("bot", reply)
        st.session_state.messages.append({"role": "bot", "text": reply})
