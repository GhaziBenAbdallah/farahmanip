# import streamlit as st

# st.components.v1.iframe(
#     "https://docs.google.com/forms/d/e/1FAIpQLSfFXvoZffUTZVqE_dQ_1ugzCfBOxJofDhDx4Oi8ppfWeDhEnw/viewform?embedded=true",
#     height=520,
#     width=700,
#     scrolling=True
# )



# import streamlit as st
# import time
# import secrets
# import qrcode
# from io import BytesIO
# import json
# import os
# import threading

# TOKEN_DURATION = 20 * 60
# TOKEN_FILE = "token_store.json"

# _lock = threading.Lock()

# # ─── File helpers ───

# def load_token():
#     if not os.path.exists(TOKEN_FILE):
#         return {"token": None, "expiry": 0}

#     with open(TOKEN_FILE, "r") as f:
#         return json.load(f)

# def save_token(token, expiry):
#     with open(TOKEN_FILE, "w") as f:
#         json.dump({"token": token, "expiry": expiry}, f)

# # ─── Token logic ───

# def generate_token():
#     with _lock:
#         token = secrets.token_urlsafe(16)
#         expiry = time.time() + TOKEN_DURATION
#         save_token(token, expiry)
#     return token

# def is_token_valid(check_token):
#     with _lock:
#         data = load_token()
#         if not data["token"]:
#             return False
#         if check_token != data["token"]:
#             return False
#         return time.time() < data["expiry"]

# # ─── QR ───

# def generate_qr(url):
#     img = qrcode.make(url)
#     buf = BytesIO()
#     img.save(buf, format="PNG")
#     return buf.getvalue()

# # ─── UI ───

# st.title("Accès sécurisé via QR")

# BASE_URL = "farahmanip.streamlit.app"
# if st.button("Générer QR sécurisé"):
#     token = generate_token()
#     link = f"{BASE_URL}/?token={token}"
#     st.image(generate_qr(link), width=300)
#     st.code(link)

# # ─── Verification ───

# token_param = st.query_params.get("token")

# if token_param:
#     if is_token_valid(token_param):
#         st.success("Accès autorisé ✅")
#         st.components.v1.iframe(
#             "https://docs.google.com/forms/d/e/1FAIpQLSc_WIQH1I6QC4uBqxPqjzobHT09P4bbzPa_MbB438FN8kY7NQ/viewform?embedded=true",
#             height=600,
#             width=760,
#             scrolling=True
#         )
#     else:
#         st.error("QR expiré ou invalide ❌")



import streamlit as st
st.set_page_config(page_title="QR Secure Access", layout="centered")

import time
import secrets
import qrcode
from io import BytesIO
import json
import os
import threading

# =====================
# CONFIG
# =====================

TOKEN_DURATION = 20 * 60  # 20 minutes
TOKEN_FILE = "token_store.json"
ADMIN_SECRET = "VIP-2026"     # 🔐 change this
BASE_URL = "https://farahmanip.streamlit.app/"

_lock = threading.Lock()

# =====================
# FILE STORAGE
# =====================

def load_token():
    if not os.path.exists(TOKEN_FILE):
        return {"token": None, "expiry": 0}

    with open(TOKEN_FILE, "r") as f:
        return json.load(f)

def save_token(token, expiry):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token, "expiry": expiry}, f)

# =====================
# TOKEN LOGIC
# =====================

def generate_token():
    with _lock:
        token = secrets.token_urlsafe(16)
        expiry = time.time() + TOKEN_DURATION
        save_token(token, expiry)
    return token

def is_token_valid(check_token):
    with _lock:
        data = load_token()
        if not data["token"]:
            return False
        if check_token != data["token"]:
            return False
        return time.time() < data["expiry"]

# =====================
# QR GENERATION
# =====================

def generate_qr(url):
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# =====================
# UI LOGIC
# =====================

st.title("🔒 Secure QR Access System")

token_param = st.query_params.get("token")

# ==================================================
# USER MODE (QR scanned)
# ==================================================
if token_param:

    if is_token_valid(token_param):
        st.success("✅ Access granted")
        # st.write("🎉 Welcome to protected content!")
        st.components.v1.iframe(
            "https://docs.google.com/forms/d/e/1FAIpQLSc_WIQH1I6QC4uBqxPqjzobHT09P4bbzPa_MbB438FN8kY7NQ/viewform?embedded=true",
            height=600,
            width=760,
            scrolling=True
        )
    else:
        st.error("❌ QR expired or invalid")

    st.stop()   # ⛔ Prevent admin UI from loading

# ==================================================
# ADMIN MODE (Home page)
# ==================================================

st.subheader("🔐 Admin Login")

secret = st.text_input("Enter secret code", type="password")

if secret == ADMIN_SECRET:

    st.success("Admin unlocked 🔓")

    if st.button("Generate secure QR"):

        token = generate_token()
        secure_link = f"{BASE_URL}/?token={token}"

        st.image(generate_qr(secure_link), width=280)
        st.code(secure_link)

        expires_in = int(load_token()["expiry"] - time.time())
        st.info(f"⏳ Expires in {expires_in//60} minutes")

elif secret:
    st.error("Wrong secret code ❌")
