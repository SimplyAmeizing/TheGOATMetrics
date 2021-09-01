



def league_avg(dict, c1, empty_dict):
    if len(c1['FG3A']) != 0 and c1['FG3A'][0] != "":
        if (float(c1['FG3A'][0]) * float(c1['GP'][0])) > 100:
            if(float(c1['FG3_PCT'][0]) > 0.42):
                empty_dict['3pEff'] = 10
            elif(float(c1['FG3_PCT'][0]) > 0.40):
                empty_dict['3pEff'] = 9
            elif(float(c1['FG3_PCT'][0]) > 0.385):
                empty_dict['3pEff'] = 8
            elif(float(c1['FG3_PCT'][0]) > 0.37):
                empty_dict['3pEff'] = 7
            elif(float(c1['FG3_PCT'][0]) > 0.36):
                empty_dict['3pEff'] = 6
            elif(float(c1['FG3_PCT'][0]) > 0.34):
                empty_dict['3pEff'] = 5
            elif(float(c1['FG3_PCT'][0]) > 0.32):
                empty_dict['3pEff'] = 4
            elif(float(c1['FG3_PCT'][0]) > 0.3):
                empty_dict['3pEff'] = 3
            elif(float(c1['FG3_PCT'][0]) > 0.29):
                empty_dict['3pEff'] = 2
            elif(float(c1['FG3_PCT'][0]) > 0.28):
                empty_dict['3pEff'] = 1
            else:
                empty_dict['3pEff'] = 0
        else:
            empty_dict['3pEff'] = 0
    else:
        empty_dict['3pEff'] = 0
    
    count = 0
    if(len(c1['REB'][0]) != None and c1['REB'][0] != ""):
        if float(c1['REB'][0]) *  float(c1['GP'][0]) > 100:
            count += 1
            if(float(c1['REB'][0]) > 9):
                empty_dict['RB'] = 10
            elif(float(c1['REB'][0]) > 8.2):
                empty_dict['RB'] = 9
            elif(float(c1['REB'][0]) > 7.2):
                empty_dict['RB'] = 8
            elif(float(c1['REB'][0]) > 6.2):
                empty_dict['RB'] = 7
            elif(float(c1['REB'][0]) > 5.2):
                empty_dict['RB'] = 6
            elif(float(c1['REB'][0]) > 4.2):
                empty_dict['RB'] = 5
            elif(float(c1['REB'][0]) > 3.5):
                empty_dict['RB'] = 4
            elif(float(c1['REB'][0]) > 3):
                empty_dict['RB'] = 3
            elif(float(c1['REB'][0]) > 2.5):
                empty_dict['RB'] = 2
            elif(float(c1['REB'][0]) > 2):
                empty_dict['RB'] = 1
            else:
                empty_dict['RB'] = 0
            
        else:
            empty_dict['RB'] = 0
    else:
        empty_dict['RB'] = 0

    if dict['TRB'] and dict['TRB'][-1] != "":
        if float(c1['REB'][0]) * float(c1['GP'][0]) > 100:
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
        if float(c1['AST'][0]) * float(c1["GP"][0]) > 100:
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

    if(len(c1['AST'][0]) != None):
        if float(c1['AST'][0]) * float(c1["GP"][0]) > 100:
            
            count += 1
            if float(c1['AST'][0]) > 9.5:
                empty_dict['AST'] = 10
            elif float(c1['AST'][0]) > 8:
                empty_dict['AST'] = 9
            elif float(c1['AST'][0]) > 6.5:
                empty_dict['AST'] = 8
            elif float(c1['AST'][0]) > 5:
                empty_dict['AST'] = 7
            elif float(c1['AST'][0]) > 3.5:
                empty_dict['AST'] = 6
            elif float(c1['AST'][0]) > 2:
                empty_dict['AST'] = 5
            elif float(c1['AST'][0]) > 1.7:
                empty_dict['AST'] = 4
            elif float(c1['AST'][0]) > 1.4:
                empty_dict['AST'] = 3
            elif float(c1['AST'][0]) > 1.1:
                empty_dict['AST'] = 2
            elif float(c1['AST'][0]) > 0.8:
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
        if(c1['GP'] != 0):
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

    if(c1['PTS'][0] != None and c1['FG_PCT'][0] != None and c1['FT_PCT'][0] != None):
    
        if float(c1['PTS'][0]) > 25:
            empty_dict["PTS"] = 10
        elif float(c1['PTS'][0]) > 22:
            empty_dict['PTS'] = 9
        elif float(c1['PTS'][0]) > 19:
            empty_dict['PTS'] = 8
        elif float(c1['PTS'][0]) > 16:
            empty_dict['PTS'] = 7
        elif float(c1['PTS'][0]) > 13:
            empty_dict['PTS'] = 6
        elif float(c1['PTS'][0]) > 10:
            empty_dict['PTS'] = 5
        elif float(c1['PTS'][0]) > 8:
            empty_dict['PTS'] = 4
        elif float(c1['PTS'][0]) > 6:
            empty_dict['PTS'] = 3
        elif float(c1['PTS'][0]) > 4:
            empty_dict['PTS'] = 2
        elif float(c1['PTS'][0]) > 2:
            empty_dict['PTS'] = 1
        else:
            empty_dict['PTS']=0

        if float(c1['FG_PCT'][0]) > .51:
            empty_dict['FG'] = 10
        elif float(c1['FG_PCT'][0]) >.50:
            empty_dict['FG'] = 9
        elif float(c1['FG_PCT'][0]) >.49:
            empty_dict['FG'] = 8
        elif float(c1['FG_PCT'][0]) >.48:
            empty_dict['FG'] = 7
        elif float(c1['FG_PCT'][0]) >.47:
            empty_dict['FG'] = 6
        elif float(c1['FG_PCT'][0]) >.46:
            empty_dict['FG'] = 5
        elif float(c1['FG_PCT'][0]) >.45:
            empty_dict['FG'] = 4
        elif float(c1['FG_PCT'][0]) >.43:
            empty_dict['FG'] = 3
        elif float(c1['FG_PCT'][0]) >.42:
            empty_dict['FG'] = 2
        elif float(c1['FG_PCT'][0]) >.41:
            empty_dict['FG'] = 1
        else:
            empty_dict['FG'] = 0

        if float(c1['FT_PCT'][0]) > .89:
            empty_dict['FT'] = 10
        elif float(c1['FT_PCT'][0]) > .86:
            empty_dict['FT'] = 9
        elif float(c1['FT_PCT'][0]) > .83:
            empty_dict['FT'] = 8
        elif float(c1['FT_PCT'][0]) > .80:
            empty_dict['FT'] = 7
        elif float(c1['FT_PCT'][0]) > .77:
            empty_dict['FT'] = 6
        elif float(c1['FT_PCT'][0]) > .74:
            empty_dict['FT'] = 5
        elif float(c1['FT_PCT'][0]) > .71:
            empty_dict['FT'] = 4
        elif float(c1['FT_PCT'][0]) > .68:
            empty_dict['FT'] = 3
        elif float(c1['FT_PCT'][0]) > .65:
            empty_dict['FT'] = 2
        elif float(c1['FT_PCT'][0]) > .62:
            empty_dict['FT'] = 1
        else:
            empty_dict['FT'] = 0

        empty_dict['SCR'] = empty_dict['PTS'] * 0.7 + empty_dict['FG'] * 0.2 + empty_dict['FT'] * .1
    else:
        empty_dict["SCR"] = 0
    
    return None