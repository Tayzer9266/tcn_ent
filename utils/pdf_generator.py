import io
from fpdf import FPDF
from datetime import datetime, timedelta

class PDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def generate_wedding_pdf(self, form_data):
        """Generate a PDF from wedding form data"""
        self.add_page()

        # Header
        self.set_font("Helvetica", 'B', 16)
        self.cell(0, 10, "Wedding Questionnaire Responses", 0, 1, 'C')
        self.ln(5)

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
        self.ln(10)
        self.set_font("Helvetica", 'I', 8)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')

        # Use UTF-8 encoding instead of latin1
        return self.output(dest='S').encode('latin1')
    
    def _add_section_header(self, title):
        """Add a section header to the PDF"""
        self.ln(10)
        self.set_font("Helvetica", 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(2)

    def generate_quote_form_pdf(self, form_data):
        """Generate a PDF from quote form data"""
        self.add_page()

        # Header
        self.set_font("Helvetica", 'B', 16)
        self.cell(0, 10, "Quote Form", 0, 1, 'C')
        self.ln(5)

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
        self.set_font("Helvetica", '', 12)
        self.multi_cell(0, 10, str(form_data.get('comments') or 'No comments'))

        return self.output(dest='S').encode('latin1')

    def generate_dj_contract_pdf(self, booking_data):
        """Generate a DJ Contract PDF from booking data"""
        # Calculate end_time if not provided and service_hours is available
        end_time_str = booking_data.get('end_time', '')
        if (not end_time_str or end_time_str.lower() in ['not provided', 'end time', '']) and 'service_hours' in booking_data:
            try:
                hours = float(booking_data['service_hours'])
                if hours > 0:
                    start_time_str = booking_data.get('start_time', '')
                    if start_time_str and start_time_str.lower() not in ['not provided', 'start time', '']:
                        try:
                            # Parse start_time assuming format '%I:%M %p'
                            start_dt = datetime.strptime(start_time_str, '%I:%M %p')
                            end_dt = start_dt + timedelta(hours=hours)
                            booking_data['end_time'] = end_dt.strftime('%I:%M %p')
                        except ValueError:
                            # If parsing fails, keep the original end_time
                            pass
            except (ValueError, TypeError):
                # If service_hours cannot be converted to float, skip
                pass

        self.add_page()

        # Header
        self.set_font("Helvetica", 'B', 14)
        self.cell(0, 12, "TCN Entertainment", 0, 1, 'C')
        self.set_font("Helvetica", 'B', 18)
        self.cell(0, 12, "DJ CONTRACT", 0, 1, 'C')
        self.ln(5)

        # Template based on DJ Contract.docx
        template = """

I. PARTIES
This DJ Contract ("Contract" hereinafter) is signed by {dj_name} ("DJ" hereinafter) and {client_name} ("Client" hereinafter) on {contract_date} wherein both parties agreed on the following terms.

II. EVENT DESCRIPTION
This Contract sets out the event details and terms and conditions where DJ {dj_name} will perform.
Will be providing the musical entertainment including any tools need for the sound system to function properly for
Event on {event_date}. Below is the detailed event information:

Performer(s): {dj_name}
Event Title: {event_type}
Date: {event_date}
Start Time: {start_time}
End Time: {end_time}
Venue: {venue}
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



{dj_name}         Date: {contract_date}                                           {client_name}           Date: {contract_date}  
                                                                        
"""

        # Process equipment_list to unnest arrays and put each item on a new line with line numbers
        equipment_list = booking_data.get('equipment_list', '1. MC/DJ performance\n2. Premium PA Sound System\n3. Wireless Microphones\n4. Complimentary Dance Lights')
        # Ensure equipment_list is a string
        if not isinstance(equipment_list, str):
            equipment_list = str(equipment_list)
        # Remove brackets if present
        equipment_list = equipment_list.strip('[]{}')
        if ',' in equipment_list:
            # Split by comma and add line numbers
            items = [item.strip().strip('"').replace("'", "") for item in equipment_list.split(',')]
            equipment_list = '\n'.join([f"{i+1}. {item}" for i, item in enumerate(items)])
        else:
            # If no commas, treat as single item or already formatted
            equipment_list = '1. ' + equipment_list.strip().replace("'", "")

        # Replace placeholders
        contract_text = template.format(
            dj_name=booking_data.get('dj_name', 'Tay Nguyen'),
            client_name=booking_data.get('client_name', 'Client Name'),
            contract_date=booking_data.get('contract_date', datetime.now().strftime('%m/%d/%Y')),
            event_date=booking_data.get('event_date', 'Event Date'),
            start_time=booking_data.get('start_time', 'Start Time'),
            end_time=booking_data.get('end_time', 'End Time'),
            venue=booking_data.get('venue', booking_data.get('venue_name', booking_data.get('event_location', 'Venue Name'))),
            event_location=booking_data.get('venue_address', booking_data.get('event_location', 'Venue Address')),
            total_fee=booking_data.get('total_fee', '0.00'),
            deposit=booking_data.get('deposit', '60.00'),
            event_type=booking_data.get('event_type', 'Event Type'),
            equipment_list=equipment_list
        )

        # Set font and add text
        self.set_font("Helvetica", '', 10)
        self.multi_cell(0, 8, contract_text)

        # Footer
        self.ln(10)
        self.set_font("Helvetica", 'I', 8)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')

        return self.output(dest='S').encode('latin1')

    def _add_field(self, label, value):
        """Add a field to the PDF"""
        self.set_font("Helvetica", 'B', 10)
        self.cell(60, 6, f"{label}:", 0, 0)
        self.set_font("Helvetica", '', 10)

        # Handle long text by splitting into multiple lines
        if value and len(str(value)) > 50:
            self.multi_cell(0, 6, str(value))
        else:
            self.cell(0, 6, str(value) if value else "Not provided", 0, 1)
        self.ln(1)

def generate_wedding_pdf_response(form_data):
    """Generate a PDF from wedding form data"""
    generator = PDFGenerator()
    return generator.generate_wedding_pdf(form_data)

class QuotePDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def _add_section_header(self, title):
        """Add a section header to the PDF"""
        self.ln(10)
        self.set_font("Helvetica", 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(2)

    def _add_field(self, label, value):
        """Add a field to the PDF"""
        self.set_font("Helvetica", 'B', 10)
        self.cell(60, 6, f"{label}:", 0, 0)
        self.set_font("Helvetica", '', 10)

        # Handle long text by splitting into multiple lines
        if value and len(str(value)) > 50:
            self.multi_cell(0, 6, str(value))
        else:
            self.cell(0, 6, str(value) if value else "Not provided", 0, 1)
        self.ln(1)

    def generate_quote_pdf(self, quote_data, itemized_df, booking_id, customer_name, event_date, event_type):
        """Generate a PDF from quote data"""
        self.add_page()

        # Header
        self.set_font("Helvetica", 'B', 16)
        self.cell(0, 10, "Event Quote Estimate", 0, 1, 'C')
        self.ln(5)

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
        self.set_font("Helvetica", 'B', 10)
        self.cell(80, 8, "Product/Service", 1, 0, 'L')
        self.cell(20, 8, "Units", 1, 0, 'C')
        self.cell(30, 8, "Market Price", 1, 0, 'R')
        self.cell(30, 8, "Your Price", 1, 0, 'R')
        self.cell(30, 8, "Savings", 1, 1, 'R')

        # Add table rows
        self.set_font("Helvetica", '', 10)
        for _, row in itemized_df.iterrows():
            self.cell(80, 8, str(row.get('items', '')), 1, 0, 'L')
            self.cell(20, 8, str(row.get('units', '')), 1, 0, 'C')
            self.cell(30, 8, f"${float(row.get('market_price', 0)):,.2f}", 1, 0, 'R')
            self.cell(30, 8, f"${float(row.get('total', 0)):,.2f}", 1, 0, 'R')
            self.cell(30, 8, f"${float(row.get('savings', 0)):,.2f}", 1, 1, 'R')

        # Footer
        self.ln(10)
        self.set_font("Helvetica", 'I', 8)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')

        return self.output(dest='S').encode('latin1')

def generate_quote_pdf_response(quote_data, itemized_df, booking_id, customer_name, event_date, event_type):
    """Generate a PDF from quote data"""
    generator = QuotePDFGenerator()
    return generator.generate_quote_pdf(quote_data, itemized_df, booking_id, customer_name, event_date, event_type)

def generate_dj_contract_pdf_response(booking_data):
    """Generate a DJ Contract PDF from booking data"""
    generator = PDFGenerator()
    return generator.generate_dj_contract_pdf(booking_data)

def generate_quinceanera_questionnaire_pdf():
    """Generate a blank Quinceañera Questionnaire PDF"""
    generator = QuinceaneraQuestionnairePDF()
    return generator.generate_questionnaire()

class QuinceaneraQuestionnairePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """Add header to each page"""
        if self.page_no() == 1:
            # Company Logo/Name
            self.set_font('Helvetica', 'B', 20)
            self.cell(0, 12, 'TCN Entertainment', 0, 1, 'C')
            
            # Title
            self.set_font('Helvetica', 'B', 18)
            self.cell(0, 10, 'Quinceanera Questionnaire', 0, 1, 'C')
            
            # Subtitle
            self.set_font('Helvetica', 'I', 10)
            self.cell(0, 8, 'Please complete this form to help us create your perfect celebration', 0, 1, 'C')
            self.ln(5)
    
    def footer(self):
        """Add footer to each page"""
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def add_section_title(self, title):
        """Add a section title"""
        self.ln(8)
        self.set_font('Helvetica', 'B', 13)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, title, 0, 1, 'L', True)
        self.ln(3)
    
    def add_field(self, label, width=180, height=6):
        """Add a fillable field"""
        self.set_font('Helvetica', '', 10)
        self.cell(0, height, f'{label}: {"_" * int(width/2)}', 0, 1)
        self.ln(1)
    
    def add_checkbox_field(self, label):
        """Add a checkbox field"""
        self.set_font('Helvetica', '', 10)
        self.cell(5, 6, '[ ]', 0, 0)
        self.cell(0, 6, f' {label}', 0, 1)
        self.ln(1)
    
    def add_yes_no_field(self, label):
        """Add a Yes/No checkbox field"""
        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, f'{label}:', 0, 1)
        self.cell(10, 6, '', 0, 0)
        self.cell(5, 6, '[ ]', 0, 0)
        self.cell(15, 6, ' Yes', 0, 0)
        self.cell(5, 6, '[ ]', 0, 0)
        self.cell(15, 6, ' No', 0, 1)
        self.ln(2)
    
    def add_text_area(self, label, lines=3):
        """Add a multi-line text area"""
        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, f'{label}:', 0, 1)
        for i in range(lines):
            self.cell(0, 6, '_' * 90, 0, 1)
        self.ln(2)
    
    def add_time_field(self, label):
        """Add a time field"""
        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, f'{label}: _____ : _____ [ ] AM [ ] PM', 0, 1)
        self.ln(1)
    
    def generate_questionnaire(self):
        """Generate the complete questionnaire PDF"""
        self.add_page()
        
        # Basic Event Information
        self.add_section_title('Basic Event Information')
        self.add_field('Event Date (MM/DD/YYYY)')
        self.add_field('Host/Organizer Name')
        self.add_field('Host Phone Number')
        self.add_field('Host Email Address')
        self.add_time_field('Event Start Time')
        self.add_time_field('Event End Time')
        self.add_field('Number of Guests')
        
        # Venue Information
        self.add_section_title('Venue Information')
        self.add_field('Reception/Main Venue Name')
        self.add_field('Reception Address (Street, City, State, Zip)')
        self.add_field('Venue Phone Number')
        
        # Order of Events and Time
        self.add_section_title('Order of Events and Time')
        self.set_font('Helvetica', 'I', 9)
        self.cell(0, 5, 'Please list the order of events for your celebration with their scheduled times:', 0, 1)
        self.ln(2)

        # Create a table header
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(240, 240, 240)
        self.cell(20, 7, 'Order', 1, 0, 'C', True)
        self.cell(100, 7, 'Event Name', 1, 0, 'C', True)
        self.cell(70, 7, 'Time', 1, 1, 'C', True)

        # Add blank rows for events
        self.set_font('Helvetica', '', 9)
        for i in range(1, 21):
            self.cell(20, 7, str(i), 1, 0, 'C')
            self.cell(100, 7, '', 1, 0, 'L')
            self.cell(70, 7, ' _____ : _____ [ ] AM [ ] PM', 1, 1, 'L')

        self.ln(2)
        self.set_font('Helvetica', 'I', 8)
        self.multi_cell(0, 4, 'Note: List your events in chronological order with their scheduled times.')
        
        # Quinceañera Information
        self.add_section_title('Quinceanera Information')
        self.add_field("Quinceanera's Name")
        self.add_field('Birthday Date (MM/DD/YYYY)')
        
        # Religious Ceremony
        self.add_section_title('Religious Ceremony')
        self.add_field('Church Name (if applicable)')
        self.add_time_field('Mass Time')
        self.add_field('Priest/Pastor Contact')
        
        # Court of Honor
        self.add_section_title('Court of Honor')
        self.add_yes_no_field('Court Introduction')
        self.add_field('Number of Court Members (damas and chambelanes)')
        self.add_text_area('Court Member Names (one per line)', 4)
        self.add_field('Court Entrance Song')
        
        # Traditional Ceremonies
        self.add_section_title('Traditional Ceremonies')
        self.add_yes_no_field('Changing of Shoes Ceremony')
        self.add_field('Who will change the shoes (father/male relative)')
        self.add_field('Changing of Shoes Song')
        self.ln(2)
        self.add_yes_no_field('Crown/Tiara Ceremony')
        self.add_yes_no_field('Last Doll Ceremony')
        
        # Equipment & Services
        self.add_section_title('Equipment & Services')
        self.add_yes_no_field('Up-Lighting')
        self.add_field('How many uplights')
        self.add_field('What color')
        self.ln(2)
        self.add_yes_no_field('Projection Screen')
        self.add_yes_no_field('Photo Booth')
        self.add_field('Photo Booth Template (Standard/Custom)')
        self.add_field('Number of Images')
        self.add_yes_no_field('Photo Booth Props')
        self.add_field('Backdrop Color (White/Shimmering/Black/Other)')
        
        # New page for music sections
        self.add_page()
        
        # Music Programming
        self.add_section_title('Music Programming')
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 6, 'Cocktail Hour Music Style (check all that apply):', 0, 1)
        self.set_font('Helvetica', '', 10)
        
        cocktail_styles = ['Big Band', 'Soft Rock', 'Current Top 40', 'Alternative',
                          'Motown', 'R&B', 'Smooth Jazz', 'Country',
                          'Vitamin String Quartet', 'Afrobeats']
        for i in range(0, len(cocktail_styles), 2):
            self.cell(5, 6, '[ ]', 0, 0)
            self.cell(45, 6, f' {cocktail_styles[i]}', 0, 0)
            if i + 1 < len(cocktail_styles):
                self.cell(5, 6, '[ ]', 0, 0)
                self.cell(45, 6, f' {cocktail_styles[i+1]}', 0, 1)
            else:
                self.ln()
        
        self.ln(3)
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 6, 'Dinner Music Style (check all that apply):', 0, 1)
        self.set_font('Helvetica', '', 10)
        
        for i in range(0, len(cocktail_styles), 2):
            self.cell(5, 6, '[ ]', 0, 0)
            self.cell(45, 6, f' {cocktail_styles[i]}', 0, 0)
            if i + 1 < len(cocktail_styles):
                self.cell(5, 6, '[ ]', 0, 0)
                self.cell(45, 6, f' {cocktail_styles[i+1]}', 0, 1)
            else:
                self.ln()
        
        self.ln(3)
        self.add_time_field('Dinner Time')
        self.add_field('Dinner Style (Plated/Buffet/Family Style)')
        
        # General Music Preferences
        self.add_section_title('General Music Preferences')
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 6, 'Music Genres to Include (check all that apply):', 0, 1)
        self.set_font('Helvetica', '', 10)
        
        genres = ['Oldies', 'Motown', 'Sock Hop', 'Rock', 'Emo', 'Top 40',
                 "70's Disco", "80's", "90's", 'Hip-Hop', 'Country', 'R&B',
                 'Afrobeats', 'Techno', 'Alternative', 'House', 'Afro-House', 'Remixes']
        
        for i in range(0, len(genres), 3):
            for j in range(3):
                if i + j < len(genres):
                    self.cell(5, 6, '[ ]', 0, 0)
                    self.cell(30, 6, f' {genres[i+j]}', 0, 0)
            self.ln()
        
        self.ln(3)
        self.add_field('Custom Genres or Playlist URLs')
        self.add_text_area('Must-Play Songs (up to 20)', 5)
        self.add_text_area('Do Not Play Songs', 3)
        self.add_yes_no_field('Allow Guest Song Requests')
        self.add_yes_no_field("Can DJ fade out songs that aren't working")
        
        # Cultural Music
        self.add_section_title('Cultural Music')
        self.add_text_area('Traditional Mexican Music Requests', 3)
        self.add_text_area('Mariachi Requests', 2)
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 6, 'Regional Music Preferences:', 0, 1)
        self.set_font('Helvetica', '', 10)
        self.add_checkbox_field('Norteño')
        self.add_checkbox_field('Banda')
        self.add_checkbox_field('Other: _______________________________')
        self.ln(2)
        self.add_text_area('Contemporary Latin Hits', 2)
        
        # New page for dances and coordination
        self.add_page()
        
        # Special Dances
        self.add_section_title('Special Dances')
        self.add_field('Waltz Song (traditional first dance)')
        self.add_field('Father-Daughter Dance Song')
        self.add_field('Court Waltz (group dance)')
        self.add_field('Surprise Dance Song')
        
        # Reception Elements
        self.add_section_title('Reception Elements')
        self.add_yes_no_field('Toast by Parents')
        self.add_yes_no_field('Toast by Padrinos (godparents)')
        self.add_yes_no_field('Brindis (official toast)')
        
        # Cultural Announcements
        self.add_section_title('Cultural Announcements')
        self.add_yes_no_field('Presentation of the Quinceañera')
        self.add_yes_no_field('Explanation of Traditions for Non-Latino Guests')
        
        # Line Dances
        self.add_section_title('Line Dances')
        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, 'Select appropriate dances for the celebration:', 0, 1)
        self.ln(2)
        self.add_yes_no_field('Traditional Mexican Group Dances')
        self.add_yes_no_field('Latin Dance Styles')
        self.add_yes_no_field('Standard Line Dances')
        self.add_yes_no_field('Cultural Circle Dances')
        
        # Event Coordination
        self.add_section_title('Event Coordination')
        self.add_field('Banquet Manager Name & Contact')
        self.add_field('Photographer Name & Contact')
        self.add_field('Videographer Name & Contact')
        self.add_text_area('Other Vendor Contacts', 2)
        
        # Announcements
        self.add_section_title('Announcements')
        self.add_yes_no_field('Announce that Guests Can Request Songs')
        self.add_yes_no_field('Announce Photo Booth')
        self.add_yes_no_field('Announce Guest Book Signing')
        self.add_time_field('Late Night Snack Announcement Time')
        self.add_time_field('Last Call for Alcohol Time')
        self.add_yes_no_field('15-Minute Photo Booth Warning')
        
        # Final Notes
        self.add_section_title('Final Notes')
        self.add_field('Last Song of the Night')
        self.add_text_area('Any Additional Notes or Special Requests', 4)
        
        # Footer note
        self.ln(5)
        self.set_font('Helvetica', 'I', 9)
        self.multi_cell(0, 5, 'Thank you for completing this questionnaire! Your detailed information helps us create the perfect celebration for your special day. Please return this form at your earliest convenience.')
        
        # Generate timestamp
        self.ln(5)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 5, f'Form Generated: {datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')
        
        return self.output(dest='S').encode('latin1')
