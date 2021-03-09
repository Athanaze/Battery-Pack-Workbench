from PySide import QtGui, QtCore
import sys, random
import matplotlib.pyplot as plt
import matplotlib
from preferences import *
import numpy as np

class ShowChart(QtGui.QDialog):

    def __init__(self, fdir, selectedObjects):
        super(ShowChart, self).__init__()
        
        self.freecad_dir = fdir
        self.selectedObjects = selectedObjects
        self.initUI()
        
    def initUI(self):
        # For now, just take the first object in in the list of selected objects
        #p = self.selectedObjects[0]
        #self.weight_pie(p)

        self.compare_packs()
        

    def compare_packs(self):
        fig = plt.figure()
        
        packs_name = []

        packs_weight = []
        packs_total_battery_holders_weight = []

        packs_total_cells_price = []
        packs_total_nickel_strip_price = []
        
        X = np.arange(2)

        for p in self.selectedObjects:
            packs_name.append(p.Label)

            packs_weight.append(p.total_weight)
            packs_total_battery_holders_weight.append(p.total_battery_holders_weight)
            
            packs_total_cells_price.append(p.total_cells_price)
            packs_total_nickel_strip_price.append(p.total_nickel_strip_price)

        ax = fig.add_axes(COMPARISON_PLOT_DIMENSIONS)

        ax.bar(
                X,
                packs_weight,
                color = WEIGHT_PLOT_BATTERY_PACK,
                width = BAR_WIDTH
        )

        ax.bar(
            X + BAR_WIDTH,
            packs_total_battery_holders_weight,
            color = WEIGHT_PLOT_BATTERY_HOLDERS_COLOR,
            width = BAR_WIDTH
        )
        
        ax.bar(
            X + (BAR_WIDTH*2),
            packs_total_cells_price,
            color = PRICE_PLOT_CELLS_PRICE,
            width = BAR_WIDTH
        )

        ax.bar(
            X + (BAR_WIDTH*2),
            packs_total_nickel_strip_price,
            color = PRICE_PLOT_NICKEL_STRIP_PRICE,
            width = BAR_WIDTH
        )
        
        ax.bar(packs_name,packs_weight)
        plt.show()

    # Show a weight pie plot for the given part (p)
    def weight_pie(self, p):
        colors = [
            WEIGHT_PLOT_NICKEL_STRIP_COLOR,
            WEIGHT_PLOT_CELL_COLOR,
            WEIGHT_PLOT_BATTERY_HOLDERS_COLOR
        ]
        fig1, ax1 = plt.subplots()

        weights = [
            p.total_nickel_strip_weight,
            p.total_cells_weight,
            p.total_battery_holders_weight
        ]
        
        ax1.pie(
            weights,
            colors=colors,
            startangle=PIE_START_ANGLE,
            radius=PIE_RADIUS,
            autopct=PIE_PERCENT_PRECISION,
            pctdistance=PIE_PERCENT_DIST
        )
        labels = ['Nickel strip', 'Cells', 'Battery holders']
        
        handles = []
        for i, l in enumerate(labels):
            handles.append(
                matplotlib.patches.Patch(color=colors[i], label=l)
                )
        
        ax1.legend(
            handles,
            labels=['%s : %1.1f g' % (l, s) for l, s in zip(labels, weights)],
            loc=PIE_LEGEND_LOCATION
        )

        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.axis('equal')
        plt.show()

    def exitButtonClicked(self):
        self.close()
    