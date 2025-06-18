import streamlit as st
import openai
from PIL import Image
import base64
import io

st.set_page_config(page_title="AI Chat Trading + Gambar", layout="centered")

st.title("📊 AI Trading Chat + Gambar")
st.write("Upload chart & tanya tentang sinyal trading! AI akan bantu jawab.")

# Input API Key
api_key = st.text_input("Masukkan OpenAI API Key kamu (GPT-4-Vision)", type="password")

# Upload gambar chart
uploaded_image = st.file_uploader("Upload gambar chart kamu (opsional)", type=["png", "jpg", "jpeg"])

# Convert gambar ke base64 (dibutuhkan untuk OpenAI Vision API)
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")

# History chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Kamu adalah AI spesialis trading. Jika user mengupload gambar chart, bantu analisa chart tersebut."}
    ]

# Tampilkan pesan sebelumnya
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input pertanyaan user
if prompt := st.chat_input("Tulis pertanyaan kamu di sini..."):
    st.chat_message("user").markdown(prompt)
    
    # Proses jika ada gambar
    if uploaded_image and api_key:
        image_data = encode_image(uploaded_image)
        content = [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}"
                }
            }
        ]
        st.session_state.messages.append({"role": "user", "content": content})
    else:
        # Tanpa gambar
        st.session_state.messages.append({"role": "user", "content": prompt})

    if api_key:
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",  # gpt-4-vision-capable
                messages=st.session_state.messages,
                max_tokens=800
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").markdown(reply)
        except Exception as e:
            st.error(f"❌ Gagal konek ke API OpenAI: {e}")
    else:
        st.warning("⚠️ Masukkan API key dulu bro.")

