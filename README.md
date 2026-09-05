# 🤖 ChatAI - Groq Chatbot

## 📋 Deskripsi
ChatAI adalah aplikasi chatbot interaktif berbasis web yang memanfaatkan **Groq API** untuk memberikan jawaban cerdas terhadap pertanyaan pengguna. Aplikasi ini dibangun dengan antarmuka yang modern dan responsif menggunakan **Streamlit**, serta dilengkapi dengan fitur percakapan yang mengingat konteks pembicaraan sebelumnya.

## ✨ Fitur Utama
- Tampilan chat dengan bubble (user di kanan, AI di kiri)
- Loading indicator saat AI sedang memproses jawaban
- Penanganan error dengan tampilan box merah
- Riwayat percakapan dengan konteks (AI mengingat pembicaraan sebelumnya)
- Tombol hapus chat untuk memulai ulang percakapan
- Desain responsif dan modern

## 🛠️ Teknologi yang Digunakan
- **Python 3.10+** - Bahasa pemrograman utama
- **Streamlit** - Framework frontend untuk UI interaktif
- **LangChain** - Framework integrasi dengan model AI
- **Groq API** - Backend AI (model `openai/gpt-oss-120b`)
- **python-dotenv** - Manajemen environment variables

## 📦 Cara menjalankan
1. Buat file .env di root project:
```bash
GROQ_API_KEY=your_api_key_here
```

2. Install Library
```bash
pip install streamlit pandas pillow
pip install langchain langchain-community langgraph
pip install langchain-google-genai langchain-groq