import streamlit as st
import pandas as pd

st.title("3) ✅ Cross Tab Analyzer")

def ensure_field_df():
    if "field_df" not in st.session_state:
        st.warning("Field Inventory not found. Go to Field Inventory first.")
        st.stop()

def build_crosstab(field_df: pd.DataFrame):
    ct = pd.crosstab(field_df["column_original"], field_df["report_name"])
    return ct.applymap(lambda v: "x" if v > 0 else "")

def clear_this_page():
    for k in ["cross_tab_df"]:
        if k in st.session_state:
            del st.session_state[k]

ensure_field_df()
field_df = st.session_state["field_df"]

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    if st.button("🔄 Rebuild Cross Tab", type="primary"):
        st.session_state["cross_tab_df"] = build_crosstab(field_df)
with c2:
    if st.button("🧹 Clear Cross Tab"):
        clear_this_page()
        st.rerun()

if "cross_tab_df" not in st.session_state:
    st.session_state["cross_tab_df"] = build_crosstab(field_df)

cross_tab_df = st.session_state["cross_tab_df"]

st.subheader("Report vs Field (x = present)")
search = st.text_input("Filter by column name contains:", value="").strip()

view_df = cross_tab_df
if search:
    view_df = view_df[view_df.index.astype(str).str.contains(search, case=False, na=False)]

st.dataframe(view_df, use_container_width=True)

csv_bytes = cross_tab_df.reset_index().to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Cross Tab (CSV)", data=csv_bytes, file_name="cross_tab.csv", mime="text/csv")

if st.button("➡️ Next: Normalization Engine"):
    st.switch_page("pages/4_Normalization_Engine.py")
