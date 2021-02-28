# Battery Pack Workbench

Workbench dedicated to the creation of battery packs in FreeCAD. Mainly focused on 18650-based battery packs.

Only generates battery pack as a "ortholinear grid" of cells.

## Use cases

- Quickly calculate the capacity, voltage, amps, weight, of different battery configuration (brand, 2S, 3S, etc...)
- Generate the model to check fit and dimensions
- Prepare for building the actual battery (e.g. the worbench gives you an estimate of how much nickel strip is required)

## Preferences

Preferences can be modified by changing the values in preferences.py
The easiest way to load the new preferences is to restart freecad

## Usage on non-manjaro platforms/distros : bugs, errors

I only use manjaro so you might get some errors concerning the path of scripts, assets, etc... or other issues when running this addon on other platforms/distros. If you are able to fix those, I would happily include the fixes in the project.

## Note on the included models

I have chosen to include some .step models with the workbench. This is why this workbench is relatively "heavy" to download. I am not sure if this is the proper way to do it in FreeCAD so I am open to suggestion to fix this.

## Credits

### BMS

<https://grabcad.com/library/bms-10s-up-to-5p-1>

### t-plug

<https://grabcad.com/library/tplug-male-female-t-plug-t-plug-1>

### XT-60

<https://grabcad.com/library/xt60h-connector-correct-contact-spacing-1>

### 18650 Holder

<https://grabcad.com/library/1p-18650-battery-bracket-1>

### 18650 spreadsheets

+ <https://docs.google.com/spreadsheets/d/1fYjDxxCJXfm2wdpGWCaOUGq8V8TOEgsnplHQa4YQpRQ/edit#gid=0>

+ <https://docs.google.com/spreadsheets/d/1v76d4nDLTFQiJnSk-DNkQmA3-0F7qP3t7AbiN11PJ7A/edit#gid=0>

+ All data as of Sep. 18. 2020

Note: I have not checked every values in this spreadsheets, so I recommend always checking with the producer's datasheets. The main function of these spreadsheets is to provide autocomplete and a rough idea of weight and performance. There are prices and link to sellers for some parts. I am not in any way associated with these sellers (maybe the creator of the spreadsheets is ?). I kept the informations in to give a rough idea of the price.

### Additional notes from IvanStroganov

"Note: Max values are only possible at ideal temperatures (5 to 45°C). Esp. low temperatures (-20 to 5°C) can drastically reduce performance. If only one value is given, consider it Max."

## Documentation used

### Workbench creation

<https://wiki.freecadweb.org/Workbench_creation>

### Pyside basics

<https://wiki.freecadweb.org/PySide_Beginner_Examples>

### Pyside docs

<https://srinikom.github.io/pyside-docs/PySide/QtGui/QLabel.html#PySide.QtGui.QLabel>