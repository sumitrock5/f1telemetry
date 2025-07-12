
import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt
import pandas as pd
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


# Setup plotting
fastf1.plotting.setup_mpl(
    mpl_timedelta_support=True,
    misc_mpl_mods=False,
    color_scheme='fastf1'
)

# Load race session
race = fastf1.get_session(2025, "Silverstone", "R")
race.load()

drivers = ['HAM', 'HUL']

# Your styling
my_styles = [
    {'color': 'auto', 'linestyle': 'solid', 'linewidth': 2, 'alpha': 0.8},
    {'color': 'auto', 'linestyle': 'solid', 'linewidth': 2, 'alpha': 0.8},
]

# Get all laps for the drivers
laps = race.laps.pick_drivers(drivers).reset_index()

# Select last 12 laps
max_lap = laps['LapNumber'].max()
cutoff_lap = max_lap - 15
last_12_laps = laps[laps['LapNumber'] >= cutoff_lap]

# Get compound mapping
compound_colors = plotting.get_compound_mapping(session=race)

# Plot
fig, ax = plt.subplots(figsize=(12, 5))

# Styling
background_color = (0.05, 0.05, 0.1)
ax.set_facecolor(background_color)
fig.patch.set_facecolor(background_color)


for driver in drivers:
    driver_laps = last_12_laps[last_12_laps['Driver'] == driver]
    
    style = plotting.get_driver_style(
        identifier=driver,
        style=my_styles,
        session=race
    )
    
    # Plot line
    ax.plot(
        driver_laps['LapNumber'],
        driver_laps['LapTime'],
        label=driver,
        **style
    )
    
    # Scatter dots - compound colours
    colors = driver_laps['Compound'].map(compound_colors)
    
    ax.scatter(
        driver_laps['LapNumber'],
        driver_laps['LapTime'],
        color=colors,
        s=60,
        edgecolor='black',
        linewidth=0.8,
        zorder=5,
        label=None
    )
    
    # Plot only PIT STOP vertical lines
    pits = driver_laps[driver_laps['PitInTime'].notnull()]
    
    for _, row in pits.iterrows():
        lapnum = row['LapNumber']+1
        
        # Find compound used AFTER this stop
        compound_row = driver_laps.loc[
            driver_laps['LapNumber'] > lapnum
        ].head(1)
        
        if not compound_row.empty:
            new_compound = compound_row.iloc[0]['Compound']
            compound_color = compound_colors.get(new_compound, 'white')
            
            ax.axvline(
                x=lapnum,
                color=compound_color,
                linestyle=':',
                alpha=0.8,
                linewidth=2
            )
            
            # Text slightly above lowest lap time
            min_time = driver_laps['LapTime'].min()
            
            ax.text(
                lapnum-0.1,
                min_time - pd.Timedelta(seconds=2),
                f"→ {new_compound}",
                color=compound_color,
                fontsize=9,
                rotation=90,
                ha='center',
                va='bottom'
            )

# Title etc.
ax.set_title(
    "Last 12 Laps Comparison - Hamilton vs Hülkenberg - 2025 British GP",
    fontsize=16,
    fontweight='bold'
)
ax.set_xlabel("Lap Number", fontsize=12)
ax.set_ylabel("Lap Time", fontsize=12)

ax.set_title(
    "Last 15 Laps Comparison - Hamilton vs Hülkenberg - 2025 British GP", fontsize=18, color='white', pad=20, weight='bold'
)

ax.set_xlabel("Lap Number", color='white', fontsize=13, labelpad=10)
ax.set_ylabel("Lap Time", color='white', fontsize=13, labelpad=10)


ax.grid(True, which='both', linestyle='--', alpha=0.3)

# Add legend for drivers only
plotting.add_sorted_driver_legend(
    ax, race,
    title="Driver",
    loc='upper right',
    frameon=True
)

plt.tight_layout()
plt.show()
