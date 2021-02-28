from PySide import QtGui, QtCore
import sys, random


class ShowChart(QtGui.QDialog):

    def __init__(self, fdir):
        super(ShowChart, self).__init__()
        
        self.freecad_dir = fdir
        self.initUI()
        
    def initUI(self):
        mainLayout = QtGui.QVBoxLayout()
        
        scene = QtGui.QGraphicsScene()

        families = [1,2,3,4,5,6,7,8,9,10]
        total = 0
        set_angle = 0
        count1 = 0
        colours = []
        total = sum(families)

        for count in range(len(families)):
            number = []
            for count in range(3):
                number.append(random.randrange(0, 255))
            colours.append(QtGui.QColor(number[0],number[1],number[2]))

        for family in families:
            # Max span is 5760, so we have to calculate corresponding span angle
            angle = round(float(family*5760)/total)
            ellipse = QtGui.QGraphicsEllipseItem(0,0,400,400)
            ellipse.setPos(0,0)
            ellipse.setStartAngle(set_angle)
            ellipse.setSpanAngle(angle)
            ellipse.setBrush(colours[count1])
            set_angle += angle
            count1 += 1
            scene.addItem(ellipse)

        view = QtGui.QGraphicsView(scene)
        view.show()
        '''
        view = QtWebEngine.QWebView(mainLayout)
        view.load(QtWebEngine.QUrl("https://www.chartjs.org/docs/latest/charts/doughnut.html"))
        view.show()

        mainLayout.addWidget(view)
        '''

        option1Button = QtGui.QPushButton("Exit")
        option1Button.clicked.connect(self.exitButtonClicked)
        
        mainLayout.addWidget(self.addToDbCheckBox)

        self.setLayout(mainLayout)
        # define window		xLoc,yLoc,xDim,yDim
        self.setGeometry(250, 250, 0, 50)
        self.setWindowTitle("Chart")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def exitButtonClicked(self):
        self.close()
    