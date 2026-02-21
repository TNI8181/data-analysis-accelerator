import streamlit as st
import pandas as pd
from io import BytesIO

st.title("7) 📤 Export Center")

def add_sheet(writer, key, sheet_name):
    if key in st.session_state:
        df = st.session_state[key]
        if df is not None and hasattr(df, "to_excel"):
            df.to_excel(writer, index=False, sheet_name=sheet_name)

st.caption("Exports everything available in session_state into one Excel workbook.")

c1, c2 = st.columns([1, 2])
with c1:
    if st.button("🧹 Clear ALL Outputs"):
        for k in ["profile_df","field_df","cross_tab_df","mapping_df","normalized_field_df","glossary_df"]:
            if k in st.session_state:
                del st.session_state[k]
        st.success("Cleared outputs (uploads still retained).")

# Build export
buffer = BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    if "profile_df" in st.session_state:
        st.session_state["profile_df"].to_excel(writer, index=False, sheet_name="Profile")

    if "field_df" in st.session_state:
        st.session_state["field_df"].to_excel(writer, index=False, sheet_name="Field_Inventory")

    if "cross_tab_df" in st.session_state:
        # crosstab has index; write it cleanly
        st.session_state["cross_tab_df"].reset_index().to_excel(writer, index=False, sheet_name="Cross_Tab")

    if "mapping_df" in st.session_state:
        st.session_state["mapping_df"].to_excel(writer, index=False, sheet_name="Normalization_Map")

    if "normalized_field_df" in st.session_state:
        st.session_state["normalized_field_df"].to_excel(writer, index=False, sheet_name="Normalized_Inventory")

    if "glossary_df" in st.session_state:
        st.session_state["glossary_df"].to_excel(writer, index=False, sheet_name="Glossary")

st.download_button(
    "⬇️ Download Accelerator Outputs (XLSX)",
    data=buffer.getvalue(),
    file_name="data_analysis_accelerator_outputs.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("---")
if st.button("⬅️ Back to Upload & Profile"):
    st.switch_page("pages/1_Upload_&_Profile.py")
