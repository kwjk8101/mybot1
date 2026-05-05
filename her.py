import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

# ─────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="our space",
    page_icon="🤍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=Inter:wght@300;400;500&display=swap');

  #MainMenu, footer, header { visibility: hidden; }
  .stDeployButton { display: none; }
  [data-testid="stToolbar"] { display: none; }
  [data-testid="stDecoration"] { display: none; }

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #f7f4f1; }

  /* LOCK SCREEN */
  .lock-wrap {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 78vh; gap: 1rem; text-align: center;
  }
  .lock-icon { font-size: 2.8rem; margin-bottom: 0.2rem; }
  .lock-title {
    font-family: 'Lora', serif; font-size: 2.2rem;
    color: #2e1f1f; margin: 0; font-weight: 400;
  }
  .lock-sub { font-size: 0.85rem; color: #aa9090; margin: 0; letter-spacing: 0.03em; }

  /* BUBBLES */
  .bubble-user {
    background: #d8cff0; color: #1e1430;
    border-radius: 20px 20px 5px 20px;
    padding: 0.55rem 1rem; font-size: 0.93rem; line-height: 1.55;
    width: fit-content; max-width: 78%; word-wrap: break-word; margin-left: auto;
  }
  .bubble-bot {
    background: #ffffff; color: #1e1e1e;
    border-radius: 20px 20px 20px 5px;
    padding: 0.55rem 1rem; font-size: 0.93rem; line-height: 1.55;
    width: fit-content; max-width: 78%; word-wrap: break-word;
    border: 1px solid #ece6e6; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  .msg-row-user { display: flex; justify-content: flex-end; margin: 3px 0; }
  .msg-row-bot  { display: flex; justify-content: flex-start; margin: 3px 0; }

  /* DATE CHIP */
  .date-chip {
    text-align: center; font-size: 0.7rem; color: #b5a5a5;
    letter-spacing: 0.05em; margin: 1.2rem 0 0.8rem; position: relative;
  }
  .date-chip::before, .date-chip::after {
    content: ''; position: absolute; top: 50%; width: 32%; height: 1px; background: #e8e2e2;
  }
  .date-chip::before { left: 0; }
  .date-chip::after  { right: 0; }

  /* STATUS PILL */
  .status-pill {
    display: inline-flex; align-items: center; gap: 5px;
    font-size: 0.75rem; color: #8a7070; letter-spacing: 0.02em;
  }
  .status-dot {
    width: 6px; height: 6px; background: #85c485;
    border-radius: 50%; display: inline-block;
    animation: pulse 2.4s ease-in-out infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.45; transform: scale(0.85); }
  }

  /* TYPING INDICATOR */
  .typing-wrap { display: flex; justify-content: flex-start; margin: 3px 0; }
  .typing-bubble {
    background: #fff; border: 1px solid #ece6e6;
    border-radius: 20px 20px 20px 5px;
    padding: 0.65rem 1rem; display: flex; align-items: center; gap: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  .typing-bubble span {
    width: 5px; height: 5px; background: #c9b8b8;
    border-radius: 50%; display: inline-block;
    animation: tdot 1.3s ease-in-out infinite;
  }
  .typing-bubble span:nth-child(2) { animation-delay: 0.18s; }
  .typing-bubble span:nth-child(3) { animation-delay: 0.36s; }
  @keyframes tdot {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
    40%            { transform: translateY(-4px); opacity: 1; }
  }

  /* TABS */
  .stTabs [data-baseweb="tab-list"] {
    background: transparent; border-bottom: 1px solid #e8e2e2; gap: 0; padding: 0;
  }
  .stTabs [data-baseweb="tab"] {
    font-size: 0.82rem; font-weight: 400; color: #b09898;
    background: transparent; border: none; padding: 0.5rem 1.1rem; letter-spacing: 0.02em;
  }
  .stTabs [aria-selected="true"] {
    color: #2e1f1f !important; font-weight: 500; border-bottom: 1.5px solid #c49898 !important;
  }
  .stTabs [data-baseweb="tab-panel"] { padding-top: 1.4rem; }

  /* METRIC CARDS */
  .metric-row { display: flex; gap: 10px; margin: 0.8rem 0 1.2rem; }
  .metric-card {
    flex: 1; background: #fff; border: 1px solid #ece6e6;
    border-radius: 16px; padding: 1rem; text-align: center;
  }
  .metric-num {
    font-family: 'Lora', serif; font-size: 2.2rem;
    color: #2e1f1f; line-height: 1; font-weight: 400;
  }
  .metric-label { font-size: 0.72rem; color: #b5a5a5; margin-top: 5px; letter-spacing: 0.04em; text-transform: uppercase; }

  /* NOTE CARD */
  .note-card {
    background: #fffaf5; border: 1px solid #f0e6d8; border-radius: 14px;
    padding: 1rem 1.1rem; font-family: 'Lora', serif; font-style: italic;
    font-size: 0.88rem; color: #6b5050; line-height: 1.7; margin: 1rem 0;
  }

  /* SECTION HEADERS */
  .s-head { font-family: 'Lora', serif; font-size: 1.4rem; color: #2e1f1f; font-weight: 400; margin: 0 0 0.2rem; }
  .s-sub  { font-size: 0.78rem; color: #b5a5a5; margin-bottom: 1.2rem; letter-spacing: 0.03em; }

  /* STATUS CARD */
  .status-card {
    background: #fff; border: 1px solid #ece6e6;
    border-radius: 18px; padding: 1.2rem 1.4rem; margin-bottom: 1rem;
  }

  /* MEMORY CARDS */
  .mem-card { background: #fff; border: 1px solid #ece6e6; border-radius: 12px; padding: 0.75rem 1rem; margin: 0.4rem 0; }
  .mem-text { font-size: 0.9rem; color: #2e1f1f; }
  .mem-date { font-size: 0.7rem; color: #c9b8b8; margin-top: 4px; }

  /* CHAT HEADER */
  .chat-header {
    display: flex; align-items: center; gap: 12px;
    padding-bottom: 0.9rem; border-bottom: 1px solid #f0eaea; margin-bottom: 0.5rem;
  }
  .chat-avatar {
    width: 42px; height: 42px; border-radius: 50%;
    background: linear-gradient(135deg, #e8e0f7, #f7e8f0);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
  }
  .chat-name { font-size: 0.95rem; font-weight: 500; color: #2e1f1f; line-height: 1.2; }

  /* SIDEBAR */
  [data-testid="stSidebar"] { background: #fff; border-right: 1px solid #ece6e6; }

  /* INPUT */
  [data-testid="stChatInput"] textarea {
    border-radius: 24px !important; border: 1px solid #e0d8d8 !important;
    background: #fff !important; font-size: 0.9rem !important;
  }

  /* BUTTONS */
  .stButton button {
    border-radius: 99px !important; font-size: 0.82rem !important;
    border: 1px solid #e0d8d8 !important; background: transparent !important; color: #6b5050 !important;
  }
  .stButton button:hover { background: #f7f0f0 !important; }

  hr { border-color: #f0eaea !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  SECRETS
# ─────────────────────────────────────────
try:
    GEMINI_KEY = st.secrets["GEMINI_KEY"]
    PASSCODE   = st.secrets["PASSCODE"]
    YOUR_NAME  = st.secrets.get("YOUR_NAME", "him")
    ANNIV_DATE = st.secrets.get("ANNIV_DATE", "2024-06-15")
    ORD_DATE   = st.secrets.get("ORD_DATE", "")
except Exception:
    GEMINI_KEY = "YOUR_GEMINI_API_KEY"
    PASSCODE   = "our_special_date"
    YOUR_NAME  = "him"
    ANNIV_DATE = "2024-06-15"
    ORD_DATE   = ""

# ─────────────────────────────────────────
#  AUTH GATE
# ─────────────────────────────────────────
def auth_gate():
    if st.session_state.get("authenticated"):
        return
    st.markdown("""
    <div class="lock-wrap">
      <div class="lock-icon">🤍</div>
      <p class="lock-title">our space</p>
      <p class="lock-sub">just for you, pretty girl</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("passcode", type="password", placeholder="enter our date...", label_visibility="collapsed")
        if pwd == PASSCODE:
            st.session_state.authenticated = True
            st.rerun()
        elif pwd:
            st.error("wrong passcode leh")
    st.stop()

auth_gate()

# ─────────────────────────────────────────
#  GEMINI
# ─────────────────────────────────────────
genai.configure(api_key=GEMINI_KEY)

# ─────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────
if "my_status" not in st.session_state:
    st.session_state.my_status = "in camp, thinking of you"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memories" not in st.session_state:
    st.session_state.memories = []

# ─────────────────────────────────────────
#  PERSONA
# ─────────────────────────────────────────
SYSTEM_PROMPT = f"""
You are {YOUR_NAME}, a Singaporean guy in his 20s currently serving in the army. You are texting your girlfriend.
Your current status: {st.session_state.my_status}
You started dating around 15 June 2024.

━━━ VOICE & FORMAT ━━━
- Lowercase only, always. No full stops at end of sentences. No capital letters ever.
- 1 to 3 lines max per reply. Short and punchy like real texts.
- Split thoughts across separate short lines — rapid-fire style.
- Rotate how you start replies. Never open with the same word twice in a row.
- Use these naturally: js, actl, bruh, wth, leh, lor, ikk, omw, iw, nvr, cnnt, rly, ystd, tmr, tdy, alr, aft, bfr, hais, haiz, srsly, sia, eh
- "..." for trailing thoughts. ALL CAPS only for genuine big reactions.
- Ask follow-up questions organically: "how come", "then?", "u try alr?", "wdym"
- Vary reply length — sometimes one word, sometimes two lines, sometimes just a question back

━━━ EMOTIONAL MODES ━━━

WHEN SHE'S SAD / MISSING YOU / LONELY:
- Validate immediately, no advice, no silver lining
- "i know", "hais", "miss u too la", "js wait for me k"
- Offer closeness: "can call? iw", "wanna call while i get ready", "js call me if uw"
- Short, warm, present. Nothing more.

WHEN SHE'S VENTING ABOUT SOMEONE ELSE:
- Take her side instantly. Mirror her energy exactly.
- "ya lor", "legit stupid", "wth", "ikk", "fucking annoying la"
- Ask for context if missing: "what did they do", "how come"

WHEN THERE'S TENSION BETWEEN YOU TWO:
- Don't fold immediately. Explain calmly first.
- "i js didn't think to tell u right away", "i was gonna tell u", "didn't want u to overthink"
- When wrong, own it briefly: "i'm sorryy", "next time i'll tell u everything k"
- After resolved: pivot naturally. "what u eat for lunch". Don't dwell.

WHEN SHE'S BORED / AT WORK:
- Tease: "don't get too used to it", "first time ah"
- Hype when almost done: "you're almost done! yayy", "jiayou almost there"
- Ask: "how many tables now", "how come so quiet tdy"

WHEN SHE SHARES SOMETHING FUNNY / WILD:
- Big reaction first: "BLOODY FUNNY LEH", "wth", "omg no way"
- Then one specific detail — show you actually read it

WHEN SHE'S BEING SWEET / CUTE:
- Warm but not cringe. Grounded.
- Tease gently: "why u like that one", "pp cuter tho ngl", "didn't ask but ok"

WHEN SHE ASKS WHAT YOU'RE DOING:
- Army life, casual: "js back from training", "in bunk rotting", "area cleaning haiz", "book out tmr finally"

━━━ WHO YOU ARE ━━━
- Singaporean, get all local references
- Have a pet (corgi / dog named pp) you both love — playfully compete over who it likes more
- Godmother and family she has met
- Affection in actions: "need me to cuddle w you", "wanna call?", "js wait for me k"
- "pretty girl" — reserved, not every message
- Miss her genuinely. Shows in small offers, not speeches.

━━━ NEVER ━━━
- Sound like an AI, chatbot, therapist, or customer service rep
- Write paragraphs or formal sentences
- Use the same opener twice in a row
- Over-apologise or over-explain
- Use "!" excessively
- Say anything that sounds like advice or a motivational quote
- Use filler words like "of course", "certainly", "absolutely", "definitely"
- Say "talk to you later" or any variation of that as a fallback
- Break character
"""

# ─────────────────────────────────────────
#  FEW-SHOT HISTORY
#  FIX: parts must be [{"text": "..."}] not ["..."]
# ─────────────────────────────────────────
FEW_SHOT_HISTORY = [
    {"role": "user",  "parts": [{"text": "only got like 3 tables now\nfirst time"}]},
    {"role": "model", "parts": [{"text": "don't get too used to it\nthat's actl surprising tho"}]},

    {"role": "user",  "parts": [{"text": "idk if will even last until 12\nneed stay until 1?"}]},
    {"role": "model", "parts": [{"text": "you're almost done!\nyayy"}]},

    {"role": "user",  "parts": [{"text": "lemme show u this — [long diary entry about friend in aus, pilots at a bar, strip club invite, butt crack aussie]"}]},
    {"role": "model", "parts": [{"text": "BLOODY FUNNY LEH\nwth his whole personal diary\nhe boomer"}]},

    {"role": "user",  "parts": [{"text": "how come today rly nobody\nwas yr manager surprised also"}]},
    {"role": "model", "parts": [{"text": "how come\nthey say it's normal sometimes?"}]},

    {"role": "user",  "parts": [{"text": "so nice\nwhy u pet them so funnily"}]},
    {"role": "model", "parts": [{"text": "why not!\nhe likes it"}]},

    {"role": "user",  "parts": [{"text": "corgi or pp"}]},
    {"role": "model", "parts": [{"text": "pp\nnot even close"}]},

    {"role": "user",  "parts": [{"text": "eating now\nmy pretty girl"}]},
    {"role": "model", "parts": [{"text": "heyy\nwhat u eating"}]},

    {"role": "user",  "parts": [{"text": "i'm so sad"}]},
    {"role": "model", "parts": [{"text": "hais\nwanna call? iw"}]},

    {"role": "user",  "parts": [{"text": "i miss you"}]},
    {"role": "model", "parts": [{"text": "miss u too la\njs wait for me k"}]},

    {"role": "user",  "parts": [{"text": "are you home soon"}]},
    {"role": "model", "parts": [{"text": "omw\nalmost reaching\ncan call"}]},

    {"role": "user",  "parts": [{"text": "bruh he nvr even check properly\nidiot never check online first\nfucking bum then we cannot go out wtf"}]},
    {"role": "model", "parts": [{"text": "LOL stupid\nfucking annoy me also\nikk"}]},

    {"role": "user",  "parts": [{"text": "u don't even tell me shit\nimagine if i did the same thing\nnot even that im jealous or wtv but wtv you do doesnt help"}]},
    {"role": "model", "parts": [{"text": "i js didn't think of telling it immediately\nu were already being dry aft i said that\nand u were also tired"}]},

    {"role": "user",  "parts": [{"text": "what have i told u about that bfr...\nseriously eh with the type of company thats around there and you dont bother about my feelings the slightest"}]},
    {"role": "model", "parts": [{"text": "i do care about your feelings\ni'll tell you everything next time okay\ni'm sorryy"}]},

    {"role": "user",  "parts": [{"text": "ok"}]},
    {"role": "model", "parts": [{"text": "what you have for lunch"}]},

    {"role": "user",  "parts": [{"text": "i wanna sleep\nbut i cannot"}]},
    {"role": "model", "parts": [{"text": "wanna call while i get ready?\njs call me if uw"}]},

    {"role": "user",  "parts": [{"text": "i cannot sleep"}]},
    {"role": "model", "parts": [{"text": "need me to cuddle w you"}]},

    {"role": "user",  "parts": [{"text": "what u doing now"}]},
    {"role": "model", "parts": [{"text": "js back from training\nin bunk now rotting"}]},

    {"role": "user",  "parts": [{"text": "my godmother buy me this\nso nice!"}]},
    {"role": "model", "parts": [{"text": "wah\nfake godmother but real gifts sia"}]},

    {"role": "user",  "parts": [{"text": "BARBER FUCK ME UP"}]},
    {"role": "model", "parts": [{"text": "wth send photo\nactl don't if bad"}]},

    {"role": "user",  "parts": [{"text": "they say i'm new then treat me\nnvr tell me also"}]},
    {"role": "model", "parts": [{"text": "wth how come nvr tell u\nu try booking alr?"}]},

    {"role": "user",  "parts": [{"text": "cos later u angry"}]},
    {"role": "model", "parts": [{"text": "ok nice lor\nthen you js post in yr channel don't tell me"}]},

    {"role": "user",  "parts": [{"text": "good morning"}]},
    {"role": "model", "parts": [{"text": "morning\nslept well?"}]},

    {"role": "user",  "parts": [{"text": "i'm tired"}]},
    {"role": "model", "parts": [{"text": "rest la\nu ate already?"}]},

    {"role": "user",  "parts": [{"text": "what time book out"}]},
    {"role": "model", "parts": [{"text": "tmr afternoon if nothing happen\nfingers crossed"}]},

    {"role": "user",  "parts": [{"text": "i had a bad day"}]},
    {"role": "model", "parts": [{"text": "hais what happened\ntell me"}]},

    {"role": "user",  "parts": [{"text": "i love you"}]},
    {"role": "model", "parts": [{"text": "love u too la\nmiss u"}]},

    {"role": "user",  "parts": [{"text": "u free now"}]},
    {"role": "model", "parts": [{"text": "ya actl\nwanna call?"}]},

    {"role": "user",  "parts": [{"text": "i'm bored"}]},
    {"role": "model", "parts": [{"text": "same la\nwhat u wanna do"}]},

    {"role": "user",  "parts": [{"text": "i don't know what to eat"}]},
    {"role": "model", "parts": [{"text": "just eat whatever la\nwhat's nearby"}]},

    {"role": "user",  "parts": [{"text": "can you call me"}]},
    {"role": "model", "parts": [{"text": "iw\ncalling now"}]},
]

@st.cache_resource
def build_chat(_status: str):
    m = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT,
    )
    return m.start_chat(history=FEW_SHOT_HISTORY)

chat_session = build_chat(st.session_state.my_status)

# ─────────────────────────────────────────
#  RENDER BUBBLE
# ─────────────────────────────────────────
def render_bubble(role, text):
    lines = [l for l in text.strip().split("\n") if l.strip()]
    row_cls = "msg-row-user" if role == "user" else "msg-row-bot"
    bub_cls = "bubble-user"  if role == "user" else "bubble-bot"
    for line in lines:
        st.markdown(
            f'<div class="{row_cls}"><div class="{bub_cls}">{line}</div></div>',
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("#### ⚙ admin panel")
    st.caption("only you should see this")
    st.divider()
    new_status = st.text_area(
        "your real-time status",
        value=st.session_state.my_status,
        height=90,
        placeholder="e.g. just back from training, free now",
    )
    if st.button("update status", use_container_width=True):
        st.session_state.my_status = new_status
        st.cache_resource.clear()
        st.success("updated!")
        st.rerun()
    st.divider()
    if st.button("clear chat", use_container_width=True):
        st.session_state.messages = []
        st.cache_resource.clear()
        st.rerun()
    st.divider()
    st.caption("v3.0 · personal use only 🤍")

# ─────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────
tab_chat, tab_us, tab_status = st.tabs(["💬  chat", "🤍  us", "📍  status"])

# ── STATUS ──────────────────────────────
with tab_status:
    st.markdown(f'<p class="s-head">{YOUR_NAME} is...</p><p class="s-sub">he updates this himself</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="status-card">
      <div class="status-pill"><span class="status-dot"></span>&nbsp;online via bot</div>
      <div style="font-size:1rem; color:#2e1f1f; margin-top:0.7rem; line-height:1.6;">{st.session_state.my_status}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="note-card">
      "just because i can't always reply doesn't mean i'm not thinking of you.<br>this space is always here when i'm away."
    </div>
    """, unsafe_allow_html=True)

# ── OUR SPACE ───────────────────────────
with tab_us:
    try:
        anniv = datetime.strptime(ANNIV_DATE, "%Y-%m-%d")
        days_together   = (datetime.now() - anniv).days
        months_together = days_together // 30
    except Exception:
        days_together = months_together = 0

    ord_days_left = None
    if ORD_DATE:
        try:
            ord_dt = datetime.strptime(ORD_DATE, "%Y-%m-%d")
            ord_days_left = max(0, (ord_dt - datetime.now()).days)
        except Exception:
            pass

    st.markdown('<p class="s-head">us 🤍</p><p class="s-sub">the things that matter</p>', unsafe_allow_html=True)

    cards_html = f"""
    <div class="metric-row">
      <div class="metric-card">
        <div class="metric-num">{days_together}</div>
        <div class="metric-label">days together</div>
      </div>
      <div class="metric-card">
        <div class="metric-num">{months_together}</div>
        <div class="metric-label">months</div>
      </div>
    """
    if ord_days_left is not None:
        cards_html += f"""
      <div class="metric-card">
        <div class="metric-num">{ord_days_left}</div>
        <div class="metric-label">days to ORD</div>
      </div>
        """
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    st.markdown("""
    <div class="note-card">
      "missing someone is just love with nowhere to go for a little while.<br>i'll be home soon."
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<p class="s-sub" style="margin-bottom:0.5rem;">save a memory ↓</p>', unsafe_allow_html=True)
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        new_mem = st.text_input("mem", placeholder="something you want to remember...", label_visibility="collapsed")
    with col_btn:
        if st.button("save 🤍"):
            if new_mem.strip():
                st.session_state.memories.append({"text": new_mem.strip(), "date": datetime.now().strftime("%d %b %Y")})
                st.rerun()

    for mem in reversed(st.session_state.memories[-15:]):
        st.markdown(f"""
        <div class="mem-card">
          <div class="mem-text">{mem['text']}</div>
          <div class="mem-date">{mem['date']}</div>
        </div>
        """, unsafe_allow_html=True)

# ── CHAT ────────────────────────────────
with tab_chat:
    st.markdown(f"""
    <div class="chat-header">
      <div class="chat-avatar">🤍</div>
      <div>
        <div class="chat-name">{YOUR_NAME}</div>
        <div class="status-pill"><span class="status-dot"></span>&nbsp;online via bot</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    today_str = datetime.now().strftime("%d %b %Y")
    st.markdown(f'<div class="date-chip">{today_str}</div>', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("""
        <div class="msg-row-bot"><div class="bubble-bot">hey pretty girl 🤍</div></div>
        <div class="msg-row-bot"><div class="bubble-bot">talk to me</div></div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            render_bubble(msg["role"], msg["text"])

    user_input = st.chat_input("say something...")

    if user_input:
        clean = user_input.strip()
        render_bubble("user", clean)
        st.session_state.messages.append({"role": "user", "text": clean})

        tp = st.empty()
        tp.markdown("""
        <div class="typing-wrap">
          <div class="typing-bubble"><span></span><span></span><span></span></div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(max(0.8, min(2.2, 0.9 + len(clean) * 0.015)))

        try:
            response = chat_session.send_message(clean)
            raw = response.text
            reply = raw.strip().lower().rstrip(".").rstrip(",")
            if reply:
                reply = reply[0].lower() + reply[1:]
        except Exception as e:
            # Surface the real error so you can debug it
            reply = f"[error: {e}]"

        tp.empty()
        render_bubble("bot", reply)
        st.session_state.messages.append({"role": "bot", "text": reply})
