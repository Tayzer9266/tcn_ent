import streamlit as st
import sys
import os
import base64
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from profiles_data import profile_manager
from components.header_auth import render_auth_header

# Page configuration
st.set_page_config(
    page_title="Professional Profile",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Render authentication header
render_auth_header()

# Custom CSS for professional profile with slideshow
page_style = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}

.profile-hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3em 2em;
    border-radius: 15px;
    color: white;
    margin-bottom: 2em;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.profile-name {
    font-size: 3em;
    font-weight: 800;
    margin-bottom: 0.2em;
}

.profile-title {
    font-size: 1.5em;
    opacity: 0.9;
    margin-bottom: 1em;
}

.rating-badge {
    background: rgba(255,255,255,0.2);
    padding: 0.5em 1em;
    border-radius: 25px;
    display: inline-block;
    font-size: 1.2em;
    margin-right: 1em;
}

.stat-box {
    background: white;
    padding: 1.5em;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.stat-number {
    font-size: 2.5em;
    font-weight: 700;
    color: #667eea;
}

.stat-label {
    color: #666;
    font-size: 0.9em;
    text-transform: uppercase;
}

.tab-content {
    background: white;
    padding: 2em;
    border-radius: 10px;
    box-shadow: 0 2px 15px rgba(0,0,0,0.08);
    margin-top: 1em;
}

/* Slideshow Styles */
.slideshow-container {
    position: relative;
    max-width: 100%;
    margin: auto;
    background: #000;
    border-radius: 10px;
    overflow: hidden;
}

.slide {
    display: none;
    width: 100%;
}

.slide.active {
    display: block;
}

.slide img {
    width: 100%;
    height: 250px;
    object-fit: cover;
}

.slide-controls {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 10px;
    z-index: 10;
}

.slide-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: rgba(255,255,255,0.5);
    cursor: pointer;
    transition: all 0.3s;
}

.slide-dot.active {
    background: white;
    width: 30px;
    border-radius: 6px;
}

.slide-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0,0,0,0.5);
    color: white;
    padding: 15px 20px;
    cursor: pointer;
    font-size: 24px;
    border: none;
    z-index: 10;
    transition: background 0.3s;
}

.slide-nav:hover {
    background: rgba(0,0,0,0.8);
}

.slide-prev {
    left: 10px;
}

.slide-next {
    right: 10px;
}

.review-card {
    background: #f8f9fa;
    padding: 1.5em;
    border-radius: 10px;
    margin-bottom: 1em;
    border-left: 4px solid #667eea;
}

.review-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5em;
}

.review-author {
    font-weight: 600;
    color: #333;
}

.review-date {
    color: #999;
    font-size: 0.9em;
}

.review-stars {
    color: #ffc107;
    font-size: 1.2em;
    margin-bottom: 0.5em;
}

.review-title {
    font-weight: 600;
    color: #667eea;
    margin-bottom: 0.5em;
}

.action-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1em 2em;
    border-radius: 25px;
    border: none;
    font-size: 1.1em;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s;
}

.action-button:hover {
    transform: translateY(-2px);
}

.video-container {
    position: relative;
    padding-bottom: 28.125%;
    height: 0;
    overflow: hidden;
    border-radius: 10px;
    max-width: 50%;
}

.video-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# Slideshow JavaScript
slideshow_js = """
<script>
let currentSlide = 0;

function showSlide(n) {
    const slides = document.getElementsByClassName('slide');
    const dots = document.getElementsByClassName('slide-dot');
    
    if (n >= slides.length) currentSlide = 0;
    if (n < 0) currentSlide = slides.length - 1;
    
    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove('active');
        if (dots[i]) dots[i].classList.remove('active');
    }
    
    if (slides[currentSlide]) {
        slides[currentSlide].classList.add('active');
        if (dots[currentSlide]) dots[currentSlide].classList.add('active');
    }
}

function nextSlide() {
    currentSlide++;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide--;
    showSlide(currentSlide);
}

function goToSlide(n) {
    currentSlide = n;
    showSlide(currentSlide);
}

// Auto-advance slideshow every 5 seconds
setInterval(nextSlide, 5000);

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    showSlide(currentSlide);
});
</script>
"""

# Helper functions
def get_base64_image(image_path):
    """Convert image to base64"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

def render_stars(rating):
    """Render star rating"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "⭐" * full_stars
    if half_star:
        stars += "✨"
    stars += "☆" * empty_stars
    
    return stars

def get_youtube_embed_url(url):
    """Convert YouTube URL to embed URL"""
    if 'youtube.com/watch?v=' in url:
        video_id = url.split('watch?v=')[1].split('&')[0]
        return f"https://www.youtube.com/embed/{video_id}"
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1].split('?')[0]
        return f"https://www.youtube.com/embed/{video_id}"
    return url

# Get profile information from session state or URL parameters
profile_type = None
profile_id = None

# Check session state first
if 'profile_type' in st.session_state and 'profile_id' in st.session_state:
    profile_type = st.session_state.profile_type
    profile_id = st.session_state.profile_id
