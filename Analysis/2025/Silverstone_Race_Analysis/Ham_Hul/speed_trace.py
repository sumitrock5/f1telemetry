import fastf1
from fastf1 import plotting
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os
import csv
import array
import pandas as pd
import bisect
from math import log10, floor

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Use a bold font here
FONT_SIZE_TITLE = 72
FONT_SIZE_LABEL = 72
FONT_SIZE_SMALL = 72

# Enable dark mode and matplotlib timedelta handling
plotting.setup_mpl(
    mpl_timedelta_support=True,
    misc_mpl_mods=False,
    color_scheme='fastf1'
)

# Load session
session = fastf1.get_session(2025, "Silverstone", "R")
session.load()

# Drivers and laps to compare
drivers = ['HAM', 'HUL']
laps_of_interest = list(range(44, 49))  # laps 44-48 inclusive

# Create figure
fig, ax = plt.subplots(figsize=(10, 5))

# Styling
background_color = (0.05, 0.05, 0.1)
ax.set_facecolor(background_color)
fig.patch.set_facecolor(background_color)


# Plot traces for each driver and lap
for driver in drivers:
    driver_laps = session.laps.pick_drivers(driver)

    # Get driver's color only
    driver_color = plotting.get_driver_style(
        identifier=driver,
        style='color',
        session=session
    )

    for _, lap in driver_laps.iterrows():
        if lap['LapNumber'] not in laps_of_interest:
            continue

        tel = lap.get_car_data().add_distance()

        # ax.plot(
        # tel['Distance'],
        # tel['Speed'],
        # color=driver_color['color']
        # )
        if driver == "HAM" and lap["LapNumber"] == 47:
            # Highlight Hamilton's lap 47
            ax.plot(
                tel['Distance'],
                tel['Speed'],
                color=driver_color['color'],
                linewidth=3.5,
                alpha=1.0,
                zorder=5,
                label=None  # Don't duplicate legend
            )
        else:
            # Other laps (including all of HUL)
            ax.plot(
                tel['Distance'],
                tel['Speed'],
                color=driver_color['color'],
                linewidth=1.2,
                alpha=0.5,
                zorder=2,
                label=None
            )



# Get circuit info
circuit_info = session.get_circuit_info()

if circuit_info and circuit_info.corners is not None:
    v_min, v_max = ax.get_ylim()
    v_min = v_min if v_min < 0 else v_min - 20
    v_max = v_max + 20

    ax.vlines(
        x=circuit_info.corners['Distance'],
        ymin=v_min,
        ymax=v_max,
        colors='grey',
        linestyles='dotted',
        alpha=0.5,
        linewidth=0.8
    )

    for _, corner in circuit_info.corners.iterrows():
        txt = f"{corner['Number']}{corner['Letter']}"
        ax.text(
            corner['Distance'],
            v_min - 10,
            txt,
            va='center_baseline',
            ha='center',
            fontsize=8,
            color='white'
        )

# Title and labels
ax.set_title(
    "Speed Trace Comparison (Laps 44–48)\nHamilton vs Hülkenberg - 2025 British GP", fontsize=18, color='white', pad=20, weight='bold'
)

ax.set_xlabel("Distance (m)", color='white', fontsize=13, labelpad=10)
ax.set_ylabel("Speed (km/h)", color='white', fontsize=13, labelpad=10)
# Grid
ax.grid(True, linestyle='--', alpha=0.3)

# Legend
ax.legend(loc='upper right', frameon=True, fontsize=10)

# Adjust y-limits to show corner labels
ymin, ymax = ax.get_ylim()
ax.set_ylim([ymin - 40, ymax + 20])
ax.set_ylim([150, 320])
ax.set_xlim([3500, 5500])
plt.tight_layout()
plt.show()
