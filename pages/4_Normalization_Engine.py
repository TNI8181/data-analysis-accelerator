import streamlit as st
import pandas as pd

st.title("4) 🧠 Normalization Engine")

def ensure_field_df():
    if "field_df" not in st.session_state:
        st.warning("Field Inventory not found. Go to Field Inventory first.")
        st.stop()

def clear_norm_outputs():
    for k in ["mapping_df", "normalized_field_df", "glossary_df"]:
        if k in st.session_state:
            del st.session_state[k]

ensure_field_df()
field_df = st.session_state["field_df"].copy()

st.caption("You define how columns homogenize. We never change column_original; we add column_homogenized.")

# Simple default suggestion: trim + collapse spaces + lower + underscores
def suggest_homogenized(col: str) -> str:
    s = str(col).strip()
    s = " ".join(s.split())
    s = s.replace(" ", "_")
    return s.lower()

distinct_cols = sorted(field_df["column_original"].dropna().astype(str).unique().tolist())
default_map = pd.DataFrame({
    "column_original": distinct_cols,
    "column_homogenized": [suggest_homogenized(c) for c in distinct_cols]
})

st.markdown("### Option A: Auto-suggest mapping (editable)")
edited_map = st.data_editor(
    st.session_state.get("mapping_df", default_map),
    use_container_width=True,
    num_rows="dynamic"
)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("💾 Save Mapping", type="primary"):
        st.session_state["mapping_df"] = edited_map
        st.success("Saved mapping.")
with col2:
    if st.button("🧹 Clear Normalization Outputs"):
        clear_norm_outputs()
        st.rerun()

if "mapping_df" in st.session_state:
    mapping_df = st.session_state["mapping_df"].copy()

    # Apply mapping
    map_dict = dict(zip(mapping_df["column_original"].astype(str), mapping_df["column_homogenized"].astype(str)))
    field_df["column_homogenized"] = field_df["column_original"].astype(str).map(map_dict).fillna("")

    st.subheader("Normalized Field Inventory")
    st.dataframe(field_df, use_container_width=True)

    st.session_state["normalized_field_df"] = field_df

    csv_bytes = mapping_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Mapping (CSV)", data=csv_bytes, file_name="normalization_mapping.csv", mime="text/csv")

    if st.button("➡️ Next: Glossary Builder"):
        st.switch_page("pages/5_Glossary_Builder.py")
else:
    st.info("Save a mapping to generate normalized output.")
