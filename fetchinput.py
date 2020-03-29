import pandas as pd


def get_input(options):
    filename = options['datainput']
    print(filename)

    path_of_file = 'input/' + filename

    dataframe = pd.read_excel(path_of_file)
    inputdata = dataframe.set_index('team', drop=False)

    teams = inputdata.index.values.tolist()

    data = inputdata.to_dict('series')

    data_zimmer = data['zimmer']
    dict_zimmer = data_zimmer.to_dict()

    data_unvertraeglichkeiten = data['unvertraeglichkeiten']
    dict_unvertraeglichkeiten = data_unvertraeglichkeiten.to_dict()

    data_vorspeise = data['vorspeise']
    dict_vorspeise = data_vorspeise.to_dict()

    data_hauptspeise = data['hauptspeise']
    dict_hauptspeise = data_hauptspeise.to_dict()

    data_nachspeise = data['nachspeise']
    dict_nachspeise = data_nachspeise.to_dict()

    data_kawo = data['kawo']
    dict_kawo = data_kawo.to_dict()

    data_email = data['email']
    dict_email = data_email.to_dict()

    return teams, dict_zimmer, dict_unvertraeglichkeiten, dict_vorspeise, dict_hauptspeise, dict_nachspeise, dict_kawo, dict_email
