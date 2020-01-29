
# This is the script that estimate the energy for the DNN architecture

import numpy as np
import yaml
from estimate_counts import *
from decimal import Decimal
from mapping import Mapping

def main():

    # Unit energy for MAC operation
    # Emac = 2.12e-12

    with open("hardware.cfg") as file:
        hardware_parameter_list = yaml.load(file, Loader=yaml.FullLoader)
    with open("network.cfg") as file:
        network_parameter_list = yaml.load(file, Loader=yaml.FullLoader)

    if hardware_parameter_list['tech_node'] == 65:
        Emac = 2.12e-12
    # The initialization
    FU = 0
    L0 = 0
    L1 = 0

    E_FU = 0
    E_L0 = 0
    E_L1 = 0
    
    print(hardware_parameter_list)

    report_activity_counts = hardware_parameter_list['Report_activity_counts']

    for i in range(0,len(network_parameter_list)):
        if network_parameter_list[i]['type'] == 'convolution':
            # Layer info of workload
            Zrate = network_parameter_list[i]['zero_rate']
            # Input feature map
            x = network_parameter_list[i]['in_X']
            y = network_parameter_list[i]['in_Y']
            z = network_parameter_list[i]['in_channel']

            # Output feature map
            u = network_parameter_list[i]['out_X']
            v = network_parameter_list[i]['out_Y']
            w = network_parameter_list[i]['out_channel']

            k = network_parameter_list[i]['kernel'] # Kernel size
            bs = network_parameter_list[i]['batch_size'] # Batch size is 4
            dataflow = hardware_parameter_list['Dataflow']

            # Mapping information for the architeture
            ax, p, q, r, t, n, m = Mapping.define_dataflow(dataflow, x, y)
    
            vE = f_energy_model(Zrate, x, y, z, u, v, w, k, bs, ax, p, q, r, t, n, m)
    
            # vE = vE * Emac

            FU = FU + np.sum(vE[0])
            L0 = L0 + np.sum(vE[1:4])
            L1 = L1 + np.sum(vE[5:8])

            vE = vE * Emac

            E_FU = E_FU + np.sum(vE[0])
            E_L0 = E_L0 + np.sum(vE[1:4])
            E_L1 = E_L1 + np.sum(vE[5:8])

    # This part print the number of activity counts
    if report_activity_counts == True:
        FU = Decimal(str(FU))
        print("The number of computation is ", '{:.2e}'.format(FU))
        L0 = Decimal(str(L0))

        print("The number of L0 memory read and write is ", '{:.2e}'.format(L0))
        L1 = Decimal(str(L1))
        print("The number of L1 memory read and write is ", '{:.2e}'.format(L1))
        # total = Decimal(str(FU+L0+L1))
        # print("The total energy is ", '{:.2e}'.format(total), "J")
    
    E_FU = Decimal(str(E_FU))
    print("The energy of computation is ", '{:.2e}'.format(E_FU), "J")
    E_L0 = Decimal(str(E_L0))

    print("The energy of L0 memory read and write is ", '{:.2e}'.format(E_L0), "J")
    E_L1 = Decimal(str(E_L1))
    print("The energy of L1 memory read and write is ", '{:.2e}'.format(E_L1), "J")
    E_total = Decimal(str(E_FU+E_L0+E_L1))
    print("The total energy is ", '{:.2e}'.format(E_total), "J")

    # This part saves these results to a txt file
    f = open("energy_estimation_results.txt","w+")
    f.write("The energy for computation is '{:.2e}'.format(E_FU) J")
    
    f.write("The energy for L0 memory read and write is '{:.2e}'.format(E_L0) J")

    f.write("The energy for L1 memory read and write is '{:.2e}'.format(E_L1), J")
    f.write("The total energy is '{:.2e}'.format(E_total), J")
    f.close()
    print("Results saved to energy_estimation_results.txt")

if __name__=="__main__":
    main()
