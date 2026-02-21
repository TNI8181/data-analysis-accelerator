import streamlit as st
import pandas as pd

st.title("5) 📚 Glossary Builder")

def ensure_normalized():
    if "normalized_field_df" not in st.session_state:
        st.warning("No normalized fields found. Go to Normalization Engine first.")
        st.stop()

ensure_normalized()
nf = st.session_state["normalized_field_df"].copy()

gloss_fields = sorted([x for x in nf["column_homogenized"].dropna().astype(str).unique().tolist() if x.strip() != ""])
base = pd.DataFrame({
    "field_name": gloss_fields,
    "business_definition": ["" for _ in gloss_fields],
    "notes": ["" for _ in gloss_fields]
})

st.caption("Fill definitions. Export later from Export Center (or download here).")

glossary_df = st.data_editor(
    st.session_state.get("glossary_df", base),
    use_container_width=True,
    num_rows="dynamic"
)

c1, c2 = st.columns([1, 2])
with c1:
    if st.button("💾 Save Glossary", type="primary"):
        st.session_state["glossary_df"] = glossary_df
        st.success("Saved glossary.")
with c2:
    if st.button("➡️ Next: AI Mapping Assistant"):
        st.switch_page("pages/6_AI_Mapping_Assistant.py")

csv_bytes = glossary_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Glossary (CSV)", data=csv_bytes, file_name="glossary.csv", mime="text/csv")
