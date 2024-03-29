# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 18:57:13 2018

@author: Kevin
"""
from gurobipy import *


def get_input(options):
    teams, zimmer, unvertraeglichkeiten, vorspeise, hauptspeise, nachspeise, kawo = multidict({
        'A': ['3186', '', 0, 1, 2, 1],
        'B': ['3571', '', 1, 0, 1, 2],
        'C': ['6333', '', 1, 0, 2, 3],
        'D': ['4712', '', 1, 0, 1, 3],
        'E': ['5944', '', 2, 0, 0, 2],
        'F': ['7732', '', 0, 1, 0, 1],
        'G': ['7766', '', 0, 2, 2, 1],
        'H': ['3633', '', 2, 0, 0, 3],
        'I': ['5227', '', 0, 2, 1, 3],
        'J': ['1547', '', 1, 2, 0, 2],
        'K': ['5692', '', 1, 1, 0, 1],
        'L': ['4173', '', 0, 0, 1, 1],
        'M': ['2597', '', 0, 2, 2, 3],
        'N': ['1455', '', 2, 0, 2, 1],
        'O': ['9985', '', 0, 2, 0, 3],
        'P': ['2584', '', 1, 0, 0, 3],
        'Q': ['7484', '', 2, 1, 0, 1],
        'R': ['2154', '', 0, 1, 0, 2],
        'S': ['1559', '', 0, 0, 0, 3],
        'T': ['4855', '', 2, 0, 1, 1],
        'U': ['7146', '', 0, 1, 0, 3],
        'V': ['3188', '', 0, 2, 0, 2],
        'W': ['4137', '', 1, 0, 2, 2],
        'X': ['4621', '', 0, 2, 1, 2],
        'Y': ['7275', '', 1, 0, 0, 3],
        'Z': ['5733', '', 0, 0, 2, 2],
        'AA': ['7839', '', 2, 0, 1, 1],
        'AB': ['8668', '', 1, 0, 2, 3],
        'AC': ['4954', '', 0, 1, 1, 3],
        'AD': ['5823', '', 0, 1, 1, 2],
        'AE': ['4915', '', 2, 2, 0, 2],
        'AF': ['8256', '', 2, 1, 0, 1],
        'AG': ['9862', '', 0, 2, 2, 1],
        'AH': ['4175', '', 0, 0, 0, 2],
        'AI': ['8477', '', 1, 0, 2, 1],
        'AJ': ['3532', '', 2, 1, 0, 1],
        'AK': ['1753', '', 1, 0, 2, 2],
        'AL': ['9969', '', 2, 2, 0, 3],
        'AM': ['7414', '', 0, 1, 1, 3],
        'AN': ['5154', '', 2, 2, 0, 2],
        'AO': ['6577', '', 2, 1, 0, 2],
        'AP': ['6357', '', 0, 0, 2, 1],
        'AQ': ['2439', '', 0, 1, 1, 2],
        'AR': ['2674', '', 0, 2, 0, 3],
        'AS': ['8681', '', 2, 0, 2, 3],
        'AT': ['2323', '', 1, 2, 0, 3],
        'AU': ['9694', '', 1, 1, 0, 3],
        'AV': ['2883', '', 0, 2, 2, 1],
        'AW': ['2411', '', 0, 1, 1, 3],
        'AX': ['5849', '', 2, 2, 0, 2],
    })


    speisen = ['vorspeise', 'hauptspeise', 'nachspeise']
    kawos = ['1', '2', '3']

    email = {}
    for i in teams:
        email[i] = ''

    return teams, zimmer, unvertraeglichkeiten, vorspeise, hauptspeise, nachspeise, kawo, email, speisen, kawos
