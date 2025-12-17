# streamlit_app.py
import asyncio
import re
import pandas as pd
import streamlit as st

from my_bot import CustomerSupportBot
from order_logs import ORDER_DB, describe_order, describe_all_orders


@st.cache_resource
def get_bot():
    return CustomerSupportBot()


async def get_kare_reply(history):
    bot = get_bot()
    return await bot.respond(history)


# ---------------- HELPER FUNCTIONS ----------------

def extract_order_ids(text):
    return re.findall(r"\b\d{6}\b", text)


def is_greeting(text):
    t = text.lower().strip()
    return t in {"hi", "hello", "hey", "hii", "help", "support", "menu", "help me"}


def is_vague(text):
    t = text.lower()
    vague_patterns = [
        "i need help", "something went wrong",
        "issue", "problem", "help", "support"
    ]
    return any(p in t for p in vague_patterns)


def user_confirmed(text):
    return text.strip().lower() in {
        "yes", "yeah", "yep", "correct",
        "that's correct", "thats correct", "y"
    }


def model_should_show_menu(user_text):
    return is_greeting(user_text) or is_vague(user_text)


# ---------------- SYSTEM INJECTION ENGINE ----------------

def inject_kare_system_messages(history, last_msg):
    extra = []

    # 0) Identity check
    if "phone" not in st.session_state or "email" not in st.session_state:
        extra.append({"role": "system", "content": "USER_IDENTITY_MISSING"})
        return extra

    ids = extract_order_ids(last_msg)

    # 1) Smart menu
    if model_should_show_menu(last_msg):
        extra.append({"role": "system", "content": "SMART_MENU_TRIGGER"})
        return extra

    # 2) Order ID provided
    if ids:
        oid = ids[0]
        if oid in ORDER_DB:
            extra.append({"role": "system",
                          "content": f"ORDER_ID_GIVEN_EXISTS {oid}. Wait for user confirmation."})
        else:
            extra.append({"role": "system",
                          "content": f"ORDER_ID_INVALID {oid}. Ask user to pick from valid orders."})
        return extra

    # 3) User said YES
    if user_confirmed(last_msg):
        prev = None
        for msg in reversed(history[:-1]):
            if msg["role"] == "assistant":
                prev = msg["content"]
                break

        if prev:
            prev_ids = extract_order_ids(prev)
            if prev_ids:
                oid = prev_ids[0]
                if oid in ORDER_DB:
                    extra.append({"role": "system",
                                  "content": f"ORDER_CONFIRMED {oid}"})
                    extra.append({"role": "system",
                                  "content": describe_order(oid)})
                    return extra

        extra.append({"role": "system", "content": "NO_ORDER_TO_CONFIRM"})
        return extra

    return extra


# ---------------- STREAMLIT UI ----------------

def main():
    st.set_page_config(page_title="Swiggy Support Simulation", layout="centered")
    st.title("Swiggy Support Simulation")
    st.caption("Test your system prompt on real complaints and export transcripts.\nDesigned by Architha A Murthy")

    # ---------- IDENTITY FORM (PHASE 0) ----------
    st.subheader("User Verification (Demo)")
    phone = st.text_input("Enter your phone number")
    email = st.text_input("Enter your email")

    if phone:
        st.session_state["phone"] = phone
    if email:
        st.session_state["email"] = email

    # -------- Session Setup --------
    if "history" not in st.session_state:
        st.session_state.history = []

    if "attachments" not in st.session_state:
        st.session_state.attachments = []

    # -------- Render History --------
    for msg in st.session_state.history:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])

    # -------- Attachments --------
    uploaded = st.file_uploader(
        "Attach images (optional) — e.g., burnt food, wrong item, damaged packaging",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
    )

    user_text = st.chat_input("Type a complaint or reply")

    if user_text:
        idx = len(st.session_state.history)
        st.session_state.history.append({"role": "user", "content": user_text})

        extra = []

        # Handle images
        if uploaded:
            filenames = [f.name for f in uploaded]
            st.session_state.attachments.append(
                {"turn_index": idx, "filenames": filenames}
            )
            extra.append({"role": "system",
                          "content": f"User uploaded {len(filenames)} images. Assume they support the issue."})

        # Inject system rules
        extra += inject_kare_system_messages(st.session_state.history, user_text)

        # Identity block always included
        identity = {
            "role": "system",
            "content": f"USER_IDENTITY phone={st.session_state.get('phone')} email={st.session_state.get('email')}"
        }

        messages_for_model = [identity, *extra, *st.session_state.history]

        reply = asyncio.run(get_kare_reply(messages_for_model))
        st.session_state.history.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)

    # -------- Export / Reset --------
    st.markdown("---")
    if st.session_state.history:
        c1, c2 = st.columns(2)

        with c1:
            if st.button("Clear conversation"):
                st.session_state.history = []
                st.session_state.attachments = []
                st.rerun()

        with c2:
            if st.button("Reset"):
                st.session_state.clear()
                st.rerun()

        out = []
        for m in st.session_state.history:
            out.append(f"{m['role'].upper()}:\n{m['content']}\n\n")

        st.download_button(
            "Download conversation as TXT",
            data="".join(out).encode("utf-8"),
            file_name="kare_conversation.txt",
        )


if __name__ == "__main__":
    main()
