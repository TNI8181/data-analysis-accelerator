import streamlit as st
import pandas as pd

st.title("Field Inventory")

# -------------------------------
# Check Session State
# -------------------------------
if "uploaded_files" not in st.session_state:
    st.warning("No files found. Please go to Home and upload files first.")
    st.stop()

uploaded_files = st.session_state["uploaded_files"]
source_system = st.session_state.get("source_system", "Unknown")

st.success(f"Source System: {source_system}")
st.write(f"Files Loaded: {len(uploaded_files)}")

# -------------------------------
# Build Field-Level Inventory
# -------------------------------
field_rows = []

for f in uploaded_files:
    try:
        if f.name.lower().endswith(".csv"):
            df = pd.read_csv(f)
            report_label = f.name

            for col in df.columns:
                field_rows.append({
                    "report_name": report_label,
                    "column_original": str(col)
                })

        else:
            xls = pd.ExcelFile(f)
            for sheet in xls.sheet_names:
                df = xls.parse(sheet)
                report_label = f.name  # NO sheet name per your requirement

                for col in df.columns:
                    field_rows.append({
                        "report_name": report_label,
                        "column_original": str(col)
                    })

    except Exception as e:
        st.error(f"Could not process {f.name}: {e}")

field_df = pd.DataFrame(field_rows)

if field_df.empty:
    st.warning("No fields found.")
    st.stop()

st.subheader("Raw Field Inventory")
st.dataframe(field_df, use_container_width=True)

# -------------------------------
# Cross Tab (X / Blank)
# -------------------------------
st.subheader("Report vs Field Cross Tab")

cross_tab = pd.crosstab(
    field_df["column_original"],
    field_df["report_name"]
)

cross_tab = cross_tab.applymap(lambda v: "x" if v > 0 else "")

st.dataframe(cross_tab, use_container_width=True)
