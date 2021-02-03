from PySide import QtGui, QtCore
from completerCreator import get_completer
import FreeCAD
import FreeCADGui
import batteryPackUtils as bpUtils
import Part
import Cell
class BatteryPackDialog(QtGui.QDialog):

    def __init__(self, fdir):
        super(BatteryPackDialog, self).__init__()
        
        self.freecad_dir = fdir
        self.initUI()
        
    def initUI(self):
        mainLayout = QtGui.QVBoxLayout()

        self.model = self.textFieldHelper("Model (Markings)"," | Note : if you don't find the model in the autocomplete, you have to create a new cell first", mainLayout)
        mainLayout.addWidget(self.model)

        mainLayout.addWidget(QtGui.QLabel("Number of cells in series"))
        self.qSpinBox_n_cells_in_series = QtGui.QSpinBox()
        mainLayout.addWidget(self.qSpinBox_n_cells_in_series)

        mainLayout.addWidget(QtGui.QLabel("Number of cells in parallel"))
        self.qSpinBox_n_cells_in_parallel = QtGui.QSpinBox()
        mainLayout.addWidget(self.qSpinBox_n_cells_in_parallel)

        mainLayout.addWidget(QtGui.QLabel("Number of cells in the x axis of the pack"))
        self.qSpinBox_n_cells_in_width = QtGui.QSpinBox()
        mainLayout.addWidget(self.qSpinBox_n_cells_in_width)

        mainLayout.addWidget(QtGui.QLabel("Number of cells in the y axis of the pack"))
        self.qSpinBox_n_cells_in_height = QtGui.QSpinBox()
        mainLayout.addWidget(self.qSpinBox_n_cells_in_height)

        mainLayout.addWidget(QtGui.QLabel("Space between cells in mm"))
        self.qSpinBox_space_cells = QtGui.QSpinBox()
        mainLayout.addWidget(self.qSpinBox_space_cells)

        option1Button = QtGui.QPushButton("Create pack with this cell")
        option1Button.clicked.connect(self.createPack)
        
        
        mainLayout.addWidget(option1Button)

        self.setLayout(mainLayout)
        # define window		xLoc,yLoc,xDim,yDim
        self.setGeometry(	250, 250, 0, 50)
        self.setWindowTitle("New battery pack")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    # Just a wrapper to add text fields (with desrciption and autocomplete) to
    # the given layout in a concise way
    def textFieldHelper(self, label, label_help, layout):
        layout.addWidget(QtGui.QLabel(label+label_help))
        lineEdit = QtGui.QLineEdit()
        lineEdit.setCompleter(get_completer(label, self.freecad_dir))
        return lineEdit
    
    def createPack(self):
        self.n_cells_in_series = self.qSpinBox_n_cells_in_series.value()
        self.n_cells_in_parallel = self.qSpinBox_n_cells_in_parallel.value()
        self.n_cells_in_width = self.qSpinBox_n_cells_in_width.value()
        self.n_cells_in_height = self.qSpinBox_n_cells_in_height.value()
        self.space_between_cells = self.qSpinBox_space_cells.value()
        self.cell = Cell.Cell(self.model.text(), self.freecad_dir)
        # Dimensions in mm
        # For now, harcoded for 18650 cells
        radius = 9
        height = 65

        for w in range(self.n_cells_in_width):
            self.create3dCell(radius, height, w, True)
            FreeCAD.ActiveDocument.recompute()
        
        for h in range(self.n_cells_in_height):
            self.create3dCell(radius, height, h, True)
            FreeCAD.ActiveDocument.recompute()
        
        
        
        FreeCADGui.SendMsgToActiveView("ViewFit")
        FreeCAD.ActiveDocument.recompute()

        self.close()
    
    # If in width, widthOrHeight = True, otherwise False
    def create3dCell(self, radius, height, index, widthOrHeight):
        doc = FreeCAD.ActiveDocument
        label = "Cell-w-"+str(index)
        doc.addObject("Part::Cylinder","Cylinder")
        doc.ActiveObject.Label = label
        
        print(label)
        doc.ActiveObject.Radius = str(radius)+' mm'
        doc.ActiveObject.Height = str(height)+' mm'
        
        doc.ActiveObject.getObject(label).ShapeColor = self.cell.getShapeColor()

        doc.ActiveObject.getObject(label).ShapeColor = self.cell.getShapeColor()
        
        if widthOrHeight:
            self.doc.getObject(label).Placement = App.Placement(App.Vector((index*radius)+self.space_between_cells,0,0),App.Rotation(App.Vector(0,0,1),0))

        else:
            self.doc.getObject(label).Placement = App.Placement(App.Vector(0,(index*radius)+self.space_between_cells,0),App.Rotation(App.Vector(0,0,1),0))


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

