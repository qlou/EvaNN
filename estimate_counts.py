
import numpy as np
import os, subprocess, tempfile
import yaml
from cacti_wrapper import CactiWrapper

def f_energy_model_crossbar(n, ADC_bits, device, crossbar_size):

    if device != "ReRAM" and device != "FeFET":
        raise ValueError("The device type is not supported!")
    # The ReRAM data is from Zhao, Meiran, et al. 2017 IEEE International Electron Devices Meeting (IEDM). IEEE, 2017.
    if device == "ReRAM":
        # These are the unit energy
        E_mux = 6.628e-16 # (J) Assume 1T1R here
        E_decoder = 1.0602e-13 #(J)
        E_array = 2.18352174e-15 #(J)
        # E_ADC = 
        energy_per_crossbar = 0.016384*1e-9

    # The FeFET data is from Ni, Kai, et al. 2019 Symposium on VLSI Technology. IEEE, 2019.
    if device == "FeFET":
        energy_per_crossbar = 0.02048*1e-9

    # Use a reference to scale the ADC design, the reference is obtained from
    P_ref = 20e-6
    f_ref = 40e6
    ADC_bits_ref = 8.9

    ADC_energy = P_ref * 1/f_ref *4**(ADC_bits-ADC_bits_ref)

    total_energy = energy_per_crossbar*n + ADC_energy*crossbar_size*n
    return total_energy

def f_energy_model(Zrate, x, y, z, u, v, w, k, bs, ax, p, q, r, t, n, m):

    nzr = 1-Zrate

    numV = 9
    e = np.zeros((numV, 1))
    vol_res = np.zeros((numV, 1))

    # print(vol_res.shape)

    with open("hardware.cfg") as file:
        hardware_parameter_list = yaml.load(file, Loader = yaml.FullLoader)


    # temp_output = tempfile.mkstemp()[0]
    # subprocess.call(exec_list)
    # temp_dir = tempfile.gettempdir()
    """
    script_path = 'cacti/cacti_temp.sh'
    cacti_run = open("cacti/cacti_temp.sh","w")
    cacti_run.write("chmod +x cacti/cacti_temp.sh\n")
    cacti_run.write("./cacti -infile L0_mem.cfg > L0_mem_results.txt")
    cacti_run.close()
    print('Running Cacti ... ')
    os.system('sh cacti/cacti_temp.sh')
    """
    # L0_size = hardware_parameter_list['L0_MEM_Size']
    # L1_size = hardware_parameter_list['L1_MEM_Size']
    cacti = CactiWrapper("L0")
    cacti = CactiWrapper("L1")
    cacti_exec_dir = './'
    if os.path.isfile(cacti_exec_dir + 'tmp_output.txt'):
        os.remove(cacti_exec_dir + 'tmp_output.txt')
    temp_output =  tempfile.mkstemp()[0]
    # call cacti executable to evaluate energy consumption
    cacti_exec_path = cacti_exec_dir + 'cacti'
    exec_list = [cacti_exec_path, '-infile', 'L0_mem.cfg']
    # print(exec_list)
    # print(temp_output)
    # ret = subprocess.run(exec_list, stdout=temp_output)
    ret = subprocess.run(exec_list, stdout=subprocess.PIPE)
    # print(ret.stdout)

    with open("111111.txt", "wb") as cacti_result:
        cacti_result.write(ret.stdout)

    with open("111111.txt", "r") as file:
        for line in file:
            if 'Total dynamic read energy per access' in line:
                # print(line)
                line = line.split(":")
                L0_unit_read_energy = float(line[1])
            if 'Total dynamic write energy per access' in line:
                line = line.split(":")
                L0_unit_write_energy = float(line[1])

    exec_list = [cacti_exec_path, '-infile', 'L1_mem.cfg']
    ret = subprocess.run(exec_list, stdout=subprocess.PIPE)

    with open("222222.txt", "wb") as cacti_result:
        cacti_result.write(ret.stdout)

    with open("222222.txt", "r") as file:
        for line in file:
            if 'Total dynamic read energy per access' in line:
                # print(line)
                line = line.split(":")
                L0_unit_read_energy = float(line[1])
            if 'Total dynamic write energy per access' in line:
                line = line.split(":")
                L0_unit_write_energy = float(line[1])


    # print(unit_write_energy, unit_read_energy)

    # flag = subprocess.call('sh cacti/cacti_temp.sh')
    # subprocess.call('cacti/cacti -infile cache.cfg')
    # if flag !=0:
    #    error("Cacti failed!")
    """
    f = open(script_path, 'a+')
    if len(f.readlines()) > 1000:
        print('WARN:  CACTI Plug-in... temp logs at: ', script_path, 'exceeds 1000 lines, delete file and create new one')
        os.remove(script_path)
        f = open(script_path, 'a+')
    f.write('\n ------------------------- \n')
    # f.write('Original Request: \n ' + str(original_request) + '\n')
    f.write(str())
    for i in exec_list:
        f.write(i + ' ')
    f.close()
    os.chmod(script_path, 0o775)
    subprocess.call(exec_list, stdout=temp_output)
    """

    # temp_output = tempfile.mkstemp()[0]
    # subprocess.call(exec_list, stdout=temp_output)
    # The e[0] is the MAC computation
    # The e[1] to e[3] represents the 
    e[0] = 1
    # e[1] = 0.62*np.sqrt(hardware_parameter_list['L0_MEM_Size'])/2.12
    e[1] = L0_unit_read_energy
    e[2] = 7.73/2.12
    # e[3] = 0.62*np.sqrt(hardware_parameter_list['L1_MEM_Size'])/2.12
    e[3] = L0_unit_write_energy
    e[4] = 0.62/2.12
    e[5] = 6*e[0]
    e[6] = 9*e[1]
    e[7] = 6*e[0]
    e[8] = 9*e[1]
    
    vol_res[0] = 1
    vol_res[1] = u*v*w*bs
    vol_res[2] = u*v*p*t*bs
    vol_res[3] = 1*min(v, ax)*p*t*bs
    vol_res[4] = 1*min(v, ax)*p*t*bs
    vol_res[5] = u*v*w*bs
    vol_res[6] = u*v*p*t*bs
    vol_res[7] = 1*min(v, ax)*p*t*bs
    vol_res[8] = 1*min(v, ax)*p*t*bs

    bfu = vol_res*k*k*q*r

    vol_op = vol_res
    vol_op[1] = x*y*q*r*bs
    vol_op[2] = k*k*q*r*p*t

    vol_op[5] = x*y*q*r*bs
    vol_op[6] = k*k*q*r*p*t

    vol_in = vol_op
    vol_in[4] = bfu[4]*nzr

    aui = vol_in
    aui[1] = aui[1] * k*t
    aui[2] = aui[2] * ax
    aui[5] = aui[5] * nzr
    aui[6] = aui[6] * nzr

    vol_out = vol_op
    vol_out[1] = bfu[1]
    vol_out[2] = bfu[2]
    vol_out[3] = bfu[3]

    auo = vol_out;
    auo[2] = auo[2] * nzr
    auo[3] = auo[3] * nzr
    auo[8] = auo[8] * nzr

    alpha = auo / bfu
    alpha[0] = nzr

    ru = aui / auo
    ru[0] = 0

    nmac = bs*u*v*w*k*k*z
    # vE = nmac*(ru+1)*alpha*e
    vE = nmac*(ru+1)*alpha
    return vE
    
