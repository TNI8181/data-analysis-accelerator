import streamlit as st

st.title("6) 🤖 AI Mapping Assistant (Placeholder)")

st.info(
    "This page is a safe placeholder so navigation works. "
    "Next, we can add: source-to-target suggestions, semantic clustering, and fit-gap mapping outputs."
)

c1, c2 = st.columns([1, 2])
with c1:
    if st.button("➡️ Next: Export Center", type="primary"):
        st.switch_page("pages/7_Export_Center.py")

with c2:
    if st.button("⬅️ Back: Glossary Builder"):
        st.switch_page("pages/5_Glossary_Builder.py")
