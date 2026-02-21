import streamlit as st
import pandas as pd

st.title("2) 🧾 Field Inventory")

def ensure_uploads():
    if "uploaded_files" not in st.session_state:
        st.warning("Upload files first (go to Upload & Profile).")
        st.stop()

def build_field_inventory(uploaded_files):
    rows = []
    for f in uploaded_files:
        try:
            if f.name.lower().endswith(".csv"):
                df = pd.read_csv(f)
                for col in df.columns:
                    rows.append({
                        "report_name": f.name,              # ✅ file name only
                        "column_original": str(col)         # ✅ never modified
                    })
            else:
                xls = pd.ExcelFile(f)
                for sheet in xls.sheet_names:
                    df = xls.parse(sheet)
                    for col in df.columns:
                        rows.append({
                            "report_name": f.name,          # ✅ file name only (ignore sheet)
                            "column_original": str(col)
                        })
        except Exception as e:
            st.error(f"Could not process {f.name}: {e}")
    return pd.DataFrame(rows)

def clear_this_page():
    for k in ["field_df", "cross_tab_df", "mapping_df", "normalized_field_df", "glossary_df"]:
        if k in st.session_state:
            del st.session_state[k]

ensure_uploads()

top1, top2, top3 = st.columns([1, 1, 2])
with top1:
    if st.button("🔄 Rebuild Inventory"):
        st.session_state["field_df"] = build_field_inventory(st.session_state["uploaded_files"])
with top2:
    if st.button("🧹 Clear Inventory Outputs"):
        clear_this_page()
        st.rerun()

if "field_df" not in st.session_state:
    st.session_state["field_df"] = build_field_inventory(st.session_state["uploaded_files"])

field_df = st.session_state["field_df"]

st.subheader("Raw Field Inventory")
st.caption("report_name = file name only. column_original preserved exactly.")
st.dataframe(field_df, use_container_width=True)

csv_bytes = field_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Field Inventory (CSV)", data=csv_bytes, file_name="field_inventory.csv", mime="text/csv")

if st.button("➡️ Next: Cross Tab Analyzer"):
    st.switch_page("pages/3_Cross_Tab_Analyzer.py")
