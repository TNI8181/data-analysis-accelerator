import streamlit as st
import pandas as pd

st.title("📋 Field Inventory")

if "uploaded_files" not in st.session_state:
    st.warning("Upload files first.")
    st.stop()

field_rows = []

for f in st.session_state["uploaded_files"]:
    try:
        if f.name.lower().endswith(".csv"):
            df = pd.read_csv(f)
            for col in df.columns:
                field_rows.append({
                    "report_name": f.name,
                    "column_original": str(col)
                })
        else:
            xls = pd.ExcelFile(f)
            for sheet in xls.sheet_names:
                df = xls.parse(sheet)
                for col in df.columns:
                    field_rows.append({
                        "report_name": f.name,
                        "column_original": str(col)
                    })
    except Exception as e:
        st.error(f"Error processing {f.name}: {e}")

field_df = pd.DataFrame(field_rows)
st.session_state["field_df"] = field_df

st.dataframe(field_df, use_container_width=True)
