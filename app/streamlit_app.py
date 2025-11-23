import streamlit as st
import requests
from datetime import datetime

API_URL = "https://ee96a76c97be.ngrok-free.app/chat"

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="MaMaCare Assistant",
    page_icon="🩷",
    layout="centered",
)

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_phone" not in st.session_state:
    st.session_state.user_phone = None

# ---------- PHONE NUMBER GATE ----------
if not st.session_state.user_phone:

    st.markdown("""
    <h1 style='text-align: center;'>🩷 MaMaCare AI</h1>
    <p style='text-align: center; color: gray;'>
    To begin, please enter your phone number.
    </p>
    """, unsafe_allow_html=True)

    phone = st.text_input(
        "Phone Number",
        placeholder="+2348012345678"
    )

    if st.button("Start Session", type="primary"):

        if not phone or len(phone) < 10:
            st.error("Please enter a valid phone number")
        else:
            st.session_state.user_phone = phone
            st.success("Session started ✅")
            st.rerun()

    st.stop()


# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center;'>🩷 MaMaCare AI</h1>
<p style='text-align: center; color: gray;'>
Your personal maternal health companion
</p>
""", unsafe_allow_html=True)

# ---------- CHAT HISTORY ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------- USER INPUT ----------
user_input = st.chat_input("How are you feeling today? For example: 'I feel nauseous and tired'")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": str(datetime.now())
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Loading indicator
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "message": user_input,
                        "user_id": st.session_state.user_phone
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data.get("response") or data.get("message") or str(data)
                else:
                    bot_reply = "⚠️ Something went wrong. Please try again."

            except Exception as e:
                bot_reply = f"⚠️ Error connecting to server: {e}"

            st.markdown(bot_reply)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply,
        "time": str(datetime.now())
    })


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 👤 Patient Session")
    st.write(f"**Phone:** {st.session_state.user_phone}")

    st.markdown("## 🩺 About")
    st.write(
        """
        This AI helps you track:
        - Menstrual cycles
        - Pregnancy status
        - Symptoms
        - Medications & tests
        - Doctor visits

        ⚠️ Always consult a doctor.
        """
    )

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("End session"):
        st.session_state.user_phone = None
        st.session_state.messages = []
        st.rerun()
