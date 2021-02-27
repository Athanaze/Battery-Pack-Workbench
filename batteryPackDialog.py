from PySide import QtGui, QtCore
from completerCreator import get_completer
import FreeCAD as App
import FreeCADGui as Gui
import batteryPackUtils as bpUtils
import Part
from Cell import Cell

BATTERY_PACK_DEFAULT_PART_LABEL = "Battery pack"

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
        s = self.qSpinBox_n_cells_in_series.value()
        p = self.qSpinBox_n_cells_in_parallel.value()

        self.cell = Cell(self.model.text(), self.freecad_dir)
        # For now, n cells in series = width, n cells in para = length
        n_cells_in_width = s
        n_cells_in_height = p

        # /!\ space_between_cells must be a STRING formatted like so : '1 mm'
        space_between_cells = str(self.qSpinBox_space_cells.value()) + " mm"

        App.ActiveDocument.recompute()
        prop = 'App::Property'
        App.activeDocument().Tip = App.activeDocument().addObject('App::Part','Part')
        App.activeDocument().Part.addProperty(prop+'Length', 'Width', 'Dimensions', 'Battery pack width').Width = '10 mm'
        App.activeDocument().Part.Label = BATTERY_PACK_DEFAULT_PART_LABEL
        App.activeDocument().Part.addProperty(prop+'Integer', 'S', 'Cells arrangement', 'Cells in series').S = s
        App.activeDocument().Part.addProperty(prop+'Integer', 'P', 'Cells arrangement', 'Cells in parallel').P = p
        App.activeDocument().Part.addProperty(
            prop+'Length',
            'space_between_cells',
            'Cells arrangement',
            'Space between cells'
        ).space_between_cells = space_between_cells

        App.activeDocument().Part.addProperty(prop+'String', 'cell', 'Cell', 'Model of Cell used').cell = self.model.text()
        
        
        Gui.activateView('Gui::View3DInventor', True)
        Gui.activeView().setActiveObject('part', App.activeDocument().Part)
        App.ActiveDocument.recompute()

        # Dimensions in mm
        # For now, harcoded for 18650 cells
        radius = 9
        height = 65

        for w in range(n_cells_in_width):
            self.create3dCell(radius, height, w, True)
            App.ActiveDocument.recompute()
        
        for h in range(n_cells_in_height):
            self.create3dCell(radius, height, h, True)
            App.ActiveDocument.recompute()
        
        Gui.SendMsgToActiveView("ViewFit")
        App.ActiveDocument.recompute()

        self.close()
    
    # If in width, widthOrHeight = True, otherwise False
    def create3dCell(self, radius, height, index, widthOrHeight):
        doc = App.ActiveDocument
        label = "Cell-w-"+str(index)
        doc.addObject("Part::Cylinder","Cylinder")
        doc.ActiveObject.Label = label
        
        print(label)
        doc.ActiveObject.Radius = str(radius)+' mm'
        doc.ActiveObject.Height = str(height)+' mm'
        ''''
        doc.ActiveObject.getObject(label).ShapeColor = self.cell.getShapeColor()

        doc.ActiveObject.getObject(label).ShapeColor = self.cell.getShapeColor()
        
        if widthOrHeight:
            self.doc.getObject(label).Placement = App.Placement(App.Vector((index*radius)+self.space_between_cells,0,0),App.Rotation(App.Vector(0,0,1),0))

        else:
            self.doc.getObject(label).Placement = App.Placement(App.Vector(0,(index*radius)+self.space_between_cells,0),App.Rotation(App.Vector(0,0,1),0))

        '''
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