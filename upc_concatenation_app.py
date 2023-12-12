import pandas as pd
import streamlit as st
print("Before import")
from openpyxl import load_workbook
print("After import")

try:
    from openpyxl import load_workbook
except Exception as e:
    print(f"Error during import: {e}")

# Function to clean and preprocess the data
def preprocess_data(df):
    df['offer_id2'] = df['offer_id2'].str.strip()
    df['_14_char_barcode'] = df['_14_char_barcode'].apply(lambda x: '{:.0f}'.format(x).zfill(14))
    new_df = df.groupby('offer_id2')['_14_char_barcode'].apply(lambda x: ','.join(x)).reset_index()
    return new_df

# Streamlit app
st.title('UPC Concatenation App')

# File upload section
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Load data from Excel
    df = pd.read_excel(uploaded_file)

    # Preprocess the data
    new_df = preprocess_data(df)

    # Display processed data
    st.dataframe(new_df)

    # Download button for the processed data
    st.download_button(
        label="Download Processed Data as Excel",
        data=new_df.to_excel,
        file_name="processed_data.xlsx",
        key="processed_data",
    )
