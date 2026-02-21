import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Data Analysis Accelerator", layout="wide")
st.title("📂 Data Analysis Accelerator")

# ---------------------------------------------------
# Session State
# ---------------------------------------------------
if "profile_df" not in st.session_state:
    st.session_state["profile_df"] = pd.DataFrame()

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0  # used to reset file uploader

# ===================================================
# 🔄 UPLOAD REPORTS SECTION
# ===================================================
st.header("🔄 Upload Reports")

uploaded_files = st.file_uploader(
    "Upload report files (Excel or CSV)",
    type=["xlsx", "csv"],
    accept_multiple_files=True,
    key=f"uploader_{st.session_state['uploader_key']}"
)

# Buttons BELOW uploader (as requested)
btn1, btn2 = st.columns([1, 1])

with btn1:
    clear_update = st.button("🧹 Clear Records", use_container_width=True)

with btn2:
    process = st.button("✅ Process Files", type="primary", use_container_width=True)

if clear_update:
    st.session_state["profile_df"] = pd.DataFrame()
    st.session_state["uploader_key"] += 1  # forces file uploader reset
    st.success("Update section cleared.")
    st.stop()

if process:
    if not uploaded_files:
        st.warning("Please upload at least one file.")
        st.stop()

    #upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    profile_rows = []

    for f in uploaded_files:
        try:
            if f.name.lower().endswith(".csv"):
                df = pd.read_csv(f)
                for col in df.columns:
                    profile_rows.append({
                        "Report Name": f.name,
                        "Column Name": str(col),
                        #"Upload Time": upload_time
                    })
            else:
                xls = pd.ExcelFile(f)
                for sheet in xls.sheet_names:
                    df = xls.parse(sheet)
                    for col in df.columns:
                        profile_rows.append({
                            "Report Name": f.name,
                            "Column Name": str(col),
                            #"Upload Time": upload_time
                        })
        except Exception as e:
            st.error(f"Error reading {f.name}: {e}")

    st.session_state["profile_df"] = pd.DataFrame(profile_rows)
    st.success("Files processed successfully.")

st.divider()

# ===================================================
# 📊 PROFILE SECTION
# ===================================================
st.header("📊 Profile")

if not st.session_state["profile_df"].empty:
    st.dataframe(st.session_state["profile_df"], use_container_width=True)
else:
    st.info("No profile data available. Upload and process files above.")
