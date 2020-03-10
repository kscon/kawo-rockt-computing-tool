# -*- coding: utf-8 -*-
from gurobipy import * 
import visualizedistributionresult

def number_of_teams(teams):
  counter = 0
  for i in teams:
    counter += 1
  return counter

def print_output(teams, speisen, x, y ):
  print("--- Welches Team kocht welchen Gang ---")
  for i in teams:
    for s in speisen:
      if(y[i,s].x > 0.5):
        print('Es kocht Team %s den Gang %s.' % (i,s))
  print("")

  print("---Welche Gäste hat ein Team für seinen Gang ---")
  for s in speisen:
    for i in teams:
        for j in teams:
          if i != j:
            if (x[i,j,s].x > 0.5):
              print('Es kocht Team %s für Team %s den Gang %s.' % (i,j,s))
              #print('Dabei sollte das Team %s bitte auf %s verzichten.'% (i, unvertraeglichkeiten[j]))
                
  print("")
  print("--- Wie sieht die Route eines Teams aus ---")
  for j in teams: 
    for s in speisen:
      for i in teams:
        if i != j:
          if (x[i,j,s].x > 0.5):
            print('Das Team %s muss zu Team %s für den Gang %s.' % (j,i,s))
  print('')

def postprocessing(teams, speisen, kawo, x, y, p, mc, tm,c,d):
  print("##### POST PROCESSING #####\n")
  print("--- Welches Team kocht nicht seinen präferierten Gang ---")
  for i in teams: 
    for s in speisen:
      if(p[i,s] * y[i,s].x >= 50):
        print('Es kocht Team %s seinen am wenigsten präferierten Gang.' % (i))
      elif(p[i,s] * y[i,s].x >= 5):
        print("Es kocht Team %s seinen zweit-präferierten Gang." % (i)) 
 
  print("")
  conflicts = 0
  for i in teams:
    for j in teams:
      if i != j:
        teamcount = 0
        for s in speisen: # Team i bekocht Team j
          if(x[i,j,s].x > 0.5):
            teamcount = teamcount + 1
        
        for g in teams: # Team i und Team j treffen sich bei einem fremden Team
          if(g != i and g != j):
            for s in speisen:
              if(x[g,i,s].x > 0.5 and x[g,j,s].x > 0.5):
                teamcount = teamcount + 1
          
        for s in speisen: # Team j bekocht Team i
          if(x[j,i,s].x > 0.5):
            teamcount = teamcount + 1
          
        if(teamcount > 1):
          print("Team %s und Team %s treffen %i-mal aufeinander!" %(i,j,teamcount))
          conflicts = conflicts +1
  print("Es gibt insgesamt %i Teamwiedertreffen" % (conflicts/2))

  teamnumber = number_of_teams(teams)
  print("\nEs gibt %i teilnehmende Teams" %(teamnumber))
  print("")
  for i in teams:
    for j in teams:
      if (i != j and mc[i,j].x > 0.5):
        print("Meet-twice variable für Team %s und Team %s hat den Wert %f" %(i,j, mc[i,j].x))

  print("\n--- Verteilung der Kawos ---")
  count_3k = 0
  count_2k = 0
  count_1k = 0
  for i in teams:
    for s in speisen:
      A = []
      A.append(kawo[i])
      if y[i,s].x > 0.5:
        for j in teams:
          if( i != j and x[i,j,s].x > 0.5):
            A.append(kawo[j])
        
        if(1 in A and 2 in A and 3 in A):
          count_3k = count_3k +1
        elif((1 in A and 2 in A) or (1 in A and 3 in A) or (2 in A and 3 in A) ):
          count_2k = count_2k +1
        elif(1 in A or 2 in A or 3 in A):
          count_1k = count_1k +1
    
  print("Es gibt %i Gänge mit Beteiligung aller Kawos" %(count_3k))
  print("Es gibt %i Gänge mit Beteiligung zweier Kawos" % (count_2k))
  print("Es gibt %i Gänge mit Beteiligung eines Kawos\n" % (count_1k))

  visualizedistributionresult.visualize(count_1k,count_2k,count_3k)

  kawo_distribution_for_team(teams, speisen, kawo, x,y)
  #print_teams_met(teams, speisen, x,y, tm)
  team_cooks_not_for_three(teams, speisen, x, y,c,d)

