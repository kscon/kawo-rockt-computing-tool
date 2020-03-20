import visualizeoutput


def postprocessing(teams, speisen, kawo, x, y, p, mc, tm, c, d):
    print("##### POST PROCESSING #####\n")

    print_teams_dishes(speisen, teams, y)

    print_teams_guests(speisen, teams, x)

    print_teams_route(speisen, teams, x)

    print_teams_not_cooking_preferred_dish(p, speisen, teams, y)

    print_teams_meet_several_times(speisen, teams, x)

    count_1k, count_2k, count_3k = print_kawo_distribution_per_dish(kawo, speisen, teams, x, y)

    visualizeoutput.visualize(count_1k, count_2k, count_3k)

    print_kawo_distribution_for_team(teams, speisen, kawo, x, y)
    # print_teams_met(teams, speisen, x,y, tm)
    print_team_cooks_not_for_three(teams, speisen, x, y, c, d)


def print_teams_route(speisen, teams, x):
    print("--- Wie sieht die Route eines Teams aus ---")
    for j in teams:
        for s in speisen:
            for i in teams:
                if i != j:
                    if (x[i, j, s] > 0.5):
                        print('Das Team %s muss zu Team %s für den Gang %s.' % (j, i, s))
    print("")


def print_teams_guests(speisen, teams, x):
    print("---Welche Gäste hat ein Team für seinen Gang ---")
    for s in speisen:
        for i in teams:
            for j in teams:
                if i != j:
                    if (x[i, j, s] > 0.5):
                        print('Es kocht Team %s für Team %s den Gang %s.' % (i, j, s))
                        # print('Dabei sollte das Team %s bitte auf %s verzichten.'% (i, unvertraeglichkeiten[j]))
    print("")


def print_teams_dishes(speisen, teams, y):
    print("--- Welches Team kocht welchen Gang ---")
    print(y)
    for i in teams:
        for s in speisen:
            if (y[i, s] > 0.5):
                print('Es kocht Team %s den Gang %s.' % (i, s))
    print("")


def print_kawo_distribution_per_dish(kawo, speisen, teams, x, y):
    print("\n--- Verteilung der Kawos ---")
    count_3k = 0
    count_2k = 0
    count_1k = 0
    for i in teams:
        for s in speisen:
            A = []
            A.append(kawo[i])
            if y[i, s] > 0.5:
                for j in teams:
                    if (i != j and x[i, j, s] > 0.5):
                        A.append(kawo[j])

                if (1 in A and 2 in A and 3 in A):
                    count_3k = count_3k + 1
                elif ((1 in A and 2 in A) or (1 in A and 3 in A) or (2 in A and 3 in A)):
                    count_2k = count_2k + 1
                elif (1 in A or 2 in A or 3 in A):
                    count_1k = count_1k + 1
    print("Es gibt %i Gänge mit Beteiligung aller Kawos" % (count_3k))
    print("Es gibt %i Gänge mit Beteiligung zweier Kawos" % (count_2k))
    print("Es gibt %i Gänge mit Beteiligung eines Kawos\n" % (count_1k))
    return count_1k, count_2k, count_3k


def print_teams_meet_several_times(speisen, teams, x):
    conflicts = 0
    for i in teams:
        for j in teams:
            if i != j:
                teamcount = 0
                for s in speisen:  # Team i bekocht Team j
                    if (x[i, j, s] > 0.5):
                        teamcount = teamcount + 1

                for g in teams:  # Team i und Team j treffen sich bei einem fremden Team
                    if (g != i and g != j):
                        for s in speisen:
                            if (x[g, i, s] > 0.5 and x[g, j, s] > 0.5):
                                teamcount = teamcount + 1

                for s in speisen:  # Team j bekocht Team i
                    if (x[j, i, s] > 0.5):
                        teamcount = teamcount + 1

                if (teamcount > 1):
                    print("Team %s und Team %s treffen %i-mal aufeinander!" % (i, j, teamcount))
                    conflicts = conflicts + 1
    print("Es gibt insgesamt %i Teamwiedertreffen" % (conflicts / 2))


def print_teams_not_cooking_preferred_dish(p, speisen, teams, y):
    print("--- Welches Team kocht nicht seinen präferierten Gang ---")
    for i in teams:
        for s in speisen:
            if p[i, s] * y[i, s] >= 50:
                print('Es kocht Team %s seinen am wenigsten präferierten Gang.' % (i))
            elif p[i, s] * y[i, s] >= 5:
                print("Es kocht Team %s seinen zweit-präferierten Gang." % (i))
    print("")


def print_team_cooks_not_for_three(teams, speisen, x, y, c, d):
    print("")
    for i in teams:
        for s in speisen:
            if (c[i, s] > 0.5):
                A = [j for j in teams if i != j and x[i, j, s] > 0.5]
                if (len(A) == 3):
                    print("team %s cooks for three teams! " % (i))
                else:
                    print("Something went wrong")
            elif (d[i, s] > 0.5):
                A = [j for j in teams if i != j and x[i, j, s] > 0.5]
                if (len(A) == 1):
                    print("team %s cooks for one team! " % (i))
                else:
                    print("Something went wrong")


def print_kawo_distribution_for_team(teams, speisen, kawo, x, y):
    for i in teams:
        A = []
        # A.append(kawo[i])
        for s in speisen:
            if (y[i, s] > 0.5):
                for j in teams:
                    if (i != j and x[i, j, s] > 0.5):
                        A.append(kawo[j])

            for j in teams:
                if (i != j and x[j, i, s] > 0.5):
                    A.append(kawo[j])
                    for g in teams:
                        if (i != g and j != g and x[j, g, s] > 0.5):
                            A.append(kawo[g])
        if ((A.count(1) == 0 and kawo[i] != 1) or (A.count(2) == 0 and kawo[i] != 2) or (
                A.count(3) == 0 and kawo[i] != 3)):
            print("Team %s (aus dem Kawo%s) trifft auf %i Kawo1 Teams, %i Kawo2 Teams und %i Kawo3 Teams" % (
                i, kawo[i], A.count(1), A.count(2), A.count(3)))


def print_teams_met(teams, speisen, x, y, tm):
    print("")
    for i in teams:
        for j in teams:
            if i != j and tm[i, j] > 0.5:
                print("Team %s trifft auf Team %s" % (i, j))
