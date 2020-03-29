def preprocessing(teams, zimmer, speisen, vorspeise, hauptspeise, nachspeise, kawo, kawos, options):
    num_of_teams = number_of_teams(teams)
    check_room_conflicts_maximum(teams, zimmer)
    count_teams_kawo_origin(teams, kawo)
    kawo_bin = set_kawo_bin(teams, kawo, kawos)
    p = calculate_preferences(teams, speisen, vorspeise, hauptspeise, nachspeise)

    return p, kawo_bin, num_of_teams

def number_of_teams(teams):
    counter = 0
    for i in teams:
        counter += 1
    print("\nEs gibt %i teilnehmende Teams" % (counter))
    print("")
    return counter


def check_room_conflicts_maximum(teams, zimmer):
    global i
    for i in teams:
        counter = 1
        number = zimmer[i]
        for j in teams:
            if i != j and number == zimmer[j]:
                counter = counter + 1
        if counter > 3:
            print("Es gibt zu viele Teams mit Zimmernummer %s" % (number))


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
    print("Es gibt %i Kawo1, %i Kawo2 und %i Kawo3 Teams.\n" % (count_k1, count_k2, count_k3))


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