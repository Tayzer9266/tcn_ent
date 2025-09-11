with open('pages/2_Request_Quote.py', 'r') as f:
    lines = f.readlines()
lines[0] = lines[0].lstrip()
with open('pages/2_Request_Quote.py', 'w') as f:
    f.writelines(lines)
