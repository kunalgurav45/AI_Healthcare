import streamlit as st
from pymongo import MongoClient
import bcrypt
from datetime import datetime, timezone

# 🔥 REDIRECT CHECK (FIXED TOP PE)
if "user_profile" in st.session_state:
    st.switch_page("pages/0_home.py")
    st.stop()

st.set_page_config(page_title="Medibot Login", page_icon="🩺", layout="wide", initial_sidebar_state="collapsed")

# ---------------- DB ----------------
users = None
db_error = None
try:
    client = MongoClient(st.secrets["mongo_uri"], serverSelectionTimeoutMS=3000)
    client.admin.command("ping")
    db = client[st.secrets["mongo_db_name"]]
    users = db["users"]
except Exception as error:
    db_error = str(error)

st.sidebar.empty()

# ---------------- SESSION ----------------
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# ---------------- CSS ----------------
st.markdown("""<style>
html, body, .stApp {height: 100vh !important; overflow: hidden !important;}
header, [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
[data-testid="stSidebar"] {display: none !important;}
.block-container {padding-top: 0rem !important; padding-bottom: 0rem !important;}
section.main {height: 100vh; display: flex; align-items: center;}
.stApp {
background-image: url("https://static.investindia.gov.in/s3fs-public/2025-05/medical-technology-blog-banner-7.jpg");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
}
.stApp::before {
content: ""; position: fixed; width: 100%; height: 100%;
background: rgba(0, 120, 200, 0.55); z-index: -1;
}
div[data-testid="stTextInput"] input {
border-radius: 25px !important;
padding: 10px 14px !important;
background: rgba(255,255,255,0.9) !important;
color: black !important;
}
label {color: white !important;}
div.stButton > button {
border-radius: 25px !important;
height: 40px !important;
font-weight: 600;
background: linear-gradient(90deg, #00C6FF, #0072FF);
color: white !important;
border: none;
}
h1, h2, h3, p {color: white !important;}
</style>""", unsafe_allow_html=True)

if db_error:
    st.warning("Database is unavailable. Update the MongoDB URI in .streamlit/secrets.toml before logging in or signing up.")

# ---------------- LANGUAGE ----------------
TRANSLATIONS = {
"en": {"app_name":"Medibot","tagline":"AI Powered Healthcare Assistant","signup_title":"Create Account","first_name":"First Name","last_name":"Last Name","email":"Email","password":"Password","confirm_password":"Confirm Password","signup_btn":"Sign Up","google_btn":"Sign Up with Google"},
"hi": {"app_name":"मेडीबोट","tagline":"एआई हेल्थकेयर असिस्टेंट","signup_title":"अकाउंट बनाएं","first_name":"पहला नाम","last_name":"अंतिम नाम","email":"ईमेल","password":"पासवर्ड","confirm_password":"पासवर्ड पुष्टि","signup_btn":"साइन अप","google_btn":"गूगल से साइन अप"},
"mr": {"app_name":"मेडीबोट","tagline":"एआय आधारित आरोग्य सहाय्यक","signup_title":"अकाउंट तयार करा","first_name":"पहिले नाव","last_name":"आडनाव","email":"ईमेल","password":"पासवर्ड","confirm_password":"पासवर्ड पुन्हा टाका","signup_btn":"साइन अप","google_btn":"गूगलने साइन अप करा"}
}

if "lang" not in st.session_state:
    st.session_state.lang = "en"

def t(key):
    return TRANSLATIONS[st.session_state.lang][key]

# ---------------- LANGUAGE ----------------
top_left, top_right = st.columns([6,2])
with top_right:
    st.session_state.lang = st.selectbox("", ["en","hi","mr"])

# ---------------- LAYOUT ----------------
left, right = st.columns([1,1])  
with left:
    st.markdown(f"<h1 style='font-size:50px'>{t('app_name')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:18px'>{t('tagline')}</p>", unsafe_allow_html=True)

with right:

    # -------- LOGIN --------
    if st.session_state.show_login:
        st.markdown("### Login")

        email_login = st.text_input("Email")
        password_login = st.text_input("Password", type="password")

        if st.button("Login"):
            if users is None:
                st.error("Login is unavailable until the MongoDB connection is restored.")
                st.stop()

            user = users.find_one({"email": email_login})

            if user:
                # 🔥 FIX: password ko bytes me convert kar
                stored_password = user.get("password") or user.get("password_hash")

                if isinstance(stored_password, str):
                    stored_password = stored_password.encode()

                if bcrypt.checkpw(password_login.encode(), stored_password):

                    st.session_state["user_profile"] = {
                        "first_name": user.get("first_name", user.get("name", "")),
                        "last_name": user.get("last_name", ""),
                        "email": user["email"],
                        "auth_provider": "local"
                    }

                    st.success("Login successful ✅")
                    st.switch_page("pages/0_home.py")
                    st.stop()

                else:
                    st.error("Wrong password ❌")

            else:
                st.error("User not found ❌")

    # -------- SIGNUP --------
    else:
        st.markdown(f"### {t('signup_title')}")

        with st.form("signup"):
            c1, c2 = st.columns(2)
            with c1:
                first = st.text_input(t("first_name"))
            with c2:
                last = st.text_input(t("last_name"))

            email = st.text_input(t("email"))
            password = st.text_input(t("password"), type="password")
            confirm = st.text_input(t("confirm_password"), type="password")

            col1, col2 = st.columns(2)

            with col1:
                submit = st.form_submit_button(t("signup_btn"))

            with col2:
                login_click = st.form_submit_button("Login")

            if submit:
                if users is None:
                    st.error("Signup is unavailable until the MongoDB connection is restored.")
                elif not first or not last or not email or not password:
                    st.warning("Fill all fields")
                elif password != confirm:
                    st.error("Password mismatch")
                else:
                    existing = users.find_one({"email": email})
                    if existing:
                        st.error("User already exists ⚠️")
                    else:
                        users.insert_one({
                            "name": first,
                            "email": email,
                            # 🔥 FIX: ensure bytes store ho
                            "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
                            "created": datetime.now(timezone.utc)
                        })
                        st.success("Signup successful ✅")
                        st.session_state.show_login = True
                        st.rerun()

        google = st.button(t("google_btn"), use_container_width=True)

# ---------------- ACTION ----------------
if 'login_click' in locals() and login_click:
    st.session_state.show_login = True
    st.rerun()

if 'google' in locals() and google:
    st.login()