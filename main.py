# main file for computing an optimal route for running-dinner
import postprocessing
import preprocessing
import solvemodel
import readconfig
import fetchinput

def main():
    # read config file
    options = readconfig.read_config()

    # fetch input files
    teams, zimmer, unvertraeglichkeiten, vorspeise, hauptspeise, nachspeise, dorm, email, speisen, dorms \
        = fetchinput.get_input(options)

    # do preprocessing
    p, kawo_bin, number_of_teams = preprocessing.preprocessing(teams, zimmer, speisen, vorspeise, hauptspeise,
                                                               nachspeise, dorm, dorms, options)

    # solve the model
    x, y, mc, tm, c, d = solvemodel.solve(teams, zimmer, speisen, p, kawo_bin, dorms, number_of_teams, options)

    # do postprocessing and visualization
    postprocessing.postprocessing(options, teams, speisen, zimmer, dorm, unvertraeglichkeiten, email, x, y, p, mc, tm,
                                  c, d)


if __name__ == '__main__':
    main()
