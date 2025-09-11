from utils.pdf_generator import PDFGenerator

# Test PDF generation with None comments
generator = PDFGenerator()
form_data_none = {
    'first_name': 'Test',
    'last_name': 'User',
    'event_date': '2023-10-01',
    'start_time': '18:00',
    'event_location': 'Test Venue',
    'comments': None  # Test None
}

form_data_empty = {
    'first_name': 'Test',
    'last_name': 'User',
    'event_date': '2023-10-01',
    'start_time': '18:00',
    'event_location': 'Test Venue',
    'comments': ''  # Test empty
}

try:
    pdf_bytes = generator.generate_quote_form_pdf(form_data_none)
    print("PDF generated successfully with None comments")
except Exception as e:
    print(f"Error with None comments: {e}")

try:
    pdf_bytes = generator.generate_quote_form_pdf(form_data_empty)
    print("PDF generated successfully with empty comments")
except Exception as e:
    print(f"Error with empty comments: {e}")
