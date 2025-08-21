import json
import re
import os
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
import contextily as ctx

# ---------------- CONFIG ----------------
VENUES_FILE = "venues.json"
DIARY_FILE = "diary.txt"
OUTPUT_DIR = "maps"
# ----------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

visit_re = re.compile(
    r"^On\s+(?P<date>\d{1,2}\s+[A-Za-z]+\s+\d{4}),\s*I\s*went\s+(?P<loc>[A-Za-z0-9_\-/]+)\s+at\s+(?P<time>\d{1,2}:\d{2}\s*[AP]M)\.",
    re.IGNORECASE
)

deg_re = re.compile(
    r"(?P<deg>-?\d+(?:\.\d+)?)\s*degrees\s+on\s+(?P<date>\d{1,2}\s+[A-Za-z]+\s+\d{4})",
    re.IGNORECASE
)

DATE_FMTS = ["%d %B %Y"]

def parse_date(s):
    for fmt in DATE_FMTS:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Unrecognized date: {s}")

def load_inputs(venues_path, diary_path):
    with open(venues_path, "r") as f:
        venues = json.load(f)
    with open(diary_path, "r") as f:
        diary_lines = [line.strip() for line in f if line.strip()]
    return venues, diary_lines

def process(venues, diary_lines):
    per_day = {}
    for line in diary_lines:
        m = visit_re.match(line)
        if m:
            d = parse_date(m.group("date"))
            t = datetime.strptime(m.group("time"), "%I:%M %p").time()
            loc = m.group("loc")
            per_day.setdefault(d, {"entries": [], "bearing": 0})
            per_day[d]["entries"].append({"time": t, "loc": loc})
            continue
        m2 = deg_re.search(line)
        if m2:
            d = parse_date(m2.group("date"))
            bearing = float(m2.group("deg"))
            per_day.setdefault(d, {"entries": [], "bearing": 0})
            per_day[d]["bearing"] = bearing
            continue
        print(f"ERROR: regex not found for {line}")
    for d in per_day:
        per_day[d]["entries"].sort(key=lambda e: e["time"])
    return per_day

def fmt_date_for_filename(d):
    return d.strftime("%Y-%m-%d")

def rotate_image(path, angle_deg):
    with Image.open(path) as im:
        # rotate with expand=True to avoid cropping
        im_rot = im.rotate(angle_deg, expand=True)
        im_rot.save(path)  # overwrite or save as new file
        print(f"Rotated {path} by {angle_deg}°")

def generate_map_png(date_key, info, venues, out_dir):
    coords = []
    labels = []
    for entry in info["entries"]:
        loc = entry["loc"]
        if loc in venues:
            v = venues[loc]
            x = v["location"]["x"]
            y = v["location"]["y"]
            coords.append((x, y))
            labels.append(f"{v.get('roomName', loc)}\n{entry['time'].strftime('%I:%M %p')}")
        else:
            print(f"Error: Unable to find {loc}")

    if not coords:
        print(f"No valid locations for {date_key}, skipping.")
        return

    xs, ys = zip(*coords)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(xs, ys, 'ro-', linewidth=2, markersize=6)  # route line
    for (x, y), label in zip(coords, labels):
        ax.text(x, y, label, fontsize=8, ha='right')

    # Add base map from contextily
    # Transform to Web Mercator
    import geopandas as gpd
    import pandas as pd
    gdf = gpd.GeoDataFrame(pd.DataFrame({'x': xs, 'y': ys}),
                           geometry=gpd.points_from_xy(xs, ys),
                           crs="EPSG:4326").to_crs(epsg=3857)

    ax.clear()
    ax.plot(gdf.geometry.x, gdf.geometry.y, 'ro-', linewidth=2, markersize=6)
    for geom, label in zip(gdf.geometry, labels):
        ax.text(geom.x, geom.y, label, fontsize=8, ha='right')

    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

    # Rotate map according to bearing
    # bearing = info.get("bearing", 0)
    # if bearing != 0:
    #     trans = Affine2D().rotate_deg_around(gdf.geometry.x.mean(), gdf.geometry.y.mean(), bearing) + ax.transData
    #     for line in ax.lines:
    #         line.set_transform(trans)
    #     for text in ax.texts:
    #         text.set_transform(trans)

    ax.set_axis_off()
    out_path = os.path.join(out_dir, f"{fmt_date_for_filename(date_key)}.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=200)
    plt.close()

    bearing = info.get("bearing", 0)
    if bearing != 0:
        rotate_image(out_path, bearing)

    print(f"Saved {out_path}")

def main():
    venues, diary_lines = load_inputs(VENUES_FILE, DIARY_FILE)
    per_day = process(venues, diary_lines)
    for d in sorted(per_day.keys()):
        generate_map_png(d, per_day[d], venues, OUTPUT_DIR)

if __name__ == "__main__":
    main()
