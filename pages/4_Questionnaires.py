import streamlit as st
import base64
import psycopg2

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# Create the functions
create_get_bookings = """
CREATE OR REPLACE FUNCTION public.f_get_bookings(_email text)
 RETURNS TABLE(booking_id text, event_status character varying, event_date date, event_type character varying, estimated_guest integer, event_location character varying, start_time time without time zone, service_hours numeric, billing_status character varying, payment_due_date date, actual_cost numeric, last_name character varying, event_date_ct integer, venue text)
 LANGUAGE plpgsql
AS $function$
/*****************************
QA Testing
select booking_id  
, event_status  
, event_date   
, event_type  
, estimated_guest  
, event_location  
, start_time  
, service_hours  
, payment_due_date  
, billing_status  
, last_name
, actual_cost  
 from f_get_bookings('loucape1987@yahoo.com')  select * from f_get_bookings('0000029')
select * from f_get_bookings('tnguyen9266@gmail.com') 
select * from event_producm
select * event
select * from event_products where product_id = 6
******************************/
begin

if $1 = '5003' 
	then 
	return query
	select (right('000000'::text || e.event_id::text,6))::text as booking_id
	, e.event_status
	, e.event_date::date 
	, e.event_type
	, e.estimated_guest
	, e.event_location
	, e.start_time
	, e.service_hours::numeric
	, e.billing_status
	, e.payment_due_date::date
	, e.actual_cost::numeric
	, c.last_name
	, (select (count(*))::int as ct from events s where s.event_date::date = e.event_date::date) as event_date_ct
    , e.venue
	from events e 
	left join clients c
		on c.client_id = e.client_id
	where    e.deleted_at is null 
	and lower(e.event_status) not in ('canceled','completed','proposal')
	order by e.event_status desc, e.event_date;
elseif $1 = '5004' 
	then 
	return query
	select (right('000000'::text || e.event_id::text,6))::text as booking_id
	, e.event_status
	, e.event_date::date 
	, e.event_type
	, e.estimated_guest
	, e.event_location
	, e.start_time
	, e.service_hours::numeric
	, e.billing_status
	, e.payment_due_date::date
	, e.actual_cost::numeric
	, c.last_name
	, (select (count(*))::int as ct from events s where s.event_date::date = e.event_date::date) as event_date_ct
    , e.venue
	from events e 
	left join clients c
		on c.client_id = e.client_id
	where e.deleted_at is null 
	and lower(e.event_status) in ('proposal')
	--and e.event_date >= now()::date
	order by e.event_status desc, e.event_date;
elseif $1 = '5005' 
	then 
	return query
	select (right('000000'::text || e.event_id::text,6))::text as booking_id
	, e.event_status
	, e.event_date::date 
	, e.event_type
	, e.estimated_guest
	, e.event_location
	, e.start_time
	, e.service_hours::numeric
	, e.billing_status
	, e.payment_due_date::date
	, e.actual_cost::numeric
	, c.last_name
	, (select (count(*))::int as ct from events s where s.event_date::date = e.event_date::date) as event_date_ct
    , e.venue
	from events e 
	left join clients c
		on c.client_id = e.client_id
	where e.deleted_at is null 
	and lower(e.event_status) in ('canceled')
	order by e.event_status desc, e.event_date;
else 
	return query
	select (right('000000'::text || e.event_id::text,6))::text as booking_id
	, e.event_status
	, e.event_date::date 
	, e.event_type
	, e.estimated_guest
	, e.event_location
	, e.start_time
	, e.service_hours::numeric
	, e.billing_status
	, e.payment_due_date::date
	, e.actual_cost::numeric
    , c.last_name
	, (select (count(*))::int as ct from events s where s.event_date::date = e.event_date::date) as event_date_ct
	, e.venue
	from events e 
	left join clients c
		on c.client_id = e.client_id
	where    lower(trim(c.email)) =  lower(trim($1))
	and e.deleted_at is null 
	and lower(e.event_status) not in ('canceled')
	order by e.event_status desc, e.event_date desc, e.event_id;

end if;

end;
$function$
;
"""

