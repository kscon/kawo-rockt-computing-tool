# This file is used to read the "CONFIG.txt" file and set its options.

def read_config():
    Options_list = {'verbose': 1, 'datainput': '', 'logging': 0,
                    'mtod': 1, 'visualize': 1, 'mntt': 1, 'mad': 1,
                    'heuristic': 0, 'pdw': 0, 'madw': 1, 'mnttw': 2}
    print("##### OPTIONS: #####")
    try:
        with open("CONFIG.txt", 'r') as configfile:
            for line in configfile:
                if line[0] == '#':
                    continue

                line_string = line.lower()
                line_string = line_string.replace(" ", "")

                flag = 0

                line_list = line_string.strip().split('=')

                if line_string[0:7] == "verbose":
                    if line_string[8] == '0':
                        Options_list.update(verbose=0)
                        print("Verbose level set to no output")
                    elif line_string[8] == '1':
                        Options_list.update(verbose=1)
                        print("Verbose level set to important output")
                    elif line_string[8] == '2':
                        Options_list.update(verbose=2)
                        print("Verbose level set to all output")
                    else:
                        flag = 1

                elif line_string[0:9] == 'datainput':
                    inputfilename = line_string[10:]
                    inputfilename = inputfilename[:-1]
                    Options_list.update(datainput=inputfilename)

                elif line_string[0:7] == "logging":
                    if line_string[8] == '0':
                        Options_list.update(logging=0)
                        print("Logging level set to no output")
                    elif line_string[8] == '1':
                        Options_list.update(logging=1)
                        print("Logging level set to important output")
                    elif line_string[8] == '2':
                        Options_list.update(logging=2)
                        print("Logging level set to all output")
                    else:
                        flag = 1

                elif line_list[0] == 'morethanonedorm':
                    if line_list[1] == '0':
                        Options_list.update(mtod=0)
                        print("More than one dorm option inactive")
                    elif line_list[1] == '1':
                        Options_list.update(mtod=1)
                        print("More than one dorm option active")
                    else:
                        flag = 1

                elif line_list[0] == 'visualize':
                    if line_list[1] == '0':
                        Options_list.update(visualize=0)
                        print("Visualization inactive")
                    elif line_list[1] == '1':
                        Options_list.update(visualize=1)
                        print("Visualization active")
                    else:
                        flag = 1

                elif line_list[0] == 'meetnoteamtwice':
                    if line_list[1] == '0':
                        Options_list.update(mntt=0)
                        print("Meet no team twice option inactive")
                    elif line_list[1] == '1':
                        Options_list.update(mntt=1)
                        print("Meet no team twice option active")
                    else:
                        flag = 1

                elif line_list[0] == 'meetalldorms':
                    if line_list[1] == '0':
                        Options_list.update(mad=0)
                        print("Meet all dorms option inactive")
                    elif line_list[1] == '1':
                        Options_list.update(mad=1)
                        print("Meet all dorms option active")
                    else:
                        flag = 1

                elif line_list[0] == 'heuristicsolution':
                    if line_list[1] == '0':
                        Options_list.update(heuristic=0)
                        print("Heuristic solution finding inactive")
                    elif line_list[1] == '1':
                        Options_list.update(heuristic=1)
                        print("Heuristic solution finding active")
                    else:
                        flag = 1

                elif line_list[0] == 'preferreddishweight':
                    if line_list[1] == '0':
                        Options_list.update(pdw=0)
                        print("Priority of preferred dish optimization set to 0")
                    elif line_list[1] == '1':
                        Options_list.update(pdw=1)
                        print("Priority of preferred dish optimization set to 1")
                    elif line_list[1] == '2':
                        Options_list.update(pdw=2)
                        print("Priority of preferred dish optimization set to 2")
                    else:
                        flag = 1

                elif line_list[0] == 'meetalldormsweight':
                    if line_list[1] == '0':
                        Options_list.update(madw=0)
                        print("Priority of meet all dorms optimization set to 0")
                    elif line_list[1] == '1':
                        Options_list.update(madw=1)
                        print("Priority of meet all dorms optimization set to 1")
                    elif line_list[1] == '2':
                        Options_list.update(madw=2)
                        print("Priority of meet all dorms optimization set to 2")
                    else:
                        flag = 1

                elif line_list[0] == 'meetnoteamtwiceweight':
                    if line_list[1] == '0':
                        Options_list.update(mnttw=0)
                        print("Priority of meet no team twice optimization set to 0")
                    elif line_list[1] == '1':
                        Options_list.update(mnttw=1)
                        print("Priority of meet no team twice optimization set to 1")
                    elif line_list[1] == '2':
                        Options_list.update(mnttw=2)
                        print("Priority of meet no team twice optimization set to 2")
                    else:
                        flag = 1

                assert (flag == 0)

        print("##### End of Options #####")
        return Options_list

    except FileNotFoundError:
        print('Warning: No configuration file "CONFIG.txt" found. Default values are used ')
        return Options_list
