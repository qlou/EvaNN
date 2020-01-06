
# This is the script that estimate the energy for the DNN architecture

import numpy as np
import yaml
from estimate_counts import *
from decimal import Decimal
from mapping import Mapping

def main():

    # Unit energy for MAC operation
    Emac = 2.12e-12

    with open("hardware.cfg") as file:
        hardware_parameter_list = yaml.load(file, Loader=yaml.FullLoader)
    with open("network.cfg") as file:
        network_parameter_list = yaml.load(file, Loader=yaml.FullLoader)
    # print(p_list)
    # print(p_list['X'])
    # Layer info of workload
    Zrate = network_parameter_list['zero_rate']
    # Input feature map
    x = network_parameter_list['in_X']
    y = network_parameter_list['in_Y']
    z = network_parameter_list['in_channel']

    # Output feature map
    u = network_parameter_list['out_X']
    v = network_parameter_list['out_Y']
    w = network_parameter_list['out_channel']

    k = network_parameter_list['kernel'] # Kernel size
    bs = network_parameter_list['batch_size'] # Batch size is 4
    dataflow = hardware_parameter_list['Dataflow']

    # Mapping information for the architeture
    ax, p, q, r, t, n, m = Mapping.define_dataflow(dataflow, x, y)
    
    vE = f_energy_model(Zrate, x, y, z, u, v, w, k, bs, ax, p, q, r, t, n, m)
    
    vE = vE * Emac


    # This part print the energy number
    FU = Decimal(str(np.sum(vE[0])))
    print("The energy for computation is ", '{:.2e}'.format(FU), "J")
    L0 = Decimal(str(np.sum(vE[1:4])))

    print("The energy for L0 memory read and write is ", '{:.2e}'.format(L0), "J")
    L1 = Decimal(str(np.sum(vE[5:8])))
    print("The energy for L1 memory read and write is ", '{:.2e}'.format(L1), "J")
    total = Decimal(str(np.sum(vE)))
    print("The total energy is ", '{:.2e}'.format(total), "J")

    # This part saves these results to a txt file
    
if __name__=="__main__":
    main()
