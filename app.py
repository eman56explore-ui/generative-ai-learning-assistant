import streamlit as st
import requests
import json

# ==========================================
# 1. CUTE & FEMININE THEME STYLING (🌸 SOFT PASTELS)
# ==========================================
st.set_page_config(
    page_title="🌸 LilyAI Blossom Chat", 
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a beautiful, cute, feminine UI with rounded shapes
st.markdown("""
    <style>
    /* Soft Blush Cream Background with Pastel Glow */
    .stApp {
        background: linear-gradient(135deg, #FFF5F5 0%, #FFF0F6 50%, #F3E8FF 100%);
        color: #4A4A4A;
        font-family: 'Quicksand', 'Inter', sans-serif;
    }
    
    /* Cute Pastel Pink & Purple Buttons with Glow */
    .stButton>button {
        background: linear-gradient(135deg, #FF8E9E 0%, #E879F9 100%);
        color: white !important;
        border: none;
        padding: 12px 24px;
        border-radius: 20px; /* Super cute rounded buttons */
        font-weight: bold;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(255, 142, 158, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 15px rgba(232, 121, 249, 0.5);
    }
    
    /* Soft Lavender Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FDF2F8 !important;
        border-right: 2px dashed #FBCFE8;
    }
    
    /* Dreamy Pastel Gradient Title */
    h1 {
        font-family: 'Comfortaa', sans-serif;
        font-weight: 700;
        background: linear-gradient(to right, #FF6B8B, #D946EF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Styling Chat Bubbles to look soft and rounded */
    [data-testid="stChatMessage"] {
        border-radius: 20px !important;
        background-color: white !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        border: 1px solid #FCE7F3 !important;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CUTE SIDEBAR WITH GIRLY SHAPE GRAPHICS 🎀
# ==========================================
st.title("🌸 LilyAI Blossom Workspace")
st.caption("✨ Your Aesthetic, Safe, and Sweet Local AI Bestie | Powered by Ollama")

with st.sidebar:
    st.markdown("<h2 style='color:#DB2777; text-align:center;'>🎀 Lily's Corner</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # Cute Custom Shape Graphic: Using Heart node-shapes instead of corporate grids
    st.markdown("<b style='color:#BE185D;'>How We Talk: 💕</b>", unsafe_allow_html=True)
    st.graphviz_chart('''
        digraph {
            node [color="#F472B6" fontcolor="#DB2777" style=filled fillcolor="#FFF1F2" shape=egg penwidth=2]
            edge [color="#F472B6" style=dashed]
            "You ✨" -> "Pretty App 🌸" [label="Ask"]
            "Pretty App 🌸" -> "Ollama Brain 🧠" [label="Send"]
            "Ollama Brain 🧠" -> "You ✨" [label="Reply 💕"]
        }
    ''')
    st.write("---")
    
    # Session Controls
    st.markdown("<b style='color:#BE185D;'>Session Care:</b>", unsafe_allow_html=True)
    if st.button("💖 Clear Chat & Refresh", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 3. CHAT CODES & RENDERING
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 4. PERSONALIZED PROFESSIONAL BOT LOGIC 🌸
# ==========================================
if user_input := st.chat_input("Type your magical thoughts here... 💕"):
    
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("<em style='color:#F472B6;'>Processing your request beautifully... ✨🌸</em>", unsafe_allow_html=True)
        
        # SYSTEM PROMPT: Setting a supportive, intelligent, expert personal helper vibe
        system_instructions = (
            "You are LilyAI, an incredibly smart, highly capable, expert professional AI assistant. "
            "Your personality is warm, articulate, encouraging, and brilliantly organized. "
            "Provide professional, deeply insightful answers. Use clean markdown formatting, neat bullet points, "
            "and beautiful text structuring to ensure clarity."
        )
        
        engineered_prompt = f"{system_instructions}\n\nUser Query: {user_input}\nProfessional Response:"
        
        OLLAMA_API_URL = "http://localhost:11434/api/generate"
        payload = {
            "model": "phi3",
            "prompt": engineered_prompt,
            "stream": True 
        }
        
        try:
            response = requests.post(OLLAMA_API_URL, json=payload, stream=True, timeout=120)
            
            if response.status_code == 200:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        line_data = json.loads(line.decode('utf-8'))
                        token = line_data.get("response", "")
                        full_response += token
                        response_placeholder.markdown(full_response + " 💖") # Cute heart cursor effect
                response_placeholder.markdown(full_response)
                ai_response = full_response
            else:
                ai_response = "🌸 *Oops! Something went wrong with the connection. Let's try again!*"
                response_placeholder.markdown(ai_response)
                
        except requests.exceptions.ConnectionError:
            ai_response = "🌸 *Oh no! Your local Ollama brain is offline. Please make sure the black terminal window is open!*"
            response_placeholder.markdown(ai_response)
        except Exception as e:
            ai_response = f"🌸 *An error occurred:* {str(e)}"
            response_placeholder.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})




