import streamlit as st

st.set_page_config(
    page_title="Data Analysis Accelerator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏢 Data Analysis Accelerator (Base)")
st.caption("Multipage app. Start with Upload & Profile → Field Inventory → Cross Tab → Normalization → Glossary → Export.")

st.markdown("### Start here")
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("➡️ Go to Upload & Profile", type="primary"):
        st.switch_page("pages/1_Upload_&_Profile.py")

with col2:
    st.info("Use the left sidebar to navigate pages. Upload files once; other pages reuse cached results from session_state.")

st.markdown("---")

st.markdown("### Quick reset (clears everything)")
if st.button("🧹 Clear ALL Session Data"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.success("Cleared session_state. Now go to Upload & Profile.")
