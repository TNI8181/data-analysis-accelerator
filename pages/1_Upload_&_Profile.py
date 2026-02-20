import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Data Analysis Accelerator", layout="wide")

st.title("📂 Data Analysis Accelerator")

# Initialize session state
if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = []

if "profile_df" not in st.session_state:
    st.session_state["profile_df"] = pd.DataFrame()

# ==========================================================
# 🔹 SECTION 1 — UPDATE (File Upload Only)
# ==========================================================
st.header("🔄 Update Reports")

uploaded_files = st.file_uploader(
    "Upload report files (Excel or CSV)",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

if st.button("Update Reports"):

    if not uploaded_files:
        st.warning("Please upload at least one file.")
        st.stop()

    st.session_state["uploaded_files"] = uploaded_files
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    profile_rows = []

    for f in uploaded_files:
        try:
            # CSV Handling
            if f.name.lower().endswith(".csv"):
                df = pd.read_csv(f)

                for col in df.columns:
                    profile_rows.append({
                        "Report Name": f.name,
                        "Column Name": col,
                        "Upload Time": upload_time
                    })

            # Excel Handling
            else:
                xls = pd.ExcelFile(f)
                for sheet in xls.sheet_names:
                    df = xls.parse(sheet)

                    for col in df.columns:
                        profile_rows.append({
                            "Report Name": f.name,
                            "Column Name": col,
                            "Upload Time": upload_time
                        })

        except Exception as e:
            st.error(f"Error reading {f.name}: {e}")

    profile_df = pd.DataFrame(profile_rows)
    st.session_state["profile_df"] = profile_df

    st.success("Reports updated successfully.")

# ==========================================================
# 🔹 SECTION 2 — PROFILE (Metadata View)
# ==========================================================
st.header("📊 Profile")

if not st.session_state["profile_df"].empty:

    st.dataframe(
        st.session_state["profile_df"],
        use_container_width=True
    )

else:
    st.info("No reports uploaded yet. Use the Update section above.")
