from utils.pdf_generator import PDFGenerator

# Test data with PostgreSQL array format
booking_data = {
    'dj_name': 'Tay Nguyen',
    'client_name': 'Test Client',
    'contract_date': '10/01/2023',
    'event_date': '10/15/2023',
    'start_time': '6:00 PM',
    'end_time': '10:00 PM',
    'event_location': 'Test Venue',
    'total_fee': '500.00',
    'deposit': '60.00',
    'event_type': 'Birthday Party',
    'equipment_list': '{MC/DJ performance,Premium PA Sound System,Wireless Microphones,Complimentary Dance Lights,Fog Machine}'
}

generator = PDFGenerator()
contract_bytes = generator.generate_dj_contract_pdf(booking_data)
contract_text = contract_bytes.decode('latin1')

print("Full contract text:")
print(repr(contract_text))

# Extract the equipment section from the contract text
lines = contract_text.split('\n')
print("\nLines:")
for i, line in enumerate(lines):
    print(f"{i}: {repr(line)}")

equipment_section = []
in_equipment = False
for line in lines:
    if 'Shall bring the following equipment and personnel:' in line:
        in_equipment = True
        continue
    if in_equipment and line.strip():
        if line.startswith('V.') or line.startswith('VI.'):
            break
        equipment_section.append(line.strip())

print("\nEquipment section in contract:")
for item in equipment_section:
    print(f"- {item}")
