from PySide import QtGui, QtCore
from completerCreator import get_completer



class SetCellValues(QtGui.QDialog):

    def __init__(self, fdir):
        super(SetCellValues, self).__init__()
        
        self.freecad_dir = fdir
        
        self.initUI()
        
    def initUI(self):
        

        option1Button = QtGui.QPushButton("Option 1")
        option1Button.clicked.connect(self.onOption1)
        option2Button = QtGui.QPushButton("Option 2")
        option2Button.clicked.connect(self.onOption2)
        option3Button = QtGui.QPushButton("Option 3")
        option3Button.clicked.connect(self.onOption3)
        option4Button = QtGui.QPushButton("Option 4")
        option4Button.clicked.connect(self.onOption4)
        option5Button = QtGui.QPushButton("Option 5")
        option5Button.clicked.connect(self.onOption5)
        #
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttonBox.addButton(option1Button, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(option2Button, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(option3Button, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(option4Button, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(option5Button, QtGui.QDialogButtonBox.ActionRole)
        #

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(buttonBox)

        # If the brand already exists in the database, please write it exactly the same way
        # (the autocomplete is here to help the user)
        self.textFieldHelper("Brand"," | e.g. Samsung", mainLayout)
        self.textFieldHelper("Model (Markings)"," | e.g. INR18650-35E", mainLayout)
        self.textFieldHelper("Capacity (mAh)"," | e.g. 3450", mainLayout)
        self.textFieldHelper("Discharge A (Max)","", mainLayout)
        self.textFieldHelper("Charging A (Max)","", mainLayout)
        self.textFieldHelper("Chemistry"," | e.g. INR / NMC (LiNiMnCoO2)", mainLayout)
        self.textFieldHelper("Color (Wrap)"," | e.g. Red", mainLayout)
        self.textFieldHelper("Color (Ring)"," | e.g. Purple", mainLayout)
        self.textFieldHelper("Data Sheet"," | http link", mainLayout)
        self.textFieldHelper("Data Sheet (Backup)","", mainLayout)
        self.textFieldHelper("Web", "",mainLayout)
        self.textFieldHelper("Notes", "", mainLayout)

        self.addToDbCheckBox = QtGui.QCheckBox("Add to local database")
        self.addToDbCheckBox.toggle()
        mainLayout.addWidget(self.addToDbCheckBox)
        self.setLayout(mainLayout)
        # define window		xLoc,yLoc,xDim,yDim
        self.setGeometry(	250, 250, 0, 50)
        self.setWindowTitle("Pick a Button")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    # Just a wrapper to add text fields (with desrciption and autocomplete) to
    # the given layout in a concise way
    def textFieldHelper(self, label, label_help, layout):
        layout.addWidget(QtGui.QLabel(label+label_help))
        lineEdit = QtGui.QLineEdit()
        lineEdit.setCompleter(get_completer(label, self.freecad_dir))
        layout.addWidget(lineEdit)

    def onOption1(self):
        self.retStatus = 1
        self.close()

    def onOption2(self):
        self.retStatus = 2
        self.close()

    def onOption3(self):
        self.retStatus = 3
        self.close()

    def onOption4(self):
        self.retStatus = 4
        self.close()

    def onOption5(self):
        self.retStatus = 5
        self.close()


'''
if form.retStatus==1:
	routine1()
elif form.retStatus==2:
	routine2()
elif form.retStatus==3:
	routine3()
elif form.retStatus==4:
	routine4()
elif form.retStatus==5:
	routine5()'''
