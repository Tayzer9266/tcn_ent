import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.pdf_generator import generate_dj_contract_pdf_response

# Sample booking data
sample_booking_data = {
    'dj_name': 'Tay Nguyen',
    'client_name': 'John Doe',
    'contract_date': '11/22/2025',
    'event_date': '11/21/2025',
    'start_time': '6:00 PM',
    'end_time': '10:00 PM',
    'service_hours': 4,
    'event_location': 'Eagle Historic Hillsboro, Texas',
    'total_fee': '668.00',
    'deposit': '60.00',
    'event_type': 'Wedding',
    'equipment_list': 'MC/DJ performance\nPremium PA Sound System\nWireless Microphones\nComplimentary Dance Lights'
}

# Generate PDF
pdf_bytes = generate_dj_contract_pdf_response(sample_booking_data)

# Save to file for inspection
with open('test_contract.pdf', 'wb') as f:
    f.write(pdf_bytes)

print("Test contract PDF generated successfully!")
print("Check 'test_contract.pdf' for the output.")
