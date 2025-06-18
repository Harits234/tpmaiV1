import streamlit as st
import openai

st.set_page_config(page_title="AI Chat Trading", layout="centered")

st.title("💬 AI Chat Trading Assistant")
st.write("Tanya apapun tentang dunia trading (forex, crypto, saham, dll). Dibalas oleh AI spesialis trading.")

# Input API Key dari user
api_key = st.text_input("Masukkan OpenAI API Key kamu (gpt-3.5-turbo)", type="password")

# Inisialisasi session state untuk menyimpan history chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Kamu adalah AI asisten ahli dalam trading forex, crypto, dan saham. Jawablah semua pertanyaan dengan fokus pada dunia trading, analisa teknikal, strategi entry, psikologi trading, dan hal-hal sejenis. Jika pertanyaannya tidak berkaitan dengan trading, tolong arahkan kembali ke topik trading."}
    ]

# Tampilkan history chat sebelumnya
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input pertanyaan baru dari user
if prompt := st.chat_input("Tulis pertanyaan kamu di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    if api_key:
        try:
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").markdown(reply)
        except Exception as e:
            st.error(f"❌ Gagal koneksi ke OpenAI API:\n\n{e}")
    else:
        st.warning("⚠️ Masukkan API key kamu dulu untuk mulai chatting.")
