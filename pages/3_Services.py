import streamlit as st
import base64

# ---- HEADER SECTION ----
st.set_page_config(
    page_title="Services",
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

st.image("pages/images/services.png", width=1750) 

# Inject CSS for background color
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.service-card {
    background: white;
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    border-left: 5px solid #e63946;
}
.service-feature {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    border-left: 3px solid #457b9d;
}
.feature-list {
    list-style-type: none;
    padding-left: 0;
}
.feature-list li {
    padding: 8px 0;
    border-bottom: 1px solid #eee;
}
.feature-list li:last-child {
    border-bottom: none;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---- SERVICES INTRODUCTION ----
with st.container():
    st.markdown('<div class="section-title">🌟 Premium Entertainment Services</div>', unsafe_allow_html=True)
    st.markdown("""
    At TCN Entertainment, we transform ordinary events into extraordinary experiences with our comprehensive range of professional entertainment services. 
    From stunning lighting effects to interactive entertainment options, we have everything you need to create unforgettable memories.
    """)
    st.markdown("---")

# ---- LIGHTING EFFECTS SECTION ----
with st.container():
    st.markdown('<div class="section-title">💡 Professional Lighting Effects</div>', unsafe_allow_html=True)
    
    # Disco Ball
    with st.container():
        st.markdown("### 🪩 Mirror Ball / Disco Ball")
        st.markdown("""
        Create that classic disco atmosphere with our professional mirror ball setup. The rotating mirror ball casts thousands of sparkling lights 
        across your venue, creating a magical, retro-inspired dance floor experience that gets everyone moving.
        
        **Features:**
        - Professional-grade mirror ball with motorized rotation
        - Multiple lighting patterns and speeds
        - Creates sparkling light effects throughout the venue
        - Perfect for retro-themed parties and dance events
        - Complements any music genre
        """)
    
    st.markdown("---")
    
    # Moving Heads
    with st.container():
        st.markdown("### 🤖 Intelligent Moving Heads")
        st.image("pages/images/moving_heads.jpg", width=500)
        st.markdown("""
        Our intelligent moving head lights are the pinnacle of modern lighting technology. These robotic fixtures can pan, tilt, change colors, 
        and create dynamic patterns automatically or follow the beat of the music for a truly immersive experience.
        
        **Capabilities:**
        - 360-degree pan and tilt movement
        - RGBW color mixing with millions of colors
        - Pattern projection and gobo effects
        - Sound-activated and DMX controlled
        - Create aerial effects and beam shows
        """)
    
    st.markdown("---")
    
    # Wash Lighting
    with st.container():
        st.markdown("### 🌈 Wash Lighting")
        st.markdown("""
        Transform your entire venue with beautiful, even color washing. Our wash lights bathe your space in vibrant colors, creating the perfect 
        ambiance for any event theme or mood. From soft pastels to bold primaries, set the tone for your celebration.
        
        **Benefits:**
        - Even, consistent color coverage
        - Smooth color fading and transitions
        - Create mood lighting for any occasion
        - Complement architectural features
        - Energy-efficient LED technology
        """)
    
    st.markdown("---")
    
    # Venue Uplighting
    with st.container():
        st.markdown("### 🏛️ Venue Uplighting")
        st.markdown("""
        Elevate your venue's architecture and create a sophisticated atmosphere with professional uplighting. Strategically placed lights 
        highlight architectural features, create depth, and transform ordinary spaces into extraordinary environments.
        
        **Applications:**
        - Highlight walls, columns, and architectural details
        - Create color themes matching your event
        - Wireless and battery-operated options available
        - DMX control for synchronized effects
        - Perfect for weddings, galas, and corporate events
        """)

# ---- SPECIAL EFFECTS SECTION ----
with st.container():
    st.markdown("---")
    st.markdown('<div class="section-title">✨ Special Effects & Atmosphere</div>', unsafe_allow_html=True)
    
    # Dancing on Clouds
    with st.container():
        st.markdown("### ☁️ Dancing on Clouds (Fog/Smoke Effects)")
        st.image("pages/images/dancing_clouds.jpg", width=500)
        st.markdown("""
        Create an ethereal, magical atmosphere with our professional fog and haze machines. The "dancing on clouds" effect adds depth to lighting, 
        makes laser beams visible, and creates a dreamlike environment that enchants your guests.
        
        **Features:**
        - Professional haze machines for subtle atmosphere
        - Low-lying fog for dramatic floor effects
        - Odorless, non-toxic fog fluid
        - DMX controlled for precise timing
        - Perfect for first dances and special moments
        """)
    
    st.markdown("---")
    
    # Cold Sparks
    with st.container():
        st.markdown("### ✨ Cold Spark Machines")
        st.markdown("""
        Make a grand entrance or highlight special moments with our cold spark machines. These pyrotechnic effects create spectacular showers of 
        sparks without the heat or fire hazard of traditional fireworks, making them safe for indoor use.
        
        **Safety & Features:**
        - Cold sparks (no heat, safe for indoor use)
        - Multiple firing patterns and durations
        - Wireless remote control
        - ADA compliant and venue-friendly
        - Perfect for grand entrances, first dances, countdowns
        """)

# ---- ENTERTAINMENT SECTION ----
with st.container():
    st.markdown("---")
    st.markdown('<div class="section-title">🎤 Interactive Entertainment</div>', unsafe_allow_html=True)
    
    # Karaoke
    with st.container():
        st.markdown("### 🎵 Professional Karaoke Setup")
        st.markdown("""
        Get the party singing with our complete karaoke system! We provide everything needed for hours of singing entertainment, from current 
        hits to classic favorites. Perfect for breaking the ice and getting everyone involved.
        
        **Complete Package Includes:**
        - Professional wireless microphones
        - Extensive song library (50,000+ songs)
        - HD display with lyrics
        - Sound system optimized for vocals
        - Song request management system
        - Host/MC services available
        """)

# ---- MICROPHONES SECTION ----
with st.container():
    st.markdown("---")
    st.markdown('<div class="section-title">🎤 Microphones</div>', unsafe_allow_html=True)
    
    # Lapel Mics for Officiant
    with st.container():
        st.markdown("### 🎙️ Lapel Mics for Officiant")
        st.image("pages/images/lapel_mic.jpg", width=500)
        st.markdown("""
        Ensure clear and crisp audio for your officiant with our professional lapel microphones. Perfect for weddings, ceremonies, and events where clear speech is paramount.
        
        **Features:**
        - Wireless lapel microphones
        - Crystal clear audio quality
        - Easy to use and setup
        - Perfect for officiants, speakers, and presenters
        """)

# ---- PHOTO SERVICES SECTION ----
with st.container():
    st.markdown("---")
    st.markdown('<div class="section-title">📸 Photo & Memory Services</div>', unsafe_allow_html=True)

    # DSLR Photo Booth
    with st.container():
        st.markdown("### 📷 DSLR Photo Booth Experience")
        st.markdown("""
        Capture unforgettable moments with our professional DSLR photo booth service. Unlike basic photo booths, we use high-quality DSLR cameras
        and professional lighting to ensure stunning, print-ready photos that your guests will treasure.

        **Premium Features:**
        - Professional DSLR camera with high-resolution output
        - Studio-quality lighting setup
        - Instant 4x6 or 2x6 prints on premium photo paper
        - Custom branding and templates
        - Digital copies with online gallery
        - Props and backdrops included
        - Social media sharing station
        - Attendant included for seamless operation
        """)

        # Add YouTube video
        st.markdown(
            """
            <iframe width="560" height="315" src="https://www.youtube.com/embed/5QJF-xi3Tog" frameborder="0" allowfullscreen></iframe>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Custom Monogram
    with st.container():
        st.markdown("### 🔤 Custom Monogram, Logo Projection & Slideshow Projection")
        st.markdown("""
        Personalize your event with custom monogram projection services. We project your names, wedding date, logo, or custom design onto walls,
        floors, or dance floors, creating a truly personalized experience.

        **Customization Options:**
        - Custom designed monograms and logos
        - Wedding date and names projection
        - Company branding for corporate events
        - Color matching to your theme
        - Multiple projection surfaces available
        - Digital files accepted (AI, EPS, PNG, JPG)
        - Slideshow projection for memorable moments
        - Live photo booth slideshow display
        """)

# ---- POP-UP TATTOOS SECTION ----
with st.container():
    st.markdown("---")
    st.markdown('<div class="section-title">🎨 Pop-Up Tattoo Services</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown("### 🖌️ Temporary Tattoo Station")
        st.markdown("""
        Add a fun and interactive element to your event with our professional pop-up tattoo service. Our licensed tattoo artists create custom temporary tattoos using high-quality, skin-safe inks that last for days or weeks.

        **Features:**
        - Licensed and experienced tattoo artists
        - Custom designs or pre-made templates
        - Temporary tattoos (water-transfer or airbrush)
        - Safe, hypoallergenic inks
        - Perfect for parties, festivals, and themed events
        - Mobile setup for any location
        - Age-appropriate designs available
        """)

# ---- PHOTOGRAPHERS SECTION ----
with st.container():
    st.markdown("---")
    st.markdown('<div class="section-title">📸 Professional Photography Services</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown("### 📷 Event Photography")
        st.markdown("""
        Capture every precious moment of your event with our professional photographers. From candid shots to posed portraits, we ensure you have beautiful memories to cherish forever.

        **Services Include:**
        - Wedding and engagement photography
        - Corporate event photography
        - Portrait sessions
        - High-resolution digital images
        - Professional editing and retouching
        - Online gallery for easy sharing
        - Print packages available
        - Same-day previews available
        """)

# ---- EVENT COORDINATORS SECTION ----
with st.container():
    st.markdown("---")
    st.markdown('<div class="section-title">🎉 Event Coordination Services</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown("### 📋 Full-Service Event Planning")
        st.markdown("""
        Let our experienced event coordinators handle every detail of your special occasion. From concept to execution, we ensure your vision becomes reality with seamless planning and flawless execution.

        **Coordination Services:**
        - Complete event planning and design
        - Vendor management and coordination
        - Timeline creation and management
        - On-site coordination during the event
        - Budget management
        - Theme development and decor planning
        - Guest list management
        - Day-of coordination for weddings and parties
        """)

# ---- DJ SERVICES SECTION ----
with st.container():
    st.markdown("---")
    st.markdown('<div class="section-title">🎵 Professional DJ Services</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown("### 🎧 DJ Performance & Sound System")
        st.markdown("""
        Elevate your event with our professional DJ services. Our skilled DJs create the perfect soundtrack, keep the energy high, and ensure everyone has an amazing time on the dance floor.

        **DJ Services Include:**
        - Professional sound system setup
        - Custom music selection and playlists
        - Lighting integration
        - MC services and crowd engagement
        - Song requests and special dedications
        - Wireless microphones for announcements
        - Backup equipment for reliability
        - Multiple DJs available for long events
        """)

# ---- CALL TO ACTION ----
with st.container():
    st.markdown("---")
    st.markdown('<div class="section-title">🚀 Ready to Create Magic?</div>', unsafe_allow_html=True)
    st.markdown("""
    Each of our services can be customized to fit your specific event needs. Whether you're planning an intimate gathering or a large-scale production, 
    we have the equipment and expertise to make it unforgettable.
    """)
    
    st.markdown(
        """
        <div style="text-align:center; margin: 40px 0;">
            <a href="Request_Quote" style="background:#e63946;color:#fff;padding:1em 2em;border-radius:8px;font-size:1.3em;font-weight:700;text-decoration:none;box-shadow:0 4px 12px rgba(230,57,70,0.2);transition:all 0.3s ease;">
                📩 Get a Custom Quote Today!
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style="text-align:center; color:#666; font-size:0.9em;">
            All services include professional setup, operation, and breakdown by experienced technicians
        </div>
        """,
        unsafe_allow_html=True
    )


 
