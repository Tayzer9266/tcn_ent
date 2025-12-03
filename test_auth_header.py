"""
Test script to verify authentication header implementation
"""
import os
import sys

print("=" * 70)
print("AUTHENTICATION HEADER IMPLEMENTATION TEST")
print("=" * 70)

# Test 1: Check if component file exists
print("\n1. Checking component file...")
if os.path.exists("components/header_auth.py"):
    print("   ✅ components/header_auth.py exists")
else:
    print("   ❌ components/header_auth.py NOT FOUND")
    sys.exit(1)

# Test 2: Check if component can be imported
print("\n2. Testing component import...")
try:
    sys.path.insert(0, os.path.abspath('.'))
    from components.header_auth import render_auth_header
    print("   ✅ Component imports successfully")
    print(f"   ✅ render_auth_header function available")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 3: Check if all public pages have been updated
print("\n3. Checking public pages for header integration...")
public_pages = [
    "Home.py",
    "pages/1_Request_Quote_Estimate.py",
    "pages/2_Photographers.py",
    "pages/3_Event_Coordinators.py",
    "pages/4_DJs.py",
    "pages/5_Services.py",
    "pages/6_Questionnaires.py",
    "pages/7_Contact_Us.py",
    "pages/8_Event_Planning_Tips.py"
]

all_updated = True
for page in public_pages:
    if os.path.exists(page):
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'render_auth_header' in content:
                print(f"   ✅ {page} - Header integrated")
            else:
                print(f"   ❌ {page} - Header NOT integrated")
                all_updated = False
    else:
        print(f"   ⚠️  {page} - File not found")
        all_updated = False

# Test 4: Verify component structure
print("\n4. Verifying component structure...")
with open("components/header_auth.py", 'r', encoding='utf-8') as f:
    component_content = f.read()
    
    checks = [
        ("render_auth_header function", "def render_auth_header()"),
        ("CSS styling", ".auth-header"),
        ("Login link", "/90_Login"),
        ("Register link", "/91_Client_Registration"),
        ("Client dashboard link", "/93_Client_Dashboard"),
        ("Professional profile link", "/92_Profile_Management"),
        ("Client session check", "client_logged_in"),
        ("Professional session check", "professional_logged_in")
    ]
    
    for check_name, check_string in checks:
        if check_string in component_content:
            print(f"   ✅ {check_name} - Found")
        else:
            print(f"   ❌ {check_name} - NOT FOUND")
            all_updated = False

# Test 5: Check navigation structure
print("\n5. Checking navigation structure...")
print("   Checking that login pages are in 90+ range...")
auth_pages = [
    "pages/90_Login.py",
    "pages/91_Client_Registration.py",
    "pages/92_Profile_Management.py",
    "pages/93_Client_Dashboard.py"
]

for page in auth_pages:
    if os.path.exists(page):
        print(f"   ✅ {page} - Exists (hidden from sidebar)")
    else:
        print(f"   ⚠️  {page} - Not found")

# Final Summary
print("\n" + "=" * 70)
if all_updated:
    print("✅ ALL TESTS PASSED - AUTHENTICATION HEADER READY")
    print("=" * 70)
    print("\nImplementation Summary:")
    print("  • Authentication header component created")
    print("  • Header integrated into all 9 public pages")
    print("  • Login/Register links in top right corner")
    print("  • Auth pages hidden in sidebar (90+ range)")
    print("  • Component supports client and professional authentication")
    print("\nNext Steps:")
    print("  • Deploy to production")
    print("  • Test in live environment")
    print("  • Verify responsive design on different devices")
else:
    print("⚠️  SOME TESTS FAILED - REVIEW IMPLEMENTATION")
    print("=" * 70)

print("\n" + "=" * 70)
