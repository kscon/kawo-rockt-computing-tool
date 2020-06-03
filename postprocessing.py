import visualizeoutput
import os

def postprocessing(options, teams, speisen, zimmer, kawo, unvertraeglichkeiten, email, x, y, p, mc, tm, c, d):
    global opt
    opt = options
    log("##### POST PROCESSING #####\n")

    # print analyses of distribution result
    print_teams_not_cooking_preferred_dish(p, speisen, teams, y)
    print_teams_meet_several_times(speisen, teams, x)
    count_1k, count_2k, count_3k = print_kawo_distribution_per_dish(kawo, speisen, teams, x, y)
    # visualizeoutput.visualize(count_1k, count_2k, count_3k)
    print_kawo_distribution_for_team(teams, speisen, kawo, x, y)
    print_team_cooks_not_for_three(teams, speisen, x, c, d)

    # print team dependent data:
    prepare_output_directory()
    write_team_dishes(speisen, teams, y, email)
    write_teams_guests(speisen, teams, unvertraeglichkeiten, x)
    write_teams_route(speisen, teams, zimmer, kawo, x)

    log('##### ----- #####')


def prepare_output_directory():
    if not os.path.exists('output/team_output'):
        os.makedirs('output/team_output')
    else:
        for file in os.listdir('output/team_output'):
            os.remove(os.path.join('output/team_output', file))


def write_teams_route(speisen, teams, zimmer, kawo, x):
    # print("--- Wie sieht die Route eines Teams aus ---")
    for j in teams:
        directory_string = "output/team_output/" + str(j) + ".txt"
        outfile = open(directory_string, "a")
        for s in speisen:
            for i in teams:
                if i != j:
                    if x[i, j, s] > 0.5:
                        log('Das Team %s muss zu Team %s für den Gang %s.' % (j, i, s))

                        tmp_output_string = "Das Team muss zu Team " + str(i) + " in Zimmer " + str(zimmer[i]) + \
                                            " (Kawo " + str(kawo[i]) + ") für den Gang " + str(s) + "\n"
                        outfile.write(tmp_output_string)
    log("")


def write_teams_guests(speisen, teams, unvertraeglichkeiten, x):
    # print("---Welche Gäste hat ein Team für seinen Gang ---")
    for s in speisen:
        for i in teams:
            directory_string = "output/team_output/" + str(i) + ".txt"
            outfile = open(directory_string, "a")
            for j in teams:
                if i != j:
                    if x[i, j, s] > 0.5:
                        log('Es kocht Team %s für Team %s den Gang %s.' % (i, j, s))
                        log('Dabei sollte das Team %s bitte auf %s verzichten.' % (i, unvertraeglichkeiten[j]))

                        tmp_output_string = "Es kocht das Team für Team " + str(j) + \
                                            ". Dabei sollte nach Möglichkeit auf " + str(unvertraeglichkeiten[j]) + \
                                            " verzichtet werden.\n"
                        outfile.write(tmp_output_string)
    log("")


def write_team_dishes(speisen, teams, y, email):
    # print("--- Welches Team kocht welchen Gang ---")
    for i in teams:
        directory_string = "output/team_output/" + str(i) + ".txt"
        outfile = open(directory_string, "w")
        for s in speisen:
            if y[i, s] > 0.5:
                log('Es kocht Team %s den Gang %s.' % (i, s))
                outfile.write(email[i] + '\n')
                tmp_output_string = "Es kocht Team " + str(i) + " den Gang " + str(s) + "\n"
                outfile.write(tmp_output_string)
    log("")


def print_kawo_distribution_per_dish(kawo, speisen, teams, x, y):
    log("\n--- Verteilung der Kawos ---")
    count_3k = 0
    count_2k = 0
    count_1k = 0
    for i in teams:
        for s in speisen:
            A = []
            A.append(kawo[i])
            if y[i, s] > 0.5:
                for j in teams:
                    if i != j and x[i, j, s] > 0.5:
                        A.append(kawo[j])

                if (1 in A and 2 in A and 3 in A):
                    count_3k = count_3k + 1
                elif (1 in A and 2 in A) or (1 in A and 3 in A) or (2 in A and 3 in A):
                    count_2k = count_2k + 1
                elif (1 in A or 2 in A or 3 in A):
                    count_1k = count_1k + 1
    log("Es gibt %i Gänge mit Beteiligung aller Kawos" % (count_3k))
    log("Es gibt %i Gänge mit Beteiligung zweier Kawos" % (count_2k))
    log("Es gibt %i Gänge mit Beteiligung eines Kawos\n" % (count_1k))
    return count_1k, count_2k, count_3k


def print_teams_meet_several_times(speisen, teams, x):
    conflicts = 0
    for i in teams:
        for j in teams:
            if i < j:
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
                    log("Team %s und Team %s treffen %i-mal aufeinander!" % (i, j, teamcount))
                    conflicts = conflicts + 1
    log("Es gibt insgesamt %i Teamwiedertreffen" % (conflicts))


def print_teams_not_cooking_preferred_dish(p, speisen, teams, y):
    log("--- Welches Team kocht nicht seinen präferierten Gang ---")
    for i in teams:
        for s in speisen:
            if p[i, s] * y[i, s] >= 50:
                log('Es kocht Team %s seinen am wenigsten präferierten Gang.' % (i))
            elif p[i, s] * y[i, s] >= 5:
                log("Es kocht Team %s seinen zweit-präferierten Gang." % (i))
    print("")


def print_team_cooks_not_for_three(teams, speisen, x, c, d):
    log("")
    for i in teams:
        for s in speisen:
            if (c[i, s] > 0.5):
                A = [j for j in teams if i != j and x[i, j, s] > 0.5]
                if (len(A) == 3):
                    log("team %s cooks for three teams! " % (i))
                else:
                    log("Something went wrong")
            elif (d[i, s] > 0.5):
                A = [j for j in teams if i != j and x[i, j, s] > 0.5]
                if (len(A) == 1):
                    log("team %s cooks for one team! " % (i))
                else:
                    log("Something went wrong")


def print_kawo_distribution_for_team(teams, speisen, kawo, x, y):
    for i in teams:
        A = []
        for s in speisen:
            if (y[i, s] > 0.5):
                for j in teams:
                    if (i != j and x[i, j, s] > 0.5):
                        A.append(kawo[j])

            for j in teams:
                if i != j and x[j, i, s] > 0.5:
                    A.append(kawo[j])
                    for g in teams:
                        if i != g and j != g and x[j, g, s] > 0.5:
                            A.append(kawo[g])
        if ((A.count(1) == 0 and kawo[i] != 1) or (A.count(2) == 0 and kawo[i] != 2) or (
                A.count(3) == 0 and kawo[i] != 3)):
            log("Team %s (aus dem Kawo%s) trifft auf %i Kawo1 Teams, %i Kawo2 Teams und %i Kawo3 Teams" % (
                i, kawo[i], A.count(1), A.count(2), A.count(3)))


def print_teams_met(teams, tm):
    log("")
    for i in teams:
        for j in teams:
            if i != j and tm[i, j] > 0.5:
                log("Team %s trifft auf Team %s" % (i, j))


def log(s):
    print(s)
    if opt['writeoutput']:
        directory_string = "output/log.txt"
        outfile = open(directory_string, "a")
        outfile.write(s)
