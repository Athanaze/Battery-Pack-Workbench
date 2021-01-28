# Creates completer that will that will be used by other parts of the workbench
# Autocomplete is mostly based on the .csv spreadsheets
import csv
from PySide import QtGui, QtCore
import preferences
# Returns a PySide.QtGui.QCompleter
def get_completer(column_name, freecad_dir):
    
    completer_list = []
    with open(freecad_dir+"Mod/battery_pack/identification_ref.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            b = row[column_name]

            if (b not in completer_list) and b != "": 
                completer_list.append(b)
    completer = QtGui.QCompleter(completer_list)
    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    completer.setMaxVisibleItems(preferences.N_ITEMS_IN_AUTOCOMPLETE)
    return completer
