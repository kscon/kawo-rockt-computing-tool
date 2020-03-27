# This file is used to read the "CONFIG.txt" file and set its options.

def read_config():
    Options_list = {}
    print("##### OPTIONS: #####")
    try:
        with open("CONFIG.txt", 'r') as configfile:
            for line in configfile:
                if line[0] == '#':
                    continue

                line_string = line.lower()
                line_string = line_string.replace(" ", "")

                if line_string[0:7] == "verbose":
                    if line_string[8] == '1':
                        Options_list['verbose'] = 1
                        print("Verbose mode active")
                    else:
                        print("Verbose mode inactive")
                elif line_string[0:10] == 'datainput':
                    inputfilename = line_string[11:]
                    Options_list.update(datainput=inputfilename)

                else:
                    continue
        return Options_list

    except FileNotFoundError:
        print('Warning: No configuration file "CONFIG.txt" found. Default values are used (This can lead to'
              'undesired behaviour!')
        return Options_list