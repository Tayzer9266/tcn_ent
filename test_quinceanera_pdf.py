"""
Test script to generate the Quinceañera Questionnaire PDF
"""
from utils.pdf_generator import generate_quinceanera_questionnaire_pdf
from datetime import datetime

def main():
    """Generate and save the Quinceañera Questionnaire PDF"""
    print("Generating Quinceañera Questionnaire PDF...")
    
    try:
        # Generate the PDF
        pdf_bytes = generate_quinceanera_questionnaire_pdf()
        
        # Save to file
        filename = f"Quinceanera_Questionnaire_{datetime.now().strftime('%Y%m%d')}.pdf"
        with open(filename, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✓ PDF successfully generated: {filename}")
        print(f"✓ File size: {len(pdf_bytes)} bytes")
        print("\nThe PDF includes:")
        print("  • TCN Entertainment branding")
        print("  • Professional layout with sections")
        print("  • All questionnaire fields from the Streamlit form")
        print("  • Fillable fields with checkboxes and text areas")
        print("  • Page numbers and proper formatting")
        
    except Exception as e:
        print(f"✗ Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
