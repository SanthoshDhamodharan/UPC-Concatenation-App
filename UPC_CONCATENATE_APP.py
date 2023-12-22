#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import streamlit as st
import io
import base64
import tempfile

# Logo display section
st.title('Logos')

# List of logos with their URLs
logos = {
    'United Supermarkets': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/United_Supermarkets_Logo.png',
    'MarketStreet': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/MarketStreet_Logo.png',
    'Albertsons Market': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/Albertsons%20Market_Logo.png',
    'Amigos': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/Amigos_Logo.png',
}

# Display logos side by side
with st.container():
    for logo_name, logo_url in logos.items():
        st.image(logo_url, caption=logo_name, use_column_width=True)

# Streamlit app
st.title('UPC Concatenation App')

# File upload section
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

# User input for column names
offer_id_column = st.text_input("Enter the column name in which title is given in your dataset:")
barcode_column = st.text_input("Enter the column name in which UPC code is given in your dataset:")

# Placeholder for user-specified file name
file_name_placeholder = st.empty()
file_name = file_name_placeholder.text_input("Enter the desired file name (without extension):")

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




