## main file for computing an optimal route for running-dinner
from input import kaworockt_testdata
import preprocessing
import solvemodel
import postprocessing

def main():
    # read config file

    # fetch input files
    teams, zimmer, unvertraeglichkeiten, speisen, vorspeise, hauptspeise, nachspeise, kawo, kawos = kaworockt_testdata.get_input()

    # do preprocessing
    p, kawo_bin, number_of_teams = preprocessing.preprocessing(teams, zimmer, speisen, vorspeise, hauptspeise, nachspeise, kawo, kawos)

    # solve the model
    x, y, p, mc, tm, c, d = solvemodel.solve(teams, zimmer, speisen, kawo, p, kawo_bin, kawos, number_of_teams)

    # do postprocessing
    postprocessing.postprocessing(teams, speisen, kawo, x, y, p, mc, tm, c, d)

    # visualization

if __name__ == '__main__':
     main()