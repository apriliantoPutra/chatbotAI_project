"""
Cara jalanin:

>>> streamlit run app.py
"""
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def init_groq():
    """Inisialisasi model Groq dengan API key"""
    if not groq_api_key:
        st.error("❌ Groq API Key tidak ditemukan!")
        return None
    
    try:
        llm = ChatGroq(
            temperature=0.7,
            groq_api_key=groq_api_key,
            model_name="openai/gpt-oss-120b"
        )
        return llm
    except Exception as e:
        st.error(f"❌ Gagal menginisialisasi Groq: {str(e)}")
        return None
    
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "llm" not in st.session_state:
    st.session_state.llm = init_groq()
    
def generate_response(prompt, history):
    """
    Fungsi untuk menghasilkan jawaban dari Groq dengan konteks percakapan
    Args:
        prompt (str): Pertanyaan dari pengguna
        history (list): Riwayat percakapan sebelumnya
    Returns:
        str: Jawaban dari AI
    """
    try:
        if st.session_state.llm is None:
            return "❌ Model tidak tersedia. Periksa API key Anda."
        
        context = ""
        for msg in history:
            if msg["role"] == "user":
                context += f"User: {msg['content']}\n"
            else:
                context += f"Assistant: {msg['content']}\n"
        
        full_prompt = f"{context}User: {prompt}\nAssistant:"
        
        response = st.session_state.llm.invoke(full_prompt)
        return response.content
    except Exception as e:
        return f"❌ Error: {str(e)}"
    
    
# --- Setting halaman ---    
st.set_page_config(
    page_title="ChatAI",
    page_icon="🤖",
    layout="centered"
)

# --- Hapus default padding ---
st.markdown(
    """
    <style>
        .main > div {
            padding-top: 2rem;
        }
        .stTextInput > div {
            height: 70px;
        }
        .stButton > button {
            height: 50px;
            margin-top: 0px;
        }
        .input-container {
            position: sticky;
            bottom: 0;
            background: white;
            padding: 10px 0;
            border-top: 1px solid #ddd;
        }
    </style>
    """, unsafe_allow_html=True
)

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"""
            <div style='
                display: flex;
                justify-content: flex-end;
                margin-bottom: 15px;
            '>
                <div style='
                    background-color: #D6EAF8;
                    padding: 12px 18px;
                    border-radius: 18px 18px 5px 18px;
                    max-width: 70%;
                    word-wrap: break-word;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                '>
                    {message["content"]}
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        if message["content"].startswith("❌"):
            st.markdown(f"""
                <div style='
                    display: flex;
                    justify-content: flex-start;
                    margin-bottom: 15px;
                '>
                    <div style='
                        background-color: #FADBD8;
                        padding: 12px 18px;
                        border-radius: 18px 18px 18px 5px;
                        max-width: 70%;
                        word-wrap: break-word;
                        border-left: 4px solid #E74C3C;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    '>
                        {message["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='
                    display: flex;
                    justify-content: flex-start;
                    margin-bottom: 15px;
                    padding-left: 5px;
                '>
                    <div style='
                        max-width: 70%;
                        word-wrap: break-word;
                        color: #2C3E50;
                        line-height: 1.6;
                    '>
                        {message["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)

has_history = len(st.session_state.chat_history) > 0

if not has_history:
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>🤖 ChatAI</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h2 style='
                background: linear-gradient(45deg, red, orange, yellow, green, blue, indigo, violet);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 40px;
                font-weight: bold;
            '>
                Selamat Datang di ChatAI
            </h2>
            <p style='font-size: 18px; color: #666;'>
                Tanyakan apa saja, saya siap membantu! 😊
            </p>
        </div>        
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "💬 Ketik pertanyaan Anda:",
        placeholder="Contoh: Apa itu kecerdasan buatan?",
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    submit_button = st.button("🚀 Kirim", use_container_width=True)

if submit_button and user_input:
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    with st.spinner("AI sedang berpikir..."):
        answer = generate_response(user_input, st.session_state.chat_history[:-1])
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })
    st.rerun()

if has_history:
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("<br>" * 3, unsafe_allow_html=True)

            
if len(st.session_state.chat_history) > 0:
    if st.sidebar.button("🗑️ Hapus Chat"):
        st.session_state.chat_history = []
        st.rerun()