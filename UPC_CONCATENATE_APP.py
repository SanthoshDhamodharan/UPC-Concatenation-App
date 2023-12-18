#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import streamlit as st
import io
import base64
import tempfile

# Function to clean and preprocess the data
def preprocess_data(df, offer_id_column, barcode_column):
    df[offer_id_column] = df[offer_id_column].str.strip()
    df[barcode_column] = df[barcode_column].apply(lambda x: '{:.0f}'.format(x).zfill(14))
    df_unique = df.drop_duplicates(subset=[offer_id_column, barcode_column])
    new_df = df_unique.groupby(offer_id_column)[barcode_column].apply(lambda x: ','.join(x)).reset_index()
    return new_df

# Function to create a download link for a file
def get_binary_file_downloader_html(file_path, file_label):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_label}">Click here to download {file_label}</a>'

# Streamlit app
st.title('UPC Concatenation App')

# File upload section
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

# User input for column names
offer_id_column = st.text_input("Enter the column name for 'offer_id2':", "offer_id2")
barcode_column = st.text_input("Enter the column name for '_14_char_barcode':", "_14_char_barcode")

# Placeholder for user-specified file name
file_name_placeholder = st.empty()
file_name = file_name_placeholder.text_input("Enter the desired file name (without extension):", "processed_data")

# Button to start processing
if st.button("Process Data"):
    if uploaded_file is not None:
        try:
            # Load data from Excel
            df = pd.read_excel(uploaded_file)

            # Preprocess the data
            new_df = preprocess_data(df, offer_id_column, barcode_column)

            # Display processed data
            st.dataframe(new_df)

            # Create an in-memory Excel file
            excel_data = io.BytesIO()
            new_df.to_excel(excel_data, index=False, engine='openpyxl')

            # Save the Excel file to a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, f"{file_name.strip()}.xlsx")
                with open(temp_file_path, "wb") as f:
                    f.write(excel_data.getvalue())

                # Provide a message to the user
                st.write(f"File '{file_name.strip()}.xlsx' has been created.")

                # Provide a download link
                st.markdown(get_binary_file_downloader_html(temp_file_path, f"{file_name.strip()}.xlsx"), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            


# In[ ]:




