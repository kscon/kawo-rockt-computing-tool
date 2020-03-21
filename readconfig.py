# This file is used to read the "config.txt" file and set its options.

def read_config():
    Options_list = {'verbose': 0}
    print("##### OPTIONS: #####")
    try:
        with open("config.txt", 'r') as configfile:
            for line in configfile:
                if line[0] == '#':
                    continue

                line_string = line.lower()
                line_string = line_string.replace(" ", "")

                if line_string[0:7] == "verbose":
                    if line_string[8] == '1':
                        Options_list['verbose'] = 1
                        print("Option for verbose output set")
                    else:
                        continue
                else:
                    continue
        return Options_list

    except FileNotFoundError:
        print('Warning: No configuration file "config.txt" found. Default values are used (This can lead to'
              'undesired behaviour!')
        return Options_list
