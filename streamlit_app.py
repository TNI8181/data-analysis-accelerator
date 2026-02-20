import streamlit as st

st.set_page_config(page_title="Data Analysis Accelerator", layout="wide")

pages = {
    "Data Analysis Accelerator": [
        st.Page("pages/1_Upload_&_Profile.py", title="Upload & Profile", icon="📤"),
        st.Page("pages/2_Field_Inventory.py", title="Field Inventory", icon="📋"),
        st.Page("pages/3_Cross_Tab_Analyzer.py", title="Cross Tab Analyzer", icon="📊"),
        st.Page("pages/4_Normalization_Engine.py", title="Normalization Engine", icon="🔄"),
        st.Page("pages/5_Glossary_Builder.py", title="Glossary Builder", icon="📘"),
        st.Page("pages/6_AI_Mapping_Assistant.py", title="AI Mapping Assistant", icon="🤖"),
        st.Page("pages/7_Export_Center.py", title="Export Center", icon="📦"),
    ]
}

pg = st.navigation(pages)
pg.run()
