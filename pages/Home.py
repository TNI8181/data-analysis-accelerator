import streamlit as st

st.set_page_config(page_title="Data Analysis Accelerator", layout="wide")

st.title("🚀 Data Analysis Accelerator")
st.caption("Enterprise Insurance Data Discovery & Standardization Platform")

st.markdown("## Modules")

st.page_link("pages/1_Upload_&_Profile.py", label="📂 Upload & Profile Reports")
st.page_link("pages/2_Field_Inventory.py", label="📋 Field Inventory")
st.page_link("pages/3_Cross_Tab_Analyzer.py", label="📊 Cross Tab Analyzer")
st.page_link("pages/4_Normalization_Engine.py", label="🔄 Normalization Engine")
st.page_link("pages/5_Glossary_Builder.py", label="📘 Glossary Builder")
st.page_link("pages/6_AI_Mapping_Assistant.py", label="🤖 AI Mapping Assistant")
st.page_link("pages/7_Export_Center.py", label="⬇️ Export Center")
