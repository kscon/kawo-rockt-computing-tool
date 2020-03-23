import pandas as pd
from gurobipy.gurobipy import multidict


def get_input():
    dframe = pd.read_excel('input/kaworockt_data.xlsx')
    # dframe.columns = ['teams', 'zimmer', 'vorspeise', 'hauptspeise', 'nachspeise', 'kawo']
    dframe2 = dframe.set_index('teams', drop=False)

    teams = dframe2.index.values.tolist()
    print(teams)
    dframe2.to_dict('series')

    return teams, zimmer, unvertraeglichkeiten, speisen, vorspeise, hauptspeise, nachspeise, kawo, kawos


def main():
    teams, data = get_input()

    data_zimmer = data['zimmer']
    # print(data0)
    dict_zimmer = data_zimmer.to_dict()

    print(data_zimmer)

    # print(teams)


if __name__ == '__main__':
    main()
