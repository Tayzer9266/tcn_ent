# Login and Profile Management System - User Guide

## Overview

A complete login and profile management system has been implemented for the TCN Entertainment website. This system allows administrators to securely log in and manage profiles for Event Coordinators, Photographers, and DJs.

## Features

### 1. **Email-Based Login System**
- Secure login page accessible at `/Login` (pages/1_Login.py)
- Email-based authentication
- Hardcoded password: `Siepe2025!`
- Session management with automatic logout
- Redirect to profile management after successful login

### 2. **Profile Management Dashboard**
- Accessible at `/Profile_Management` (pages/13_Profile_Management.py)
- Requires authentication to access
- Manage three types of profiles:
  - **Event Coordinators**
  - **Photographers**
  - **DJs**

### 3. **Profile Editing Capabilities**
Edit the following fields for each profile:
- Name
- Title
- Short Bio
- Full Bio
- Profile Image (with upload functionality)
- Social Media Links (YouTube, Instagram, Facebook)

### 4. **Database Storage**
- All profile data is stored in SQLite database (`profiles.db`)
- Changes persist across sessions
- Automatic initialization with existing profile data

## How to Use

### Step 1: Access the Login Page
1. Navigate to the website
2. Go to the "Login" page from the sidebar or directly at `/Login`
3. You'll see the login form

### Step 2: Login
1. Enter your email address
2. Enter the password: `Siepe2025!`
3. Click "Login"
4. Upon successful login, you'll be redirected to the Profile Management dashboard

### Step 3: Select Profile Type
1. On the Profile Management dashboard, you'll see three buttons:
   - 📸 Photographers
   - 🎉 Event Coordinators
   - 🎵 DJs
2. Click on the type of profile you want to manage

### Step 4: View Profiles
1. After selecting a profile type, you'll see all profiles in that category
2. Each profile card displays:
   - Profile image
   - Name
   - Title
   - Short bio preview
   - "Edit" button

### Step 5: Edit a Profile
1. Click the "Edit" button on the profile you want to modify
2. An edit form will appear with all current profile information
3. Modify any of the following fields:
   - **Name**: The person's full name
   - **Title**: Their professional title
   - **Short Bio**: Brief description (shown on profile cards)
   - **Full Bio**: Detailed biography
   - **Upload New Image**: Click to upload a new profile picture (PNG, JPG, JPEG)
   - **Social Media Links**: YouTube, Instagram, Facebook URLs

### Step 6: Save Changes
1. After making your edits, click "💾 Save Changes"
2. You'll see a success message
3. The profile list will refresh with your updates
4. Click "❌ Cancel" to discard changes

### Step 7: Logout
1. Click the "Logout" button in the top-right corner
2. You'll be redirected to the login page
3. Your session will be cleared

## File Structure

```
tcn_ent/
├── profiles_data.py              # Profile database management
├── profiles.db                   # SQLite database (auto-created)
├── pages/
│   ├── 1_Login.py               # Login page
│   ├── 8_Photographers.py       # Public photographers page (updated)
│   ├── 9_Event_Coordinators.py  # Public coordinators page (updated)
│   ├── 11_DJs.py                # Public DJs page (updated)
│   └── 13_Profile_Management.py # Admin profile management
└── pages/images/uploads/         # Uploaded profile images (auto-created)
    ├── photographers/
    ├── event_coordinators/
    └── djs/
```

## Technical Details

### Database Schema

**Photographers Table:**
- id (PRIMARY KEY)
- profile_id (UNIQUE)
- name
- title
- short_bio
- full_bio
- image_path
- youtube
- instagram
- facebook
- created_at
- updated_at

**Event Coordinators Table:**
- Same structure as Photographers

**DJs Table:**
- Same structure as Photographers

### Initial Data

The system comes pre-loaded with:
- **1 Photographer**: Samantha Lee
- **1 Event Coordinator**: Isabella Moreno
- **2 DJs**: DJ Tayzer, DJ Tyler

### Image Upload

- Uploaded images are saved to `pages/images/uploads/{profile_type}/`
- Filename format: `{profile_id}_{timestamp}.{extension}`
- Supported formats: PNG, JPG, JPEG
- Images are automatically displayed on public profile pages

## Security Notes

- Password is hardcoded as `Siepe2025!`
- Authentication state is stored in Streamlit session_state
- Profile Management page requires authentication
- Unauthenticated users are redirected to login page

## Public Profile Pages

The following pages automatically display updated profile data:
- **Photographers** (`/Photographers`)
- **Event Coordinators** (`/Event_Coordinators`)
- **DJs** (`/DJs`)

Changes made in the Profile Management dashboard are immediately reflected on these public pages.

## Troubleshooting

### Can't Login
- Verify you're using the correct password: `Siepe2025!`
- Ensure you've entered an email address
- Try refreshing the page

### Changes Not Saving
- Ensure you clicked "💾 Save Changes" button
- Check that all required fields are filled
- Verify you're still logged in (session hasn't expired)

### Images Not Displaying
- Verify the image file format (PNG, JPG, JPEG only)
- Check file size (large files may take time to upload)
- Ensure the upload directory has write permissions

### Profile Management Page Not Accessible
- Verify you're logged in
- If redirected to login, authenticate again
- Check that session hasn't expired

## Future Enhancements

Potential improvements for future versions:
- Multiple user accounts with different permissions
- Password change functionality
- Profile deletion capability
- Bulk profile import/export
- Activity logging
- Profile preview before saving
- Image cropping/resizing tools

## Support

For technical issues or questions, please contact the development team.

---

**Last Updated**: December 2024
**Version**: 1.0
