from PySide import QtGui, QtCore
from completerCreator import get_completer

class SetCellValues(QtGui.QDialog):

    def __init__(self, fdir):
        super(SetCellValues, self).__init__()
        
        self.freecad_dir = fdir
        self.initUI()
        
    def initUI(self):
        mainLayout = QtGui.QVBoxLayout()

        # If the brand already exists in the database, please write it exactly the same way
        # (the autocomplete is here to help the user)
        self.brand = self.textFieldHelper("Brand"," | e.g. Samsung", mainLayout)
        mainLayout.addWidget(self.brand)

        self.model = self.textFieldHelper("Model (Markings)"," | e.g. INR18650-35E", mainLayout)
        mainLayout.addWidget(self.model)

        self.capacity = self.textFieldHelper("Capacity (mAh)"," | e.g. 3450", mainLayout)
        mainLayout.addWidget(self.capacity)

        self.discharge = self.textFieldHelper("Discharge A (Max)","", mainLayout)
        mainLayout.addWidget(self.discharge)

        self.charging = self.textFieldHelper("Charging A (Max)","", mainLayout)
        mainLayout.addWidget(self.charging)

        self.chemistry = self.textFieldHelper("Chemistry"," | e.g. INR / NMC (LiNiMnCoO2)", mainLayout)
        mainLayout.addWidget(self.chemistry)

        self.colorWrap = self.textFieldHelper("Color (Wrap)"," | e.g. Red", mainLayout)
        mainLayout.addWidget(self.colorWrap)

        self.colorRing = self.textFieldHelper("Color (Ring)"," | e.g. Purple", mainLayout)
        mainLayout.addWidget(self.colorRing)

        self.dataSheet = self.textFieldHelper("Data Sheet"," | http link", mainLayout)
        mainLayout.addWidget(self.dataSheet)

        self.dataSheetBackup = self.textFieldHelper("Data Sheet (Backup)","", mainLayout)
        mainLayout.addWidget(self.dataSheetBackup)

        self.web = self.textFieldHelper("Web", "",mainLayout)
        mainLayout.addWidget(self.web)

        self.notes = self.textFieldHelper("Notes", "", mainLayout)
        mainLayout.addWidget(self.notes)

        self.addToDbCheckBox = QtGui.QCheckBox("Add to local database")
        self.addToDbCheckBox.toggle()
        mainLayout.addWidget(self.addToDbCheckBox)

        option1Button = QtGui.QPushButton("Add cell")
        option1Button.clicked.connect(self.addCellButtonClicked)
        
        mainLayout.addWidget(self.addToDbCheckBox)

        self.setLayout(mainLayout)
        # define window		xLoc,yLoc,xDim,yDim
        self.setGeometry(250, 250, 0, 50)
        self.setWindowTitle("New Cell")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    # Just a wrapper to add text fields (with desrciption and autocomplete) to
    # the given layout in a concise way
    def textFieldHelper(self, label, label_help, layout):
        layout.addWidget(QtGui.QLabel(label+label_help))
        lineEdit = QtGui.QLineEdit()
        lineEdit.setCompleter(get_completer(label, self.freecad_dir))
        return lineEdit
    
    def addCellButtonClicked(self):
        f = open(self.freecad_dir+"Mod/battery_pack/identification_ref.csv", 'a')
        f.write(self.makeStrList())
        f.close()

        self.close()
    
    def makeStrList(self):
        li = [
            self.brand,
            self.model,
            self.capacity,
            self.discharge,
            self.charging,
            self.chemistry,
            
            self.colorWrap,
            self.colorRing,
            
            self.dataSheet,
            self.dataSheetBackup,
            self.web,
            self.notes,
        ]
    
        s = ""
        for a in li:
            s+=a+","
        
        return s[:-1]