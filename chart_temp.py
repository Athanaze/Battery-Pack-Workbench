import matplotlib.pyplot as plt
import numpy as np
from preferences import *

# value_under is a list
def add_text_on_top_off_bar(ax, y_values, unit, x_pos_offset, color, value_under):
    
    for i, v in enumerate(y_values):
        str_value = str(v) + " "+unit
        x_pos = x_pos_offset + ( i - ((len(str_value)*PLOT_FONT_SIZE) / 2) )
        y_pos = 0.0

        if not (value_under is None):
            y_pos = v  + PLOT_LEGEND_MARGIN + value_under[i]
        else:
            y_pos = v  + PLOT_LEGEND_MARGIN
        ax.text(x_pos, y_pos, str_value, color=color)


class Part:
    def __init__(self, label, total_cells_weight, total_battery_holders_weight, total_cells_price, total_nickel_strip_price):
        self.Label = label
        self.total_cells_weight = total_cells_weight
        self.total_battery_holders_weight = total_battery_holders_weight
        self.total_cells_price = total_cells_price
        self.total_nickel_strip_price = total_nickel_strip_price

selectedObjects = [Part("label", 314.3, 3.0,433.0, 34.0), Part("label2", 323.3, 3.4,443.0, 12.0)]

fig = plt.figure()

packs_name = []

packs_cells_weight = []
packs_total_battery_holders_weight = []

packs_total_cells_price = []
packs_total_nickel_strip_price = []

X = np.arange(2)

for p in selectedObjects:
    packs_name.append(p.Label)

    packs_cells_weight.append(p.total_cells_weight)
    packs_total_battery_holders_weight.append(p.total_battery_holders_weight)
    
    packs_total_cells_price.append(p.total_cells_price)
    packs_total_nickel_strip_price.append(p.total_nickel_strip_price)

ax = fig.add_axes(COMPARISON_PLOT_DIMENSIONS)


ax.bar(
        packs_name,
        packs_total_battery_holders_weight,
        color = WEIGHT_PLOT_BATTERY_HOLDERS_COLOR,
        width = BAR_WIDTH
)

ax.bar(
    packs_name,
    packs_cells_weight,
    color = WEIGHT_PLOT_BATTERY_PACK_COLOR,
    width = BAR_WIDTH,
    bottom=packs_total_battery_holders_weight
)

ax.bar(
    X + (BAR_WIDTH),
    packs_total_cells_price,
    color = PRICE_PLOT_CELLS_COLOR,
    width = BAR_WIDTH,
    bottom = packs_total_nickel_strip_price
)

ax.bar(
    X + (BAR_WIDTH),
    packs_total_nickel_strip_price,
    color = PRICE_PLOT_NICKEL_STRIP_COLOR,
    width = BAR_WIDTH
)
ax.legend(labels=
        ['weight',
        'total battery holders weight',
        'total cells price',
        'total nickel strip price']
)


add_text_on_top_off_bar(
    ax,
    packs_cells_weight,
    "g",
    0.0,
    WEIGHT_PLOT_BATTERY_PACK_COLOR,
    packs_total_battery_holders_weight
)

add_text_on_top_off_bar(
    ax,
    packs_total_battery_holders_weight,
    "g",
    0.0,
    WEIGHT_PLOT_BATTERY_HOLDERS_COLOR,
    None
)

add_text_on_top_off_bar(
    ax,
    packs_total_cells_price,
    "$",
    BAR_WIDTH,
    PRICE_PLOT_CELLS_COLOR,
    packs_total_nickel_strip_price
)

add_text_on_top_off_bar(
    ax,
    packs_total_nickel_strip_price,
    "$",
    BAR_WIDTH,
    PRICE_PLOT_NICKEL_STRIP_COLOR,
    None
)


plt.show()