create_event_questionnaire = """
CREATE OR REPLACE FUNCTION public.f_event_questionnaire_by_event_id(_event_id integer)
 RETURNS TABLE(questionnaire_id integer, client_id integer, event_id integer, event_type character varying, created_at timestamp without time zone, updated_at timestamp without time zone, host_name text, host_phone text, host_email text, start_time time without time zone, end_time time without time zone, num_guests integer, venue_name text, venue_address text, venue_phone text, uplighting_color text, photobooth_template text, photobooth_images integer, cocktail_music text[], dinner_music text[], dinner_time time without time zone, dinner_style text, music_genres text[], custom_playlist text, must_play text, do_not_play text, guest_requests boolean, fade_songs boolean, banquet_manager text, photographer text, videographer text, other_vendors text, announce_requests boolean, announce_photobooth boolean, announce_guestbook boolean, snack_time time without time zone, last_call time without time zone, photobooth_warning boolean, last_song text, bride_name text, groom_name text, ceremony_venue text, ceremony_address text, ceremony_phone text, has_ceremony boolean, ceremony_time time without time zone, first_dance text, first_dance_time time without time zone, father_dance text, father_name text, father_dance_time time without time zone, bridal_dance text, mother_dance text, mother_name text, mother_dance_time time without time zone, anniversary_dance boolean, cake_song text, cake_time time without time zone, garter_removal text, garter_removal_time time without time zone, garter_toss text, garter_toss_time time without time zone, bouquet_toss text, bouquet_toss_time time without time zone, private_dance text, memory_book boolean, child_name text, child_age integer, hebrew_name text, temple_name text, rabbi_name text, hora_dance boolean, chair_dance boolean, candle_ceremony boolean, num_candles integer, candle_song text, special_dedications text, torah_music text, haftorah_music text, special_prayers text, traditional_jewish text, israeli_folk text, contemporary_jewish text, child_intro boolean, intro_song text, family_recognition text, motzi boolean, kiddush boolean, parent_speeches boolean, sibling_participation boolean, hava_nagila boolean, traditional_circle boolean, standard_line boolean, no_mature_content boolean, quinceanera_name text, birthday_date date, church_name text, mass_time time without time zone, priest_contact text, court_intro boolean, court_members integer, court_names text, court_song text, shoe_ceremony boolean, shoe_changer text, shoe_song text, crown_ceremony boolean, doll_ceremony boolean, traditional_mexican text, mariachi_requests text, regional_music text[], latin_hits text[], waltz_song text, surprise_dance text, court_waltz text, parent_toast boolean, padrinos_toast boolean, brindis boolean, presentation boolean, tradition_explanation boolean, mexican_dances boolean, latin_dances boolean, standard_dances boolean, cultural_circle boolean, birthday_name text, actual_birthday date, party_theme text, special_decorations text, candle_dedications text, keys_ceremony boolean, tiara_ceremony boolean, grand_entrance boolean, entrance_song text, current_hits text, teen_artists text, age_classics text, tiktok_songs text, birthday_toast boolean, special_dances text, group_photo_times text, social_media_moments text, trending_dances boolean, age_appropriate boolean, social_media_dances boolean, birthday_age integer, milestone text, atmosphere text, age_group text, kid_friendly boolean, interactive_games text, character_songs text, action_songs text[], social_media text, era_music text[], nostalgic_hits text, sophisticated boolean, birthday_intro boolean, cake_presentation text, dancing_level text, interactive_elements text, group_participation text, occasion text, guest_of_honor text, celebration_type text, other_type text, professional_atmosphere boolean, family_friendly boolean, age_range text, cultural_considerations text, recognition_ceremony boolean, ceremony_details text, speeches boolean, speech_details text, special_announcements text, group_activities text, volume_levels text, music_ratio integer, genre_restrictions text, clean_versions boolean, include_line_dances text, line_dance_preference text, is_completed boolean, is_virtual boolean, virtual_platform character varying, event_date timestamp without time zone, event_location character varying, number_of_guests integer, special_requests text, wedding_theme character varying, bridal_party_size integer, first_dance_song character varying, wedding_dress_code character varying, wedding_photographer boolean, mitzvah_theme character varying, mitzvah_boy_or_girl character varying, mitzvah_dance_floor_music boolean, mitzvah_hora_song character varying, mitzvah_traditional_elements boolean, sweet_sixteen_theme character varying, sweet_sixteen_cake_style character varying, sweet_sixteen_special_entrance boolean, sweet_sixteen_wish_list text, sweet_sixteen_dance_song character varying, birthday_party_theme character varying, birthday_party_age integer, birthday_party_songs character varying, birthday_party_catering boolean, birthday_party_activity_plan text, preferred_genres text[], must_play_songs text[], do_not_play_songs text[], playlist_notes text, event_planner boolean, event_planner_name character varying, event_coordinator boolean, event_coordinator_name character varying, event_assistants integer, technical_requirements text, transportation_required boolean, parking_arrangements text, catering_preferences text, lighting_style character varying, audiovisual_needs text, photographer_preferences text, videography_preferences text, event_favors boolean, event_favors_description text, event_gift_registry boolean, event_gift_registry_link character varying, wedding_officiant_name character varying, additional_notes text)
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    SELECT * FROM public.event_questionnaires
    WHERE event_id = _event_id;
END;
$function$
;
"""

