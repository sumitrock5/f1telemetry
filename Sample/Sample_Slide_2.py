import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import csv
import array

def load_csv_with_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

file_path = 'Miami2025_data_ham.csv'
data_ham = load_csv_with_csv(file_path)

file_path = 'Miami2025_data_lec.csv'
data_lec = load_csv_with_csv(file_path)
#The variable data is now a list of lists, where each inner list represents a row from the CSV file.


# === CONFIGURATION ===
WIDTH, HEIGHT = 1024, 576
OUTPUT_DIR = "telemetry_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Use a bold font here
FONT_SIZE_TITLE = 72
FONT_SIZE_LABEL = 72
FONT_SIZE_SMALL = 72

# === SIMULATED TELEMETRY DATA ===
distance_lec = np.array(data_lec[2], dtype=float)
speed_leclerc = np.array(data_lec[0], dtype=float)
distance_ham = np.array(data_ham[2], dtype=float)
speed_ham = np.array(data_ham[0], dtype=float)
delta = speed_ham[:321] - speed_leclerc

# === STEP 1: Create Base Slide ===
slide = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 15, 25))
draw = ImageDraw.Draw(slide)

# === STEP 2: Fonts ===
try:
    font_title = ImageFont.truetype(FONT_PATH, FONT_SIZE_TITLE)
    font_label = ImageFont.truetype(FONT_PATH, FONT_SIZE_LABEL)
    font_small = ImageFont.truetype(FONT_PATH, FONT_SIZE_SMALL)
    # Example using Titillium Web Bold
    FONT_PATH_BOLD = "fonts/TitilliumWeb-Bold.ttf"
    FONT_PATH_REGULAR = "fonts/TitilliumWeb-Regular.ttf"

    font_title = ImageFont.truetype(FONT_PATH_BOLD, FONT_SIZE_TITLE)
    font_label = ImageFont.truetype(FONT_PATH_BOLD, FONT_SIZE_LABEL)
    font_small = ImageFont.truetype(FONT_PATH_REGULAR, FONT_SIZE_SMALL)

except:
    font_title = font_label = font_small = None

# === STEP 3: Add Header Text ===
draw.text((30, 20), "MONZA - QUALIFYING ANALYSIS", font=font_title, fill="white")
draw.text((30, 70), "Driver 1: CHARLES LECLERC", font=font_label, fill="crimson")
draw.text((750, 70), "Driver 2: CARLOS SAINZ", font=font_label, fill="gold")
draw.text((30, 110), "Lap Time: 1:23.456", font=font_label, fill="white")
draw.text((750, 110), "Lap Time: 1:23.777", font=font_label, fill="white")
draw.text((450, 110), "Gap: +0.321s", font=font_label, fill="white")

# === STEP 4: SPEED COMPARISON PLOT ===
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(distance_lec, speed_leclerc, color='crimson', label='LECLERC')
ax.plot(distance_ham, speed_ham, color='gold', label='HAMILTON')
ax.set_facecolor((0.05, 0.05, 0.1))
ax.set_title("Speed Comparison", fontsize=14, color='white')
ax.set_xlabel("Distance (km)", color='white')
ax.set_ylabel("Speed (km/h)", color='white')
ax.tick_params(colors='white')
ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
fig.patch.set_facecolor((0.05, 0.05, 0.1))
plt.tight_layout()
plot_path = os.path.join(OUTPUT_DIR, "speed_comparison.png")
fig.savefig(plot_path, dpi=100)
plt.close(fig)

# === STEP 5: DELTA CHART ===
fig2, ax2 = plt.subplots(figsize=(10, 1.5))
ax2.plot(distance_lec, delta, color='orange')
ax2.axhline(0, color='white', linewidth=0.5)
ax2.set_title("Delta (SAINZ - LECLERC)", fontsize=12, color='white')
ax2.set_facecolor((0.05, 0.05, 0.1))
ax2.tick_params(colors='white')
fig2.patch.set_facecolor((0.05, 0.05, 0.1))
plt.tight_layout()
delta_path = os.path.join(OUTPUT_DIR, "delta_chart.png")
fig2.savefig(delta_path, dpi=100)
plt.close(fig2)

# === STEP 6: Paste Charts into Slide ===
speed_chart = Image.open(plot_path).resize((960, 200))
delta_chart = Image.open(delta_path).resize((960, 120))
slide.paste(speed_chart, (32, 160))
slide.paste(delta_chart, (32, 400))

# === STEP 7: Save Final Slide ===
final_slide_path = os.path.join(OUTPUT_DIR, "monza_qualifying_analysis.png")
slide.save(final_slide_path)
print(f"Slide saved to: {final_slide_path}")
