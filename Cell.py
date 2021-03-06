import csv
import preferences

# Stores the shape colors corresponding to the english words

COLORS = {
        "Beige":(0.6667,0.4902,0.3176),

        "Black":(0.0, 0.0, 0.0),
        "Translucent (Hidden)":(0.0, 0.0, 0.0),

        "Blue":(0.0, 0.0, 1.0),
        "Blue / Green (Light)":(0.0, 0.0, 1.0),
        "Blue (Light)":(0.0, 0.8, 1.0),
        "Blue - Light":(0.0, 0.8, 1.0),
        "Blue - Sky":(0.0, 0.8, 1.0),
        "Blue (Transparent)":(0.0, 0.8, 1.0),

        "Brown":(0.329, 0.188, 0.050),
        
        "Cardboard (Natural)":(0.329, 0.188, 0.050),

        "Cyan Blue":(0.0, 0.8, 1.0),
        "Cyan / Sky Blue":(0.0, 0.8, 1.0),

        "Gray":(0.670, 0.670, 0.670),

        "Green":(0.0,1.0,0.4980),
        "Green / Apple":(0.0,1.0,0.4980),
        "Green / Blue":(0.0,1.0,0.4980),
        "Green-Blue":(0.0392,0.3412,0.3725),
        "Green-Cyan":(0.0,0.6667,0.5882),
        "Green (Light)":(0.0,1.0,0.4980),
        
        "Khaki-Yellow":(0.333, 0.333, 0.0),
        "Khaki-Yellow (Erbsensuppe)":(0.333, 0.333, 0.0),

        "Mustard":(0.333, 0.333, 0.0),

        "Orange":(1.0,0.3333,0.0),

        "Peach":(1.0, 0.8, 0.7),

        "Pink":(1.0,0.3333,1.0),

        "Purple":(0.6667,0.3333,1.0),
        "Purple (Light)":(0.6667,0.0,1.0),
        "Purple / Maroon":(0.6667,0.0,1.0),
        "Purple / Pink":(1.0,0.3333,1.0),
        "Slate/Purple":(1.0,0.3333,1.0),

        "Red":(1.0, 0.0, 0.0),
        "Salmon":(0.776, 0.607, 0.443),

        "Teal":(0.0, 0.5, 0.5),
        "Turquoise":(0.0,1.0,0.7333),

        "White":(1.0, 1.0, 1.0),
        "White (translucent)":(1.0, 1.0, 1.0),
        "White / Translucent":(1.0, 1.0, 1.0),

        "Yellow":(1.0, 1.0, 0.0),
        "Yellow - Green (Dirty)":(1.0, 1.0, 0.0),
        "Yellow - Green (Light)":(1.0, 1.0, 0.0),
        
        "Maroon":(0.1020,0.0745,0.0471),
}

CURRENCY_SYMBOLS = [
    "$",
    "€",
    "£",
    "¥",
    "₿"
]

class Cell:

    def setup_price_attributes(self, s):
    
        found = False
        for sym in CURRENCY_SYMBOLS:
            if sym in s:
                found = True
                s = s.replace(sym, "")
                self.currency = sym
        
        if not found:
            print("NO CURRENCY SYMBOL FOUND")
        
        s = s.replace(" ", "")
        self.price = float(s)
    
    # Construction by the Model number.
    # Mainly assigns the values from the .csv and put some default values when needed
    def __init__(self, model_number, freecad_dir):
        

        # IDENTIFICATION REF
        found = False    
        with open(freecad_dir+"Mod/battery_pack/identification_ref.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Model (Markings)'] == model_number:
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

        # PRICE PERFORMANCE
        found = False    
        with open(freecad_dir+"Mod/battery_pack/price_performance.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Model'] == model_number:
                    found = True                    
                    self.setup_price_attributes(row['Price (Euro - nkon.nl)'])
                    self.weight = float(row['max. Weight in g (Datasheet)'])
                    self.perf_notes = row['Notes']

        if not found:
            print(model_number)
            print("ERROR : could not find the matching model number in price_performance.csv")
            print("Using the same values as for the Samsung INR18650-35E")
            self.price = 3.25
            self.weight = 50.0
            self.perf_notes = "default values"
        
        self.radius = preferences.DEFAULT_CELL_RADIUS
        self.height = preferences.DEFAULT_CELL_HEIGHT

    def getShapeColor(self):
        try:
            return COLORS[self.colorWrap]
        except KeyError:
            return COLORS[preferences.DEFAULT_CELL_COLOR]
            
    def getLineColor(self):
        return COLORS[preferences.DEFAULT_CELL_LINE_COLOR]

   