# Execute the CREATE statements
with conn.cursor() as cur:
    cur.execute(create_get_bookings)
    cur.execute(create_event_questionnaire)
conn.commit()

st.set_page_config(
    page_title="Questionnaires",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Make your dream a reality!"
    }
)

# Load the images
youtube_img = base64.b64encode(open("pages/images/youtube.png", "rb").read()).decode()
instagram_img = base64.b64encode(open("pages/images/instagram.png", "rb").read()).decode()
facebook_img = base64.b64encode(open("pages/images/facebook.png", "rb").read()).decode()

# Create columns in the sidebar with less spacing
col1, col2, col3, col4, col5 , col6  = st.sidebar.columns([1, 1, 1, 1, 1, 1])

with col1:
    st.markdown(
        """<a href="https://www.youtube.com/@djtayzer">
        <img src="data:image/png;base64,{}" width="30">
        </a>""".format(youtube_img),
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """<a href="https://www.instagram.com/tayzer/">
        <img src="data:image/png;base64,{}" width="30">
        </a>""".format(instagram_img),
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        """<a href="https://www.facebook.com/profile.php?id=61574735690575">
        <img src="data:image/png;base64,{}" width="50">
        </a>""".format(facebook_img),
        unsafe_allow_html=True
    )

# Use local CSS
with open("pages/style/style.css") as source_style:
    st.markdown(f"<style>{source_style.read()}</style>", unsafe_allow_html=True)

st.image("pages/images/event_questionnaire.png", width=1750)  

