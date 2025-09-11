# Test the equipment_list processing
equipment_list = 'MC/DJ performance, Premium PA Sound System, Wireless Microphones, Complimentary Dance Lights, Fog Machine'

if ',' in equipment_list:
    equipment_list = '\n'.join([item.strip() for item in equipment_list.split(',')])

print("Processed equipment_list:")
print(repr(equipment_list))
print("\nFormatted:")
print(equipment_list)
