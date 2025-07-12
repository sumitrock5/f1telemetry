import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import csv
import array
import pandas as pd
import bisect
from math import log10, floor


def round_sig(x, sig=3):
    if x == 0:
        return 0
    import math
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

def load_csv_with_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

file_path = 'Data_nor.csv'
data_nor = load_csv_with_csv(file_path)

file_path = 'Data_pia.csv'
data_pia = load_csv_with_csv(file_path)

file_path = 'Data_Circuit.csv'
data_circuit = load_csv_with_csv(file_path)
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
distance_pia = np.array(data_pia[2], dtype=float)
speed_pia = np.array(data_pia[0], dtype=float)
time_pia = np.array(data_pia[1], dtype=str)
distance_nor = np.array(data_nor[2], dtype=float)
speed_nor = np.array(data_nor[0], dtype=float)
time_nor = np.array(data_nor[1], dtype=str)
#if distance_nor[0]<distance_pia[0]:
#    index = bisect.bisect_left(distance_nor, distance_pia[0])
#    delta = time_nor[index:] - time_pia
#if distance_nor[0]>distance_pia[0]:
#    index = bisect.bisect_left(distance_pia, distance_nor[0])
#    delta = time_nor - time_pia[index:]


laptime_nor=pd.to_timedelta(str(time_nor[-1]))
minutes = laptime_nor.components.minutes
seconds = laptime_nor.components.seconds
milliseconds = laptime_nor.components.milliseconds
formatted_nor = f"{minutes:02}:{seconds:02}:{milliseconds:03}"

laptime_pia=pd.to_timedelta(str(time_pia[-1]))
minutes = laptime_pia.components.minutes
seconds = laptime_pia.components.seconds
milliseconds = laptime_pia.components.milliseconds
formatted_pia = f"{minutes:02}:{seconds:02}:{milliseconds:03}"

print(laptime_nor.total_seconds())
print(laptime_pia.total_seconds())

laptime_pia_new=[0]*(len(time_pia))
laptime_nor_new=[0]*(len(time_nor))

for i in range(len(time_pia)):
    laptime_pia_new[i]=pd.to_timedelta(str(time_pia[i])).total_seconds()
for i in range(len(time_nor)):
    laptime_nor_new[i]=pd.to_timedelta(str(time_nor[i])).total_seconds()

if len(distance_pia)<len(distance_nor):
    x_int=distance_pia
    y_int=laptime_pia_new
    delta=[0]*len(laptime_pia_new)
    x_int2=distance_nor
    y_int2=laptime_nor_new
    c=-1

if len(distance_pia)>=len(distance_nor):
    x_int=distance_nor
    y_int=laptime_nor_new
    delta=[0]*len(laptime_nor_new)
    x_int2=distance_pia
    y_int2=laptime_pia_new
    c=1



laptime_int=0
j=0
i=0
for j in range(len(x_int)):
    for i in range(len(x_int2)-1):
            x0, x1 = x_int2[i], x_int2[i + 1]
            if x0 <= x_int[j] <= x1:
                y0, y1 = y_int2[i], y_int2[i + 1]
                # Linear interpolation formula
                weight = (x_int[j] - x0) / (x1 - x0)
                laptime_int= y0 + weight * (y1 - y0)
            if j==len(x_int)-1:
                laptime_int=y1
    delta[j]=c*(y_int[j]-laptime_int)

#print(y_int)
#print(y_int2)

delta = np.array(delta, dtype=float)
#delta[len(delta)-2]=delta[len(delta)-1]

      
#print(delta)
#delta = speed_nor[:321] - speed_pia

circuit_corner_length = np.array(data_circuit[0], dtype=float)
circuit_corner_number = np.array(data_circuit[1], dtype=str)

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
draw.text((30, 20), "MIAMI - QUALIFYING ANALYSIS", font=font_title, fill="white")
draw.text((30, 70), "Driver 1: CHARLES LECLERC", font=font_label, fill="crimson")
draw.text((750, 70), "Driver 2: LEWIS HAMILTON", font=font_label, fill="gold")
draw.text((30, 110), "Lap Time: " + formatted_pia, font=font_label, fill="white")
draw.text((750, 110), "Lap Time: " + formatted_nor, font=font_label, fill="white")
draw.text((450, 110), "Gap: +0.321s", font=font_label, fill="white")


# Define sector boundaries (in meters) — adjust these as per actual track data
sectors = {
    "Sector 1": (0, circuit_corner_length[5]-100),
    "Sector 2": (circuit_corner_length[5]-100, circuit_corner_length[9]-100),
    "Sector 3": (circuit_corner_length[9]-100, max(distance_pia)),
}

fig, ax = plt.subplots(figsize=(16, 6))  # Wide plot for better visibility

# Plot speed traces with slightly thicker lines and subtle transparency
ax.plot(distance_pia, speed_pia, color='#00F076', label='Piastri', linewidth=2.3, alpha=0.95)
ax.plot(distance_nor, speed_nor, color='#FF8700', label='Norris', linewidth=2.3, alpha=0.95)

# Styling
background_color = (0.05, 0.05, 0.1)
ax.set_facecolor(background_color)
fig.patch.set_facecolor(background_color)
ax.set_title("Speed Trace Comparison", fontsize=18, color='white', pad=20, weight='bold')
ax.set_xlabel("Distance (m)", color='white', fontsize=13, labelpad=10)
ax.set_ylabel("Speed (km/h)", color='white', fontsize=13, labelpad=10)

# Tick adjustments
ax.tick_params(colors='white', labelsize=11, width=1)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Grid styling
ax.grid(True, color='gray', linestyle='--', linewidth=0.3, alpha=0.3)

# Corner markers

