#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import streamlit as st
import io
import base64
import tempfile

# Set wider layout
st.set_page_config(layout="wide")

# Workaround for wide layout
st.markdown("""
    <style>
        .reportview-container {
            display: flex;
            flex-direction: column; /* Align content in a vertical column */
            align-items: center; /* Center content horizontally */
            width: 100%;
        }
        .logo-container {
            display: flex;
            justify-content: space-between; /* Space between logos */
            align-items: center; /* Center logos vertically */
            margin: 10px 0; /* Add margin on the top */
        }
        .logo-container img {
            max-height: 100px; /* Set the maximum height of the logo */
            width: auto; /* Allow the width to adjust accordingly */
            margin: 0 10px; /* Adjust margin on both sides */
        }
        .top-left-logo {
            order: 1; /* Order the logo to be the first in the container (top-left corner) */
        }
        .top-right-logo {
            order: 2; /* Order the logo to be the second in the container (top-right corner) */
        }
    </style>
""", unsafe_allow_html=True)

# Title for Our Clients
st.title('Our Clients')

# List of logos with their URLs
logos = {
    'United Supermarkets': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/United_Supermarkets_Logo.png',
    'MarketStreet': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/MarketStreet_Logo.png',
    'Albertsons Market': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/Albertsons_Market_Logo.png',
    'Amigos': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/Amigos_Logo.png',
}

# Display logos side by side horizontally
logo_html = '<div class="logo-container">'
for logo, url in logos.items():
    logo_html += '<img src="{}" alt="{}">'.format(url, logo)
logo_html += '</div>'

# Render logos using HTML
st.markdown(logo_html, unsafe_allow_html=True)

# The rest of your code...

# File upload section with hidden default uploader
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"], key="fileuploader", accept_multiple_files=False)

# User input for column names
offer_id_column = st.text_input("Enter the column name in which title is given in your dataset:")
barcode_column = st.text_input("Enter the column name in which UPC code is given in your dataset:")

# Placeholder for user-specified file name
file_name_placeholder = st.empty()
file_name = file_name_placeholder.text_input("Enter the desired file name (without extension):", key="file_name_input")

# Button to start processing
if st.button("Click to Process Data"):
    if uploaded_file is not None and offer_id_column and barcode_column and file_name:
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
                temp_file_path = os.path.join(temp_dir, "{}.xlsx".format(file_name.strip()))
                with open(temp_file_path, "wb") as f:
                    f.write(excel_data.getvalue())

                # Provide a message to the user
                st.write("File '{}.xlsx' has been created.".format(file_name.strip()))

                # Provide a download link
                st.markdown(get_binary_file_downloader_html(temp_file_path, "{}.xlsx".format(file_name.strip())), unsafe_allow_html=True)
        except Exception as e:
            st.error("An error occurred: {}".format(str(e)))
    else:
        st.warning("Please provide valid input for all fields.")
            


# In[ ]:




