import streamlit as st
import requests

# ── 1. Page Configuration ──────────────────────────────────────────────────
st.set_page_config(
    page_title="TNAU Farmer Schemes AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "http://127.0.0.1:8000/chat"

# ── 2. Verified, on-topic images (Wikimedia Commons / Pexels, compressed) ──
HERO_IMG = "https://images.pexels.com/photos/36705018/pexels-photo-36705018.jpeg?auto=compress&cs=tinysrgb&w=1600"
IMG_SEED = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Paddy_field_in_Tamil_Nadu_India.jpg/500px-Paddy_field_in_Tamil_Nadu_India.jpg"
IMG_MECH = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Rice_Transplanter_in_India.jpg/500px-Rice_Transplanter_in_India.jpg"
IMG_WATER = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/India_-_TN_-_11-01_-_The_Farm_-_17_-_ponds_%285445434964%29.jpg/500px-India_-_TN_-_11-01_-_The_Farm_-_17_-_ponds_%285445434964%29.jpg"
IMG_PUMP = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Agricultural_irrigation_pump_set_with_borewell%2C_Vrindavan%2C_Uttar_Pradesh%2C_India.jpg/500px-Agricultural_irrigation_pump_set_with_borewell%2C_Vrindavan%2C_Uttar_Pradesh%2C_India.jpg"

# ── 3. Scheme content, grounded in the TN Agri Schemes source document ────
SCHEME_CARDS = [
    {
        "icon": "🌱",
        "title": "Seed & Crop Production",
        "blurb": "₹2/kg premium on certified Paddy seed, Seed Village Scheme & SRI demos.",
        "image": IMG_SEED,
        "prompt": "What is the premium for certified Paddy seed production and how does the Seed Village Scheme work?",
    },
    {
        "icon": "🚜",
        "title": "Farm Mechanisation",
        "blurb": "25% subsidy on tractors, power tillers, rotavators & paddy transplanters.",
        "image": IMG_MECH,
        "prompt": "What is the subsidy for purchasing a Tractor, Power Tiller or Paddy Transplanter under the Agricultural Mechanisation Programme?",
    },
    {
        "icon": "💧",
        "title": "Water & Irrigation",
        "blurb": "Up to 100% support for farm ponds, percolation ponds and check dams.",
        "image": IMG_WATER,
        "prompt": "What are the benefits offered for Rain Water Harvesting, Farm Ponds and check dams?",
    },
    {
        "icon": "⚡",
        "title": "Pump Sets & Energy",
        "blurb": "Subsidy for replacing old electrical pump sets with efficient BIS pump sets.",
        "image": IMG_PUMP,
        "prompt": "What is the subsidy for replacing an old agricultural electrical pump set with a new one?",
    },
    {
        "icon": "🛡️",
        "title": "Insurance & Credit",
        "blurb": "Crop Insurance (NAIS) premium support and Kisan Credit Card facilities.",
        "image": None,
        "prompt": "How does the National Agricultural Insurance Scheme and the Kisan Credit Card Scheme help farmers?",
    },
]

SIDEBAR_QUESTIONS = {
    "🌱 Seeds & Crop Production": [
        "What is the subsidy for Paddy seed multiplication scheme?",
        "Tell me about the Seed Village Scheme.",
        "What support is given for System of Rice Intensification (SRI)?",
    ],
    "🚜 Mechanisation & Equipment": [
        "What is the subsidy for purchasing a Tractor under Agricultural Mechanisation?",
        "Is subsidy available for a Power Tiller or Paddy Transplanter?",
    ],
    "💧 Water & Irrigation": [
        "What are the benefits offered for Rain Water Harvesting and Farm Ponds?",
        "Tell me about check dams and percolation ponds.",
    ],
    "⚡ Pump Sets": [
        "What is the subsidy for replacing an old pump set?",
    ],
    "🛡️ Insurance & Credit": [
        "How does the Crop Insurance Scheme (NAIS) work?",
        "What is the Kisan Credit Card Scheme and its benefits?",
    ],
}

# ── 4. Theme: fonts, colors, hero, cards, chat bubbles ─────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

:root {
    --tn-green-dark: #0f3d24;
    --tn-green: #1b5e20;
    --tn-green-mid: #2e7d32;
    --tn-green-light: #66bb6a;
    --tn-gold: #f4a900;
    --tn-gold-dark: #c67c00;
    --tn-cream: #fbf7ec;
    --tn-text: #1a1a1a;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Poppins', sans-serif; }

[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(180deg, rgba(10,30,18,0.82), rgba(10,30,18,0.75)),
        url("__HERO_IMG__");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
@media (max-width: 768px) {
    [data-testid="stAppViewContainer"] { background-attachment: scroll; }
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }

/* ── Hero banner ── */
.hero-banner {
    text-align: center;
    padding: 2.2rem 1rem 1.4rem 1rem;
}
.hero-banner h1 {
    color: #ffffff;
    font-size: 2.6rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
    text-shadow: 0 2px 10px rgba(0,0,0,0.35);
}
.hero-banner h1 span {
    background: linear-gradient(90deg, var(--tn-gold), #ffd166);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.hero-banner p.tagline {
    color: #eef5ee;
    font-size: 1.08rem;
    max-width: 680px;
    margin: 0 auto 1rem auto;
    opacity: 0.95;
}
.badge-row { display: flex; justify-content: center; gap: 0.6rem; flex-wrap: wrap; }
.badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.35);
    color: #fff;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 500;
    backdrop-filter: blur(4px);
}

/* ── Scheme cards ── */
.scheme-card {
    background: rgba(255,255,255,0.95);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.scheme-card:hover { transform: translateY(-4px); box-shadow: 0 10px 22px rgba(0,0,0,0.35); }
.scheme-card img {
    width: 100%;
    height: 100px;
    object-fit: cover;
    display: block;
}
.scheme-card .icon-tile {
    width: 100%;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.4rem;
    background: linear-gradient(135deg, var(--tn-green-mid), var(--tn-green-dark));
}
.scheme-card .body { padding: 0.7rem 0.85rem 0.9rem 0.85rem; }
.scheme-card .body h4 {
    margin: 0 0 0.25rem 0;
    font-size: 0.95rem;
    color: var(--tn-green-dark);
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
}
.scheme-card .body p {
    margin: 0;
    font-size: 0.8rem;
    color: #333;
    line-height: 1.25rem;
}

/* ── Buttons (quick-question chips + card CTAs) ── */
.stButton > button {
    background: #ffffff;
    color: var(--tn-green-dark);
    border: 1.5px solid var(--tn-green-mid);
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.82rem;
    padding: 0.35rem 0.9rem;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: var(--tn-gold);
    border-color: var(--tn-gold-dark);
    color: #1a1a1a;
}

/* ── Chat bubbles ── */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.92);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
[data-testid="stChatMessage"] p { color: #111111; }

h1, h2, h3, p, label { color: #f2f5f0; }
[data-testid="stSidebar"] * { color: #eef2ee; }
[data-testid="stSidebar"] { background: rgba(10, 30, 18, 0.92); }

/* Footer */
.app-footer {
    text-align: center;
    color: #dce7dc;
    font-size: 0.78rem;
    padding: 1.2rem 0 0.4rem 0;
    border-top: 1px solid rgba(255,255,255,0.15);
    margin-top: 1.5rem;
}
.app-footer a { color: var(--tn-gold); text-decoration: none; }
</style>
""".replace("__HERO_IMG__", HERO_IMG),
    unsafe_allow_html=True,
)

# ── 5. Hero header ──────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero-banner">
    <h1>🌾 Tamil Nadu Farmer <span>Schemes</span> Assistant</h1>
    <p class="tagline">Ask about seed subsidies, farm mechanisation, irrigation support, pump sets,
    crop insurance and credit — answered from official TNAU scheme records.</p>
    <div class="badge-row">
        <span class="badge">✅ TNAU Sourced</span>
        <span class="badge">🏛️ State &amp; Central Schemes</span>
        <span class="badge">🤖 AI-Powered Guidance</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ── 6. Visual scheme-category explorer ─────────────────────────────────
cols = st.columns(len(SCHEME_CARDS))
for col, scheme in zip(cols, SCHEME_CARDS):
    with col:
        media_html = (
            f'<img src="{scheme["image"]}" alt="{scheme["title"]}"/>'
            if scheme["image"]
            else f'<div class="icon-tile">{scheme["icon"]}</div>'
        )
        st.markdown(
            f"""
            <div class="scheme-card">
                {media_html}
                <div class="body">
                    <h4>{scheme['icon']} {scheme['title']}</h4>
                    <p>{scheme['blurb']}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Ask about this →", key=f"card_{scheme['title']}", use_container_width=True):
            st.session_state.quick_prompt = scheme["prompt"]

st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

# ── 7. Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Options & Controls")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.subheader("💡 Quick Questions")
    st.caption("Grouped by scheme category — click to ask instantly.")

    for category, questions in SIDEBAR_QUESTIONS.items():
        with st.expander(category):
            for i, q in enumerate(questions):
                if st.button(q, key=f"sb_{category}_{i}", use_container_width=True):
                    st.session_state.quick_prompt = q

    st.divider()
    st.info(
        "Data sourced directly from the [TNAU Agritech Portal]"
        "(https://agritech.tnau.ac.in/expert_system/paddy/Schemes.html)."
    )
    st.caption("⚠️ AI-generated answers may be incomplete. Please confirm eligibility "
               "and current subsidy rates with your local Agriculture Officer before applying.")

# ── 8. Chat history ─────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

AVATARS = {"user": "🧑‍🌾", "assistant": "🌾"}

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=AVATARS.get(message["role"])):
        st.markdown(message["content"])

# ── 9. Handle input (chat box or quick-question / card click) ──────────
user_input = st.chat_input("E.g., How can I get a subsidy for a power tiller?")

if "quick_prompt" in st.session_state:
    user_input = st.session_state.quick_prompt
    del st.session_state.quick_prompt

if user_input:
    st.chat_message("user", avatar=AVATARS["user"]).markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        with st.spinner("🔎 Searching TNAU scheme records..."):
            response = requests.post(BACKEND_URL, json={"question": user_input}, timeout=30)
            response.raise_for_status()
            payload = response.json()

        if "answer" in payload:
            answer = payload["answer"]
            with st.chat_message("assistant", avatar=AVATARS["assistant"]):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Backend error: {payload.get('error', 'Unknown error from server.')}")

    except requests.exceptions.Timeout:
        st.error("⏱️ The request took too long. The backend may be busy — please try again.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Could not reach the backend. Is your FastAPI server running on port 8000?")
    except requests.exceptions.RequestException as e:
        st.error(f"Something went wrong while contacting the backend: {e}")

# ── 10. Footer ───────────────────────────────────────────────────────────
st.markdown(
    """
<div class="app-footer">
    🌾 Built for Tamil Nadu farmers &nbsp;•&nbsp;
    Source: <a href="https://agritech.tnau.ac.in/expert_system/paddy/Schemes.html" target="_blank">TNAU Agritech Portal</a>
    &nbsp;•&nbsp; This is an informational AI assistant, not an official government service.
</div>
""",
    unsafe_allow_html=True,
)
