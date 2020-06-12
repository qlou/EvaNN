
import yaml

class CactiWrapper:
    def CactiWrapper():
        # Copy all the configurations into the Cacti configuration files
        
        with open("hardware.cfg") as file:
            hardware_parameter_list = yaml.load(file, Loader=yaml.FullLoader)
            print(hardware_parameter_list)
        with open("network.cfg") as file:
            network_parameter_list = yaml.load(file, Loader=yaml.FullLoader)

        ### Generate L0 memory
        L0_size = hardware_parameter_list['L0_MEM_Size']
        config_file = open("cacti/L0_mem.cfg","w+")
        config_file.write("# Cache size\n")
        config_file.write("-size (bytes) " + str(L0_size) +"\n")
        # Identify power gating
        config_file.write("# power gating\n")
        config_file.write("-Array Power Gating - \"false\"\n")
        config_file.write("-WL Power Gating - \"false\"\n")
        config_file.write("-CL Power Gating - \"false\"\n")
        config_file.write("-Bitline floating - \"false\"\n")
        config_file.write("-Interconnect Power Gating - \"false\"\n")
        config_file.write("-Power Gating Performance Loss 0.01\n")
        config_file.write("\n")

        # Identify line size
        config_file.write("-block size (bytes) 8 \n")
        config_file.write("\n")

        # Model associativity, can select from 2, 4, 8, etc.
        config_file.write("-associativity 0 \n")
        config_file.write("\n")

        # Different port
        config_file.write("-read-write port 1\n")
        config_file.write("-exclusive read port 0\n")
        config_file.write("-exclusive write port 0\n")
        config_file.write("-single ended read ports 0\n")
        config_file.write("-UCA bank count 1\n")
        config_file.write("\n")

        # Technology node
        technology_node = hardware_parameter_list["tech_node"]*0.001
        config_file.write("-technology (u) "+ str(technology_node) +"\n")

        # Data array cell type, select from "itrs-hp", "itrs-lstp", "itrs-lop"
        config_file.write("-Data array cell type - \"itrs-hp\"\n")
        # Following parameters can be "itrs-hp", "itrs-lstp", "itrs-lop"
        config_file.write("-Data array peripheral type - \"itrs-hp\"\n")
        # Following parameters can be values of (itrs-hp, itrs-lstp, itrs-lop, lp-dram, comm-dram)
        config_file.write("-Tag array cell type - \"itrs-hp\"\n")
        # Following parameters can be one of three values -- (itrs-hp, itrs-lstp, itrs-lop)
        config_file.write("-Tag array peripheral type - \"itrs-hp\"\n")

        # Bus width, could range from 16 to 512
        config_file.write("-output/input bus width 512\n")
        # 300 - 400 in step of 10
        config_file.write("-operating temperature (K) 360\n")

        # Identify type of memory
        # Type of memory - cache (with a tag array) or "ram" (scratch ram similar to a register file)
        # or main memory (no tag array and every access will happen at a page granularity Ref: CACTI 5.3 report)
        config_file.write("-cache type \"cache\"\n")

        # to model special structure like branch target buffers, directory, etc. 
        # change the tag size parameter
        # if you want cacti to calculate the tagbits, set the tag size to "default", could also be 22
        config_file.write("-tag size (b) \"default\"\n")

        # fast - data and tag access happen in parallel
        # sequential - data array is accessed after accessing the tag array
        # normal - data array lookup and tag access happen in parallel
        #          final data block is broadcasted in data array h-tree 
        #          after getting the signal from the tag array
        config_file.write("-access mode (normal, sequential, fast) - \"fast\"\n")

        # Design objective for UCA (or banks in NUCA)
        config_file.write("-design objective (weight delay, dynamic power, leakage power, cycle time, area) 0:0:0:100:0\n")

        
        # Percentage deviation from the minimum value 
        # Ex: A deviation value of 10:1000:1000:1000:1000 will try to find an organization
        # that compromises at most 10% delay. 
        # NOTE: Try reasonable values for % deviation. Inconsistent deviation
        # percentage values will not produce any valid organizations. For example,
        # 0:0:100:100:100 will try to identify an organization that has both
        # least delay and dynamic power. Since such an organization is not possible, CACTI will
        # throw an error. Refer CACTI-6 Technical report for more details
        config_file.write()

        config_file.close()