# Fallback to query params
elif 'profile_type' in st.query_params and 'profile_id' in st.query_params:
    profile_type = st.query_params['profile_type']
    profile_id = st.query_params['profile_id']

if not profile_type or not profile_id:
    st.error("❌ No professional profile specified.")
    st.info("Please select a professional from the listings page.")
    st.stop()

# Get profile data
profile = profile_manager.get_profile_by_id(profile_type, profile_id)

if not profile:
    st.error("❌ Professional profile not found.")
    st.stop()

# Get reviews for this professional
try:
    from sqlalchemy import create_engine, text
    db_config = st.secrets["postgres"]
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(connection_string)
    conn = engine.connect()
    
    result = conn.execute(text('''
        SELECT review_id, client_name, rating, review_title, review_text, 
               event_type, event_date, verified_booking, helpful_count, created_at
        FROM professional_reviews
        WHERE professional_type = :prof_type AND professional_id = :prof_id
        ORDER BY created_at DESC
    '''), {'prof_type': profile_type, 'prof_id': profile_id})
    
    reviews = [dict(row._mapping) for row in result.fetchall()]
    conn.close()
except Exception as e:
    reviews = []
    print(f"Error loading reviews: {e}")

# Parse gallery images and videos
try:
    gallery_images = json.loads(profile.get('gallery_images', '[]')) if profile.get('gallery_images') else []
except:
    gallery_images = []

try:
    gallery_videos = json.loads(profile.get('gallery_videos', '[]')) if profile.get('gallery_videos') else []
except:
    gallery_videos = []

# Don't add profile image to gallery - keep them separate

# HERO SECTION
st.markdown(f'''
<div class="profile-hero">
    <div class="profile-name">{profile['name']}</div>
    <div class="profile-title">{profile['title']}</div>
    <div>
        <span class="rating-badge">
            {render_stars(profile.get('average_rating', 0))} {profile.get('average_rating', 0):.1f}/5.0
        </span>
        <span class="rating-badge">
            📍 {profile.get('service_city', 'Dallas')}, {profile.get('service_state', 'TX')}
        </span>
        <span class="rating-badge">
            💼 {profile.get('events_completed', 0)}+ Events
        </span>
    </div>
</div>
''', unsafe_allow_html=True)

