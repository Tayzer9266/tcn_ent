"""
Test script to verify profile database setup
"""
from profiles_data import profile_manager

print("=" * 60)
print("PROFILE DATABASE TEST")
print("=" * 60)

# Test Photographers
print("\n📸 PHOTOGRAPHERS:")
photographers = profile_manager.get_all_profiles("photographers")
print(f"Total: {len(photographers)}")
for p in photographers:
    print(f"  - {p['name']} ({p['title']})")

# Test Event Coordinators
print("\n🎉 EVENT COORDINATORS:")
coordinators = profile_manager.get_all_profiles("event_coordinators")
print(f"Total: {len(coordinators)}")
for c in coordinators:
    print(f"  - {c['name']} ({c['title']})")

# Test DJs
print("\n🎵 DJs:")
djs = profile_manager.get_all_profiles("djs")
print(f"Total: {len(djs)}")
for d in djs:
    print(f"  - {d['name']} ({d['title']})")

print("\n" + "=" * 60)
print("✅ All profiles loaded successfully!")
print("=" * 60)
