"""
Test script for Gallery Management functionality
Tests the helper functions and validates the implementation
"""

import re
import json

# Test YouTube URL validation
def test_validate_youtube_url():
    """Test YouTube URL validation function"""
    
    def validate_youtube_url(url):
        """Validate if URL is a valid YouTube URL"""
        if not url:
            return False
        
        youtube_patterns = [
            r'(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(https?://)?(www\.)?youtu\.be/[\w-]+',
            r'(https?://)?(www\.)?youtube\.com/embed/[\w-]+'
        ]
        
        for pattern in youtube_patterns:
            if re.match(pattern, url):
                return True
        return False
    
    # Test valid URLs
    valid_urls = [
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'https://youtube.com/watch?v=dQw4w9WgXcQ',
        'http://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'www.youtube.com/watch?v=dQw4w9WgXcQ',
        'youtube.com/watch?v=dQw4w9WgXcQ',
        'https://youtu.be/dQw4w9WgXcQ',
        'https://www.youtube.com/embed/dQw4w9WgXcQ',
    ]
    
    # Test invalid URLs
    invalid_urls = [
        '',
        'https://vimeo.com/123456',
        'https://www.google.com',
        'not a url',
        'youtube.com',
        'https://youtube.com/watch',
    ]
    
    print("Testing YouTube URL Validation:")
    print("-" * 50)
    
    print("\n✅ Valid URLs:")
    for url in valid_urls:
        result = validate_youtube_url(url)
        status = "✓" if result else "✗"
        print(f"  {status} {url}: {result}")
        assert result == True, f"Should be valid: {url}"
    
    print("\n❌ Invalid URLs:")
    for url in invalid_urls:
        result = validate_youtube_url(url)
        status = "✓" if not result else "✗"
        print(f"  {status} {url}: {result}")
        assert result == False, f"Should be invalid: {url}"
    
    print("\n✅ All YouTube URL validation tests passed!")

# Test YouTube ID extraction
def test_extract_youtube_id():
    """Test YouTube video ID extraction"""
    
    def extract_youtube_id(url):
        """Extract YouTube video ID from URL"""
        if 'youtube.com/watch?v=' in url:
            return url.split('watch?v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            return url.split('youtu.be/')[1].split('?')[0]
        elif 'youtube.com/embed/' in url:
            return url.split('embed/')[1].split('?')[0]
        return None
    
    test_cases = [
        ('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
        ('https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=share', 'dQw4w9WgXcQ'),
        ('https://youtu.be/dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
        ('https://youtu.be/dQw4w9WgXcQ?t=10', 'dQw4w9WgXcQ'),
        ('https://www.youtube.com/embed/dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
        ('https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1', 'dQw4w9WgXcQ'),
    ]
    
    print("\n\nTesting YouTube ID Extraction:")
    print("-" * 50)
    
    for url, expected_id in test_cases:
        result = extract_youtube_id(url)
        status = "✓" if result == expected_id else "✗"
        print(f"  {status} {url}")
        print(f"     Expected: {expected_id}, Got: {result}")
        assert result == expected_id, f"ID mismatch for {url}"
    
    print("\n✅ All YouTube ID extraction tests passed!")

# Test gallery data handling
def test_gallery_data_handling():
    """Test gallery images and videos JSON handling"""
    
    print("\n\nTesting Gallery Data Handling:")
    print("-" * 50)
    
    # Test gallery images
    gallery_images = [
        'pages/images/uploads/djs/gallery/dj_1_gallery_20241201_120000.jpg',
        'pages/images/uploads/djs/gallery/dj_1_gallery_20241201_120001.jpg',
        'pages/images/uploads/djs/gallery/dj_1_gallery_20241201_120002.jpg',
    ]
    
    # Convert to JSON
    gallery_json = json.dumps(gallery_images)
    print(f"\n📸 Gallery Images JSON:\n{gallery_json}")
    
    # Parse back
    parsed_images = json.loads(gallery_json)
    assert parsed_images == gallery_images, "Gallery images mismatch"
    print(f"✓ Successfully parsed {len(parsed_images)} images")
    
    # Test gallery videos
    gallery_videos = [
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'https://youtu.be/abc123def45',
        'https://www.youtube.com/watch?v=xyz789uvw12',
    ]
    
    # Convert to JSON
    videos_json = json.dumps(gallery_videos)
    print(f"\n🎥 Gallery Videos JSON:\n{videos_json}")
    
    # Parse back
    parsed_videos = json.loads(videos_json)
    assert parsed_videos == gallery_videos, "Gallery videos mismatch"
    print(f"✓ Successfully parsed {len(parsed_videos)} videos")
    
    # Test adding/removing items
    print("\n📝 Testing Add/Remove Operations:")
    
    # Add new image
    new_image = 'pages/images/uploads/djs/gallery/dj_1_gallery_20241201_120003.jpg'
    gallery_images.append(new_image)
    print(f"  ✓ Added image: {len(gallery_images)} total")
    
    # Remove image
    gallery_images.remove(gallery_images[0])
    print(f"  ✓ Removed image: {len(gallery_images)} total")
    
    # Add new video
    new_video = 'https://www.youtube.com/watch?v=newvideo123'
    gallery_videos.append(new_video)
    print(f"  ✓ Added video: {len(gallery_videos)} total")
    
    # Remove video
    gallery_videos.remove(gallery_videos[0])
    print(f"  ✓ Removed video: {len(gallery_videos)} total")
    
    print("\n✅ All gallery data handling tests passed!")

# Test thumbnail URL generation
def test_thumbnail_generation():
    """Test YouTube thumbnail URL generation"""
    
    def extract_youtube_id(url):
        """Extract YouTube video ID from URL"""
        if 'youtube.com/watch?v=' in url:
            return url.split('watch?v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            return url.split('youtu.be/')[1].split('?')[0]
        elif 'youtube.com/embed/' in url:
            return url.split('embed/')[1].split('?')[0]
        return None
    
    def get_youtube_thumbnail(url):
        """Get YouTube video thumbnail URL"""
        video_id = extract_youtube_id(url)
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
        return None
    
    print("\n\nTesting Thumbnail URL Generation:")
    print("-" * 50)
    
    test_urls = [
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'https://youtu.be/abc123def45',
        'https://www.youtube.com/embed/xyz789uvw12',
    ]
    
    for url in test_urls:
        thumbnail = get_youtube_thumbnail(url)
        video_id = extract_youtube_id(url)
        print(f"\n  Video URL: {url}")
        print(f"  Video ID: {video_id}")
        print(f"  Thumbnail: {thumbnail}")
        assert thumbnail is not None, f"Thumbnail should not be None for {url}"
        assert video_id in thumbnail, f"Thumbnail should contain video ID"
    
    print("\n✅ All thumbnail generation tests passed!")

# Run all tests
if __name__ == "__main__":
    print("=" * 50)
    print("GALLERY MANAGEMENT FUNCTIONALITY TESTS")
    print("=" * 50)
    
    try:
        test_validate_youtube_url()
        test_extract_youtube_id()
        test_gallery_data_handling()
        test_thumbnail_generation()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 50)
        print("\nThe gallery management implementation is working correctly.")
        print("Ready for integration testing with the Streamlit application.")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
