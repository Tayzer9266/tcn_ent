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
# Table of Contents
st.markdown("## Table of Contents")
st.markdown("""
- [🎧 The Best Placement of a DJ in a Venue: Front and Center](#dj-placement)
- [💡 The Power of Dance Floor Lighting](#dance-floor-lighting)
- [💡 Intelligent Lighting Depends on DJ Placement](#intelligent-lighting)
- [💑 Sweetheart Table Placement: Completing the Energy Circle](#sweetheart-table)
""")

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

 
# ---- DJ Placement ----
with st.container():
    st.markdown('<div class="section-title" id="dj-placement">🎧 The Best Placement of a DJ in a Venue: Front and Center</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("pages/images/dance_floor_layout.png", width=400)
    with col2:
        st.markdown("""
        When planning an event, one of the most overlooked yet critical decisions is where to place the DJ. While lighting, décor, and seating often take center stage in planning, the DJ’s position can make or break the energy of the night.

        To maximize a DJ’s potential, the best spot is directly in front of the dance floor—not tucked away in a corner, not hidden behind a bar, but right where the action happens.
        """)
    st.markdown("---")

    # Disco Ball
    with st.container():
        st.markdown("### 🥁 The DJ as the Conductor")
        st.markdown("""
        Think of the DJ as the conductor of an orchestra. Just as a conductor guides musicians through tempo, dynamics, and emotion, the DJ guides the crowd through rhythm, energy, and atmosphere.

        You wouldn’t place a conductor in the corner of a concert hall, disconnected from the musicians. Likewise, you shouldn’t isolate the DJ from the dance floor.

        By being front and center, the DJ commands attention, sets the tempo, and becomes the focal point of the party’s energy. Guests instinctively look toward the booth, syncing their movements with the beats and cues.
        """)

    st.markdown("---")

    # Moving Heads
    with st.container():
        st.markdown("### 👀 Visibility and Engagement")
        st.markdown("""
        Positioning the DJ in front of the dance floor gives them a clear line of sight to the crowd. This visibility is essential for several reasons:
        """)
        st.markdown("""
        - **Read the room**: Knowing when to keep a track rolling or when to switch gears.
        - **Spot energy shifts**: Seeing when the crowd is ready for a hype moment or needs a breather.
        - **Interact directly**: Using the mic to hype the crowd, call out special moments, or build anticipation before a drop.
        """)
        st.markdown("""
        Without this vantage point, the DJ risks playing blind, unable to adjust to the crowd’s pulse in real time.
        """)

    st.markdown("---")
    

# ---- The Power of Dance Floor Lighting ----
 
    with st.container():
        st.markdown("### 💡 The Power of Dance Floor Lighting")
        st.markdown("""
        While the DJ sets the tempo, dance floor lighting amplifies the atmosphere. Together, they create a multisensory experience that keeps guests engaged.
        """)
    st.markdown("---")
    # Energy Flow and Atmosphere
    with st.container():
        st.markdown("### ⚡ Energy Flow and Atmosphere")

        st.markdown("""
        Front placement ensures that the energy flows naturally from the booth to the dance floor. When paired with lighting, the DJ booth becomes the command center of the celebration. The sound and visuals radiate outward, enveloping the crowd in a unified experience.
        """)

    st.markdown("---")

    with st.container():
        st.markdown("### 🎉 The Takeaway")
        st.markdown("""
        If you want your DJ to maximize their potential, place them in front of the dance floor and pair them with strategic lighting design. This transforms them from a background music provider into the conductor of the celebration, orchestrating every beat, transition, and hype moment—while lighting amplifies the emotion and energy.

        The result? A dance floor that stays alive, a crowd that feels connected, and a party that guests will remember long after the last song fades.
        """)
    st.markdown("---")
# ---- Intelligent Lighting Depends on DJ Placement ----
with st.container():
    st.markdown("### 💡 Intelligent Lighting Depends on DJ Placement")
    st.markdown("""
        In most professional setups, intelligent lighting fixtures like moving heads are preprogrammed to work with a dance floor positioned directly in front of the DJ booth. These lights are designed to sweep across the crowd, spotlight key moments, and sync with the music.
        """)
    st.image("pages/images/moving_heads.jpg", width=400)
    st.markdown("""
    When the DJ is placed front and center, the lighting system performs exactly as intended:
    - Moving heads track the dance floor with precision.
    - Preprogrammed effects align with the DJ’s cues, creating seamless audio-visual energy.
    - Crowd interaction is enhanced because the DJ and lighting are working in tandem.

    But if the DJ is pushed to the back or corner of the venue, these advanced lighting techniques lose their impact. The lights may point in the wrong direction, miss the crowd entirely, or create awkward angles that break the immersive experience.

    In short, misplacing the DJ prevents the full use of intelligent lighting technology and diminishes the atmosphere you’ve invested in.
    """)
    st.markdown("---")
# ---- 💑 Sweetheart Table Placement: Completing the Energy Circle----
with st.container():


    st.markdown("### 💑 Sweetheart Table Placement: Completing the Energy Circle")
    st.markdown("""
        To truly maximize the energy of your wedding reception, it’s not just about where the DJ goes — it’s also about how you arrange the sweetheart table and guest seating around the dance floor. """)
    # Lapel Mics for Officiant
    with st.container():
        st.markdown("### 🎯 Ideal Layout:")
        st.markdown("""
 
        - DJ Booth: Positioned front and center of the dance floor.
        - Sweetheart Table or Wedding Party Table: Placed directly opposite the DJ booth, on the far side of the dance floor.
        - Guest Tables: Arranged in a semi-circle or full circle around the dance floor, flanking both the DJ and sweetheart table.
                    
        This layout creates a balanced energy loop:
                    
        - The DJ controls the tempo and hype from one side.
        - The couple or wedding party anchors the emotional center from the other.
        - Guests surround the dance floor, forming a natural amphitheater of excitement.
        """)

        st.markdown("### 💡 Why This Works:")
        st.markdown("""
        - **Visual symmetry**: Guests can see both the DJ and the couple, reinforcing the connection between music, celebration, and love.
        - **Energy focus**: The dance floor becomes the central stage, with sound and lighting flowing outward from the DJ and emotional energy flowing inward from the couple.
        - **Guest engagement**: With tables encircling the dance floor, guests feel included and encouraged to join in — no one feels stuck in the back or disconnected.
        - **Lighting synergy**: Moving heads and washes can sweep across the entire room, hitting both the DJ and sweetheart table for dramatic moments like the first dance or grand entrance.
        """)

# ---- Footer ----
st.markdown("---")
st.markdown("### Ready to Elevate Your Event?")
st.markdown("Contact TCN Entertainment today to discuss your party vibe planning needs and ensure your event is unforgettable!")
 

 
