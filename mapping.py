
class Mapping():
    def define_dataflow(dataflow, x, y):
        if dataflow == "row_stationary":
            ax = x
            p = y
            q = 1
            r = 1
            t = 1
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

        if dataflow == "crossbar":
            print("needs to be implemented")
            quit()

        return ax, p, q, r, t, n, m
