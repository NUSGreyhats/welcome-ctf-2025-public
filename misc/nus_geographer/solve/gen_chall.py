import pandas as pd
import random
from datetime import datetime, timedelta

# ==== CONFIG ====
input_file = "nusmods.xlsx"  # your xlsx filename
output_file = "diary.txt"
start_date = datetime(2025, 7, 24)
start_hour = 8
end_hour = 18  # exclusive
# ===============

# Read Sheet1 (locations)
df1 = pd.read_excel(input_file, sheet_name=0)

lines = []

# Group rows by day so we can sort times
for day, group in df1.groupby("Day"):
    date = start_date + timedelta(days=int(day) - 1)
    n = len(group)

    # Generate n random times within the range
    times = []
    for _ in range(n):
        time = None
        while time in times or time == None:
          hour = random.randint(start_hour, end_hour - 1)
          minute = random.randint(0, 59)
          time = timedelta(hours=hour, minutes=minute)
        times.append(time)

    # Sort times to ensure increasing order
    times.sort()

    # Assign sorted times to locations
    for row, tdelta in zip(group.itertuples(), times):
        random_time = datetime.combine(datetime(2025, 1, 1), datetime.min.time()) + tdelta
        line = f"On {date.strftime('%d %B %Y')}, I went {row.Location} at {random_time.strftime('%-I:%M %p')}."
        lines.append(line)

# Read Sheet2 (temperature)
df2 = pd.read_excel(input_file, sheet_name=1)
for _, row in df2.iterrows():
    date = start_date + timedelta(days=int(row["Day"]) - 1)
    temp = row["Temperature"]
    line = f"Today's weather was so hot! How is it {temp} degrees on {date.strftime('%d %B %Y')}?"
    lines.append(line)

# Shuffle temperature lines with the visits (optional)
# temp_lines = [line for line in lines if line.startswith("Today's weather")]
# visit_lines = [line for line in lines if not line.startswith("Today's weather")]

# # Keep visits in time order, shuffle weather lines in
# final_lines = []
# for date in sorted({start_date + timedelta(days=int(d) - 1) for d in df1["Day"]}):
#     # visits for this day
#     day_visits = [line for line in visit_lines if line.startswith(f"On {date.strftime('%d %B %Y')}")]
#     # any weather for this day
#     day_weather = [line for line in temp_lines if date.strftime('%d %B %Y') in line]
#     final_lines.extend(day_visits + day_weather)

random.shuffle(lines)

# Write to text file
with open(output_file, "w") as f:
    f.write("\n".join(lines))

print(f"Written {len(lines)} lines to {output_file}")