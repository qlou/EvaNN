
import numpy as np
import math

class Mapping():
    def define_dataflow(dataflow, x, y):
        if dataflow == "row_stationary":
            # The Eyeriss paper defines these parameters
            ax = x
            p = y
            q = 1
            r = 4
            t = 2
            n = 1
            m = 96

        if dataflow == "output_stationary":
            ax = x
            p = y
            q = 1
            r = 2
            t = 1
            n = 2
            m = 96
        return ax, p, q, r, t, n, m

    def crossbar_computing_convolution(dataflow, w, x, y, z, crossbar_size, device_bit):
        # This computes the number of crossbars
        total_row = x*y*z
        num_of_crossbar_in_row = math.ceil(total_row/crossbar_size)
        total_column = w*device_bit
        num_of_crossbar_in_column = math.ceil(total_column/crossbar_size)
        num_of_crossbar = num_of_crossbar_in_row * num_of_crossbar_in_column
        return num_of_crossbar

    def crossbar_computing_fully_connected(dataflow, x, y, crossbar_size, device_bit):
        # This computes the number of crossbars
        total_row = x
        num_of_crossbar_in_row = math.ceil(total_row/crossbar_size)
        total_column = y*device_bit
        num_of_crossbar_in_column = math.ceil(total_column/crossbar_size)
        num_of_crossbar = num_of_crossbar_in_row * num_of_crossbar_in_column
        return num_of_crossbar


