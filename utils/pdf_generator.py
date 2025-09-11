import io
from fpdf import FPDF
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
    def generate_wedding_pdf(self, form_data):
        """Generate a PDF from wedding form data"""
        self.pdf.add_page()
        
        # Header
        self.pdf.set_font("Helvetica", 'B', 16)
        self.pdf.cell(0, 10, "Wedding Questionnaire Responses", 0, 1, 'C')
        self.pdf.ln(5)
        
        # Event Information
        self._add_section_header("Basic Event Information")
        self._add_field("Event Date", form_data.get('event_date', 'Not provided'))
        self._add_field("Host Name", form_data.get('host_name', 'Not provided'))
        self._add_field("Host Phone", form_data.get('host_phone', 'Not provided'))
        self._add_field("Host Email", form_data.get('host_email', 'Not provided'))
        self._add_field("Start Time", form_data.get('start_time', 'Not provided'))
        self._add_field("End Time", form_data.get('end_time', 'Not provided'))
        self._add_field("Number of Guests", form_data.get('num_guests', 'Not provided'))
        
        # Venue Information
        self._add_section_header("Venue Information")
        self._add_field("Venue Name", form_data.get('venue_name', 'Not provided'))
        self._add_field("Venue Address", form_data.get('venue_address', 'Not provided'))
        self._add_field("Venue Phone", form_data.get('venue_phone', 'Not provided'))
        
        # Couple Information
        self._add_section_header("Couple Information")
        self._add_field("Bride's Name", form_data.get('bride_name', 'Not provided'))
        self._add_field("Groom's Name", form_data.get('groom_name', 'Not provided'))
        
        # Ceremony Details
        self._add_section_header("Ceremony Details")
        self._add_field("Ceremony Venue", form_data.get('ceremony_venue', 'Not provided'))
        self._add_field("Ceremony Address", form_data.get('ceremony_address', 'Not provided'))
        self._add_field("Ceremony Phone", form_data.get('ceremony_phone', 'Not provided'))
        self._add_field("Ceremony Music", form_data.get('has_ceremony', 'Not provided'))
        self._add_field("Ceremony Time", form_data.get('ceremony_time', 'Not provided'))
        
        # Equipment & Services
        self._add_section_header("Equipment & Services")
        self._add_field("Up-Lighting", form_data.get('uplighting', 'Not provided'))
        if form_data.get('uplighting') == 'Yes':
            self._add_field("Up-Lighting Count", form_data.get('uplighting_count', 'Not specified'))
            self._add_field("Up-Lighting Color", form_data.get('uplighting_color', 'Not specified'))
        self._add_field("Projection Screen", form_data.get('projection', 'Not provided'))
        self._add_field("Photo Booth", form_data.get('photobooth', 'Not provided'))
        if form_data.get('photobooth') == 'Yes':
            self._add_field("Photo Booth Template", form_data.get('photobooth_template', 'Not specified'))
            self._add_field("Number of Images", form_data.get('photobooth_images', 'Not specified'))
            self._add_field("Props", form_data.get('photobooth_props', 'Not specified'))
            self._add_field("Backdrop Color", form_data.get('photobooth_backdrop', 'Not specified'))
        
        # Music Programming
        self._add_section_header("Music Programming")
        self._add_field("Cocktail Music", ', '.join(form_data.get('cocktail_music', [])) or 'Not specified')
        self._add_field("Dinner Music", ', '.join(form_data.get('dinner_music', [])) or 'Not specified')
        self._add_field("Dinner Time", form_data.get('dinner_time', 'Not provided'))
        self._add_field("Dinner Style", form_data.get('dinner_style', 'Not provided'))
        
        # General Music Preferences
        self._add_section_header("General Music Preferences")
        self._add_field("Music Genres", ', '.join(form_data.get('music_genres', [])) or 'Not specified')
        self._add_field("Custom Playlist", form_data.get('custom_playlist', 'Not provided'))
        self._add_field("Must-Play Songs", form_data.get('must_play', 'Not provided'))
        self._add_field("Do Not Play Songs", form_data.get('do_not_play', 'Not provided'))
        self._add_field("Guest Requests", form_data.get('guest_requests', 'Not provided'))
        self._add_field("Fade Songs", form_data.get('fade_songs', 'Not provided'))
        
        # Special Wedding Moments
        self._add_section_header("Special Wedding Moments")
        self._add_field("First Dance Song", form_data.get('first_dance', 'Not provided'))
        self._add_field("First Dance Time", form_data.get('first_dance_time', 'Not provided'))
        self._add_field("Father-Bride Dance Song", form_data.get('father_dance', 'Not provided'))
        self._add_field("Father's Name", form_data.get('father_name', 'Not provided'))
        self._add_field("Father-Bride Dance Time", form_data.get('father_dance_time', 'Not provided'))
        self._add_field("Bridal Party Dance Song", form_data.get('bridal_dance', 'Not provided'))
        self._add_field("Mother-Groom Dance Song", form_data.get('mother_dance', 'Not provided'))
        self._add_field("Mother's Name", form_data.get('mother_name', 'Not provided'))
        self._add_field("Mother-Groom Dance Time", form_data.get('mother_dance_time', 'Not provided'))
        self._add_field("Anniversary Dance", form_data.get('anniversary_dance', 'Not provided'))
        self._add_field("Cake Cutting Song", form_data.get('cake_song', 'Not provided'))
        self._add_field("Cake Cutting Time", form_data.get('cake_time', 'Not provided'))
        
        # Wedding Ceremonies
        self._add_section_header("Wedding Ceremonies")
        self._add_field("Garter Removal Song", form_data.get('garter_removal', 'Not provided'))
        self._add_field("Garter Removal Time", form_data.get('garter_removal_time', 'Not provided'))
        self._add_field("Garter Toss Song", form_data.get('garter_toss', 'Not provided'))
        self._add_field("Garter Toss Time", form_data.get('garter_toss_time', 'Not provided'))
        self._add_field("Bouquet Toss Song", form_data.get('bouquet_toss', 'Not provided'))
        self._add_field("Bouquet Toss Time", form_data.get('bouquet_toss_time', 'Not provided'))
        
        # Event Coordination
        self._add_section_header("Event Coordination")
        self._add_field("Banquet Manager", form_data.get('banquet_manager', 'Not provided'))
        self._add_field("Photographer", form_data.get('photographer', 'Not provided'))
        self._add_field("Videographer", form_data.get('videographer', 'Not provided'))
        self._add_field("Other Vendors", form_data.get('other_vendors', 'Not provided'))
        
        # Announcements
        self._add_section_header("Announcements")
        self._add_field("Announce Song Requests", form_data.get('announce_requests', 'Not provided'))
        self._add_field("Announce Photo Booth", form_data.get('announce_photobooth', 'Not provided'))
        self._add_field("Announce Guest Book", form_data.get('announce_guestbook', 'Not provided'))
        self._add_field("Snack Time", form_data.get('snack_time', 'Not provided'))
        self._add_field("Last Call Time", form_data.get('last_call', 'Not provided'))
        self._add_field("Photo Booth Warning", form_data.get('photobooth_warning', 'Not provided'))
        
        # Final Notes
        self._add_section_header("Final Notes")
        self._add_field("Last Song", form_data.get('last_song', 'Not provided'))
        self._add_field("Private Dance Song", form_data.get('private_dance', 'Not provided'))
        self._add_field("Memory Book", form_data.get('memory_book', 'Not provided'))
        self._add_field("Additional Notes", form_data.get('additional_notes', 'Not provided'))
        
        # Footer
        self.pdf.ln(10)
        self.pdf.set_font("Helvetica", 'I', 8)
        self.pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')

        # Use UTF-8 encoding instead of latin1
        return self.pdf.output(dest='S').encode('latin1')
    
    def _add_section_header(self, title):
        """Add a section header to the PDF"""
        self.pdf.ln(10)
        self.pdf.set_font("Helvetica", 'B', 12)
        self.pdf.set_fill_color(240, 240, 240)
        self.pdf.cell(0, 8, title, 0, 1, 'L', 1)
        self.pdf.ln(2)
    
    def generate_quote_form_pdf(self, form_data):
        """Generate a PDF from quote form data"""
        self.pdf.add_page()

        # Header
        self.pdf.set_font("Helvetica", 'B', 16)
        self.pdf.cell(0, 10, "Quote Form", 0, 1, 'C')
        self.pdf.ln(5)

        # Contact Information
        self._add_section_header("Contact Information")
        self._add_field("Service Type", form_data.get('service_types', 'Not provided'))
        self._add_field("First Name", form_data.get('first_name', 'Not provided'))
        self._add_field("Last Name", form_data.get('last_name', 'Not provided'))
        self._add_field("Phone", form_data.get('phone_number', 'Not provided'))
        self._add_field("Email", form_data.get('email', 'Not provided'))

        # Event Details
        self._add_section_header("Event Details")
        self._add_field("Event Date", form_data.get('event_date', 'Not provided'))
        self._add_field("Service Hours", form_data.get('service_hours', 'Not provided'))
        self._add_field("Event Type", form_data.get('event_type', 'Not provided'))
        self._add_field("Venue Name", form_data.get('venue_name', 'Not provided'))
        self._add_field("Venue Address", form_data.get('event_location', 'Not provided'))
        self._add_field("Venue Phone", form_data.get('venue_phone', 'Not provided'))

        # Services
        self._add_section_header("Services")
        self._add_field("Microphone", 'Yes' if form_data.get('microphone') else 'No')
        self._add_field("Dancing Lights", 'Yes' if form_data.get('dancing_lights') else 'No')
        self._add_field("Disco Ball", 'Yes' if form_data.get('disco_ball') else 'No')
        self._add_field("Uplighting", 'Yes' if form_data.get('uplighting') else 'No')
        self._add_field("Uplight Count", form_data.get('uplight_ct', 'Not provided'))
        self._add_field("Fog Machine", 'Yes' if form_data.get('fog_machine') else 'No')
        self._add_field("Low Fog Machine", 'Yes' if form_data.get('low_fog_machine') else 'No')
        self._add_field("Monogram", 'Yes' if form_data.get('monogram') else 'No')
        self._add_field("Cold Sparks", 'Yes' if form_data.get('cold_sparks') else 'No')
        self._add_field("Photo Booth", 'Yes' if form_data.get('photo_booth') else 'No')
        self._add_field("Photo Booth Prints", form_data.get('photo_booth_prints', 'Not provided'))
        self._add_field("Backdrop Type", form_data.get('back_drop_type', 'Not provided'))
        self._add_field("Backdrop Props", 'Yes' if form_data.get('backdrop_props') else 'No')

        # Comments
        self._add_section_header("Comments")
        self.pdf.set_font("Helvetica", '', 12)
        self.pdf.multi_cell(0, 10, form_data.get('comments', 'No comments'))

        return self.pdf.output(dest='S').encode('latin1')

    def generate_dj_contract_pdf(self, booking_data):
        """Generate a DJ Contract PDF from booking data"""
        self.pdf.add_page()

        # Header
        self.pdf.set_font("Helvetica", 'B', 14)
        self.pdf.cell(0, 12, "TCN Entertainment", 0, 1, 'C')
        self.pdf.set_font("Helvetica", 'B', 18)
        self.pdf.cell(0, 12, "DJ CONTRACT", 0, 1, 'C')
        self.pdf.ln(5)

        # Template based on DJ Contract.docx
        self.pdf.set_font("Helvetica", 'I', 8)
        template = """
 

I. PARTIES
This DJ Contract ("Contract" hereinafter) is signed by {dj_name} ("DJ" hereinafter) and {client_name} ("Client" hereinafter) on {contract_date} wherein both parties agreed on the following terms.

II. EVENT DESCRIPTION
This Contract sets out the event details and terms and conditions where DJ {dj_name} will perform.
Will be providing the musical entertainment including any tools need for the sound system to function properly for
Event on {event_date}. Below is the detailed event information:

Performer(s): {dj_name}
Event Title: {event_type}
Date: {contract_date}
Start Time: {start_time}
End Time: {end_time}
Location: {event_location}

III. PAYMENT
The total fee which will be paid to DJ under this contract is ${total_fee}. A non-refundable deposit of ${deposit} is required. The balance due is paid by credit card or check at the date of the event unless other arrangements have been agreed upon by {dj_name} to perform from {start_time} until {end_time} on the date of the event. In case there is a need to extend performance, the Client shall pay $50.00 per hour for the extension. Entrance fee, parking and electrical fees will be paid by the Client.

IV. EQUIPMENT
{dj_name} Shall bring the following equipment and personnel:
{equipment_list}

V. TERMINATION OF THE CONTRACT
If the contract is terminated by the Client before the event day, the deposit paid will not be refunded. In case the Contract is terminated on the day of the event, DJ will be entitled to the full contract price and the balance due will be paid on the same day. In both cases, Client shall notify the termination to the DJ in writing.
If the DJ will not be able to perform in an emergency (i.e. accident, health problems, force majeure etc.), the DJ must find a DJ to perform on his behalf and ensure that he fulfills the obligation arising from this contract. If the DJ cannot provide any replacements, DJ shall refund all fees previously paid by the Client, including the deposit.

VI. ENTIRE AGREEMENT
This Contract with any attachments constitutes the complete understanding of the parties to this Contract, regarding the subject matter contained in this Contract, and supersedes all other agreements or arrangements, either oral or in writing.

VII. AMENDMENTS
Any modification or variation of this Contract shall be in writing with the mutual consent of the parties.
Both parties agree to the terms and conditions stated above as demonstrated by their signatures as follows:



{dj_name}
Date: {contract_date}

{client_name}
Date: {contract_date}
"""

        # Replace placeholders
        contract_text = template.format(
            dj_name=booking_data.get('dj_name', 'Tay Nguyen'),
            client_name=booking_data.get('client_name', 'Client Name'),
            contract_date=booking_data.get('contract_date', datetime.now().strftime('%m/%d/%Y')),
            event_date=booking_data.get('event_date', 'Event Date'),
            start_time=booking_data.get('start_time', 'Start Time'),
            end_time=booking_data.get('end_time', 'End Time'),
            event_location=booking_data.get('event_location', 'Event Location'),
            total_fee=booking_data.get('total_fee', '0.00'),
            deposit=booking_data.get('deposit', '60.00'),
            event_type=booking_data.get('event_type', 'Event Type'),
            equipment_list=booking_data.get('equipment_list', 'MC/DJ performance\nPremium PA Sound System\nWireless Microphones\nComplimentary Dance Lights')
        )

        # Set font and add text
        self.pdf.set_font("Helvetica", '', 10)
        self.pdf.multi_cell(0, 8, contract_text)

        # Footer
        self.pdf.ln(10)
        self.pdf.set_font("Helvetica", 'I', 8)
        self.pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')

        return self.pdf.output(dest='S').encode('latin1')

    def _add_field(self, label, value):
        """Add a field to the PDF"""
        self.pdf.set_font("Helvetica", 'B', 10)
        self.pdf.cell(60, 6, f"{label}:", 0, 0)
        self.pdf.set_font("Helvetica", '', 10)

        # Handle long text by splitting into multiple lines
        if value and len(str(value)) > 50:
            self.pdf.multi_cell(0, 6, str(value))
        else:
            self.pdf.cell(0, 6, str(value) if value else "Not provided", 0, 1)
        self.pdf.ln(1)

