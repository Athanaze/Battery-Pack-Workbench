N_ITEMS_IN_AUTOCOMPLETE = 100

# Cell
DEFAULT_CELL_RADIUS = 9
DEFAULT_CELL_COLOR = "Pink"
DEFAULT_CELL_LINE_COLOR = "Black"
# Unit : mm
DEFAULT_CELL_RADIUS = 9
DEFAULT_CELL_HEIGHT = 65

# Nickel strip
NICKEL_STRIP_COLOR = (0.5, 0.5, 0.5, 0.0)
NICKEL_STRIP_LINE_POINT_COLOR = (0.0, 0.0, 0.0, 0.0)

# Unit : mm
NICKEL_STRIP_WIDTH = 8.0
NICKEL_STRIP_HEIGHT = 0.15 

# Unit : g
NICKEL_STRIP_WEIGHT_PER_MM3 = 0.00857


# Note : For now, these are made up, to see if the system works
# Unit : g
BATTERY_HOLDER_WEIGHT = 0.5
T_CONNECTOR_WEIGHT = 1.2
XT_60_CONNECTOR_WEIGHT = 1.5

BATTERY_PACK_DEFAULT_PART_LABEL = "Battery_pack"

# Prices

NICKEL_STRIP_PRICE_PER_MM = 0.0035

# "System" related constants
MOD_FOLDER_NAME = "battery_pack"
MENU_TITLE = "Battery Pack"

### PLOT ###

# Must be a pretty low angle so the small percentages
# text are stack horizontally
# and do not show up on top of one another...
PIE_START_ANGLE = 15

PIE_RADIUS = 1.2
PIE_PERCENT_DIST = PIE_RADIUS + 0.05
PIE_PERCENT_PRECISION = '%1.2f%%'

# Colors on the pie and on the comparison charts
WEIGHT_PLOT_NICKEL_STRIP_COLOR = 'grey'
WEIGHT_PLOT_CELL_COLOR = 'royalblue'
WEIGHT_PLOT_BATTERY_HOLDERS_COLOR = 'deeppink'
WEIGHT_PLOT_BATTERY_PACK = "darkred"

PIE_LEGEND_LOCATION = "upper left"


# Comparison between battery packs

# The dimensions [left, bottom, width, height] of the axes.
# All quantities are in fractions of figure width and height.
COMPARISON_PLOT_DIMENSIONS = [0.2,0.06,0.8,0.8]
BAR_WIDTH = 0.25

PRICE_PLOT_CELLS_PRICE = 'gold'
PRICE_PLOT_NICKEL_STRIP_PRICE = 'orange'