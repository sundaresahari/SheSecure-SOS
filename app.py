import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SheSecure",
    page_icon="🚨",
    layout="centered"
)

# ---------------- LOAD DATA ----------------
data = pd.read_csv("threat_incident.csv")

# Demo malicious URLs
malicious_urls = [
    "http://fakebank-login.com",
    "http://free-money-now.net",
    "http://malware-download.org"
]

# Emergency contacts (DEMO numbers)
PARENT_NUMBER = "+918072740267"
GUARDIAN_NUMBER = "+916385205987"

# ---------------- TITLE ----------------
st.title("🚨 SheSecure")
st.markdown("### Intelligent Threat Protection & SOS Platform for Women’s Safety")

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🔐 Threat Protection", "🚨 SOS Emergency", "📊 Dashboard"]
)

# ================= HOME =================
if menu == "🏠 Home":
    st.write("""
    **SheSecure** is a mobile-first safety platform designed to protect women from
    **digital threats** and **physical danger**.

    ### Why SheSecure?
    - 🔐 Malicious link & unsafe area detection
    - 🚨 One-tap SOS emergency response
    - 📞 Instant contact with parents/guardians
    - 📱 Works on any smartphone browser

    👉 Built for **speed, prevention, and safety**.
    """)

# ================= THREAT PROTECTION =================
elif menu == "🔐 Threat Protection":
    st.header("🔐 Threat Protection")

    option = st.radio(
        "Choose Check Type",
        ["🌐 Malicious URL Check", "📍 Area Safety Check"]
    )

    # ---- URL CHECK ----
    if option == "🌐 Malicious URL Check":
        url = st.text_input("Enter URL")

        if st.button("Check URL"):
            if url.strip() == "":
                st.warning("Please enter a URL.")
            elif url in malicious_urls:
                st.error("❌ Malicious URL Detected")
                st.write("⚠️ Possible phishing or malware threat.")
            else:
                st.success("✅ URL appears safe (demo check).")

    # ---- AREA CHECK ----
    if option == "📍 Area Safety Check":
        location = st.selectbox("Select Location", data["Location"])

        if st.button("Check Area"):
            record = data[data["Location"] == location].iloc[0]

            if record["Incidents"] >= 5:
                st.error("🔴 High Risk Area")
            elif record["Incidents"] >= 2:
                st.warning("🟠 Medium Risk Area")
            else:
                st.success("🟢 Low Risk Area")

# ================= SOS EMERGENCY =================
elif menu == "🚨 SOS Emergency":
    st.header("🚨 SOS Emergency Assistance")

    location = st.selectbox("Your Current Location", data["Location"])
    live_location = st.text_input("Live Location (Google Maps link / Area name)")

    current_hour = datetime.datetime.now().hour
    time_status = "Night" if current_hour >= 18 or current_hour <= 6 else "Day"
    st.write(f"🕒 Time Detected: **{time_status}**")

    if st.button("🚨 ACTIVATE SOS"):
        record = data[data["Location"] == location].iloc[0]

        # Threat Intelligence Logic
        if record["Incidents"] >= 5 and time_status == "Night":
            st.error("🔴 HIGH RISK SITUATION")
        elif record["Incidents"] >= 3:
            st.warning("🟠 MODERATE RISK – Stay Alert")
        else:
            st.success("🟢 LOWER RISK – Stay Cautious")

        st.info(f"""
        🆘 **Emergency Instructions**
        - Move to a safe or crowded place
        - Contact your emergency contacts immediately
        - Share your location if possible

        📍 **Location:** {live_location if live_location else "Not shared"}
        """)

        # ---- CALL BUTTONS ----
        st.markdown(
            f"""
            <a href="tel:{PARENT_NUMBER}">
                <button style="background:#d62828;color:white;padding:14px;
                font-size:18px;border:none;border-radius:10px;width:100%;">
                📞 Call Parent
                </button>
            </a><br><br>

            <a href="tel:{GUARDIAN_NUMBER}">
                <button style="background:#6a040f;color:white;padding:14px;
                font-size:18px;border:none;border-radius:10px;width:100%;">
                📞 Call Guardian
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

        # ---- SMS BUTTON ----
        st.markdown(
            f"""
            <br>
            <a href="sms:{PARENT_NUMBER}?body=SOS!%20I%20am%20in%20danger.%20My%20location:%20{live_location}">
                <button style="background:#003049;color:white;padding:14px;
                font-size:18px;border:none;border-radius:10px;width:100%;">
                📩 Send SOS SMS
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

# ================= DASHBOARD =================
elif menu == "📊 Dashboard":
    st.header("📊 Threat Intelligence Dashboard")

    fig, ax = plt.subplots()
    ax.bar(data["Location"], data["Incidents"])
    ax.set_title("Incident Count by Location")
    ax.set_ylabel("Number of Incidents")
    ax.set_xticklabels(data["Location"], rotation=45)

    st.pyplot(fig)
    st.caption("Analyzing incident patterns helps predict unsafe areas.")
