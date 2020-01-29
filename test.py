

import yaml

Emac = 2.12e-12

with open("network.cfg") as file:
    network_parameter_list = yaml.load(file, Loader=yaml.FullLoader)

print(network_parameter_list[1]['layer_2'])
print(len(network_parameter_list))
