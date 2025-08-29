#!/usr/bin/env python3
"""
Test script to verify form loading functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_form_import():
    """Test that forms can be imported correctly"""
    form_types = ["Wedding", "Mitzvah", "Quinceanera", "Sweet_Sixteen", "Birthday_Party", "General_Party"]
    
    print("Testing form imports...")
    
    for form_type in form_types:
        try:
            # Import the form module
            module_name = f"pages.questionnaires.{form_type}_Form"
            module = __import__(module_name, fromlist=['render'])
            
            # Test that the render function exists
            if hasattr(module, 'render'):
                print(f"✅ {form_type}_Form.py - Import successful, render function found")
            else:
                print(f"❌ {form_type}_Form.py - Render function not found")
                
        except ImportError as e:
            print(f"❌ {form_type}_Form.py - Import failed: {e}")
        except Exception as e:
            print(f"❌ {form_type}_Form.py - Error: {e}")

def test_form_paths():
    """Test that form files exist"""
    form_types = ["Wedding", "Mitzvah", "Quinceanera", "Sweet_Sixteen", "Birthday_Party", "General_Party"]
    
    print("\nTesting form file paths...")
    
    for form_type in form_types:
        file_path = os.path.join("pages", "questionnaires", f"{form_type}_Form.py")
        if os.path.exists(file_path):
            print(f"✅ {file_path} - File exists")
        else:
            print(f"❌ {file_path} - File not found")

if __name__ == "__main__":
    print("=== Form Loading Test ===\n")
    test_form_paths()
    test_form_import()
    print("\n=== Test Complete ===")
