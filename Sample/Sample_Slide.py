import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image

# === Configuration ===
output_dir = "telemetry_charts"
os.makedirs(output_dir, exist_ok=True)
chart_size = (500, 400)  # Width x Height for each chart
slide_size = (1080, 1350)
background_color = (25, 25, 25)

# === Generate Sample Data (Replace this with real telemetry data) ===
distance = np.linspace(0, 5, 100)
throttle = 80 - 40 * np.sin(distance * 2)
brake = 60 + 30 * np.sin(distance * 2 + 1)
speed_lap1 = 250 + 20 * np.sin(distance * 2)
speed_lap10 = 240 + 15 * np.sin(distance * 2.1)
gear = np.round(5 + np.sin(distance * 3)).astype(int)
rpm = np.random.normal(11000, 500, 20)
lap_times = np.linspace(1.32, 1.38, 20)

# === Chart 1: Throttle & Brake Overlay ===
plt.figure(figsize=(4, 3))
plt.plot(distance, throttle, label='Throttle', color='deepskyblue')
plt.plot(distance, brake, label='Brake', color='red')
plt.title("Throttle / Brake")
plt.xlabel("Distance (km)")
plt.ylabel("Pressure (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/throttle_brake.png", dpi=300)
plt.close()

# === Chart 2: Speed Comparison ===
plt.figure(figsize=(4, 3))
plt.plot(distance, speed_lap1, label='Lap 1', color='orange')
plt.plot(distance, speed_lap10, label='Lap 10', color='blue')
plt.title("Speed Comparison")
plt.xlabel("Distance (km)")
plt.ylabel("Speed (km/h)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/speed_comparison.png", dpi=300)
plt.close()

# === Chart 3: Gear Usage ===
plt.figure(figsize=(4, 3))
plt.plot(distance, gear, color='lime')
plt.title("Gear Usage")
plt.xlabel("Distance (km)")
plt.ylabel("Gear")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/gear_usage.png", dpi=300)
plt.close()

# === Chart 4: RPM vs Lap Time ===
plt.figure(figsize=(4, 3))
plt.scatter(lap_times, rpm, color='yellow')
plt.title("RPM vs Lap Time")
plt.xlabel("Lap Time (min)")
plt.ylabel("RPM")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/rpm_vs_laptime.png", dpi=300)
plt.close()

# === Combine into Slide ===
slide = Image.new("RGB", slide_size, background_color)
positions = [(40, 40), (540, 40), (40, 690), (540, 690)]
chart_files = [
    "throttle_brake.png", "speed_comparison.png",
    "gear_usage.png", "rpm_vs_laptime.png"
]

for pos, file in zip(positions, chart_files):
    chart_path = os.path.join(output_dir, file)
    chart_img = Image.open(chart_path).resize(chart_size)
    slide.paste(chart_img, pos)

# === Save Final Slide ===
final_slide_path = os.path.join(output_dir, "f1_telemetry_slide.png")
slide.save(final_slide_path)
print(f"Saved slide to: {final_slide_path}")
