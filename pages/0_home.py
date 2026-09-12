import streamlit as st

st.set_page_config(
    page_title="Medibot Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOGIN CHECK ----------------
if "user_profile" not in st.session_state:
    st.switch_page("login.py")

profile = st.session_state.user_profile

# ---------------- HIDE DEFAULT PAGE NAV ----------------
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Medibot")

if "profile_pic" not in st.session_state:
    st.session_state.profile_pic = None

uploaded_file = st.sidebar.file_uploader("Upload Profile", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.session_state.profile_pic = uploaded_file

if st.session_state.profile_pic:
    st.sidebar.image(st.session_state.profile_pic, width=80)
else:
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)

st.sidebar.markdown(f"""
{profile.get("first_name","")} {profile.get("last_name","")}  
{profile.get("email","")}
""")

st.sidebar.markdown("---")

st.sidebar.markdown("👤 Profile")

if st.sidebar.button("⚙️ Settings"):
    st.switch_page("settings")

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("login.py")

# ---------------- LANGUAGE ----------------
TRANSLATIONS = {
    "en": {
        "title": "🏠 Medibot Dashboard",
        "profile": "User Profile",
        "first_name": "First Name",
        "last_name": "",
        "email": "Email",
        "provider": "Provider",
        "provider_local": "Local",
        "provider_google": "Google",
    }
}

if "lang" not in st.session_state:
    st.session_state.lang = "en"

def t(key):
    return TRANSLATIONS[st.session_state.lang][key]

# ---------------- LAYOUT ----------------
main, right = st.columns([3,1])

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: url("https://www.intertek.com/siteassets/blogs/2024-04-16-blog-widebanner.jpg") no-repeat center center fixed;
    background-size: cover;
}

.stApp::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(4px);
    z-index: -1;
}

.label { color: rgb(14, 17, 23); }
.value { font-weight: 600; margin-bottom: 10px; }

div.stButton > button {
    border-radius: 12px;
    background: #0f172a;
    color: white;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MAIN ----------------
with main:

    st.markdown(f"## {t('title')}")
    st.subheader(t("profile"))

    provider = profile.get("auth_provider", "local")
    provider_text = "Google" if provider == "google" else "Local"

    for label, value in [
        (t("first_name"), profile.get("first_name", "")),
        (t("last_name"), profile.get("last_name", "")),
        (t("email"), profile.get("email", "")),
        (t("provider"), provider_text),
    ]:
        st.markdown(f"<div class='label'>{label}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='value'>{value}</div>", unsafe_allow_html=True)

# ---------------- RIGHT SIDE ----------------
with right:
    st.markdown("### 📂 Pages")

    if st.button("0 Home", use_container_width=True):
        st.switch_page("pages/0_home.py")

    if st.button("1 Dashboard", use_container_width=True):
        st.switch_page("pages/1_dashboard.py")

    if st.button("2 Disease", use_container_width=True):
        st.switch_page("pages/2_Disease-Prediction-and-medical-recommendation.py")

    if st.button("3 Drug", use_container_width=True):
        st.switch_page("pages/3_drug_recommendation.py")

    if st.button("4 Heart", use_container_width=True):
        st.switch_page("pages/4_heart_Disease_Risk_Assesment.py")

    if st.button("5 Medibot", use_container_width=True):
        st.switch_page("pages/5_Medibot.py")