# -*- coding: utf-8 -*-
from gurobipy import *


# store the actual variable values into the dict as gurobi does not do this automatically
def store_variable_values(teams, speisen, x, y, mc, tm, c, d):
    for i in teams:
        for s in speisen:
            y[i, s] = y[i, s].X
            c[i, s] = c[i, s].X
            d[i, s] = d[i, s].X
    for i in teams:
        for j in teams:
            if i != j:
                for s in speisen:
                    x[i, j, s] = x[i, j, s].X
    for i in teams:
        for j in teams:
            if i != j:
                mc[i, j] = mc[i, j].x
                tm[i, j] = tm[i, j].x


def solve(teams, zimmer, speisen, p, kawo_bin, kawos, number_of_teams):
    model = Model("Kawo3Rockt!")

    model.modelsense = GRB.MINIMIZE

    # variable holds if team i cooks the dish s for the team j (at the location of i), or not
    x = {}
    for i in teams:
        for j in teams:
            if i != j:
                for s in speisen:
                    x[i, j, s] = model.addVar(name='x_' + i + '_' + j + '_' + s, vtype=GRB.BINARY)

    # variable holds if team i cooks dish s or not (helper variable for easier output)
    y = {}
    for i in teams:
        for s in speisen:
            y[i, s] = model.addVar(name='y_' + i + '_' + s, vtype=GRB.BINARY)

    # variables that hold the value 1 if the number of guest teams of team i for dish s is three (c[i] = 1) or one (
    # d[i] = 1)
    c = {}
    for i in teams:
        for s in speisen:
            c[i, s] = model.addVar(name='c_' + i + '_' + s, vtype=GRB.BINARY)

    d = {}
    for i in teams:
        for s in speisen:
            d[i, s] = model.addVar(name='d_' + i + '_' + s, vtype=GRB.BINARY)

    # variable that holds 1 if teams i and j meet twice
    mc = {}
    for i in teams:
        for j in teams:
            if i != j:
                mc[i, j] = model.addVar(name='mc_' + i + '_' + j, vtype=GRB.BINARY)

    # Variable that is one if the team i meets team j at any dish
    tm = {}
    for i in teams:
        for j in teams:
            if i != j:
                tm[i, j] = model.addVar(name="tm_" + i + "_" + j, vtype=GRB.BINARY)

    # objective function:
    model.setObjective(
        100 * quicksum(c[i, s] for i in teams for s in speisen)  # amount of teams having 3 other teams as guests
        + 100 * quicksum(d[i, s] for i in teams for s in speisen)  # amount of teams having 1 other team as guests
        + quicksum(p[i, s] * y[i, s] for i in teams for s in speisen)  # teams cooking their preferred dish
        + 400 * quicksum(mc[i, j] for i in teams for j in teams if i < j)  # punish if two teams meet twice
        + 200 * quicksum(tm[i, j] for i in teams for j in teams if i < j)
        # punish if a team does not meet teams of every other Kawo
    )

    model.update()

    # Constraints:

    # model.addConstr(quicksum(x['Ersti & Ersti', j, s] + x['Die Kräuterkenner und Gewürzgarnierer', j, s] for j in
    # teams if j != 'Ersti & Ersti' and j != 'Die Kräuterkenner und Gewürzgarnierer' for s in speisen)  == 6 )

    # 1. Variable linking x and y. Allow a number of guest teams unequal to 2 if the number of overall teams is not
    # dividable by 3.
    for i in teams:
        for s in speisen:
            model.addConstr(quicksum(x[i, j, s] for j in teams if i != j) == 2 * y[i, s] + c[i, s] - d[i, s])
            model.addConstr(c[i, s] + d[i, s] <= y[i, s])

    # 2. Every team cooks exactly one dish
    for i in teams:
        model.addConstr(quicksum(y[i, s] for s in speisen) == 1)

    # 3. Every dish is cooked by enough teams such that every team can be part of a dish as a guest.
    # A higher value for the constant 'f' allows more solutions for not fitting team numbers, though f = 1 is sufficient
    # for most cases
    num = number_of_teams
    for s in speisen:
        f = 1
        model.addConstr(quicksum(y[i, s] for i in teams) <= (num // 3) + f)
        model.addConstr(quicksum(y[i, s] for i in teams) >= (num // 3) - f)

    # 4. Every team is guest for the dishes which it does not cook
    for j in teams:
        for s in speisen:
            model.addConstr(quicksum(x[i, j, s] for i in teams if i != j) == (1 - y[j, s]))

    # 5. Avoid room conflicts (only relevant in some cases where two teams want to cook at the same location).
    # If so, do not allow the conflicting teams to cook the same dish.
    for i in teams:
        for ii in teams:
            if (i < ii and zimmer[i] == zimmer[ii]):
                for s in speisen:
                    model.addConstr(y[i, s] + y[ii, s] <= 1)

    # 6. Try to prevent meeting a team twice
    # 6a. Meeting a team at a dish from a third team implies do not cook for that team
    for i in teams:
        for j in teams:
            if (i != j):
                for g in teams:
                    if (g != i and g != j):
                        for s in speisen:
                            for ss in speisen:
                                if (s != ss):
                                    model.addConstr(x[g, i, s] + x[g, j, s] <= 2 - x[i, j, ss] + mc[i, j])

    # 6b. Meeting a team at a dish from a third team implies do not meet at a fourth team
    for i in teams:
        for j in teams:
            if (i < j):
                for g in teams:
                    if (g != i and g != j):
                        for s in speisen:
                            for gg in teams:
                                for ss in speisen:
                                    if (g < gg and i != gg and j != gg and s != ss):
                                        model.addConstr(
                                            x[g, i, s] + x[g, j, s] <= 3 - (x[gg, i, ss] + x[gg, j, ss]) + mc[i, j])

    # 6c. If a team i has cooked for a team j, prevent that team j cooks for team i
    for i in teams:
        for j in teams:
            if i < j:
                for s in speisen:
                    for ss in speisen:
                        if (s != ss):
                            model.addConstr(x[i, j, s] <= 1 - x[j, i, ss] + mc[i, j])

    # 6d. Make the variable assignment symmetric
    for i in teams:
        for j in teams:
            if i < j:
                model.addConstr(mc[i, j] == mc[j, i])

    # 7. Try to have a team meet teams of every kawo
    # 7a. A team is met when cooked for it
    for i in teams:
        for j in teams:
            for s in speisen:
                if i < j:
                    model.addConstr(x[i, j, s] <= tm[i, j])

    # 7b. Team i meets a team j if both are guests of team g
    for i in teams:
        for j in teams:
            for g in teams:
                if (i < j and i != g and j != g):
                    for s in speisen:
                        model.addConstr(x[g, j, s] <= tm[i, j] + (1 - x[g, i, s]))

    # 7c. Make teams meet variable symmetric
    for i in teams:
        for j in teams:
            if i < j:
                model.addConstr(tm[i, j] == tm[j, i])

    # 7d. The main constraint. Try to meet at least one team of every kawo
    for i in teams:
        for k in kawos:
            model.addConstr(quicksum(kawo_bin[j, k] * tm[i, j] for j in teams if i != j) >= 1)  # - knm[i,k])

    ## CONFIG
    model.setParam('TimeLimit', 30 * 60)

    # Optimize the model
    model.optimize()

    if model.status == GRB.OPTIMAL or True:
        print('\n Optimaler gefundener Zielfunktionswert: %g\n' % model.ObjVal)
        store_variable_values(teams, speisen, x, y, p, mc, tm, c, d)
        return x, y, mc, tm, c, d

    else:
        print('Keine Optimalloesung gefunden. Status: %i' % (model.status))
    return model
