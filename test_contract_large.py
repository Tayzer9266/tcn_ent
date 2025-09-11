import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.pdf_generator import generate_dj_contract_pdf_response

# Sample booking data with large text
sample_booking_data = {
    'dj_name': 'Tay Nguyen',
    'client_name': 'John Doe',
    'contract_date': '11/22/2025',
    'event_date': '11/21/2025',
    'start_time': '6:00 PM',
    'end_time': '10:00 PM',
    'event_location': 'Eagle Historic Hillsboro, Texas',
    'total_fee': '668.00',
    'deposit': '60.00',
    'event_type': 'Wedding',