def team_cooks_not_for_three(teams, speisen, x,y,c,d):
  print("")
  for i in teams:
    for s in speisen:
      if(c[i,s].x > 0.5):
        A = [j for j in teams if i != j and x[i,j,s].x > 0.5]
        if (len(A) == 3):
          print("team %s cooks for three teams! " % (i))
        else:
          print("Something went wrong")
      elif(d[i,s].x > 0.5):
        A = [j for j in teams if i != j and x[i,j,s].x > 0.5]
        if (len(A) == 1):
          print("team %s cooks for one team! " % (i))
        else:
          print("Something went wrong")        

def kawo_distribution_for_team(teams, speisen, kawo, x,y):
  for i in teams:
    A = []
    #A.append(kawo[i])
    for s in speisen:
      if(y[i,s].x > 0.5):
        for j in teams:
          if(i != j and x[i,j,s].x > 0.5):
            A.append(kawo[j])
      
      for j in teams:
        if (i!= j and x[j,i,s].x > 0.5):
          A.append(kawo[j])
          for g in teams:
            if (i != g and j != g and x[j,g,s].x > 0.5):
              A.append(kawo[g])
    if((A.count(1) == 0 and kawo[i] != 1) or (A.count(2) == 0 and kawo[i] != 2) or (A.count(3) == 0 and kawo[i] != 3)):
      print("Team %s (aus dem Kawo%s) trifft auf %i Kawo1 Teams, %i Kawo2 Teams und %i Kawo3 Teams"%(i, kawo[i], A.count(1), A.count(2), A.count(3)))

def print_teams_met(teams, speisen, x,y, tm):
  print("")
  for i in teams:
    for j in teams:
      if i != j and tm[i,j].x > 0.5:
        print("Team %s trifft auf Team %s" %(i,j))

