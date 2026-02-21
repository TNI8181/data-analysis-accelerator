import streamlit as st
import pandas as pd

st.title("1) 📥 Upload & Profile")

# -----------------------------
# Helpers
# -----------------------------
def clear_upload_state():
    for k in [
        "source_system", "uploaded_files",
        "profile_df", "field_df",
        "cross_tab_df", "mapping_df",
        "normalized_field_df", "glossary_df"
    ]:
        if k in st.session_state:
            del st.session_state[k]

def build_profile(uploaded_files, exclude_consolidated: bool):
    rows = []
    for f in uploaded_files:
        try:
            if f.name.lower().endswith(".csv"):
                df = pd.read_csv(f)
                rows.append({
                    "file_name": f.name,
                    "sheet_name": "(csv)",
                    "rows": len(df),
                    "columns": len(df.columns),
                    "sample_columns": ", ".join([str(c) for c in df.columns[:12]])
                })
            else:
                xls = pd.ExcelFile(f)
                for sheet in xls.sheet_names:
                    if exclude_consolidated and "consolidated" in sheet.lower():
                        continue
                    df = xls.parse(sheet)
                    rows.append({
                        "file_name": f.name,
                        "sheet_name": sheet,
                        "rows": len(df),
                        "columns": len(df.columns),
                        "sample_columns": ", ".join([str(c) for c in df.columns[:12]])
                    })
        except Exception as e:
            rows.append({
                "file_name": f.name,
                "sheet_name": "(error)",
                "rows": None,
                "columns": None,
                "sample_columns": f"ERROR: {e}"
            })
    return pd.DataFrame(rows)

# -----------------------------
# UI
# -----------------------------
colA, colB = st.columns([2, 1])

with colA:
    source_system = st.text_input(
        "Source System Name",
        value=st.session_state.get("source_system", "")
    )

with colB:
    exclude_consolidated = st.checkbox(
        "Exclude sheets containing 'Consolidated'",
        value=True
    )

uploaded_files = st.file_uploader(
    "Upload report files (Excel/CSV)",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

btn1, btn2, btn3 = st.columns([1, 1, 2])
with btn1:
    process = st.button("✅ Process Files", type="primary")
with btn2:
    if st.button("🧹 Clear Uploads"):
        clear_upload_state()
        st.rerun()
with btn3:
    st.caption("Tip: Upload once. Other pages will reuse cached artifacts.")

# -----------------------------
# Processing
# -----------------------------
if process:
    if not uploaded_files:
        st.warning("Upload at least one Excel or CSV file.")
        st.stop()
    if not source_system.strip():
        st.warning("Enter Source System Name.")
        st.stop()

    st.session_state["source_system"] = source_system.strip()
    st.session_state["uploaded_files"] = uploaded_files

    profile_df = build_profile(uploaded_files, exclude_consolidated=exclude_consolidated)
    st.session_state["profile_df"] = profile_df

    st.success(f"Processed {len(uploaded_files)} file(s) for: {source_system.strip()}")

# -----------------------------
# Display
# -----------------------------
if "profile_df" in st.session_state:
    st.subheader("Profile Summary")
    st.dataframe(st.session_state["profile_df"], use_container_width=True)

    if st.button("➡️ Next: Field Inventory"):
        st.switch_page("pages/2_Field_Inventory.py")
else:
    st.info("Upload files and click **Process Files** to continue.")
