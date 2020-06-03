def preprocessing(teams, zimmer, speisen, vorspeise, hauptspeise, nachspeise, kawo, kawos, options):
    global opt
    opt = options
    log('\n##### PREPROCESSING #####')

    num_of_teams = number_of_teams(teams)
    log("Es gibt %i teilnehmende Teams" % (num_of_teams))

    number = check_room_conflicts_maximum(teams, zimmer)
    if number > 0:
        log("Es gibt zu viele Teams mit Zimmernummer %s" % (number))

    count_k1, count_k2, count_k3 = count_teams_kawo_origin(teams, kawo)
    log("Es gibt %i Kawo1, %i Kawo2 und %i Kawo3 Teams" % (count_k1, count_k2, count_k3))

    log('##### End of Preprocessing #####\n')

    kawo_bin = set_kawo_bin(teams, kawo, kawos)
    p = calculate_preferences(teams, speisen, vorspeise, hauptspeise, nachspeise)

    return p, kawo_bin, num_of_teams

def number_of_teams(teams):
    return len(teams)

def check_room_conflicts_maximum(teams, zimmer):
    global i
    for i in teams:
        counter = 1
        number = zimmer[i]
        for j in teams:
            if i != j and number == zimmer[j]:
                counter = counter + 1
        if counter > 3:
            return number
    return 0

def count_teams_kawo_origin(teams, kawo):
    global i
    count_k1 = 0
    count_k2 = 0
    count_k3 = 0
    for i in teams:
        if (kawo[i] == 1):
            count_k1 = count_k1 + 1
        elif (kawo[i] == 2):
            count_k2 = count_k2 + 1
        elif (kawo[i] == 3):
            count_k3 = count_k3 + 1
    return count_k1, count_k2, count_k3

def set_kawo_bin(teams, kawo, kawos):
    global i
    kawo_bin = {(i, k): 0 for i in teams for k in kawos}
    for i in teams:
        k = str(kawo[i])
        kawo_bin[i, k] = 1
    return kawo_bin

def calculate_preferences(teams, speisen, vorspeise, hauptspeise, nachspeise):
    p = {(i, s): 100 for i in teams for s in speisen}

    for i in teams:
        for s in speisen:
            if s == 'vorspeise':
                p[i, s] = 10 ** vorspeise[i]
            elif s == 'hauptspeise':
                p[i, s] = 10 ** hauptspeise[i]
            else:
                p[i, s] = 10 ** nachspeise[i]
    return p


def log(s):
    print(s)
    if opt['writeoutput']:
        directory_string = "output/log.txt"
        outfile = open(directory_string, "a")
        outfile.write(s)
