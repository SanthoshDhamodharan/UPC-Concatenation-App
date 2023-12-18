#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import streamlit as st
import io

# Function to clean and preprocess the data
def preprocess_data(df):
    df['offer_id2'] = df['offer_id2'].str.strip()
    df['_14_char_barcode'] = df['_14_char_barcode'].apply(lambda x: '{:.0f}'.format(x).zfill(14))
    df_unique = df.drop_duplicates(subset=['offer_id2', '_14_char_barcode'])
    new_df = df_unique.groupby('offer_id2')['_14_char_barcode'].apply(lambda x: ','.join(x)).reset_index()
    return new_df

# Streamlit app
st.title('UPC Concatenation App')

# File upload section
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

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
            new_df = preprocess_data(df)

            # Display processed data
            st.dataframe(new_df)

            # Create an in-memory Excel file
            excel_data = io.BytesIO()
            new_df.to_excel(excel_data, index=False, engine='openpyxl')

            # Save the Excel file to the user's local "Downloads" folder with user-specified or auto-generated file name
            final_file_name = f"{file_name.strip()}.xlsx"
            user_downloads_path = os.path.expanduser("~")
            file_path = os.path.join(user_downloads_path, "Downloads", final_file_name)
            
            with open(file_path, "wb") as f:
                f.write(excel_data.getvalue())

            # Provide a message to the user
            st.write(f"File '{final_file_name}' has been downloaded to your local 'Downloads' folder.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


# In[ ]:




