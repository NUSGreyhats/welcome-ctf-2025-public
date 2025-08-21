import json
import folium

# Load JSON from file
with open("venues.json", "r") as f:
    data = json.load(f)

# Create empty map object (we'll fit bounds later)
m = folium.Map(tiles="OpenStreetMap")

# List to store coordinates for fitting bounds
coords = []

# Add markers from JSON
for key, value in data.items():
    if not "location" in value: continue

    lat = value["location"]["y"]  # Latitude
    lon = value["location"]["x"]  # Longitude
    name = f"{key}({value["roomName"]})"

    folium.Marker(
        location=[lat, lon],
        popup=key,
        tooltip=name
    ).add_to(m)

    coords.append([lat, lon])

# Adjust map to fit all points
if coords:
    m.fit_bounds(coords)

# Save map to HTML
m.save("map.html")
print("Map saved to map.html")
