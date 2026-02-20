import streamlit as st
import pandas as pd

st.title("📊 Report vs Field Cross Tab")

if "field_df" not in st.session_state:
    st.warning("Generate field inventory first.")
    st.stop()

field_df = st.session_state["field_df"]

cross_tab = pd.crosstab(
    field_df["column_original"],
    field_df["report_name"]
)

cross_tab = cross_tab.applymap(lambda v: "x" if v > 0 else "")

st.dataframe(cross_tab, use_container_width=True)