def generate_wedding_pdf_response(form_data):
    """Generate a PDF from wedding form data"""
    generator = PDFGenerator()
    return generator.generate_wedding_pdf(form_data)

class QuotePDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def _add_section_header(self, title):
        """Add a section header to the PDF"""
        self.pdf.ln(10)
        self.pdf.set_font("Helvetica", 'B', 12)
        self.pdf.set_fill_color(240, 240, 240)
        self.pdf.cell(0, 8, title, 0, 1, 'L', 1)
        self.pdf.ln(2)

    def _add_field(self, label, value):
        """Add a field to the PDF"""
        self.pdf.set_font("Helvetica", 'B', 10)
        self.pdf.cell(60, 6, f"{label}:", 0, 0)
        self.pdf.set_font("Helvetica", '', 10)

        # Handle long text by splitting into multiple lines
        if value and len(str(value)) > 50:
            self.pdf.multi_cell(0, 6, str(value))
        else:
            self.pdf.cell(0, 6, str(value) if value else "Not provided", 0, 1)
        self.pdf.ln(1)

    def generate_quote_pdf(self, quote_data, itemized_df, booking_id, customer_name, event_date, event_type):
        """Generate a PDF from quote data"""
        self.pdf.add_page()
        
        # Header
        self.pdf.set_font("Helvetica", 'B', 16)
        self.pdf.cell(0, 10, "Event Quote Estimate", 0, 1, 'C')
        self.pdf.ln(5)
        
        # Quote Information
        self._add_section_header("Quote Information")
        self._add_field("Booking ID", booking_id)
        self._add_field("Customer Name", customer_name)
        self._add_field("Event Date", event_date.strftime('%Y-%m-%d') if event_date else 'Not provided')
        self._add_field("Event Type", event_type)
        
        # Summary Totals
        self._add_section_header("Price Summary")
        self._add_field("Total Market Cost", f"${quote_data.get('total_market', 0):,.2f}")
        self._add_field("Your Quote Total", f"${quote_data.get('total_quote', 0):,.2f}")
        self._add_field("Total Savings", f"${quote_data.get('total_savings', 0):,.2f}")
        
        # Itemized Products & Services
        self._add_section_header("Itemized Products & Services")
        
        # Add table headers
        self.pdf.set_font("Helvetica", 'B', 10)
        self.pdf.cell(80, 8, "Product/Service", 1, 0, 'L')
        self.pdf.cell(20, 8, "Units", 1, 0, 'C')
        self.pdf.cell(30, 8, "Market Price", 1, 0, 'R')
        self.pdf.cell(30, 8, "Your Price", 1, 0, 'R')
        self.pdf.cell(30, 8, "Savings", 1, 1, 'R')
        
        # Add table rows
        self.pdf.set_font("Helvetica", '', 10)
        for _, row in itemized_df.iterrows():
            self.pdf.cell(80, 8, str(row.get('items', '')), 1, 0, 'L')
            self.pdf.cell(20, 8, str(row.get('units', '')), 1, 0, 'C')
            self.pdf.cell(30, 8, f"${float(row.get('market_price', 0)):,.2f}", 1, 0, 'R')
            self.pdf.cell(30, 8, f"${float(row.get('total', 0)):,.2f}", 1, 0, 'R')
            self.pdf.cell(30, 8, f"${float(row.get('savings', 0)):,.2f}", 1, 1, 'R')
        
        # Footer
        self.pdf.ln(10)
        self.pdf.set_font("Helvetica", 'I', 8)
        self.pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')

        return self.pdf.output(dest='S').encode('latin1')

def generate_quote_pdf_response(quote_data, itemized_df, booking_id, customer_name, event_date, event_type):
    """Generate a PDF from quote data"""
    generator = QuotePDFGenerator()
    return generator.generate_quote_pdf(quote_data, itemized_df, booking_id, customer_name, event_date, event_type)

def generate_dj_contract_pdf_response(booking_data):
    """Generate a DJ Contract PDF from booking data"""
    generator = PDFGenerator()
    return generator.generate_dj_contract_pdf(booking_data)
