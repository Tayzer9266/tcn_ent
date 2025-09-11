# Test the equipment_list processing for different formats

# Test comma-separated with brackets and apostrophes
equipment_list1 = '[MC/DJ performance, Premium PA Sound System, Wireless Microphones, Complimentary Dance Lights, Fog Machine]'
if not isinstance(equipment_list1, str):
    equipment_list1 = str(equipment_list1)
equipment_list1 = equipment_list1.strip('[]{}')
if ',' in equipment_list1:
    items = [item.strip().strip('"').replace("'", "") for item in equipment_list1.split(',')]
    equipment_list1 = '\n'.join([f"{i+1}. {item}" for i, item in enumerate(items)])
else:
    equipment_list1 = '1. ' + equipment_list1.strip().replace("'", "")

print("Processed comma-separated with brackets:")
print(repr(equipment_list1))
print("\nFormatted:")
print(equipment_list1)

print("\n" + "="*50 + "\n")

# Test PostgreSQL array format with apostrophes
equipment_list2 = '{MC/DJ performance,Premium PA Sound System,Wireless Microphones,Complimentary Dance Lights,Fog Machine}'
if not isinstance(equipment_list2, str):
    equipment_list2 = str(equipment_list2)
equipment_list2 = equipment_list2.strip('[]{}')
if ',' in equipment_list2:
    items = [item.strip().strip('"').replace("'", "") for item in equipment_list2.split(',')]
    equipment_list2 = '\n'.join([f"{i+1}. {item}" for i, item in enumerate(items)])
else:
    equipment_list2 = '1. ' + equipment_list2.strip().replace("'", "")

print("Processed PostgreSQL array:")
print(repr(equipment_list2))
print("\nFormatted:")
print(equipment_list2)

print("\n" + "="*50 + "\n")

# Test with apostrophes in items
equipment_list3 = '[MC/DJ performance, Premium PA Sound System, Wireless Microphones, Complimentary Dance Lights, Fog Machine]'
if not isinstance(equipment_list3, str):
    equipment_list3 = str(equipment_list3)
equipment_list3 = equipment_list3.strip('[]{}')
if ',' in equipment_list3:
    items = [item.strip().strip('"').replace("'", "") for item in equipment_list3.split(',')]
    equipment_list3 = '\n'.join([f"{i+1}. {item}" for i, item in enumerate(items)])
else:
    equipment_list3 = '1. ' + equipment_list3.strip().replace("'", "")

print("Processed with apostrophes removed:")
print(repr(equipment_list3))
print("\nFormatted:")
print(equipment_list3)
