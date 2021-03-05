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
        n_cells_in_height = p

        # /!\ space_between_cells must be a STRING formatted like so : '1 mm'
        self.space_between_cells = str(self.qSpinBox_space_cells.value()) + " mm"

        App.ActiveDocument.recompute()
        prop = 'App::Property'

        self.part = App.activeDocument().addObject('App::Part',BATTERY_PACK_DEFAULT_PART_LABEL)
        self.part.addProperty(prop+'Length', 'Width', 'Dimensions', 'Battery pack width').Width = '10 mm'
        self.part.addProperty(prop+'Integer', 'serie', 'Cells arrangement', 'Cells in series').serie = s
        self.part.addProperty(prop+'Integer', 'para', 'Cells arrangement', 'Cells in parallel').para = p
        self.part.addProperty(
            prop+'Length',
            'space_between_cells',
            'Cells arrangement',
            'Space between cells'
        ).space_between_cells = self.space_between_cells

        # Default value, will change when we set the number of cells, the space between the cells, etc...
        self.part.addProperty(prop+'Length', 'total_nickel_strip_length', "Connections", "Total nickel strip length").total_nickel_strip_length = 32.0
        
        self.part.addProperty(prop+'Integer', 'nc', 'Cell', 'Number of cells in the pack').nc = 0
        self.part.setExpression("nc", "serie*para")

        ### Cell ###
        self.part.addProperty(prop+'String', 'cell', 'Cell', 'Model of Cell used').cell = self.model.text()
        self.part.addProperty(prop+'Float', 'cell_price', 'Cell', 'Individual cell price').cell_price = self.cell.price
        self.part.addProperty(prop+'Float', 'cell_weight', 'Cell', 'Individual cell weight').cell_weight = self.cell.weight
        self.part.addProperty(prop+'Float', 'cell_radius', 'Cell', 'Individual cell radius').cell_radius = self.cell.radius
        self.part.addProperty(prop+'Float', 'cell_height', 'Cell', 'Individual cell height').cell_height = self.cell.height

        ### Nickel Strip ###
        self.part.addProperty(prop+'Float', 'nickel_strip_width', 'Nickel strip', 'Nickel strip width').nickel_strip_width = NICKEL_STRIP_WIDTH
        self.part.addProperty(prop+'Float', 'nickel_strip_height', 'Nickel strip', 'Nickel strip height').nickel_strip_height = NICKEL_STRIP_HEIGHT
        self.part.addProperty(prop+'Float', 'nickel_strip_weight_per_mm3', 'Nickel strip', 'Nickel strip weight per mm3').nickel_strip_weight_per_mm3 = NICKEL_STRIP_WEIGHT_PER_MM3

        ### Weight ###

        self.part.addProperty(prop+'Float', 'battery_holder_weight', 'Weight', 'Individual battery holder weight').battery_holder_weight = BATTERY_HOLDER_WEIGHT

        self.part.addProperty(prop+'Float', 'total_cells_weight', 'Weight', 'Total cells weight').total_cells_weight = 0.0
        self.part.setExpression("total_cells_weight", "cell_weight*nc")
        self.part.addProperty(prop+'Float', 'total_nickel_strip_weight', 'Weight', 'Total weight of nickel strip').total_nickel_strip_weight = 0.0
        self.part.addProperty(prop+'Float', 'total_battery_holders_weight', 'Weight', 'Total battery holders weight').total_battery_holders_weight = 0.0
        self.part.addProperty(prop+'Float', 'total_weight', 'Weight', 'Total weight of the battery pack').total_weight = 0.0
        
        ### Price ###

        self.part.addProperty(prop+'Float', 'total_cells_price', 'Price', 'Total cells price').total_cells_price = 0.0
        self.part.addProperty(prop+'Float', 'nickel_strip_price_per_mm', 'Price', 'Nickel strip price per mm').nickel_strip_price_per_mm = NICKEL_STRIP_PRICE_PER_MM
        self.part.addProperty(prop+'Float', 'total_nickel_strip_price', 'Price', 'Total nickel strip price').total_nickel_strip_price = 0.0

        Gui.activateView('Gui::View3DInventor', True)
        Gui.activeView().setActiveObject('part', self.part)
        App.ActiveDocument.recompute()

        space = float(self.space_between_cells.split(" ")[0])

        for w in range(self.part.serie):
            placement_of_last_cell = self.create3dCell(w, space)
            App.ActiveDocument.recompute()
        
        # Creates the nickel strips connecting all the cells in series
        
        # we multiply by 2 for the top and bottom strips
        self.part.setExpression("total_nickel_strip_length", "2*(  ( (serie*((cell_radius*2)) ) + serie*(space_between_cells) ) - space_between_cells )")

        self.create_nickel_strips(placement_of_last_cell)
       
        # Volume * weight per mm³
        self.part.setExpression("total_nickel_strip_weight", "total_nickel_strip_length*nickel_strip_width*nickel_strip_height*nickel_strip_weight_per_mm3")
        self.part.setExpression("total_battery_holders_weight", "battery_holder_weight*nc*2")# One holder on top, one on the bottom
        self.part.setExpression("total_weight", "total_nickel_strip_weight+total_battery_holders_weight+total_cells_weight")
        
        ### Price ###
        self.part.setExpression("total_cells_price", "cell_price*nc")
        print("L.140 !")
        self.part.setExpression("total_nickel_strip_price", "nickel_strip_price_per_mm*(total_nickel_strip_length / mm)")
        
        Gui.SendMsgToActiveView("ViewFit")
        App.ActiveDocument.recompute()

        self.close()

    def create_nickel_strips(self, placement_of_last_cell):

        top_strip = self.setup_nickel_strip("Nickel_Strip_top", placement_of_last_cell)
        top_strip.Placement.move(App.Vector(0, 0, -NICKEL_STRIP_HEIGHT))

        bottom_strip = self.setup_nickel_strip("Nickel_Strip_bottom", placement_of_last_cell)
        bottom_strip.Placement.move(App.Vector(0, 0, self.cell.height+NICKEL_STRIP_HEIGHT))
    
    def setup_nickel_strip(self, name, placement):
        nickel_strip = App.ActiveDocument.addObject("Part::Box",name)
        nickel_strip.ViewObject.LineColor = nickel_strip.ViewObject.PointColor = NICKEL_STRIP_LINE_POINT_COLOR
        nickel_strip.ViewObject.ShapeColor = NICKEL_STRIP_COLOR
        nickel_strip.Length = self.part.total_nickel_strip_length.Value / 2.0
        nickel_strip.Width = NICKEL_STRIP_WIDTH
        nickel_strip.Height = NICKEL_STRIP_HEIGHT
        nickel_strip.Placement = placement
        nickel_strip.Placement.move(App.Vector(-(nickel_strip.Length.Value-self.cell.radius), 0, 0))
        nickel_strip.Placement.move(App.Vector(0, -self.cell.radius/2, 0))
        return nickel_strip

    # s : space between each cell
    def create3dCell(self, index, s):
        doc = App.ActiveDocument
        label = "Cell-w-"+str(index)
        cell_object = doc.addObject("Part::Cylinder","Cylinder")
        cell_object.Label = label
        
        cell_object.Radius = str(self.cell.radius)+' mm'
        cell_object.Height = str(self.cell.height)+' mm'
        
        if s < 0.0:
            print("The space between each cell should not be negative !")

        placement = App.Placement(
            App.Vector(float( index*((self.cell.radius*2)+s) ),0,0),
            App.Rotation(App.Vector(0,0,1),0)
        )
        cell_object.Placement = placement
        
        cell_object.ViewObject.LineColor = cell_object.ViewObject.PointColor = self.cell.getLineColor()
        cell_object.ViewObject.ShapeColor = self.cell.getShapeColor()
        
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