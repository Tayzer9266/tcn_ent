import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.pdf_generator import generate_dj_contract_pdf_response

# Sample booking data with missing fields
sample_booking_data = {
    'dj_name': '',  # Missing DJ name
    'client_name': '',  # Missing client name
    'contract_date': '',  # Missing date
    'event_date': '',  # Missing event date
    'start_time': '',  # Missing start time
    'end_time': '',  # Missing end time
    'event_location': '',  # Missing location
    'total_fee': '',  # Missing fee
    'deposit': '',  # Missing deposit
    'event_type': '',  # Missing event type
    'equipment_list': ''  # Missing equipment
}

try:
    # Generate PDF
    pdf_bytes = generate_dj_contract_pdf_response(sample_booking_data)

    # Save to file for inspection
    with open('test_contract_error.pdf', 'wb') as f:
        f.write(pdf_bytes)

    print("Test contract PDF with missing data generated successfully!")
    print("Check 'test_contract_error.pdf' for the output.")
except Exception as e:
    print(f"Error generating PDF: {e}")
