- [ ] Fix st.button to st.form_submit_button in the new_quote_form
- [ ] Fix DataFrame access bug by replacing bookings_df.empty with len(bookings) > 0
- [ ] Test the Streamlit app after fixes


Create a PDF Form to download contracts:

import streamlit as st
from fpdf import FPDF
# Streamlit form
st.title("Contract Generator")
with st.form("contract_form"):
    name = st.text_input("Client Name")
    service = st.text_input("Service Description")
    date = st.date_input("Contract Date")
    submitted = st.form_submit_button("Generate Contract")

if submitted:
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Service Contract", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Client: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Service: {service}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True)

    # Save PDF to file
    pdf.output("contract.pdf")

    # Offer download
    with open("contract.pdf", "rb") as f:
        st.download_button("Download Contract", f, file_name="contract.pdf")