"""





-deviate (delay, dynamic power, leakage power, cycle time, area) 20:100000:100000:100000:100000

# Objective for NUCA
-NUCAdesign objective (weight delay, dynamic power, leakage power, cycle time, area) 100:100:0:0:100
-NUCAdeviate (delay, dynamic power, leakage power, cycle time, area) 10:10000:10000:10000:10000

# Set optimize tag to ED or ED^2 to obtain a cache configuration optimized for
# energy-delay or energy-delay sq. product
# Note: Optimize tag will disable weight or deviate values mentioned above
# Set it to NONE to let weight and deviate values determine the 
# appropriate cache configuration
//-Optimize ED or ED^2 (ED, ED^2, NONE): "ED"
-Optimize ED or ED^2 (ED, ED^2, NONE): "ED^2"
//-Optimize ED or ED^2 (ED, ED^2, NONE): "NONE"

-Cache model (NUCA, UCA)  - "UCA"
//-Cache model (NUCA, UCA)  - "NUCA"

# In order for CACTI to find the optimal NUCA bank value the following
# variable should be assigned 0.
-NUCA bank count 0

# NOTE: for nuca network frequency is set to a default value of 
# 5GHz in time.c. CACTI automatically
# calculates the maximum possible frequency and downgrades this value if necessary

# By default CACTI considers both full-swing and low-swing 
# wires to find an optimal configuration. However, it is possible to 
# restrict the search space by changing the signaling from "default" to 
# "fullswing" or "lowswing" type.
-Wire signaling (fullswing, lowswing, default) - "Global_30"
//-Wire signaling (fullswing, lowswing, default) - "default"
//-Wire signaling (fullswing, lowswing, default) - "lowswing"

//-Wire inside mat - "global"
-Wire inside mat - "semi-global"
//-Wire outside mat - "global"
-Wire outside mat - "semi-global"

-Interconnect projection - "conservative"
//-Interconnect projection - "aggressive"

# Contention in network (which is a function of core count and cache level) is one of
# the critical factor used for deciding the optimal bank count value
# core count can be 4, 8, or 16
//-Core count 4
-Core count 8
//-Core count 16
-Cache level (L2/L3) - "L3"

-Add ECC - "true"

//-Print level (DETAILED, CONCISE) - "CONCISE"
-Print level (DETAILED, CONCISE) - "DETAILED"

# for debugging
-Print input parameters - "true"
//-Print input parameters - "false"
# force CACTI to model the cache with the 
# following Ndbl, Ndwl, Nspd, Ndsam,
# and Ndcm values
//-Force cache config - "true"
-Force cache config - "false"
-Ndwl 1
-Ndbl 1
-Nspd 0
-Ndcm 1
-Ndsam1 0
-Ndsam2 0



#### Default CONFIGURATION values for baseline external IO parameters to DRAM. More details can be found in the CACTI-IO technical report (), especially Chapters 2 and 3.

# Memory Type (D3=DDR3, D4=DDR4, L=LPDDR2, W=WideIO, S=Serial). Additional memory types can be defined by the user in extio_technology.cc, along with their technology and configuration parameters.

-dram_type "DDR3"
//-dram_type "DDR4"
//-dram_type "LPDDR2"
//-dram_type "WideIO"
//-dram_type "Serial"

# Memory State (R=Read, W=Write, I=Idle  or S=Sleep) 

//-io state  "READ"
-io state "WRITE"
//-io state "IDLE"
//-io state "SLEEP"

#Address bus timing. To alleviate the timing on the command and address bus due to high loading (shared across all memories on the channel), the interface allows for multi-cycle timing options. 

//-addr_timing 0.5 //DDR
-addr_timing 1.0 //SDR (half of DQ rate)
//-addr_timing 2.0 //2T timing (One fourth of DQ rate)
//-addr_timing 3.0 // 3T timing (One sixth of DQ rate)

# Memory Density (Gbit per memory/DRAM die)

-mem_density 4 Gb //Valid values 2^n Gb

# IO frequency (MHz) (frequency of the external memory interface).

-bus_freq 800 MHz //As of current memory standards (2013), valid range 0 to 1.5 GHz for DDR3, 0 to 533 MHz for LPDDR2, 0 - 800 MHz for WideIO and 0 - 3 GHz for Low-swing differential. However this can change, and the user is free to define valid ranges based on new memory types or extending beyond existing standards for existing dram types.

# Duty Cycle (fraction of time in the Memory State defined above)

-duty_cycle 1.0 //Valid range 0 to 1.0

# Activity factor for Data (0->1 transitions) per cycle (for DDR, need to account for the higher activity in this parameter. E.g. max. activity factor for DDR is 1.0, for SDR is 0.5)
 
-activity_dq 1.0 //Valid range 0 to 1.0 for DDR, 0 to 0.5 for SDR

# Activity factor for Control/Address (0->1 transitions) per cycle (for DDR, need to account for the higher activity in this parameter. E.g. max. activity factor for DDR is 1.0, for SDR is 0.5)

-activity_ca 0.5 //Valid range 0 to 1.0 for DDR, 0 to 0.5 for SDR, 0 to 0.25 for 2T, and 0 to 0.17 for 3T

# Number of DQ pins 

-num_dq 72 //Number of DQ pins. Includes ECC pins.

# Number of DQS pins. DQS is a data strobe that is sent along with a small number of data-lanes so the source synchronous timing is local to these DQ bits. Typically, 1 DQS per byte (8 DQ bits) is used. The DQS is also typucally differential, just like the CLK pin. 

-num_dqs 18 //2 x differential pairs. Include ECC pins as well. Valid range 0 to 18. For x4 memories, could have 36 DQS pins.

# Number of CA pins 

-num_ca 25 //Valid range 0 to 35 pins.

# Number of CLK pins. CLK is typically a differential pair. In some cases additional CLK pairs may be used to limit the loading on the CLK pin. 

-num_clk  2 //2 x differential pair. Valid values: 0/2/4.

# Number of Physical Ranks

-num_mem_dq 2 //Number of ranks (loads on DQ and DQS) per buffer/register. If multiple LRDIMMs or buffer chips exist, the analysis for capacity and power is reported per buffer/register. 

# Width of the Memory Data Bus

-mem_data_width 8 //x4 or x8 or x16 or x32 memories. For WideIO upto x128.

# RTT Termination Resistance

-rtt_value 10000

# RON Termination Resistance

-ron_value 34

# Time of flight for DQ

-tflight_value

# Parameter related to MemCAD

# Number of BoBs: 1,2,3,4,5,6,
-num_bobs 1
    
# Memory System Capacity in GB
-capacity 80    
    
# Number of Channel per BoB: 1,2. 
-num_channels_per_bob 1 

# First Metric for ordering different design points 
-first metric "Cost"
#-first metric "Bandwidth"
#-first metric "Energy"
    
# Second Metric for ordering different design points    
#-second metric "Cost"
-second metric "Bandwidth"
#-second metric "Energy"

# Third Metric for ordering different design points 
#-third metric "Cost"
#-third metric "Bandwidth"
-third metric "Energy"  
    
    
# Possible DIMM option to consider
#-DIMM model "JUST_UDIMM"
#-DIMM model "JUST_RDIMM"
#-DIMM model "JUST_LRDIMM"
-DIMM model "ALL"

#if channels of each bob have the same configurations
#-mirror_in_bob "T"
-mirror_in_bob "F"

#if we want to see all channels/bobs/memory configurations explored 
#-verbose "T"
#-verbose "F"




        # Run Cacti to obtain an output file

        # Extract energy results from the output file
        
        wordsize_in_bytes = 64
        tech_node = 65
        tech_node = tech_node  # technology node described in nm
        cache_size = 1024
        line_size = 64
        n_banks = 1
        n_rw_ports = 1
        associativity = 1  # plain scratchpad is a direct mapped cache
        rw_ports = n_rw_ports  # assumes that all the ports in the plain scratchpad are read wrtie ports instead of exclusive ports
        if int(rw_ports) == 0:
            rw_ports = 1  # you must have at least one port

        banks = n_banks  # number of banks you want to divide your scratchpad into, default is one
        excl_read_ports = 0  # assumes no exclusive ports of any type
        excl_write_ports = 0
        single_ended_read_ports = 0
        search_ports = 0

        # following three parameters are meaningful only for main memories
        page_sz = 0
        burst_length = 8
        pre_width = 8
        output_width = int(wordsize_in_bytes) * 8

        # to model special structure like branch target buffers, directory, etc.
        # change the tag size parameter
        # if you want cacti to calculate the tagbits, set the tag size to "default"
        specific_tag = 0
        tag_width = 0
        access_mode = 2  # 0 normal, 1 seq, 2 fast
        cache = 0  # scratch ram 0 or cache 1
        main_mem = 0

        # assign weights for CACTI optimizations
        obj_func_delay = 0
        obj_func_dynamic_power = 0
        obj_func_leakage_power = 1000000
        obj_func_area = 0
        obj_func_cycle_time = 0

        # from CACTI example config...
        dev_func_delay = 20
        dev_func_dynamic_power = 10
        dev_func_leakage_power = 100000
        dev_func_area = 100
        dev_func_cycle_time = 100


        ed_ed2_none = 2  # 0 - ED, 1 - ED^2, 2 - use weight and deviate
        temp = 300
        wt = 0  # 0 - default(search across everything), 1 - global, 2 - 5%
        # delay penalty, 3 - 10%, 4 - 20 %, 5 - 30%, 6 - low-swing
        data_arr_ram_cell_tech_flavor_in = 1  # 0(itrs-hp) 1-itrs-lstp(low standby power)
        data_arr_peri_global_tech_flavor_in = 1  # 0(itrs-hp)
        tag_arr_ram_cell_tech_flavor_in = 1  # itrs-hp
        tag_arr_peri_global_tech_flavor_in = 1  # itrs-hp
        interconnect_projection_type_in = 1  # 0 - aggressive, 1 - normal
        wire_inside_mat_type_in = 1  # 2 - global, 0 - local, 1 - semi-global
        wire_outside_mat_type_in = 1  # 2 - global
        REPEATERS_IN_HTREE_SEGMENTS_in = 1  # wires with repeaters
        VERTICAL_HTREE_WIRES_OVER_THE_ARRAY_in = 0
        BROADCAST_ADDR_DATAIN_OVER_VERTICAL_HTREES_in = 0
        force_wiretype = 1
        wiretype = 30
        force_config = 0
        ndwl = 1
        ndbl = 1
        nspd = 0
        ndcm = 1
        ndsam1 = 0
        ndsam2 = 0
        ecc = 0


        cacti_exec_path = 'cacti/cacti'
        exec_list = [cacti_exec_path,
                         str(cache_size),
                         str(line_size),
                         str(associativity),
                         str(rw_ports),
                         str(excl_read_ports),
                         str(excl_write_ports),
                         str(single_ended_read_ports),
                         str(search_ports),
                         str(banks),
                         str(tech_node),
                         str(output_width),
                         str(specific_tag),
                         str(tag_width),
                         str(access_mode),
                         str(cache),
                         str(main_mem),
                         str(obj_func_delay),
                         str(obj_func_dynamic_power),
                         str(obj_func_leakage_power),
                         str(obj_func_area),
                         str(obj_func_cycle_time),
                         str(dev_func_delay),
                         str(dev_func_dynamic_power),
                         str(dev_func_leakage_power),
                         str(dev_func_area),
                         str(dev_func_cycle_time),
                         str(ed_ed2_none),
                         str(temp),
                         str(wt),
                         str(data_arr_ram_cell_tech_flavor_in),
                         str(data_arr_peri_global_tech_flavor_in),
                         str(tag_arr_ram_cell_tech_flavor_in),
                         str(tag_arr_peri_global_tech_flavor_in),
                         str(interconnect_projection_type_in),
                         str(wire_inside_mat_type_in),
                         str(wire_outside_mat_type_in),
                         str(REPEATERS_IN_HTREE_SEGMENTS_in),
                         str(VERTICAL_HTREE_WIRES_OVER_THE_ARRAY_in),
                         str(BROADCAST_ADDR_DATAIN_OVER_VERTICAL_HTREES_in),
                         str(page_sz),
                         str(burst_length),
                         str(pre_width),
                         str(force_wiretype),
                         str(wiretype),
                         str(force_config),
                         str(ndwl),
                         str(ndbl),
                         str(nspd),
                         str(ndcm),
                         str(ndsam1),
                         str(ndsam2),
                         str(ecc)]


        temp_output = tempfile.mkstemp()[0]
        # subprocess.call(exec_list)
        temp_dir = tempfile.gettempdir()
        script_path = temp_dir + '/cacti_temp.sh'
        print('CACTI plug-in... Command line input saved to: ', script_path)
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

CactiWrapper.CactiWrapper()

