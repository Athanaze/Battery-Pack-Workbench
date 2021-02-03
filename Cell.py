import csv
import preferences

# Stores the shape colors corresponding to the english words

COLORS = {
        "Purple":(0.6667,0.3333,1.0),
        "Purple (Light)":(0.6667,0.0,1.0),
        "Pink":(1.0,0.3333,1.0),

        "Red":(1.0, 0.0, 0.0),
        "Orange":(1.0,0.3333,0.0),
        "Black":(0.0, 0.0, 0.0),
        "White":(1.0, 1.0, 1.0),
        "Blue":(0.0, 0.0, 1.0),
        "Yellow":(1.0, 1.0, 0.0),
        "Peach":(1.0, 0.8, 0.7),
        "Khaki-Yellow":(0.333, 0.333, 0.0),
        
        "Teal":(0.0, 0.5, 0.5),
        "Turquoise":(0.0,1.0,0.7333),
        "Beige":(0.6667,0.4902,0.3176),
        "Maroon":(0.1020,0.0745,0.0471),
        "Gray":(0.3176,0.3176,0.3176),

        "Green (Light)":(0.0,1.0,0.4980),
        "Green-Blue":(0.0392,0.3412,0.3725),
        "Green-Cyan":(0.0,0.6667,0.5882),
}

class Cell:
    # Construction by the Model number
    def __init__(self, model_number, freecad_dir):
        found = False
        
        with open(freecad_dir+"Mod/battery_pack/identification_ref.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Model (Markings)'] == model_number:
                    print("!!! FOUND !!!")
                    found = True
                    self.brand = row['Brand']
                    self.model = row['Model (Markings)']
                    self.capacity = row['Capacity (mAh)']
                    self.discharge = row['Discharge A (Max)']
                    self.charging = row['Charging A (Max)']
                    self.chemistry = row['Chemistry']
                    
                    self.colorWrap = row['Color (Wrap)']
                    self.colorRing = row['Color (Ring)']

                    if (self.colorWrap == None) and (self.colorRing != None):
                        self.colorWrap = self.colorRing
                    
                    if (self.colorRing == None) and (self.colorWrap != None):
                        self.colorRing = self.colorWrap
                    
                    if self.colorWrap == None:
                        self.colorWrap = preferences.DEFAULT_CELL_COLOR
                    
                    if self.colorRing == None:
                        self.colorRing = preferences.DEFAULT_CELL_COLOR
                    
                    self.dataSheet = row['Data Sheet']
                    self.dataSheetBackup = row['Data Sheet (Backup)']
                    self.web = row['Web']
                    self.notes = row['Notes']
                    self.radius = preferences.DEFAULT_CELL_RADIUS

        if not found:
            print(model_number)
            print("ERROR : could not find the matching model number in identification_ref.csv")
    
    def getShapeColor(self):
        return COLORS[self.colorWrap]