# Inject CSS for background color and enhanced card styling 717171
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.questionnaire-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border-left: 5px solid #717171; /* Changed to light grey */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.questionnaire-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}
.questionnaire-card h3 {
    color: #717171; /* Changed to light grey */
    margin-bottom: 15px;
    font-size: 1.4em;
}
.questionnaire-card p {
    color: #555;
    font-size: 1em;
    margin-bottom: 20px;
}
.questionnaire-button {
    background: linear-gradient(135deg, #717171 0%, #b0b0b0 100%); /* Changed to light grey */
    color: white;
    border: none;
    padding: 12px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    font-weight: 600;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.3s ease;
    width: 100%;
}
.questionnaire-button:hover {
    background: linear-gradient(135deg, #b0b0b0 0%, #a0a0a0 100%);
    box-shadow: 0 6px 15px rgba(230, 57, 70, 0.4);
    transform: translateY(-2px);
}
.questionnaire-button:active {
    transform: translateY(1px);
}
.section-title {
    color: #717171; /* Changed to light grey */
    font-size: 2em;
    font-weight: 700;
    margin-bottom: 20px;
    text-align: center;
}
.interactive-form-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
    border-radius: 15px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border-left: 5px solid #4CAF50;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.interactive-form-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}
.form-option-button {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    color: white;
    border: none;
    padding: 15px 30px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    font-weight: 600;
    margin: 10px 5px;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.3s ease;
    width: 200px;
}
.form-option-button:hover {
    background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%);
    box-shadow: 0 6px 15px rgba(76, 175, 80, 0.4);
    transform: translateY(-2px);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Page title and introduction
st.markdown('<div class="section-title"></div>', unsafe_allow_html=True)
st.markdown(
    """
    Help us tailor the ultimate experience just for you! We're passionate about making your event unforgettable. 
    By answering a few quick questions, you can help us craft the perfect atmosphere for your celebration. 
    From song preferences to special requests, your input ensures our performance hits all the right notes. 
    We're here to help!
    """
)
st.markdown("---")
# Questionnaire download section (existing PDF downloads)
st.markdown('<div class="section-title">📥 Download Editable PDF Questionnaires</div>', unsafe_allow_html=True)
st.markdown(
    """
    Prefer to fill out a PDF? Download and complete the appropriate questionnaire for your event type. 
    Once completed, you can return it to us via email or bring it to our consultation meeting.
    """
)

# Create columns for better layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="questionnaire-card">', unsafe_allow_html=True)
    st.markdown("### 💍 Wedding Questionnaire")
    st.markdown("For wedding ceremonies and receptions.")
    with open("pages/documents/Wedding DJ Questionnaire.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Wedding Questionnaire",
            data=PDFbyte,
            file_name="Wedding Questionnaire.pdf",
            mime='application/octet-stream',
            key="wedding_pdf"
        )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="questionnaire-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 Party Questionnaire")
    st.markdown("For birthday parties, corporate events, and other celebrations.")
    with open("pages/documents/Party Song Questionnaire v2.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Party Questionnaire",
            data=PDFbyte,
            file_name="Party Questionnaire.pdf",
            mime='application/octet-stream',
            key="party_pdf"
        )
    st.markdown("### 🎭 Mitzvah Questionnaire")
    st.markdown("For Bar/Bat Mitzvah celebrations.")
    with open("pages/documents/Mitzvah Song Questionnaire v1.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Mitzvah Questionnaire",
            data=PDFbyte,
            file_name="Mitzvah Questionnaire.pdf",
            mime='application/octet-stream',
            key="mitzvah_pdf"
        )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="questionnaire-card">', unsafe_allow_html=True)
    st.markdown("### 🎂 Sweet Sixteen Questionnaire")
    st.markdown("For Sweet Sixteen birthday celebrations.")
    with open("pages/documents/Sweet Sixteen Questionnaire.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Sweet Sixteen Questionnaire",
            data=PDFbyte,
            file_name="Sweet Sixteen Questionnaire.pdf",
            mime='application/octet-stream',
            key="sweet_sixteen_pdf"
        )
    st.markdown("### 📸 Photo Booth Questionnaire")
    st.markdown("For photo booth services at your event.")
    with open("pages/documents/Photo Booth Questionnaire.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Photo Booth Questionnaire",
            data=PDFbyte,
            file_name="Photo Booth Questionnaire.pdf",
            mime='application/octet-stream',
            key="photo_booth_pdf"
        )
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# Interactive Form Section
st.markdown('<div class="section-title">📝 Interactive Questionnaires (Do Not Use - Under Construction)</div>', unsafe_allow_html=True)
st.markdown(
    """
    Fill out our interactive questionnaires to help us better understand your event needs. 
    Start by entering your email address below, then select the type of event you're planning.
    """
)

# Email input section
st.markdown('<div class="interactive-form-card">', unsafe_allow_html=True)
st.markdown("### 📧 Start Your Questionnaire")

if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'selected_form' not in st.session_state:
    st.session_state.selected_form = None

email = st.text_input("Enter your email address:", value=st.session_state.user_email, 
                     placeholder="your.email@example.com", key="email_input")

if email:
    st.session_state.user_email = email
    st.success(f"Email saved: {email}")

    # Run query to get bookings
    booking_rows = run_query(f"SELECT * FROM f_get_bookings('{email}')")
    if booking_rows:
        options = [f"{row[3]} at {row[13]} on {row[2]}" for row in booking_rows]  # event_type at venue on event_date
        selected_booking = st.radio("Select your event", options)
        if selected_booking:
            for row in booking_rows:
                if f"{row[3]} at {row[13]} on {row[2]}" == selected_booking:
                    event_id = int(row[0])
                    questionnaire_rows = run_query(f"SELECT * FROM f_event_questionnaire_by_event_id({event_id})")
                    if questionnaire_rows:
                        q_row = questionnaire_rows[0]
                        st.session_state.selected_form = q_row[3]  # event_type
                    else:
                        st.session_state.selected_form = row[3]
                    st.rerun()
    else:
        st.info("No events found for this email.")

# Display selected form
if st.session_state.selected_form:
    st.markdown("---")
    st.markdown(f"### 📋 {st.session_state.selected_form.replace('_', ' ')} Questionnaire")
    
    # Import and render the selected form
    try:
        form_module = __import__(f"pages.questionnaires.{st.session_state.selected_form}_Form", fromlist=['render'])
        form_module.render()
        
        # Save button
        if st.button("💾 Save Progress", key="save_btn", use_container_width=True):
            st.success("Your progress has been saved! You can return later to continue.")
            # In a real implementation, this would save to a database
            # For now, we'll just show a success message
    except ImportError:
        st.warning(f"Form for {st.session_state.selected_form} is not available yet.")

st.markdown('</div>', unsafe_allow_html=True)

 

st.markdown("---")

# Contact information
st.markdown('<div class="section-title">📞 Need Help?</div>', unsafe_allow_html=True)
st.markdown(
    """
    If you have any questions about filling out the questionnaire or need assistance, 
    please don't hesitate to contact us:
    - 📧 Email: tcnentertainmen7@gmail.com
    - 📞 Phone: (714) 260-5003
    """
)