# Plot the corner number just below each vertical line.
c=0
for x in circuit_corner_length:
    ax.axvline(x=x, color='white', linestyle=':', linewidth=1.6, alpha=0.5)
    if c==20 or c==25:
        ax.text(x-10, ax.get_ylim()[1]*0.8, "T"+circuit_corner_number[c],
            color='white', fontsize=10, rotation=90,
            ha='center', va='bottom', fontweight='medium')
        c=c+1
        continue
    ax.text(x-10, ax.get_ylim()[1]*0.92, "T"+circuit_corner_number[c],
            color='white', fontsize=10, rotation=90,
            ha='center', va='bottom', fontweight='medium')
    c=c+1

# Sector shading and better-positioned labels
# Highlight sectors with clearer visual distinction
for sector_name, (start, end) in sectors.items():
    # Semi-transparent, distinct-colored backgrounds per sector (alternating tone)
    ax.axvspan(start, end, alpha=0.1, color='dodgerblue' if sector_name == 'Sector 1'
               else 'seagreen' if sector_name == 'Sector 2'
               else 'crimson')

    # Add sector label clearly, centered and slightly below the axis line
    ax.text(
        (start + end) / 2,
        0.12,
        sector_name,
        transform=ax.get_xaxis_transform(),
        color='white',
        fontsize=10,
        ha='center',
        va='top',
        fontweight='bold',
        bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3', alpha=0.6)
    )


# Legend styling
legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=True)
legend.get_frame().set_facecolor('#1a1a2a')
legend.get_frame().set_edgecolor('gray')
for text in legend.get_texts():
    text.set_color('white')
    text.set_fontweight('bold')

plt.tight_layout(pad=3.0)
plot_path = os.path.join(OUTPUT_DIR, "speed_comparison.png")
fig.savefig(plot_path, dpi=120)
#plt.show()
plt.close(fig)


# === STEP 5: DELTA CHART WITH SECTORS & ENHANCED STYLING ===
fig2, ax2 = plt.subplots(figsize=(16, 3))

# Delta trace line
ax2.plot(x_int, delta, color='orange', label='Δ Lap Time (Norris – Piastri)', linewidth=1.8, antialiased=True)

# Fill where Norris is ahead
ax2.fill_between(x_int, delta, 0, where=(delta < 0), interpolate=True, color='#FF8700', alpha=0.25, label='Norris Ahead')

# Fill where Piastri is ahead
ax2.fill_between(x_int, delta, 0, where=(delta > 0), interpolate=True, color='#00F076', alpha=0.25, label='Piastri Ahead')

# Horizontal zero line
ax2.axhline(0, color='white', linewidth=0.5, linestyle='--', alpha=0.7)


# Sector shading and better-positioned labels
# Highlight sectors with clearer visual distinction
for sector_name, (start, end) in sectors.items():
    # Semi-transparent, distinct-colored backgrounds per sector (alternating tone)
    ax2.axvspan(start, end, alpha=0.1, color='dodgerblue' if sector_name == 'Sector 1'
               else 'seagreen' if sector_name == 'Sector 2'
               else 'crimson')

    # Add sector label clearly, centered and slightly below the axis line
    ax2.text(
        (start + end) / 2,
        0.18,
        sector_name,
        transform=ax2.get_xaxis_transform(),
        color='white',
        fontsize=10,
        ha='center',
        va='top',
        fontweight='bold',
        bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3', alpha=0.6)
    )

# Corner markers
# Corner markers

# Plot the corner number just below each vertical line.
c=0
for x in circuit_corner_length:
    ax2.axvline(x=x, color='white', linestyle=':', linewidth=1.6, alpha=0.5)
    if c==10 or c==12:
        ax2.text(x-10, ax2.get_ylim()[1]*0.2, "T"+circuit_corner_number[c],
            color='white', fontsize=10, rotation=90,
            ha='center', va='bottom', fontweight='medium')
        c=c+1
        continue
    ax2.text(x-10, ax2.get_ylim()[1]*0.65, "T"+circuit_corner_number[c],
            color='white', fontsize=10, rotation=90,
            ha='center', va='bottom', fontweight='medium')
    c=c+1

# Y-axis tick labels: add +/− ms
ax2.set_yticks([round_sig(min(delta), 3), 0, round_sig(max(delta), 3)])
ax2.set_yticklabels([str(round_sig(min(delta), 3)) , '0', str(round_sig(max(delta), 3))], color='white', fontsize=11)

# Grid
ax2.grid(True, which='major', axis='y', linestyle='--', linewidth=0.3, alpha=0.3)

# Axis and title styling
ax2.set_title("Time Gap (s) (Norris – Piastri)", fontsize=18, color='white', pad=20, weight='bold')

ax2.set_facecolor((0.05, 0.05, 0.1))
ax2.set_xlabel("Distance (m)", color='white', fontsize=13, labelpad=10)  # increased from 10 to 15
#ax2.set_ylabel("Speed (km/h)", color='white', fontsize=13, labelpad=10)
ax2.tick_params(colors='white')
fig2.patch.set_facecolor((0.05, 0.05, 0.1))

# Legend
# Adjust layout before placing legend
plt.tight_layout(pad=1.5, rect=[0, 0.1, 1, 1])

# Shift legend *after* layout to avoid overlap with xlabel
legend = ax2.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.55),  # Lowered from -0.35 to -0.4 for more gap
    ncol=3,
    frameon=True,
    fontsize=11
)

legend.get_frame().set_facecolor('#0c0c1a')
legend.get_frame().set_edgecolor('gray')
for text in legend.get_texts():
    text.set_color('white')
    text.set_fontweight('bold')

delta_path = os.path.join(OUTPUT_DIR, "delta_chart.png")
fig2.savefig(delta_path, dpi=100)
plt.show()
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
