"""Driver specific plot styling
===============================

Create some plots and show the usage of ``fastf1.plotting.get_driver_style``.
"""


###############################################################################
# Load the race session.


###############################################################################
# Basic driver-specific plot styling
# ----------------------------------
# Plot all the laps for Hamilton, Russel, Perez and Verstappen.
# Filter out slow laps as they distort the graph axis.
# Note: as LapTime is represented by timedelta, calling ``setup_mpl`` earlier
# is required.

# fig, ax = plt.subplots(figsize=(8, 5))

# for driver in ('HAM', 'HUL'):
#     laps = race.laps.pick_drivers(driver).pick_quicklaps().reset_index()
#     style = plotting.get_driver_style(identifier=driver,
#                                       style=['color', 'linestyle'],
#                                       session=race)
#     ax.plot(laps['LapTime'], **style, label=driver)

# # add axis labels and a legend
# ax.set_xlabel("Lap Number")
# ax.set_ylabel("Lap Time")
# ax.legend()

###############################################################################
# Sorting the legend
# ------------------
# That plot looks pretty good already, but the order of the labels in the
# legend is slightly chaotic. Instead of trying to order the labels manually,
# use :func:`fastf1.plotting.add_sorted_driver_legend`.
# Let's create the exact same plot again, but this time with a sorted legend
# which means, we only change the very last function call.

# fig, ax = plt.subplots(figsize=(8, 5))

# for driver in ('HAM', 'HUL'):
#     laps = race.laps.pick_drivers(driver).pick_quicklaps().reset_index()
#     style = plotting.get_driver_style(identifier=driver,
#                                       style=['color', 'linestyle'],
#                                       session=race)
#     ax.plot(laps['LapTime'], **style, label=driver)

# # add axis labels and a legend
# ax.set_xlabel("Lap Number")
# ax.set_ylabel("Lap Time")
# plotting.add_sorted_driver_legend(ax, race)

###############################################################################
# Creating fully custom styles
# ----------------------------
# If you want to fully customize the plot style, you can define your own
# styling variants.
#
# Note that the value ``'auto'`` is treated as a magic keyword when used in
# combination with a color. It will be replaced with the team color.
#
# We define two styles, one for the first driver and one for the second driver
# in any team.
#
# The plot that is generated here isn't intended to be very readable, but it
# shows how you can customize any plot styling parameter.

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import fastf1
from fastf1 import plotting
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

# Enable styling
plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')


race = fastf1.get_session(2025, "Silverstone", 'R')
race.load()

# Drivers to compare
drivers = ('HAM', 'HUL')

# Custom styles
my_styles = [
    {'color': 'auto', 'linestyle': '-', 'linewidth': 2, 'alpha': 1},
    {'color': 'auto', 'linestyle': '-', 'linewidth': 2.0, 'alpha': 0.9}
]

compound_colors = plotting.get_compound_mapping(session=race)

fig, ax = plt.subplots(figsize=(14, 6))

driver_offsets = {
    'HAM': +0.7,
    'HUL': -0.5
}

# Styling
background_color = (0.05, 0.05, 0.1)
ax.set_facecolor(background_color)
fig.patch.set_facecolor(background_color)


for driver in drivers:
    # All laps for driver
    laps = race.laps.pick_drivers(driver)
    #laps = laps[laps['LapTime'] < pd.Timedelta(minutes=2, seconds=10)]
    # Get driver style
    style = plotting.get_driver_style(driver, style=my_styles, session=race)

    # Plot line for lap times
    ax.plot(laps['LapNumber'], laps['LapTime'], label=driver, **style)

    # Overlay tyre compound markers
    for compound, color in compound_colors.items():
        compound_laps = laps[laps['Compound'] == compound]
        ax.scatter(
            compound_laps['LapNumber'],
            compound_laps['LapTime'],
            color=color,
            marker='o',
            s=40,
            edgecolors='black',
            linewidths=0.3,
            alpha=0.8
        )

    # Add vertical pit stop lines and label compound used after stop
    pit_laps = laps[laps['PitOutTime'].notna()]
    for _, pit_row in pit_laps.iterrows():
        pit_lap = pit_row['LapNumber']
        compound_after_pit = pit_row['Compound']
        ax.axvline(x=pit_lap, color=style['color'], linestyle=':', alpha=0.4)
        ax.text(pit_lap + 0.3, pit_row['LapTime'], f"{compound_after_pit}", color=style['color'],
                fontsize=8, rotation=90, verticalalignment='bottom')
    
    # Annotate starting tyre
    if not laps.empty:
        first_lap = laps.iloc[0]
        starting_compound = first_lap['Compound']
        ax.text(
        first_lap['LapNumber'] + driver_offsets[driver],           # x offset right of first lap
        first_lap['LapTime'] + pd.Timedelta(seconds=2),  # small vertical offset
        f"Start: {starting_compound}",
        color=style['color'],
        fontsize=7,
        rotation=90, 
        fontweight='bold',
        verticalalignment='bottom',
        horizontalalignment='left'
        )


# Plot cosmetics
# Title etc.

ax.set_title(
    "Hamilton vs Hulkenberg – 2025 British Grand Prix", fontsize=18, color='white', pad=20, weight='bold'
)

ax.set_xlabel("Lap Number", color='white', fontsize=13, labelpad=10)
ax.set_ylabel("Lap Time", color='white', fontsize=13, labelpad=10)

ax.grid(True, linestyle='--', alpha=0.3)

# Add driver-only legend
plotting.add_sorted_driver_legend(ax, race, title="Driver", loc='upper right', frameon=True)

plt.tight_layout()
plt.show()

