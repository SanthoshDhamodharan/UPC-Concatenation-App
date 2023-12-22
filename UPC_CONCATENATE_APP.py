#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import streamlit as st
import io
import base64
import tempfile

# Workaround for wide layout
st.markdown("""
    <style>
        .reportview-container {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# List of logos with their URLs
logos = {
    'United Supermarkets': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/United_Supermarkets_Logo.png',
    'MarketStreet': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/MarketStreet_Logo.png',
    'Albertsons Market': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/Albertsons%20Market_Logo.png',
    'Amigos': 'https://raw.github.com/SanthoshDhamodharan/UPC-Concatenation-App/main/Amigos_Logo.png',
}

# Set the desired height for the logo
logo_heights = {
    'United Supermarkets': 160,
    'MarketStreet': 160,
    'Albertsons Market': 160,
    'Amigos': 160,
}

# Display logos side by side horizontally
logo_html = ""
for logo, url in logos.items():
    height = logo_heights.get(logo, 500)  # Default height is set to 200 if not specified
    logo_html += f'<img src="{url}" alt="{logo}" style="height: {height}px; margin-right: 10px;">'

# Render logos using HTML
st.markdown(logo_html, unsafe_allow_html=True)

# Streamlit app
st.title('UPC Concatenation App')

# User input for column names
offer_id_column = st.text_input("Enter the column name in which title is given in your dataset:")
barcode_column = st.text_input("Enter the column name in which UPC code is given in your dataset:")

# Placeholder for user-specified file name
file_name_placeholder = st.empty()
file_name = file_name_placeholder.text_input("Enter the desired file name (without extension):")

# Button to start processing
if st.button("Process Data"):
    # Your data processing logic here
    try:
        st.write("Data processing logic goes here.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
            


# In[ ]:




