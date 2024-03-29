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
            if i < j:
                mc[i, j] = mc[i, j].x
                tm[i, j] = tm[i, j].x


def calcpriority(x):
    if x == 0:
        return 0.1
    elif x == 1:
        return 1
    else:
        return 10


# noinspection PyUnresolvedReferences
def solve(teams, zimmer, speisen, p, kawo_bin, kawos, number_of_teams, options):
    def krcb(model, where):
        if where == GRB.Callback.MIPSOL:
            sol_x = model.cbGetSolution(x)
            for i in teams:
                # check for teams meeting twice
                for j in teams:
                    if i < j:
                        teamcount = []
                        for s in speisen:  # Team i bekocht Team j
                            if sol_x[i, j, s] > 0.9999:
                                teamcount.append(1)

                        for g in teams:  # Team i und Team j treffen sich bei einem fremden Team
                            if g != i and g != j:
                                for s in speisen:
                                    if sol_x[g, i, s] > 0.9999 and sol_x[g, j, s] > 0.9999:
                                        teamcount.append(2)

                        for s in speisen:  # Team j bekocht Team i
                            if sol_x[j, i, s] > 0.9999:
                                teamcount.append(3)
                        if len(teamcount) > 1:
                            if 1 in teamcount and 3 in teamcount:
                                for s in speisen:
                                    for ss in speisen:
                                        if (s != ss):
                                            model.cbLazy(x[i, j, s] <= 1 - x[j, i, ss] + mc[i, j])
                            elif 1 in teamcount and 2 in teamcount:
                                for g in teams:
                                    if g != i and g != j:
                                        for s in speisen:
                                            for ss in speisen:
                                                if s != ss:
                                                    model.cbLazy(
                                                        x[g, i, s] + x[g, j, s] <= 2 - x[i, j, ss] + mc[i, j])
                            elif 2 in teamcount and 3 in teamcount:
                                for g in teams:
                                    if g != i and g != j:
                                        for s in speisen:
                                            for ss in speisen:
                                                if s != ss:
                                                    model.cbLazy(
                                                        x[g, i, s] + x[g, j, s] <= 2 - x[j, i, ss] + mc[i, j])
                            else:
                                for g in teams:
                                    if g != i and g != j:
                                        for s in speisen:
                                            for gg in teams:
                                                for ss in speisen:
                                                    if g < gg and i != gg and j != gg and s != ss:
                                                        model.cbLazy(
                                                            x[g, i, s] + x[g, j, s] <= 3 - (
                                                                    x[gg, i, ss] + x[gg, j, ss]) + mc[i, j])

                # check for teams meeting not all kawos
                met_kawos = []
                for j in teams:
                    for s in speisen:
                        if i != j and (sol_x[i, j, s] > 0.9999 or sol_x[j, i, s] > 0.9999):
                            for k in kawos:
                                if kawo_bin[j, k] == 1:
                                    met_kawos.append(k)
                        for g in teams:
                            if g != i and g != j and sol_x[g, i, s] > 0.9999 and sol_x[g, j, s] > 0.9999:
                                for k in kawos:
                                    if kawo_bin[g, k] == 1:
                                        met_kawos.append(k)
                met_kawos = list(set(met_kawos))
                missing_kawos = [k for k in kawos if k not in met_kawos and kawo_bin[i, k] != 1]
                for k in missing_kawos:
                    model.cbLazy(quicksum(x[i, j, s] + x[j, i, s] for s in speisen for j in teams if i != j
                                          and kawo_bin[j, k] == 1) >= 1 - km[i, k])
                    teams_k = [j for j in teams if kawo_bin[j, k] == 1 and i != j]

                    """model.cbLazy(quicksum(x[g, j, s] + x[g, i, s] for g in teams for j in teams if i != j and j != g
                                          and i != g and kawo_bin[j, k] == 1)# and kawo_bin[g, k] != 1)
                                 >= (2 * len(teams_k) + 1) - (len(teams_k)+1) * kn[i, k])
                    """
                    for j in teams_k:
                        for g in teams:
                            if i != g and j != g and kawo_bin[g, k] != 1:
                                # BUG Does not hold for all dishes
                                model.cbLazy(x[g, j, s] + x[g, i, s] >= 2 - 2 * tm[i, j])

    model = Model("Kawo3Rockt!")

    # CONFIG
    model.setParam('TimeLimit', 30 * 60)
    model.setParam('MIPFocus', 0)
    model.setParam('LazyConstraints', 1)
    # if len(teams) % 3 != 0:
    #    model.setParam('MIPGap', 10)
    # model.setParam('Heuristics', 0.75)
    # model.setParam('Symmetry', 2)

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
            if i < j:
                mc[i, j] = model.addVar(name='mc_' + i + '_' + j, vtype=GRB.BINARY)

    # Variables that is one if the team i meets team j at any dish
    tm = {}
    for i in teams:
        for j in teams:
            if i != j:
                tm[i, j] = model.addVar(name="tm_" + i + "_" + j, vtype=GRB.BINARY)

    # variable that is one if a team i does not meet any team of kawo k
    km = {}
    for i in teams:
        for k in kawos:
            km[i, k] = model.addVar(name="km_" + i + "_" + k, vtype=GRB.BINARY)

    kn = {}
    for i in teams:
        for k in kawos:
            kn[i, k] = model.addVar(name="kn_" + i + "_" + k, vtype=GRB.BINARY)

    # balance variable to penalize not meeting a team of a kawo
    kp = {}
    for i in teams:
        for k in kawos:
            kp[i, k] = model.addVar(name='kp_' + i + '_' + k, vtype=GRB.BINARY)

    madw = calcpriority(options['madw'])
    mnttw = calcpriority(options['mnttw'])

    # objective function:
    model.setObjective(
        quicksum(c[i, s] for i in teams for s in speisen)  # amount of teams having 3 other teams as guests
        + quicksum(d[i, s] for i in teams for s in speisen)  # amount of teams having 1 other team as guests
        + quicksum(p[i, s] * y[i, s] for i in teams for s in speisen)  # teams cooking their preferred dish
        + mnttw * quicksum(mc[i, j] for i in teams for j in teams if i < j)  # punish if two teams meet twice
        # + madw * quicksum(tm[i, j] for i in teams for j in teams if i < j)  # punish if a team does not meet teams of
        # every kawo
        # + madw * quicksum(0.2 * km[i, k] for i in teams for k in kawos)
        # + madw * quicksum(kn[i, k] for i in teams for k in kawos)  # punish if a team does not meet teams of
        # every kawo
        + madw * quicksum(kp[i, k] for i in teams for k in kawos)
    )

    model.update()

    # Constraints:

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
            if i < ii and zimmer[i] == zimmer[ii]:
                for s in speisen:
                    model.addConstr(y[i, s] + y[ii, s] <= 1)

    # 6a Link penalty variables
    for i in teams:
        for k in kawos:
            if kawo_bin[i, k] != 1:
                teams_k = [j for j in teams if kawo_bin[j, k] == 1 and i != j]
                model.addConstr(quicksum(tm[i, j] for j in teams_k) <= len(teams_k) - 1 + kn[i, k])

    # 6b Balance the two variables for penalizing not meeting a team from some kawo (variables km and kn)
    for i in teams:
        for k in kawos:
            model.addConstr(km[i, k] + kn[i, k] <= 1 + kp[i, k])

    """
    # 6. Try to prevent meeting a team twice
    # 6a. Meeting a team at a dish from a third team implies do not cook for that team
    for i in teams:
        for j in teams:
            if i < j:
                for g in teams:
                    if g != i and g != j:
                        for s in speisen:
                            for ss in speisen:
                                if s != ss:
                                    model.addConstr(x[g, i, s] + x[g, j, s] <= 2 - x[i, j, ss] + mc[i, j])

    if not options['heuristic']:
        # 6b. Meeting a team at a dish from a third team implies do not meet at a fourth team
        for i in teams:
            for j in teams:
                if i < j:
                    for g in teams:
                        if g != i and g != j:
                            for s in speisen:
                                for gg in teams:
                                    for ss in speisen:
                                        if g < gg and i != gg and j != gg and s != ss:
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
                    model.addConstr(x[j, i, s] <= tm[i, j])

    # 7b. Team i meets a team j if both are guests of team g
    for i in teams:
        for j in teams:
            for g in teams:
                if i < j != g and i != g:
                    for s in speisen:
                        model.addConstr(x[g, j, s] <= tm[i, j] + (1 - x[g, i, s]))
                        model.addConstr(x[g, i, s] <= tm[i, j] + (1 - x[g, j, s]))
                # elif j < i != g and j != g:
                #    for s in speisen:
                #        model.addConstr(x[g, j, s] <= tm[j, i] + (1 - x[g, i, s]))

    
    # 7c. Make teams meet variable symmetric
    for i in teams:
        for j in teams:
            if i < j:
                model.addConstr(tm[i, j] == tm[j, i])
    
    
    # 7d. The main constraint. Try to meet at least one team of every kawo
    for i in teams:
        for k in kawos:
            model.addConstr(quicksum(kawo_bin[j, k] * tm[i, j] for j in teams if i < j)
                            + quicksum(kawo_bin[j, k] * tm[j, i] for j in teams if i > j)
                            >= 1)
    """
    # Optimize the model
    model.optimize(krcb)
    # model.optimize()
    # model.computeIIS()
    # model.write('k3rockt.ilp')

    # model.write('kaworockt.lp')
    print('\n Optimal solution value found: %g\n' % model.ObjVal)
    store_variable_values(teams, speisen, x, y, mc, tm, c, d)
    return x, y, mc, tm, c, d
