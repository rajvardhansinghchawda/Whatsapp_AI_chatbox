import requests
import json

BASE = "https://4c7d-47-247-173-78.ngrok-free.app"
H = {"ngrok-skip-browser-warning": "true"}

print("=" * 70)
print("AAROHI DATA ACCESS REPORT")
print("=" * 70)

# 1. All Hospitals
print("\n### HOSPITALS ###")
r = requests.get(f"{BASE}/api/hospitals/search/", headers=H)
d = r.json()
print(f"Total: {d['count']}")
for i, h in enumerate(d["results"]):
    print(f"\n{i+1}. {h['name']}")
    print(f"   City: {h.get('city', '?')}")
    print(f"   Address: {h.get('address', '?')}")
    print(f"   Phone: {h.get('phone', '?')}")
    print(f"   Email: {h.get('email', '?')}")
    print(f"   Category: {h.get('category', '?')}")
    print(f"   Type: {h.get('hospital_type', '?')}")
    print(f"   Status: {h.get('status', '?')} | Verified: {h.get('verification_status', '?')}")
    
    depts = h.get("departments", [])
    if depts:
        print(f"   Departments ({len(depts)}):")
        for dep in depts:
            print(f"     - {dep.get('name', '?')} ({dep.get('dept_type', '?')}) | Floor: {dep.get('floor', '?')}")
    
    svcs = h.get("services", [])
    if svcs:
        print(f"   Services ({len(svcs)}):")
        for s in svcs:
            print(f"     - {s.get('name', '?')} (Category: {s.get('category_name', '?')})")

# 2. Bed Availability for each hospital
print("\n\n### BED AVAILABILITY ###")
for h in d["results"]:
    r2 = requests.get(f"{BASE}/api/beds/availability/{h['id']}/", headers=H)
    beds = r2.json()
    print(f"\n{h['name']}:")
    print(f"   Total Beds: {beds.get('total_beds', 0)}")
    print(f"   Available: {beds.get('available_beds', 0)}")
    print(f"   Occupied: {beds.get('occupied_beds', 0)}")
    if beds.get("by_type"):
        for btype, bdata in beds["by_type"].items():
            print(f"   {btype}: {bdata}")

# 3. Service Categories
print("\n\n### SERVICE CATEGORIES ###")
r3 = requests.get(f"{BASE}/api/hospitals/service-categories/", headers=H)
d3 = r3.json()
print(f"Total: {d3['count']}")
for c in d3["results"]:
    print(f"  - {c.get('name', '?')} (ID: {c.get('id', '?')})")

# 4. Services
print("\n\n### ALL SERVICES ###")
r4 = requests.get(f"{BASE}/api/hospitals/services/", headers=H)
d4 = r4.json()
print(f"Total: {d4['count']}")
for s in d4["results"]:
    print(f"  - {s.get('name', '?')} | Category: {s.get('category_name', '?')}")

print("\n" + "=" * 70)
print("END OF REPORT")
print("=" * 70)
