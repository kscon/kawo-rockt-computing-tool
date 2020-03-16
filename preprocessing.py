def preprocessing():
    teamnumber = number_of_teams(teams)
    print("\nEs gibt %i teilnehmende Teams" % (teamnumber))
    print("")

def number_of_teams(teams):
    counter = 0
    for i in teams:
        counter += 1
    return counter