def solve(teams, zimmer, unvertraeglichkeiten, speisen, vorspeise, hauptspeise, nachspeise, kawo, p, kawo_bin, kawos):
    
  model = Model("Kawo3Rockt!")

  model.modelsense = GRB.MINIMIZE

  # variable holds if team i cooks the dish s for the team j (at the location of i), or not
  x = {}
  for i in teams:
      for j in teams: 
        if i != j:
          for s in speisen:
            x[i,j,s] = model.addVar(name = 'x_' + i + '_' + j + '_' + s , vtype = GRB.BINARY)
  
  # variable holds if team i cooks dish s or not (helper variable for easier output)
  y = {}
  for i in teams:
      for s in speisen:
          y[i,s] = model.addVar(name = 'y_' + i + '_' + s, vtype = GRB.BINARY)

  # variables that hold the value 1 if the number of guest teams of team i for dish s is three (c[i] = 1) or one (d[i] = 1)
  c = {}
  for i in teams:
    for s in speisen:
      c[i,s] = model.addVar(name = 'c_'+ i + '_' + s, vtype = GRB.BINARY)

  d = {}
  for i in teams:
    for s in speisen:
      d[i,s] = model.addVar(name = 'd_'+ i + '_' + s, vtype = GRB.BINARY)

  # variable that holds 1 if teams i and j meet twice
  mc = {}
  for i in teams:
    for j in teams:
      if i != j:
        mc[i,j] = model.addVar(name = 'mc_'+ i + '_' + j, vtype = GRB.BINARY)

  # Variable that is one if the team i meets team j at any dish
  tm = {}
  for i in teams:
    for j in teams:
      if i != j:
        tm[i,j] = model.addVar(name = "tm_" + i + "_" + j, vtype = GRB.BINARY)

  # objective function:
  model.setObjective( 100 * quicksum(c[i,s] for i in teams for s in speisen) # amount of teams having 3 other teams as guests
                    + 100 * quicksum(d[i,s] for i in teams for s in speisen) # amount of teams having 1 other team as guests
                    + quicksum(p[i,s] * y[i,s] for i in teams for s in speisen)  # teams cooking their preferred dish
                    + 400 * quicksum(mc[i,j] for i in teams for j in teams if i < j) # punish if two teams meet twice
                    + 200 * quicksum(tm[i,j] for i in teams for j in teams if i < j) # punish if a team does not meet teams of every other Kawo 
                    ) 

  model.update()  

  #Constraints:

  #model.addConstr(quicksum(x['Ersti & Ersti', j, s] + x['Die Kräuterkenner und Gewürzgarnierer', j, s] for j in teams if j != 'Ersti & Ersti' and j != 'Die Kräuterkenner und Gewürzgarnierer' for s in speisen)  == 6 )
 
  #1. Variable linking x and y. Allow a number of guest teams unequal to 2 if the number of overall teams is not dividable by 3.
  for i in teams:
    for s in speisen:
      model.addConstr(quicksum(x[i,j,s] for j in teams if i != j) ==  2* y[i,s]  + c[i,s] - d[i,s]) 
      model.addConstr(c[i,s] + d[i,s] <= y[i,s])

  #2. Every team cooks exactly one dish
  for i in teams:
    model.addConstr(quicksum(y[i,s] for s in speisen) == 1) 

  #3. Every dish is cooked by enough teams such that every team can be part of a dish as a guest. 
  # A higher value for the constant 'f' allows more solutions for unpairy team numbers, though f = 1 is sufficient for most cases
  num = number_of_teams(teams)
  for s in speisen:
    f = 1
    model.addConstr(quicksum(y[i,s] for i in teams) <= (num // 3) + f )
    model.addConstr(quicksum(y[i,s] for i in teams) >= (num // 3) - f )

  
  #4. Every team is guest for the dishes which it does not cook
  for j in teams:
    for s in speisen:
      model.addConstr(quicksum(x[i,j,s] for i in teams if i != j) == (1 - y[j,s]) )
  
  
  #5. Avoid room conflicts (only relevant in some cases where two teams want to cook at the same location). 
  # If so, do not allow the conflicting teams to cook the same dish.
  for i in teams:
    for ii in teams:
      if ( i < ii and zimmer[i] == zimmer[ii]):
        for s in speisen:
          model.addConstr(y[i,s] + y[ii,s] <= 1)
  
  #6. Try to prevent meeting a team twice
  #6a. Meeting a team at a dish from a third team implies do not cook for that team
  for i in teams:
    for j in teams:
      if (i != j):
        for g in teams:
          if (g != i and g != j):
              for s in speisen:
                for ss in speisen:
                  if (s != ss):
                    model.addConstr(x[g,i,s] + x[g,j,s] <= 2- x[i,j,ss] + mc[i,j])

  
  #6b. Meeting a team at a dish from a third team implies do not meet at a fourth team
  for i in teams:
    for j in teams:
      if (i < j):
        for g in teams:
          if (g != i and g != j):
              for s in speisen: 
                for gg in teams:
                  for ss in speisen:
                    if (g < gg and i != gg and j != gg and s != ss):
                      model.addConstr(x[g,i,s] + x[g,j,s] <= 3 - (x[gg,i,ss] + x[gg, j, ss]) + mc[i,j])
  

  #6c. If a team i has cooked for a team j, prevent that team j cooks for team i
  for i in teams:
    for j in teams:
      if i < j:
        for s in speisen:
          for ss in speisen:
            if (s != ss):
              model.addConstr(x[i,j,s] <= 1 - x[j,i,ss] + mc[i,j])

  #6d. Make the variable assignment symmetric
  for i in teams:
    for j in teams:
      if i < j:
        model.addConstr(mc[i,j] == mc[j,i])
  
  
  #7. Try to have a team meet teams of every kawo
  #7a. A team is met when cooked for it 
  for i in teams:
    for j in teams:
      for s in speisen:
        if i < j:
          model.addConstr(x[i,j,s] <= tm[i,j])

  #7b. Team i meets a team j if both are guests of team g
  for i in teams:
    for j in teams:
      for g in teams:
        if (i < j and i != g and j != g):
          for s in speisen:
            model.addConstr(x[g,j,s] <= tm[i,j] + (1 - x[g,i,s]))

  #7c. Make teams meet variable symmetric
  for i in teams:
    for j in teams:
      if i < j:
        model.addConstr(tm[i,j] == tm[j,i])

 
  #7d. The main constraint. Try to meet atleast one team of every kawo
  for i in teams:
    for k in kawos:
      model.addConstr(quicksum(kawo_bin[j,k] * tm[i,j] for j in teams if i != j) >= 1 ) #- knm[i,k])
  

  ## CONFIG
  model.setParam('TimeLimit', 30*60)

  # Optimize the model
  model.optimize()


  if model.status == GRB.OPTIMAL or True:
    print('\nOptimaler Zielfunktionswert: %g\n' % model.ObjVal)
    postprocessing(teams, speisen, kawo, x, y, p, mc,tm,c,d)

  else:
    print('Keine Optimalloesung gefunden. Status: %i' % (model.status))
  return model