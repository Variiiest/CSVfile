import streamlit as st
import json
import csv
import pandas as pd
from io import StringIO

# Streamlit app title
st.title('Log Analyzer - JSON to CSV Converter')

# Upload JSON file
uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

if uploaded_file is not None:
    # Read the JSON file
    data = json.load(uploaded_file)

    # Define the headers for the CSV
    headers = [
        "Name", "Selling Price", "MRP", "Image 1", "Image 2", "Image 3", 
        "Image 4", "Image 5", "Product Type", "Size", "Colour", "Description", "Visibility"
    ]
    
    # Create a list to store rows of data
    rows = []

    # Iterate through each product in the JSON data
    for product in data['products']:
        # Extract required fields
        name = product.get('title', '')
        description = product.get('body_html', '').replace('\u003cbr\u003e', '').strip()
        product_type = product.get('product_type', '')
        visibility = "Visible" if product.get('published_at') else "Not Visible"

        # Get the images (up to 5)
        images = [img.get('src', '') for img in product.get('images', [])]
        image_1 = images[0] if len(images) > 0 else ''
        image_2 = images[1] if len(images) > 1 else ''
        image_3 = images[2] if len(images) > 2 else ''
        image_4 = images[3] if len(images) > 3 else ''
        image_5 = images[4] if len(images) > 4 else ''

        # Get price details from the first variant as "Selling Price"
        variants = product.get('variants', [])
        selling_price = variants[0].get('price', '') if variants else ''
        mrp = variants[0].get('compare_at_price', selling_price) if variants else ''

        # Extract size information (concatenate all available sizes)
        sizes = ', '.join([variant.get('title', '') for variant in variants])

        # Extract the main color from tags (assumption based on tag patterns like 'c.blue')
        color_tag = next((tag for tag in product.get('tags', []) if tag.startswith('c.')), '')
        color = color_tag.replace('c.', '').capitalize() if color_tag else 'Not specified'

        # Append row data
        rows.append([
            name, selling_price, mrp, image_1, image_2, image_3, image_4, 
            image_5, product_type, sizes, color, description, visibility
        ])

    # Create a DataFrame for the extracted data
    df = pd.DataFrame(rows, columns=headers)
    
    # Show the data in the app
    st.dataframe(df)

    # Convert DataFrame to CSV
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    # Provide a download link for the CSV file
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="products.csv",
        mime="text/csv"
    )
