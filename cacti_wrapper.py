
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
        cfg_file_content = ''
        cfg_file_content += '# Cache size\n'
        cfg_file_content += '-size (bytes) " + str(L0_size) +"\n'
        # Identify power gating
        cfg_file_content += '# power gating\n'
        cfg_file_content += '-Array Power Gating - \"false\"\n'
        cfg_file_content += '-WL Power Gating - \"false\"\n'
        cfg_file_content += '-CL Power Gating - \"false\"\n'
        cfg_file_content += '-Bitline floating - \"false\"\n'
        cfg_file_content += '-Interconnect Power Gating - \"false\"\n'
        cfg_file_content += '-Power Gating Performance Loss 0.01\n'
        cfg_file_content += '\n'

        # Identify line size
        cfg_file_content += '-block size (bytes) 8 \n'
        cfg_file_content += '\n'

        # Model associativity, can select from 2, 4, 8, etc.
        cfg_file_content += '-associativity 0 \n'
        cfg_file_content += '\n'

        # Different port
        cfg_file_content += '-read-write port 1\n'
        cfg_file_content += '-exclusive read port 0\n'
        cfg_file_content += '-exclusive write port 0\n'
        cfg_file_content += '-single ended read ports 0\n'
        cfg_file_content += '-UCA bank count 1\n'
        cfg_file_content += '\n'

        # Technology node
        technology_node = hardware_parameter_list["tech_node"]*0.001
        cfg_file_content += '-technology (u) "+ str(technology_node) +"\n'

        # Data array cell type, select from "itrs-hp", "itrs-lstp", "itrs-lop"
        cfg_file_content += '-Data array cell type - \"itrs-hp\"\n'
        # Following parameters can be "itrs-hp", "itrs-lstp", "itrs-lop"
        cfg_file_content += '-Data array peripheral type - \"itrs-hp\"\n'
        # Following parameters can be values of (itrs-hp, itrs-lstp, itrs-lop, lp-dram, comm-dram)
        cfg_file_content += '-Tag array cell type - \"itrs-hp\"\n'
        # Following parameters can be one of three values -- (itrs-hp, itrs-lstp, itrs-lop)
        cfg_file_content += '-Tag array peripheral type - \"itrs-hp\"\n'

        # Bus width, could range from 16 to 512
        cfg_file_content += '-output/input bus width 512\n'
        # 300 - 400 in step of 10
        cfg_file_content += '-operating temperature (K) 360\n'

        # Identify type of memory
        # Type of memory - cache (with a tag array) or "ram" (scratch ram similar to a register file)
        # or main memory (no tag array and every access will happen at a page granularity Ref: CACTI 5.3 report)
        cfg_file_content += '-cache type \"cache\"\n'

        # to model special structure like branch target buffers, directory, etc. 
        # change the tag size parameter
        # if you want cacti to calculate the tagbits, set the tag size to "default", could also be 22
        cfg_file_content += '-tag size (b) \"default\"\n'

        # fast - data and tag access happen in parallel
        # sequential - data array is accessed after accessing the tag array
        # normal - data array lookup and tag access happen in parallel
        #          final data block is broadcasted in data array h-tree 
        #          after getting the signal from the tag array
        cfg_file_content += '-access mode (normal, sequential, fast) - \"fast\"\n'

        # Design objective for UCA (or banks in NUCA)
        cfg_file_content += '-design objective (weight delay, dynamic power, leakage power, cycle time, area) 0:0:0:100:0\n'

        
        # Percentage deviation from the minimum value 
        # Ex: A deviation value of 10:1000:1000:1000:1000 will try to find an organization
        # that compromises at most 10% delay. 
        # NOTE: Try reasonable values for % deviation. Inconsistent deviation
        # percentage values will not produce any valid organizations. For example,
        # 0:0:100:100:100 will try to identify an organization that has both
        # least delay and dynamic power. Since such an organization is not possible, CACTI will
        # throw an error. Refer CACTI-6 Technical report for more details
        cfg_file_content += '-deviate (delay, dynamic power, leakage power, cycle time, area) 20:100000:100000:100000:100000\n'
        # Objective for NUCA
        cfg_file_content += '-NUCAdesign objective (weight delay, dynamic power, leakage power, cycle time, area) 100:100:0:0:100\n'
        cfg_file_content += '-NUCAdeviate (delay, dynamic power, leakage power, cycle time, area) 10:10000:10000:10000:10000\n'

        # Set optimize tag to ED or ED^2 to obtain a cache configuration optimized for
        # energy-delay or energy-delay sq. product
        # Note: Optimize tag will disable weight or deviate values mentioned above
        # Set it to NONE to let weight and deviate values determine the 
        # appropriate cache configuration
        # Could be selected from ED^2, ED, or NONE
        cfg_file_content += '-Optimize ED or ED^2 (ED, ED^2, NONE): \"ED^2\"\n'

        # Select from NUCA or UCA
        cfg_file_content += '-Cache model (NUCA, UCA)  - \"UCA\"\n'
        
        # In order for CACTI to find the optimal NUCA bank value the following
        # variable should be assigned 0.
        cfg_file_content += '-NUCA bank count 0\n'


        # NOTE: for nuca network frequency is set to a default value of 
        # 5GHz in time.c. CACTI automatically
        # calculates the maximum possible frequency and downgrades this value if necessary

        # By default CACTI considers both full-swing and low-swing 
        # wires to find an optimal configuration. However, it is possible to 
        # restrict the search space by changing the signaling from "default" to 
        # "fullswing" or "lowswing" type.
        # Can be "Global_30", "default", or "lowswing"
        cfg_file_content += '-Wire signaling (fullswing, lowswing, default) - "Global_30"\n'
        # Can select from global or semi-global
        cfg_file_content += '-Wire inside mat - "semi-global"\n'
        # Can select from global or semi-global
        cfg_file_content += '-Wire outside mat - "semi-global"\n'
        # can be "conservative" or "aggressive"
        cfg_file_content += '-Interconnect projection - "conservative"\n'
        # Contention in network (which is a function of core count and cache level) is one of
        # the critical factor used for deciding the optimal bank count value
        # core count can be 4, 8, or 16
        cfg_file_content += '-Core count 8\n'
        cfg_file_content += '-Cache level (L2/L3) - "L3"\n'

        cfg_file_content += '-Add ECC - "true"\n'
        # Can select from CONCISE or DETAILED
        cfg_file_content += '-Print level (DETAILED, CONCISE) - "DETAILED"\n'


        # for debugging, can also be false
        cfg_file_content += '-Print input parameters - "true"\n'

        # force CACTI to model the cache with the 
        # following Ndbl, Ndwl, Nspd, Ndsam,
        # and Ndcm values
        cfg_file_content += '-Force cache config - "false"\n'
        cfg_file_content += '-Ndwl 1\n'
        cfg_file_content += '-Ndbl 1\n'
        cfg_file_content += '-Nspd 0\n'
        cfg_file_content += '-Ndcm 1\n'
        cfg_file_content += '-Ndsam1 0\n'
        cfg_file_content += '-Ndsam2 0\n'

        #### Default CONFIGURATION values for baseline external IO parameters to DRAM. More details can be found in the CACTI-IO technical report (), especially Chapters 2 and 3.

        # Memory Type (D3=DDR3, D4=DDR4, L=LPDDR2, W=WideIO, S=Serial). Additional memory types can be defined by the user in extio_technology.cc, along with their technology and configuration parameters.

        cfg_file_content += '-dram_type "DDR3"\n'

        # Memory State (R=Read, W=Write, I=Idle  or S=Sleep) 

        cfg_file_content += '-io state "WRITE"\n'

        # Address bus timing. To alleviate the timing on the command and address bus due to high loading (shared across all memories on the channel), the interface allows for multi-cycle timing options. 
        # Can select from 0.5//DDR, 1.0//SDR, 2.0//2T, 3.0//3T

        cfg_file_content += '-addr_timing 1.0 //SDR (half of DQ rate)\n'

        # Memory Density (Gbit per memory/DRAM die)

        cfg_file_content += '-mem_density 4 Gb //Valid values 2^n Gb\n'

        # IO frequency (MHz) (frequency of the external memory interface).

        # As of current memory standards (2013), valid range 0 to 1.5 GHz for DDR3, 0 to 533 MHz for LPDDR2, 0 - 800 MHz for WideIO and 0 - 3 GHz for Low-swing differential. However this can change, and the user is free to define valid ranges based on new memory types or extending beyond existing standards for existing dram types.
        cfg_file_content += '-bus_freq 800 MHz\n'
        
        # Duty Cycle (fraction of time in the Memory State defined above)
        # Valid range 0 to 1.0
        cfg_file_content += '-duty_cycle 1.0\n'

        # Activity factor for Data (0->1 transitions) per cycle (for DDR, need to account for the higher activity in this parameter. E.g. max. activity factor for DDR is 1.0, for SDR is 0.5)
        # Valid range 0 to 1.0 for DDR, 0 to 0.5 for SDR
        cfg_file_content += '-activity_dq 1.0\n' 

        # Activity factor for Control/Address (0->1 transitions) per cycle (for DDR, need to account for the higher activity in this parameter. E.g. max. activity factor for DDR is 1.0, for SDR is 0.5)
        # Valid range 0 to 1.0 for DDR, 0 to 0.5 for SDR, 0 to 0.25 for 2T, and 0 to 0.17 for 3T
        cfg_file_content += '-activity_ca 0.5\n' 

        # Number of DQ pins 
        #Number of DQ pins. Includes ECC pins.
        cfg_file_content += '-num_dq 72\n' 

        # Number of DQS pins. DQS is a data strobe that is sent along with a small number of data-lanes so the source synchronous timing is local to these DQ bits. Typically, 1 DQS per byte (8 DQ bits) is used. The DQS is also typucally differential, just like the CLK pin. 
        # 2 x differential pairs. Include ECC pins as well. Valid range 0 to 18. For x4 memories, could have 36 DQS pins.
        cfg_file_content += '-num_dqs 18\n' 

        # Number of CA pins 
        # Valid range 0 to 35 pins.
        cfg_file_content += '-num_ca 25\n' 

        # Number of CLK pins. CLK is typically a differential pair. In some cases additional CLK pairs may be used to limit the loading on the CLK pin. 
        # 2 x differential pair. Valid values: 0/2/4.
        cfg_file_content += '-num_clk  2\n' 

        # Number of Physical Ranks
        # Number of ranks (loads on DQ and DQS) per buffer/register. If multiple LRDIMMs or buffer chips exist, the analysis for capacity and power is reported per buffer/register. 
        cfg_file_content += '-num_mem_dq 2\n' 

        # Width of the Memory Data Bus
        # x4 or x8 or x16 or x32 memories. For WideIO upto x128.
        cfg_file_content += '-mem_data_width 8\n'

        # RTT Termination Resistance

        cfg_file_content += '-rtt_value 10000\n'

        # RON Termination Resistance

        cfg_file_content += '-ron_value 34\n'

        # Time of flight for DQ

        cfg_file_content += '-tflight_value\n'

        # Parameter related to MemCAD

        # Number of BoBs: 1,2,3,4,5,6,
        cfg_file_content += '-num_bobs 1\n'
    
        # Memory System Capacity in GB
        cfg_file_content += '-capacity 80\n'
    
        # Number of Channel per BoB: 1,2. 
        cfg_file_content += '-num_channels_per_bob 1\n'

        # First Metric for ordering different design points, can be cost, bandwidth, or energy
        cfg_file_content += '-first metric "Cost"\n'
        
        # Second Metric for ordering different design points    
        cfg_file_content += '-second metric "Bandwidth"\n'

        # Third Metric for ordering different design points 
        cfg_file_content += '-third metric "Energy"\n'
    
    
        # Possible DIMM option to consider
        #-DIMM model "JUST_UDIMM"
        #-DIMM model "JUST_RDIMM"
        #-DIMM model "JUST_LRDIMM"
        cfg_file_content += '-DIMM model "ALL"\n'

        #if channels of each bob have the same configurations
        #-mirror_in_bob "T"
        cfg_file_content += '-mirror_in_bob "F"\n'

        #if we want to see all channels/bobs/memory configurations explored 
        #-verbose "T"
        #-verbose "F"
        with open('cacti/L0_mem.cfg', 'w+') as output_file:
            output_file.write(cfg_file_content)


"""

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

