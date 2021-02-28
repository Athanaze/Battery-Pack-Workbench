from PySide import QtGui, QtCore
from completerCreator import get_completer
import FreeCAD as App
import FreeCADGui as Gui
import batteryPackUtils as bpUtils
import Part
from Cell import Cell
from preferences import *

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
        self.space_between_cells = str(self.qSpinBox_space_cells.value()) + " mm"

        App.ActiveDocument.recompute()
        prop = 'App::Property'
        #App.activeDocument().Tip
        self.part = App.activeDocument().addObject('App::Part',BATTERY_PACK_DEFAULT_PART_LABEL)
        self.part.addProperty(prop+'Length', 'Width', 'Dimensions', 'Battery pack width').Width = '10 mm'
        self.part.addProperty(prop+'Integer', 'S', 'Cells arrangement', 'Cells in series').S = s
        self.part.addProperty(prop+'Integer', 'P', 'Cells arrangement', 'Cells in parallel').P = p
        self.part.addProperty(
            prop+'Length',
            'space_between_cells',
            'Cells arrangement',
            'Space between cells'
        ).space_between_cells = self.space_between_cells
        
        # Default value, will change when we set the number of cells, the space between the cells, etc...
        self.part.addProperty(prop+'Length', 'total_nickel_strip_length', "Connections", "Total nickel strip length").total_nickel_strip_length = 32.0
        self.part.addProperty(prop+'String', 'cell', 'Cell', 'Model of Cell used').cell = self.model.text()
        
        
        Gui.activateView('Gui::View3DInventor', True)
        Gui.activeView().setActiveObject('part', self.part)
        App.ActiveDocument.recompute()

        # Dimensions in mm
        # For now, harcoded for 18650 cells
        radius = 9
        height = 65
        space = float(self.space_between_cells.split(" ")[0])

        for w in range(n_cells_in_width):
            placement_of_last_cell = self.create3dCell(radius, height, w, space)
            App.ActiveDocument.recompute()
        
        # Creates the nickel stripS connecting all the cells in series
        length = (n_cells_in_width*((radius*2)) ) + n_cells_in_width*(space)

        self.part.total_nickel_strip_length = 2*length # top and bottom strips
        self.create_nickel_strips(length, radius, height, placement_of_last_cell)

        Gui.SendMsgToActiveView("ViewFit")
        App.ActiveDocument.recompute()

        self.close()

    def create_nickel_strips(self, length, radius, height, placement_of_last_cell):

        top_strip = self.setup_nickel_strip("Nickel_Strip_top", length, radius, placement_of_last_cell)
        top_strip.Placement.move(App.Vector(0, 0, -NICKEL_STRIP_HEIGHT))

        bottom_strip = self.setup_nickel_strip("Nickel_Strip_bottom", length, radius, placement_of_last_cell)
        bottom_strip.Placement.move(App.Vector(0, 0, height+NICKEL_STRIP_HEIGHT))
    
    def setup_nickel_strip(self, name, length, radius, placement):
        nickel_strip = App.ActiveDocument.addObject("Part::Box",name)
        nickel_strip.ViewObject.LineColor = nickel_strip.ViewObject.PointColor = NICKEL_STRIP_LINE_POINT_COLOR
        nickel_strip.ViewObject.ShapeColor = NICKEL_STRIP_COLOR
        nickel_strip.Length = length
        nickel_strip.Width = NICKEL_STRIP_WIDTH
        nickel_strip.Height = NICKEL_STRIP_HEIGHT
        nickel_strip.Placement = placement
        nickel_strip.Placement.move(App.Vector(-(length-radius), 0, 0))
        nickel_strip.Placement.move(App.Vector(0, -radius/2, 0))
        return nickel_strip

    # s : space between each cell
    def create3dCell(self, radius, height, index, s):
        doc = App.ActiveDocument
        label = "Cell-w-"+str(index)
        cell_object = doc.addObject("Part::Cylinder","Cylinder")
        cell_object.Label = label
        
        print(label)
        cell_object.Radius = str(radius)+' mm'
        cell_object.Height = str(height)+' mm'
        
        if s < 0.0:
            print("The space between each cell should not be negative !")

        placement = App.Placement(App.Vector(float(index*radius*2)+s,0,0),App.Rotation(App.Vector(0,0,1),0))
        cell_object.Placement = placement
        
        cell_object.ViewObject.LineColor = cell_object.ViewObject.PointColor = self.cell.getLineColor()
        cell_object.ViewObject.ShapeColor = self.cell.getShapeColor()
        print(self.cell.getShapeColor())
        
        return placement
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