import pandas as pd


def get_input():
    dframe = pd.read_excel('input/kaworockt_data.xlsx')
    # dframe.columns = ['teams', 'zimmer', 'vorspeise', 'hauptspeise', 'nachspeise', 'kawo']
    dframe2 = dframe.set_index('teams', drop=False)

    teams = dframe2.index.values.tolist()

    data = dframe2.to_dict('series')

    data_zimmer = data['zimmer']
    dict_zimmer = data_zimmer.to_dict()

    data_vorspeise = data['vorspeise']
    dict_vorspeise = data_vorspeise.to_dict()

    data_hauptspeise = data['hauptspeise']
    dict_hauptspeise = data_hauptspeise.to_dict()

    data_nachspeise = data['nachspeise']
    dict_nachspeise = data_nachspeise.to_dict()

    print(dict_nachspeise)

    return teams, zimmer, speisen, vorspeise, hauptspeise, nachspeise, kawo, kawos
