



def league_avg(dict, pdf, pdf1, empty_dict):
    if pdf[1]['FG3A'][0] != None:
        if int(pdf1[1]['FG3A']) > 100:
            if(float(pdf[1]['FG3_PCT']) > 0.42):
                empty_dict['3pEff'] = 10
            elif(float(pdf[1]['FG3_PCT']) > 0.40):
                empty_dict['3pEff'] = 9
            elif(float(pdf[1]['FG3_PCT']) > 0.385):
                empty_dict['3pEff'] = 8
            elif(float(pdf[1]['FG3_PCT']) > 0.37):
                empty_dict['3pEff'] = 7
            elif(float(pdf[1]['FG3_PCT']) > 0.36):
                empty_dict['3pEff'] = 6
            elif(float(pdf[1]['FG3_PCT']) > 0.34):
                empty_dict['3pEff'] = 5
            elif(float(pdf[1]['FG3_PCT']) > 0.32):
                empty_dict['3pEff'] = 4
            elif(float(pdf[1]['FG3_PCT']) > 0.3):
                empty_dict['3pEff'] = 3
            elif(float(pdf[1]['FG3_PCT']) > 0.29):
                empty_dict['3pEff'] = 2
            elif(float(pdf[1]['FG3_PCT']) > 0.28):
                empty_dict['3pEff'] = 1
            else:
                empty_dict['3pEff'] = 0
        else:
            empty_dict['3pEff'] = 0
    else:
        empty_dict['3pEff'] = 0

    count = 0
    if(pdf1[1]['REB'][0] != None):
        if int(pdf1[1]['REB']) > 100:
            count += 1
            if(float(pdf[1]['REB']) > 9):
                empty_dict['RB'] = 10
            elif(float(pdf[1]['REB']) > 8.2):
                empty_dict['RB'] = 9
            elif(float(pdf[1]['REB']) > 7.2):
                empty_dict['RB'] = 8
            elif(float(pdf[1]['REB']) > 6.2):
                empty_dict['RB'] = 7
            elif(float(pdf[1]['REB']) > 5.2):
                empty_dict['RB'] = 6
            elif(float(pdf[1]['REB']) > 4.2):
                empty_dict['RB'] = 5
            elif(float(pdf[1]['REB']) > 3.5):
                empty_dict['RB'] = 4
            elif(float(pdf[1]['REB']) > 3):
                empty_dict['RB'] = 3
            elif(float(pdf[1]['REB']) > 2.5):
                empty_dict['RB'] = 2
            elif(float(pdf[1]['REB']) > 2):
                empty_dict['RB'] = 1
            else:
                empty_dict['RB'] = 0
            
        else:
            empty_dict['RB'] = 0
    else:
        empty_dict['RB'] = 0

    if dict['TRB'][-1] != "" and dict['TRB']:
        if int(pdf1[1]['REB']) > 100:
            count += 1
            if(float(dict['TRB'][-1]) > 15):
                empty_dict['RB%'] = 10
            elif(float(dict['TRB'][-1]) > 14):
                empty_dict['RB%'] = 9
            elif(float(dict['TRB'][-1]) > 13):
                empty_dict['RB%'] = 8
            elif(float(dict['TRB'][-1]) > 12):
                empty_dict['RB%'] = 7
            elif(float(dict['TRB'][-1]) > 11):
                empty_dict['RB%'] = 6
            elif(float(dict['TRB'][-1]) > 10):
                empty_dict['RB%'] = 5
            elif(float(dict['TRB'][-1]) > 9):
                empty_dict['RB%'] = 4
            elif(float(dict['TRB'][-1]) > 8):
                empty_dict['RB%'] = 3
            elif(float(dict['TRB'][-1]) > 7):
                empty_dict['RB%'] = 2
            elif(float(dict['TRB'][-1]) > 6):
                empty_dict['RB%'] = 1
            else:
                empty_dict['RB%'] = 0
            
        else:
            empty_dict['RB%'] = 0
    else:
        empty_dict['RB%'] = 0

    if(count != 0):
        empty_dict['RB_RANK'] = (empty_dict['RB'] + empty_dict['RB%']) / count
    else:
        empty_dict['RB_RANK'] = 0
    
    count = 0
    if(dict['AST'][-1] != "" and dict['AST']):
        if int(pdf1[1]['AST'] > 100):
            count += 1
            if(float(dict['AST'][-1]) > 29):
                empty_dict['AST%'] = 10
            elif(float(dict['AST'][-1]) > 26):
                empty_dict['AST%'] = 9
            elif(float(dict['AST'][-1]) > 23):
                empty_dict['AST%'] = 8
            elif(float(dict['AST'][-1]) > 20):
                empty_dict['AST%'] = 7
            elif(float(dict['AST'][-1]) > 17):
                empty_dict['AST%'] = 6
            elif(float(dict['AST'][-1]) > 14):
                empty_dict['AST%'] = 5
            elif(float(dict['AST'][-1]) > 12):
                empty_dict['AST%'] = 4
            elif(float(dict['AST'][-1]) > 10):
                empty_dict['AST%'] = 3
            elif(float(dict['AST'][-1]) > 8):
                empty_dict['AST%'] = 2
            elif(float(dict['AST'][-1]) > 6):
                empty_dict['AST%'] = 1
            else:
                empty_dict['AST%'] = 0
        else:
            empty_dict['AST%'] = 0
    else:
        empty_dict['AST%'] = 0

    if(pdf1[1]['AST'][0] != None):
        if int(pdf1[1]['AST'] > 100):
            count += 1
            if float(pdf[1]['AST']) > 9.5:
                empty_dict['AST'] = 10
            elif float(pdf[1]['AST']) > 8:
                empty_dict['AST'] = 9
            elif float(pdf[1]['AST']) > 6.5:
                empty_dict['AST'] = 8
            elif float(pdf[1]['AST']) > 5:
                empty_dict['AST'] = 7
            elif float(pdf[1]['AST']) > 3.5:
                empty_dict['AST'] = 6
            elif float(pdf[1]['AST']) > 2:
                empty_dict['AST'] = 5
            elif float(pdf[1]['AST']) > 1.7:
                empty_dict['AST'] = 4
            elif float(pdf[1]['AST']) > 1.4:
                empty_dict['AST'] = 3
            elif float(pdf[1]['AST']) > 1.1:
                empty_dict['AST'] = 2
            elif float(pdf[1]['AST']) > 0.8:
                empty_dict['AST'] = 1
            else:
                empty_dict['AST'] = 0
        else:
            empty_dict['AST'] = 0
    else:
        empty_dict['AST'] = 0

    if count != 0:
        empty_dict['ASTRANK'] = (empty_dict['AST'] + empty_dict['AST%']) / 2
    else:
        empty_dict["ASTRANK"] = 0

    if(dict['TS'] and dict['TS'][-1] != ""):
        if int(pdf1[1]['GP'] > 100):
            if float(dict['TS'][-1]) > .62:
                empty_dict['TSRANK'] = 10
            elif float(dict['TS'][-1]) > .60:
                empty_dict['TSRANK'] = 9
            elif float(dict['TS'][-1]) > .58:
                empty_dict['TSRANK'] = 8
            elif float(dict['TS'][-1]) > .56:
                empty_dict['TSRANK'] = 7
            elif float(dict['TS'][-1]) > .54:
                empty_dict['TSRANK'] = 6
            elif float(dict['TS'][-1]) > .52:
                empty_dict['TSRANK'] = 5
            elif float(dict['TS'][-1]) > .50:
                empty_dict['TSRANK'] = 4
            elif float(dict['TS'][-1]) > .48:
                empty_dict['TSRANK'] = 3
            elif float(dict['TS'][-1]) > .46:
                empty_dict['TSRANK'] = 2
            elif float(dict['TS'][-1]) > .44:
                empty_dict['TSRANK'] = 1
            else:
                empty_dict['TSRANK'] = 0
        else:
            empty_dict['TSRANK'] = 0
    else:
        empty_dict['TSRANK'] = 0

    if(pdf[1]['PTS'][0] != None and pdf[1]['FG_PCT'][0] != None and pdf[1]['FT_PCT'][0] != None):
    
        if float(pdf[1]['PTS']) > 25:
            empty_dict["PTS"] = 10
        elif float(pdf[1]['PTS']) > 22:
            empty_dict['PTS'] = 9
        elif float(pdf[1]['PTS']) > 19:
            empty_dict['PTS'] = 8
        elif float(pdf[1]['PTS']) > 16:
            empty_dict['PTS'] = 7
        elif float(pdf[1]['PTS']) > 13:
            empty_dict['PTS'] = 6
        elif float(pdf[1]['PTS']) > 10:
            empty_dict['PTS'] = 5
        elif float(pdf[1]['PTS']) > 8:
            empty_dict['PTS'] = 4
        elif float(pdf[1]['PTS']) > 6:
            empty_dict['PTS'] = 3
        elif float(pdf[1]['PTS']) > 4:
            empty_dict['PTS'] = 2
        elif float(pdf[1]['PTS']) > 2:
            empty_dict['PTS'] = 1
        else:
            empty_dict['PTS']=0

        if float(pdf[1]['FG_PCT']) > .51:
            empty_dict['FG'] = 10
        elif float(pdf[1]['FG_PCT']) >.50:
            empty_dict['FG'] = 9
        elif float(pdf[1]['FG_PCT']) >.49:
            empty_dict['FG'] = 8
        elif float(pdf[1]['FG_PCT']) >.48:
            empty_dict['FG'] = 7
        elif float(pdf[1]['FG_PCT']) >.47:
            empty_dict['FG'] = 6
        elif float(pdf[1]['FG_PCT']) >.46:
            empty_dict['FG'] = 5
        elif float(pdf[1]['FG_PCT']) >.45:
            empty_dict['FG'] = 4
        elif float(pdf[1]['FG_PCT']) >.43:
            empty_dict['FG'] = 3
        elif float(pdf[1]['FG_PCT']) >.42:
            empty_dict['FG'] = 2
        elif float(pdf[1]['FG_PCT']) >.41:
            empty_dict['FG'] = 1
        else:
            empty_dict['FG'] = 0

        if float(pdf[1]['FT_PCT']) > .89:
            empty_dict['FT'] = 10
        elif float(pdf[1]['FT_PCT']) > .86:
            empty_dict['FT'] = 9
        elif float(pdf[1]['FT_PCT']) > .83:
            empty_dict['FT'] = 8
        elif float(pdf[1]['FT_PCT']) > .80:
            empty_dict['FT'] = 7
        elif float(pdf[1]['FT_PCT']) > .77:
            empty_dict['FT'] = 6
        elif float(pdf[1]['FT_PCT']) > .74:
            empty_dict['FT'] = 5
        elif float(pdf[1]['FT_PCT']) > .71:
            empty_dict['FT'] = 4
        elif float(pdf[1]['FT_PCT']) > .68:
            empty_dict['FT'] = 3
        elif float(pdf[1]['FT_PCT']) > .65:
            empty_dict['FT'] = 2
        elif float(pdf[1]['FT_PCT']) > .62:
            empty_dict['FT'] = 1
        else:
            empty_dict['FT'] = 0

        empty_dict['SCR'] = empty_dict['PTS'] * 0.7 + empty_dict['FG'] * 0.2 + empty_dict['FT'] * .1

    else:
        empty_dict["SCR"] = 0
    
    return None