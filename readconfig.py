# This file is used to read the "CONFIG.txt" file and set its options.

def read_config():
    Options_list = {'writeoutput': 1, 'datainput': '', 'visualize': 1, 'heuristic': 0, 'pdw': 0, 'madw': 1, 'mnttw': 2}
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

                if line_list[0] == "writeoutput":
                    if line_list[1] == '0':
                        Options_list.update(writeoutput=0)
                        print("Output is not written")
                    elif line_list[8] == '1':
                        Options_list.update(writeoutput=1)
                        print("Output is written")
                    else:
                        flag = 1

                elif line_string[0:9] == 'datainput':
                    inputfilename = line_string[10:]
                    inputfilename = inputfilename[:-1]
                    Options_list.update(datainput=inputfilename)

                elif line_list[0] == 'visualize':
                    if line_list[1] == '0':
                        Options_list.update(visualize=0)
                        print("Visualization inactive")
                    elif line_list[1] == '1':
                        Options_list.update(visualize=1)
                        print("Visualization active")
                    else:
                        flag = 1

                elif line_list[0] == 'fastersolution':
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
