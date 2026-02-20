import streamlit as st
import pandas as pd

st.title("📂 Upload & Profile Reports")

source_system = st.text_input("Source System Name")

uploaded_files = st.file_uploader(
    "Upload report files",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

if st.button("Process Files"):

    if not uploaded_files:
        st.warning("Upload files first.")
        st.stop()

    if not source_system.strip():
        st.warning("Enter source system.")
        st.stop()

    st.session_state["source_system"] = source_system
    st.session_state["uploaded_files"] = uploaded_files

    profile_rows = []

    for f in uploaded_files:
        try:
            if f.name.lower().endswith(".csv"):
                df = pd.read_csv(f)
                profile_rows.append({
                    "file_name": f.name,
                    "rows": len(df),
                    "columns": len(df.columns)
                })
            else:
                xls = pd.ExcelFile(f)
                for sheet in xls.sheet_names:
                    df = xls.parse(sheet)
                    profile_rows.append({
                        "file_name": f.name,
                        "sheet_name": sheet,
                        "rows": len(df),
                        "columns": len(df.columns)
                    })
        except Exception as e:
            st.error(f"Error reading {f.name}: {e}")

    profile_df = pd.DataFrame(profile_rows)
    st.session_state["profile_df"] = profile_df

    st.success("Files processed.")
    st.dataframe(profile_df, use_container_width=True)
