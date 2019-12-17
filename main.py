
# This is the script that estimate the energy for the DNN architecture

import numpy as np
import yaml
from estimate_counts import *


def main():

    # Unit energy for MAC operation
    Emac = 2.12e-12

    with open("parameters.cfg") as file:
        p_list = yaml.load(file, Loader=yaml.FullLoader)

    # print(p_list)
    # print(p_list['X'])
    # Layer info of workload
    Zrate = p_list['zero_rate']
    # Input feature map
    x = p_list['in_X']
    y = p_list['in_Y']
    z = p_list['in_channel']

    # Output feature map
    u = p_list['out_X']
    v = p_list['out_Y']
    w = p_list['out_channel']

    k = p_list['kernel'] # Kernel size
    bs = p_list['batch_size'] # Batch size is 4
    dataflow = p_list['Dataflow']

    # Mapping information for the architeture
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
        # This to be done

    vE = f_energy_model(Zrate, x, y, z, u, v, w, k, bs, ax, p, q, r, t, n, m)
    
    vE = vE * Emac

    print('The energy for FU is ', np.sum(vE[0]), 'J')
    print("The energy for L0 memory is ", np.sum(vE[1:4]), "J")
    print("The energy for L1 memory is ", np.sum(vE[5:8]), "J")
    print("The total energy is ", np.sum(vE), "J")
if __name__=="__main__":
    main()
