# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 18:57:13 2018

@author: Kevin
"""
from gurobipy import *
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


teams, zimmer, unvertraeglichkeiten, vorspeise, hauptspeise, nachspeise, kawo = multidict({
    'A': ['1', 'Fleisch',                1, 0, 2, 3],
    'B': ['3514', 'Werthers Echte',         0, 2, 2, 1],
    'C': ['4303', 'Soja',                   2, 1, 0, 1], 
    'D': ['3505', '',                       0, 2, 2, 2], 
    'E': ['3509', 'Ananas',                 0, 2, 2, 1],  
    'F': ['4510', 'Fleisch',                0, 2, 2, 3], 
    'G': ['3308', 'TUNERZ HABENS DRAUF',    2, 0, 0, 3], 
    'H': ['3310', '',                       0, 2, 0, 2], 
    'I': ['1314', '',                       2, 2, 0, 2], 
    'J': ['4103', 'Fleisch',                2, 2, 0, 1],
    'K': ['4104', ' ',                      0, 1, 2, 2],
    'L': ['4304', 'Soja',                   2, 0, 2, 2], 
    'M': ['1302', '',                       0, 2, 1, 3], 
    'N': ['3310', 'Ananas',                 2, 0, 2, 1],  
    'O': ['1512', 'Fleisch',                2, 0, 0, 3], })
"""    'P': ['1111', 'Hirse',                  2, 1, 0, 2], 
    'Q': ['2113', 'Marmelade',              0, 2, 2, 3], 
    'R': ['1576', '',                       2, 1, 0, 3], 
    'S': ['4311', 'Fleisch',                2, 1, 0, 1], 
    'T': ['1212', 'Schmörebröt',            2, 2, 0, 1], 
    'U': ['6413', 'Snickers',               0, 2, 0, 2], 
    'V': ['1214', '',                       2, 2, 0, 2], 
    'W': ['1510', '',                       0, 2, 0, 1],
    'X': ['1581', 'Ananas',                 2, 0, 2, 3],  
    'Y': ['4513', 'Fleisch',                2, 1, 0, 3], 
    'Z': ['3468', 'Hirse',                  0, 1, 1, 2],
    'AA': ['1231', 'Marmelade',             0, 2, 2, 1], 
    'AB': ['2101', '',                      2, 1, 0, 2], 
    'AC': ['1214', 'Fleisch',               2, 0, 2, 3], 
    'AD': ['3457', 'Schmörebröt',           2, 1, 0, 1], 
    'AE': ['3311', 'Snickers',              0, 1, 1, 1], 
    'AF': ['4345', '',                      1, 1, 0, 2], 
    'AG': ['1510', '',                      0, 2, 0, 3],
    'AH': ['4311', 'Fleisch',                2, 1, 0, 3], 
    'AI': ['1212', 'Schmörebröt',            2, 2, 0, 1], 
    'AJ': ['6413', 'Snickers',               0, 2, 0, 2], 
    'AK': ['4564', '',                       2, 2, 0, 2], 
    'AL': ['4584', '',                       0, 2, 0, 2],
    'AM': ['1581', 'Ananas',                 2, 0, 2, 3],  
    'AN': ['4513', 'Fleisch',                2, 1, 0, 3], 
    'AO': ['1111', 'Hirse',                  0, 1, 1, 2], 
    'AP': ['4745', 'Marmelade',             0, 2, 2, 3], })
    'AQ': ['2101', '',                      2, 1, 0, 2], 
    'AR': ['4568', 'Fleisch',               2, 0, 2, 3], 
    'AS': ['1212', 'Schmörebröt',           2, 1, 0, 1], 
    'AT': ['3563', 'Snickers',              0, 1, 1, 1], 
    'AU': ['3453', '',                      1, 1, 0, 1], 
    'AV': ['2135', '',                      0, 2, 0, 3],
    'AW': ['1247', '',                      1, 2, 0, 1], 
    'AX': ['6434', '',                      1, 2, 0, 1], 
    'AZ': ['3415', 'Fleisch',               2, 1, 0, 3], 
    'BA': ['1', 'Schmörebröt',              2, 2, 0, 1], 
    'BB': ['2', 'Snickers',                 0, 2, 0, 2], 
    'BC': ['3', '',                         2, 2, 0, 2], 
    'BD': ['7531', '',                         0, 2, 0, 2],
    'BE': ['55', 'Ananas',                  2, 0, 2, 3],  
    'BF': ['5', 'Fleisch',                  2, 1, 0, 3], 
    'BG': ['3456', 'Hirse',                    0, 1, 1, 2], 
    'BH': ['5', 'Marmelade',                0, 2, 2, 3], 
    'BI': ['5679', '',                         0, 1, 0, 2], 
    'BJ': ['1', 'Fleisch',                  2, 0, 2, 3], 
    'BK': ['1234', 'Schmörebröt',           2, 1, 0, 1], 
    'BL': ['1257', 'Snickers',                 0, 1, 1, 1], 
    'BM': ['5731', '',                      1, 1, 0, 2], 
    'BN': ['1261', '',                      0, 2, 2, 3],
    'BO': ['7456', '',                      0, 2, 2, 3],
    'BP': ['5648', '',                      1, 2, 0, 3],
    'BQ': ['4568', 'Fleisch',               2, 0, 2, 3],
    'BR': ['153', '',                      1, 2, 0, 3], 
    'BS': ['7456', '',                      0, 2, 2, 3],})
    'BT': ['23', 'Snickers',              0, 1, 1, 1], 
    'BU': ['5731', '',                      1, 1, 0, 2], 
    'BV': ['1416', '',                      0, 2, 0, 3],
    'BW': ['1247', '',                      1, 2, 0, 3], 
    'BX': ['6434', '',                      1, 2, 0, 3],
    'BZ': ['3415', 'Fleisch',               2, 1, 0, 3], 
    'CA': ['13', 'Schmörebröt',              2, 2, 0, 1], 
    'CB': ['14', 'Snickers',                 0, 2, 0, 2], 
    'CC': ['152', '',                         2, 2, 0, 2], 
    'CD': ['4564', '',                         0, 2, 0, 2],
    'CE': ['1241', 'Ananas',                  2, 0, 2, 3],  
    'CF': ['4574', 'Fleisch',                  2, 1, 0, 3], 
    'CG': ['6', 'Hirse',                    0, 1, 1, 2], 
    'CH': ['5667', 'Marmelade',                0, 2, 2, 3], 
    'CI': ['6', '',                         0, 1, 0, 2], 
    'CJ': ['1', 'Fleisch',                  2, 0, 2, 3], 
    'CK': ['1234', 'Schmörebröt',           2, 1, 0, 1], 
    'CL': ['676', 'Snickers',                 0, 1, 1, 1], 
    'CM': ['5731', '',                      1, 1, 0, 2], 
    'CN': ['1261', '',                      0, 2, 2, 3], 
    'CM': ['1235', '',                         0, 2, 0, 2],
    'CO': ['5586', 'Ananas',                  2, 0, 2, 3],  
    'CP': ['6767', 'Fleisch',                  2, 1, 0, 3], 
    'CQ': ['5655', 'Hirse',                    0, 1, 1, 2], 
    'CR': ['3268', 'Marmelade',                0, 2, 2, 3], 
    'CS': ['8789', '',                         0, 1, 0, 2], 
    'CT': ['5607', 'Fleisch',                  2, 0, 2, 3], 
    'CU': ['8978', 'Schmörebröt',           2, 1, 0, 1], 
    'CV': ['7897', 'Snickers',                 0, 1, 1, 1], 
    'CW': ['8797', '',                      1, 1, 0, 2], 
    'CX': ['3245', '',                      0, 2, 2, 3],
    })
    """

speisen = ['vorspeise', 'hauptspeise', 'nachspeise']
kawos = ['1', '2','3']

p = { (i,s) : 100 for i in teams for s in speisen}

for i in teams:
    for s in speisen:
        if s == 'vorspeise':
            p[i,s] = 10 ** vorspeise[i]
        elif s == 'hauptspeise':
            p[i,s] = 10 ** hauptspeise[i]
        else:
            p[i,s] = 10 ** nachspeise[i]
       
for i in teams:
    counter = 1
    number = zimmer[i]
    for j in teams:
        if (i != j and number == zimmer[j]):
            counter = counter + 1
    if counter > 3:
        print("Es gibt zu viele Teams mit Zimmernummer %s" % (number))

count_k1 = 0
count_k2 = 0
count_k3 = 0
for i in teams:
    if(kawo[i] == 1):
        count_k1 = count_k1 +1
    elif(kawo[i] == 2):
        count_k2 = count_k2 +1
    elif(kawo[i] == 3):
        count_k3 = count_k3 +1
print("Es gibt %i Kawo1, %i Kawo2 und %i Kawo3 Teams.\n"%(count_k1, count_k2,count_k3))

kawo_bin = { (i,k) : 0 for i in teams for k in kawos}
for i in teams:
    k = str(kawo[i])
    kawo_bin[i,k] = 1

import kaworocktmodel

model = kaworocktmodel.solve(teams, zimmer, unvertraeglichkeiten, speisen, vorspeise, hauptspeise, nachspeise, kawo, p, kawo_bin, kawos)