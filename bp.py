# Represents a battery pack

class Bp():

    def __init__(n_cells_in_series, n_cells_in_para, cell):
        self.s = n_cells_in_series
        self.p = n_cells_in_para
        self.cell = cell


class Cell():
    
    # all args are str except the price and the weight which are floating point number
    
    def __init__(brand, model, capacity, price, weight, notes, color):
        self.brand = brand
        self.model = model
        self.capacity = capacity
        self.price = price
        self.weight = weight
        self.notes = notes
        self.color = color
    