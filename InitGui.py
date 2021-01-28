import batteryPackUtils as bp
class BatteryPackWorkbench (Workbench):
    
    MenuText = "Battery Pack Workbench"
    ToolTip = "A description of Battery Pack Workbench"
    Icon =FreeCAD.getUserAppDataDir()+"Mod/battery_pack/logo.svg"

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        #import MyModuleA, MyModuleB # import here all the needed files that create your FreeCAD commands
        self.list = ["Battery Pack command"] # A list of command names created in the line above
        self.appendToolbar("My Commands",self.list) # creates a new toolbar with your commands
        self.appendMenu("Batter Pack",self.list) # creates a new menu
        self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu

    def Activated(self):
        """This function is executed when the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands",self.list) # add commands to the context menu

    def GetClassName(self): 
        # This function is mandatory if this is a full python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(BatteryPackWorkbench())

# Contains all the battery packs (python object) created by the user
battery_packs = []

'''
    FreeCAD commands are the basic building block of the FreeCAD interface.
    They can appear as a button on toolbars, and as a menu entry in menus.
    But it is the same command. A command is a simple python class,
    that must contain a couple of predefined attributes and functions,
    that define the name of the command, its icon, and what to do when the command is activated.
'''

class Command_Class():
    def getIcon(self, icon_name):
        return FreeCAD.getUserAppDataDir()+"Mod/battery_pack/"+icon_name+".svg"

    def GetResources(self):
        return {'Pixmap'  : self.getIcon("new_pack"), # the name of a svg file available in the resources
                'Accel' : "Shift+N", # a default shortcut (optional)
                'MenuText': "New battery pack",
                'ToolTip' : "New battery pack"}

    def Activated(self):
        import csv
        from PySide import QtCore
        from PySide import QtGui
        import cellDialog
        

        reply = QtGui.QInputDialog.getText(None, "New battery pack","Cell Model Number (e.g. INR18650-35E)\nleave empty if you want to set values manually")
        values_manually = False
        if reply[1]: 
            if reply[0] != "":
                res = None
                with open(FreeCAD.getUserAppDataDir()+"Mod/battery_pack/identification_ref.csv", newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row['Model (Markings)'] == reply[0]:
                            res= row

                    if res != None:
                        message_str="=============================\nFound a matching Model number\n=============================\nBrand : {}\nModel (Markings) : {}\nCapacity (mAh) : {}\nDischarge A (Max) : {}\nCharging A (Max) : {}\nChemistry : {}\nColor (Wrap) : {}\nColor (Ring) : {}\nImage : {}\nData Sheet : {}\nData Sheet (Backup) : {}\nWeb : {}\nNotes : {}\n\n Use this cell ?".format(res["Brand"], res["Model (Markings)"], res["Capacity (mAh)"], res["Discharge A (Max)"], res["Charging A (Max)"], res["Chemistry"], res["Color (Wrap)"], res["Color (Ring)"], res["Image"], res["Data Sheet"], res["Data Sheet (Backup)"], res["Web"], res["Notes"])
                    
                        reply = QtGui.QMessageBox.question(None, "", message_str,
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        print("yes !")
                    if reply == QtGui.QMessageBox.No:
                        values_manually = True
            else:
                values_manually = True
        else:
            print("The user cancelled ! ")
        if values_manually:
           form = cellDialog.SetCellValues(FreeCAD.getUserAppDataDir())
           form.exec_()
           print(form.retStatus)

        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

class NewCellCommandClass():
    def getIcon(self, icon_name):
        return 

    def GetResources(self):
        return {'Pixmap'  : FreeCAD.getUserAppDataDir()+"Mod/battery_pack/new_cell.svg",
                'Accel' : "Shift+N", # a default shortcut (optional)
                'MenuText': "New Cell",
                'ToolTip' : "New Cell"}

    def Activated(self):
        import csv
        from PySide import QtCore
        from PySide import QtGui
        import cellDialog
        

        reply = QtGui.QInputDialog.getText(None, "New battery pack","Cell Model Number (e.g. INR18650-35E)\nleave empty if you want to set values manually")
        values_manually = False
        if reply[1]: 
            if reply[0] != "":
                res = None
                with open(FreeCAD.getUserAppDataDir()+"Mod/battery_pack/identification_ref.csv", newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row['Model (Markings)'] == reply[0]:
                            res= row

                    if res != None:
                        message_str="=============================\nFound a matching Model number\n=============================\nBrand : {}\nModel (Markings) : {}\nCapacity (mAh) : {}\nDischarge A (Max) : {}\nCharging A (Max) : {}\nChemistry : {}\nColor (Wrap) : {}\nColor (Ring) : {}\nImage : {}\nData Sheet : {}\nData Sheet (Backup) : {}\nWeb : {}\nNotes : {}\n\n Use this cell ?".format(res["Brand"], res["Model (Markings)"], res["Capacity (mAh)"], res["Discharge A (Max)"], res["Charging A (Max)"], res["Chemistry"], res["Color (Wrap)"], res["Color (Ring)"], res["Image"], res["Data Sheet"], res["Data Sheet (Backup)"], res["Web"], res["Notes"])
                    
                        reply = QtGui.QMessageBox.question(None, "", message_str,
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        print("yes !")
                    if reply == QtGui.QMessageBox.No:
                        values_manually = True
            else:
                values_manually = True
        else:
            print("The user cancelled ! ")
        if values_manually:
           form = cellDialog.SetCellValues(FreeCAD.getUserAppDataDir())
           form.exec_()
           print(form.retStatus)

        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand('Battery Pack command',Command_Class())
FreeCADGui.addCommand('New Cell command',NewCellCommandClass())