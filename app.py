import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="TNAU Farmer Schemes AI", 
    page_icon="🌾", 
    layout="wide"
)

# 2. Custom CSS for Background Image and UI Styling
# We use a high-quality agricultural image from Unsplash and add a dark overlay 
# so the chat text remains highly readable.
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), url("https://images.pexels.com/photos/36705018/pexels-photo-36705018.jpeg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
/* Make the chat messages look like floating glass cards */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
}
/* Style the title text to be white for contrast */
h1, h2, h3, p {
    color: #f0f2f35; /* Light text for contrast against dark overlay */
}
[data-testid="stChatMessage"] p {
    color: #000000; /* Keep chat text dark for readability */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 3. Main Header
st.title("🌾 Tamil Nadu Farmer Schemes Assistant")
st.markdown("Ask me anything about agriculture subsidies, seed multiplication, or machinery loans!")

# 4. Sidebar Options
with st.sidebar:
    st.header("⚙️ Options & Controls")
    
    # Clear Chat Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    
    # Quick Questions (Sample Prompts)
    st.subheader("💡 Quick Questions")
    st.markdown("Click below to ask:")
    
    # We use session state to pass clicked button text to the chat input
    if st.button("What is the subsidy for Paddy seeds?"):
        st.session_state.quick_prompt = "What is the subsidy for Paddy seed multiplication scheme?"
    if st.button("How much is a tractor loan?"):
        st.session_state.quick_prompt = "What is the subsidy for purchasing a Tractor under Agricultural Mechanisation?"
    if st.button("Tell me about Farm Ponds"):
        st.session_state.quick_prompt = "What are the benefits offered for Rain Water Harvesting and Farm Ponds?"

    st.divider()
    st.info("Data sourced directly from the [TNAU Agritech Portal](https://agritech.tnau.ac.in/expert_system/paddy/Schemes.html).")

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Handle User Input (from text box or quick buttons)
# Check if a quick prompt was clicked, otherwise check the chat input
user_input = st.chat_input("E.g., How can I get a subsidy for a power tiller?")

if "quick_prompt" in st.session_state:
    user_input = st.session_state.quick_prompt
    del st.session_state.quick_prompt # Clear it so it doesn't loop

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call FastAPI backend
    try:
        with st.spinner("Searching government schemes..."):
            response = requests.post("http://127.0.0.1:8000/chat", json={"question": user_input})
            response.raise_for_status()
            answer = response.json()["answer"]
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except requests.exceptions.RequestException:
        st.error("Error connecting to the backend. Is your FastAPI server running on port 8000?")