# STATISTICS ROW
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'''
    <div class="stat-box">
        <div class="stat-number">{profile.get('years_experience', 0)}</div>
        <div class="stat-label">Years Experience</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
    <div class="stat-box">
        <div class="stat-number">{profile.get('events_completed', 0)}</div>
        <div class="stat-label">Events Completed</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="stat-box">
        <div class="stat-number">{profile.get('average_rating', 0):.1f}</div>
        <div class="stat-label">Average Rating</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="stat-box">
        <div class="stat-number">{profile.get('total_reviews', 0)}</div>
        <div class="stat-label">Total Reviews</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ACTION BUTTONS
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📧 Request Quote", type="primary", use_container_width=True):
        st.switch_page("pages/94_Request_Quote.py")

with col2:
    if st.button("💬 Contact", use_container_width=True):
        st.info(f"📧 Email: {profile.get('email', 'N/A')}\n📞 Phone: {profile.get('phone', 'N/A')}")

with col3:
    if st.button("❤️ Save to Favorites", use_container_width=True):
        st.success("Added to favorites!")

with col4:
    if st.button("⬅️ Back to Listings", use_container_width=True):
        type_map = {
            'djs': 'pages/2_DJs.py',
            'photographers': 'pages/3_Photographers.py',
            'event_coordinators': 'pages/4_Event_Coordinators.py'
        }
        st.switch_page(type_map.get(profile_type, 'Home.py'))

st.markdown("---")

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["📖 Overview", "🎬 Media Gallery", "⭐ Reviews", "ℹ️ About"])

with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### Professional Overview")
    st.markdown(profile.get('overview_text', profile.get('short_bio', '')))
    
    st.markdown("### What I Offer")
    st.markdown(profile.get('full_bio', ''))
    
    if profile.get('service_radius_miles'):
        st.markdown(f"### Service Area")
        st.info(f"📍 Based in {profile.get('service_city', 'Dallas')}, {profile.get('service_state', 'TX')} - Serving within {profile.get('service_radius_miles', 50)} miles")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### Photo & Video Gallery")
    
    # SLIDESHOW
    if gallery_images:
        slideshow_html = '<div class="slideshow-container">'
        slideshow_html += '<button class="slide-nav slide-prev" onclick="prevSlide()">❮</button>'
        
        for idx, img_path in enumerate(gallery_images):
            img_base64 = get_base64_image(img_path)
            if img_base64:
                active_class = "active" if idx == 0 else ""
                slideshow_html += f'''
                <div class="slide {active_class}">
                    <img src="data:image/png;base64,{img_base64}" alt="Gallery image {idx+1}">
                </div>
                '''
        
        slideshow_html += '<button class="slide-nav slide-next" onclick="nextSlide()">❯</button>'
        
        # Slide indicators
        slideshow_html += '<div class="slide-controls">'
        for idx in range(len(gallery_images)):
            active_class = "active" if idx == 0 else ""
            slideshow_html += f'<span class="slide-dot {active_class}" onclick="goToSlide({idx})"></span>'
        slideshow_html += '</div>'
        
        slideshow_html += '</div>'
        st.markdown(slideshow_html, unsafe_allow_html=True)
        st.markdown(slideshow_js, unsafe_allow_html=True)
    else:
        st.info("No gallery images available yet.")
    
    # VIDEOS
    if profile.get('profile_video_url') or gallery_videos:
        st.markdown("### Videos")
        
        video_col1, video_col2 = st.columns(2)
        
        with video_col1:
            if profile.get('profile_video_url'):
                embed_url = get_youtube_embed_url(profile['profile_video_url'])
                st.markdown(f'''
                <div class="video-container" style="max-width: 100%;">
                    <iframe src="{embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                ''', unsafe_allow_html=True)
        
        with video_col2:
            if gallery_videos and len(gallery_videos) > 0:
                embed_url = get_youtube_embed_url(gallery_videos[0])
                st.markdown(f'''
                <div class="video-container" style="max-width: 100%;">
                    <iframe src="{embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                ''', unsafe_allow_html=True)
        
        # Display remaining gallery videos in 2-column layout
        if len(gallery_videos) > 1:
            for i in range(1, len(gallery_videos), 2):
                vid_col1, vid_col2 = st.columns(2)
                
                with vid_col1:
                    embed_url = get_youtube_embed_url(gallery_videos[i])
                    st.markdown(f'''
                    <div class="video-container" style="max-width: 100%;">
                        <iframe src="{embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                    <br>
                    ''', unsafe_allow_html=True)
                
                with vid_col2:
                    if i + 1 < len(gallery_videos):
                        embed_url = get_youtube_embed_url(gallery_videos[i + 1])
                        st.markdown(f'''
                        <div class="video-container" style="max-width: 100%;">
                            <iframe src="{embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                        </div>
                        <br>
                        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown(f"### Client Reviews ({len(reviews)})")
    
    if reviews:
        # Rating breakdown
        rating_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        for review in reviews:
            rating_counts[review['rating']] += 1
        
        st.markdown("#### Rating Breakdown")
        for rating in range(5, 0, -1):
            count = rating_counts[rating]
            percentage = (count / len(reviews) * 100) if reviews else 0
            st.progress(percentage / 100, text=f"{render_stars(rating)} ({count})")
        
        st.markdown("---")
        
        # Sort options
        sort_option = st.selectbox("Sort by:", ["Most Recent", "Highest Rated", "Most Helpful"])
        
        # Sort reviews
        if sort_option == "Highest Rated":
            reviews = sorted(reviews, key=lambda x: x['rating'], reverse=True)
        elif sort_option == "Most Helpful":
            reviews = sorted(reviews, key=lambda x: x['helpful_count'], reverse=True)
        
        # Display reviews
        for review in reviews:
            verified_badge = "✓ Verified Booking" if review.get('verified_booking') else ""
            st.markdown(f'''
            <div class="review-card">
                <div class="review-header">
                    <span class="review-author">{review['client_name']} {verified_badge}</span>
                    <span class="review-date">{review['created_at'].strftime('%B %d, %Y')}</span>
                </div>
                <div class="review-stars">{render_stars(review['rating'])}</div>
                <div class="review-title">{review.get('review_title', '')}</div>
                <div>{review['review_text']}</div>
                <div style="margin-top: 0.5em; color: #666; font-size: 0.9em;">
                    {review.get('event_type', '')} • {review.get('event_date', '')} • 
                    👍 {review.get('helpful_count', 0)} found this helpful
                </div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("No reviews yet. Be the first to leave a review!")
    
    if st.button("✍️ Write a Review", type="primary"):
        st.switch_page("pages/99_Submit_Review.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### About")
    st.markdown(profile.get('full_bio', ''))
    
    st.markdown("### Contact Information")
    col1, col2 = st.columns(2)
    
    with col1:
        if profile.get('email'):
            st.markdown(f"📧 **Email:** {profile['email']}")
        if profile.get('phone'):
            st.markdown(f"📞 **Phone:** {profile['phone']}")
        if profile.get('website'):
            st.markdown(f"🌐 **Website:** [{profile['website']}]({profile['website']})")
    
    with col2:
        st.markdown("**Social Media:**")
        if profile.get('youtube'):
            st.markdown(f"[🎥 YouTube]({profile['youtube']})")
        if profile.get('instagram'):
            st.markdown(f"[📸 Instagram]({profile['instagram']})")
        if profile.get('facebook'):
            st.markdown(f"[👥 Facebook]({profile['facebook']})")
    
    st.markdown('</div>', unsafe_allow_html=True)
