class Utils:
    def getIcon(self, icon_name):
            import preferences
            return FreeCAD.getUserAppDataDir()+"Mod/"+preferences.MOD_FOLDER_NAME+"/"+icon_name+".svg"

class BatteryPackWorkbench (Workbench, Utils):
    
    MenuText = "Battery Pack Workbench"
    ToolTip = "A description of Battery Pack Workbench"
    import preferences
    Icon = FreeCAD.getUserAppDataDir()+"Mod/"+preferences.MOD_FOLDER_NAME+"/logo.svg"

    # executed when FreeCAD starts
    def Initialize(self):
        import preferences
        self.list = ["Battery Pack command", "New Cell command", "Chart command"] # A list of command names created in the line above
        self.appendToolbar(preferences.MENU_TITLE,self.list) # creates a new toolbar with your commands
        self.appendMenu("Batter Pack",self.list) # creates a new menu
    
    # executed when the workbench is activated
    def Activated(self):
        return

    # executed when the workbench is deactivated
    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu(preferences.MENU_TITLE,self.list) # add commands to the context menu, "battery"

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

# New battery pack
class Command_Class(Utils):
    
    def GetResources(self):
        return {'Pixmap'  : self.getIcon("new_pack"), # the name of a svg file available in the resources
                'Accel' : "Shift+N", # a default shortcut (optional)
                'MenuText': "New battery pack",
                'ToolTip' : "New battery pack"}

    def Activated(self):
        import csv
        from PySide import QtCore
        from PySide import QtGui
        import batteryPackDialog as bpd
        
        form = bpd.BatteryPackDialog(FreeCAD.getUserAppDataDir())
        form.exec_()

        return
   
    def IsActive(self):
        return True

class NewCellCommandClass(Utils):

    def GetResources(self):
        return {'Pixmap'  : self.getIcon("new_cell"),
                'MenuText': "New Cell",
                'ToolTip' : "New Cell"}

    def Activated(self):
        import csv
        from PySide import QtCore
        from PySide import QtGui
        import cellDialog

        form = cellDialog.SetCellValues(FreeCAD.getUserAppDataDir())
        form.exec_()
        print(form.retStatus)

        return

    def IsActive(self):
        return True

class ChartCommandClass(Utils):

    def GetResources(self):
        return {'Pixmap'  : self.getIcon("chart"),
                'MenuText': "Chart",
                'ToolTip' : "Chart"}

    def Activated(self):
        from PySide import QtCore
        from PySide import QtGui
        import chartDialog

        form = chartDialog.ShowChart(FreeCAD.getUserAppDataDir(), FreeCADGui.Selection.getSelection())
        form.exec_()

        return

    def IsActive(self):
        return True

FreeCADGui.addCommand('Battery Pack command',Command_Class())
FreeCADGui.addCommand('New Cell command',NewCellCommandClass())
FreeCADGui.addCommand('Chart command',ChartCommandClass())