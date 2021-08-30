from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jsglue import JSGlue
from sportsreference.nba.roster import Player, Roster, AbstractPlayer
from sportsreference.nba.teams import Teams
from webscraper import find_player_name, profile_info
import webscraper
import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static.players import find_players_by_full_name
from nba_api.stats.endpoints import commonallplayers
import statRankings
from datetime import timedelta
from nba_api.stats.endpoints.draftcombinestats import DraftCombineStats
from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo



app = Flask(__name__)      
jsglue = JSGlue(app)
app.secret_key = '3yxw?poY'
app.permanent_session_lifetime = timedelta(hours=2)

@app.route("/", methods=["POST", "GET"])
@app.route("/home/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        return redirect(url_for('playerhome', name=name2))

    return redirect(url_for('profile', name="Lebron James"))

# @app.route("/search/<name>/", methods=["POST", "GET"])
# def search(name):
#     p_dict = {}
#     # if request.method == "POST":
#     #     return redirect(url_for('search', name=name2))

#     find_player_name(name, p_dict)
#     print(p_dict)
#     count = 0
#     for key in p_dict.keys():
#         if p_dict[key][3].find('Yet to play in the') != -1:
#             count += 1

#     if count == len(p_dict):
#         return render_template("fail.html")
    
#     # return jsonify(p_dict, render_template('search.html'))
#     return render_template("search.html", name=name, dict=p_dict)

# @app.route("/player/<name>/", methods=["POST", "GET"])
# def playerhome(name):
#     if request.method == "POST":
#         return redirect(url_for('playerhome', name=name))

#     pdict = {}

#     find_player_name(name, pdict)
#     id = list(pdict.keys())[0]
#     if id == "None":
#         return render_template('fail.html')
#     session['api_id'] = pdict[id][4]
    

#     return render_template("playerhome.html", id=id, name=name)



@app.route("/player/profile/<name>")
def profile(name):
    # if request.method == "POST":
    #     return redirect(url_for('search', name=name))
    dict1 = {}
    if(name.find("(") != -1):
        name1 = name.split(" (")[0]
        sub = name.split(" (")[1]
        find_player_name(name1, sub, dict1)
        if(dict1):
            id1 = list(dict1.keys())[0]
            session['api_id'] = dict1[id1][4]
        else: 
            return render_template("fail.html")

    else:
        sub = "FINE"
        result = find_player_name(name, sub, dict1)
        name1 = name
        if(dict1):
            id1 = list(dict1.keys())[0]
            session['api_id'] = dict1[id1][4]
        if(result == "Ins"):
            return render_template("fail.html")
    
    class NBA_Awards:
        def __init__(self, HOF, Champ, MVP, FMVP, DPOY, AS, ROY, ASMVP,
        ScChamp, AsChamp, RbChamp, BlkChamp, StChamp, MIP, SMOY):
            self.HOF = HOF
            self.Champ = Champ
            self.MVP = MVP
            self.FMVP = FMVP
            self.DPOY = DPOY
            self.AS = AS
            self.ROY = ROY
            self.ASMVP = ASMVP
            self.ScChamp = ScChamp
            self.AsChamp = AsChamp
            self.RbChamp = RbChamp
            self.BlkChamp = BlkChamp
            self.StChamp = StChamp
            self.MIP = MIP
            self.SMOY = SMOY

    list1 = []
    personal = []
    AllNBA = []
    amateur =[]
    list_year = []
    profile_info(id1, list1, personal, AllNBA, amateur)
    
    aw = NBA_Awards(list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7], list1[8], list1[9], list1[10], list1[11], list1[12], list1[13], list1[14])
    
    ch_str = FMVP_str = MVP_str = DPOY_str= SMOY_str= ""
    if(aw.Champ != None):
        if aw.Champ.find('x') != -1:
            ch_str += '('
            for ch in list1[15]:
                if list1[15][-1] == ch:
                    ch_str += ch +')'
                else:  
                    ch_str += ch + ", "

    if(aw.FMVP != None):
        if aw.FMVP.find('x') != -1:
            FMVP_str += '('
            for f in list1[17]:
                if list1[17][-1] == f:
                    FMVP_str += f + ')'
                else:
                    FMVP_str += f + ", "

    if(aw.MVP != None):
        if aw.MVP.find('x') != -1:
            MVP_str += '('
            for m in list1[16]:
                if list1[16][-1] == m:
                    MVP_str += m + ')'
                else:
                    MVP_str += m + ", "

    if(aw.DPOY != None):
        if aw.DPOY.find('x') != -1:
            DPOY_str += '('
            for d in list1[18]:
                if list1[18][-1] == d:
                   DPOY_str += d+ ')'
                else:
                    DPOY_str += d + ", "
    
    if(aw.SMOY != None):
        if aw.SMOY.find('x') != -1:
            SMOY_str += '('
            for sm in list1[19]:
                if list1[19][-1] == sm:
                   SMOY_str += sm + ')'
                else:
                    SMOY_str += sm + ", "

    list_year.extend([ch_str, FMVP_str, MVP_str, DPOY_str, SMOY_str]) 
    TF = webscraper.image_TF(session['api_id'])
    pdb = CommonPlayerInfo(session['api_id']).get_data_frames()[0]
    return render_template('profile.html',id = id1, name=name1, aw = aw, pers=personal, AllNBA = AllNBA, 
    amateur=amateur, list_yr = list_year, api_id=session['api_id'], TF=TF, pdb=pdb)

@app.route("/player/regularseasonstats/<id>", methods=["POST", "GET"])
def regular_stats(id):
    # if request.method == "POST":
    #     return redirect(url_for('search', name=name))
    
    name = Player(id).name
    api_id = session['api_id']
    TF = webscraper.image_TF(api_id)

    try:
        if (api_id != None):
            regular_p = playercareerstats.PlayerCareerStats(player_id=api_id, 
            per_mode36='PerGame').get_data_frames()
            player_df = regular_p[0]
            player_df_career = regular_p[1]
            player_df2 = player_df.iloc[[-1]]
            player_df2_2  = player_df2.append(player_df_career)
            player_df2_2.reset_index(drop=True, inplace=True)
        else:
            player_df = pd.DataFrame()
    except KeyError:
        player_df = pd.DataFrame()

    pdb = CommonPlayerInfo(api_id).get_data_frames()[0]
    return render_template('regular_stats.html', name=name, player_df = player_df, career = player_df_career, pdf2 =player_df2_2, id=id, api_id=api_id, TF=TF, pdb=pdb)

@app.route("/player/<id>/playoffstats", methods=["POST", "GET"])
def playoff_stats(id):
    # if request.method == "POST":
    #     return redirect(url_for('search', name=name))

    name = Player(id).name
    api_id = session['api_id']
    TF = webscraper.image_TF(api_id)
    if api_id != None:
        pdf = playercareerstats.PlayerCareerStats(player_id=api_id, per_mode36='PerGame').get_data_frames()
        if len(pdf[2] != 0):
            pdf_play = pdf[2]
            pdf_play_career = pdf[3]
            pdf_accum1 = pdf_play.iloc[[-1]]
            pdf_accum = pdf_accum1.append(pdf_play_career)
            pdf_accum.reset_index(drop=True,inplace=True)
        else:
            pdf_play = pd.DataFrame()
            pdf_accum = pd.DataFrame()
            pdf_play_career = pd.DataFrame()
    else:
        pdf_play = pd.DataFrame()
        pdf_accum= pd.DataFrame()
        pdf_play_career = pd.DataFrame()

    pdb = CommonPlayerInfo(api_id).get_data_frames()[0]
    return render_template('playoffstats.html', name = name, pdf = pdf_play, pdf_total =pdf_accum, play_career=pdf_play_career, id=id, api_id=api_id, TF=TF,pdb=pdb)

@app.route("/player/<id>/earnings/", methods=["POST", "GET"])
def career_earnings(id):
    # if request.method == "POST":
    #     return redirect(url_for('search', name=name))

    name = Player(id).name
    dict = {}
    webscraper.career_earnings_contract(id, dict)

    size = len(dict['salary']) - 1
    api_id = session['api_id']
    TF = webscraper.image_TF(api_id)

    values = []
    labels = []
    labels1 = []

    if(dict['year']):
        labels.append(int(dict['year'][0][:4]))
        for p in range(1, len(dict['year'])):
            if dict['year'][p] != "Career":
                if dict['year'][p][:4] != str(labels[-1]):
                    labels.append(int(dict['year'][p][:4]))

        for k in range(0, len(dict['curyear'])):
            if str(labels[-1]) != dict['curyear'][k][:4]:
                labels1.append(int(dict['curyear'][k][:4]))

        for j in range(0, len(dict['salary'])):
            if dict['salary'][j] != dict['salary'][size]:
                rep1 = dict['salary'][j].replace(",","")
                if (rep1.find("Minimum") != -1 and dict['year'][j][:4] == str(labels[-1])):
                    continue
                elif(rep1.find('Minimum') != -1):
                    values.append(0)
                else:
                    values.append(int(rep1[1:]) / 1000000)
        

        for i in range(0, len(dict['cursalary'])):
            if str(labels[-1]) != dict['curyear'][i][:4]:
                rep = dict['cursalary'][i].replace(",","")
                values.append(int(rep[1:]) / 1000000)
        
        labels = labels + labels1

    pdb = CommonPlayerInfo(api_id).get_data_frames()[0]
    return render_template('earnings.html', name = name, dict=dict, labels1=labels, values=values, id=id, api_id = api_id, TF=TF, pdb=pdb)


@app.route("/player/<id>/advancedregular/")
def advanced_statistics_regular(id):
    # if request.method == "POST":
    #     return redirect(url_for('search', name=name))

    name = Player(id).name
    api_id = session['api_id']
    TF = webscraper.image_TF(api_id)

    dict = {}
    webscraper.advanced_statistics_r(id, dict)
    dict.update({'Season':[], 'Age': [], 'Team':[], 'GP':[]})
    statDict = {}

    if api_id != None:
        pdf = playercareerstats.PlayerCareerStats(player_id=api_id, per_mode36='PerGame').get_data_frames()
        pdf1 = playercareerstats.PlayerCareerStats(player_id=api_id, per_mode36='Totals').get_data_frames()
        for index, row in pdf[0].iterrows():
            dict['Season'].append(row['SEASON_ID'])
            dict['Age'].append(row['PLAYER_AGE'])
            dict['Team'].append(row['TEAM_ABBREVIATION'])
            dict['GP'].append(row['GP'])
        for index, row in pdf[1].iterrows():
            dict['GP'].append(row['GP'])
    
        if len(pdf[0]) != 0:
            pdf_reg = pdf[0]
            statRankings.league_avg(dict, pdf, pdf1, statDict)
            
        else:
            pdf_reg = pd.DataFrame()
            
    else:
        pdf_reg = pd.DataFrame()

    listStats = [statDict['SCR'], statDict['ASTRANK'], statDict['TSRANK'], statDict['3pEff'], statDict['RB_RANK']]
    #we got the average stats for the nba from 1974 to 2021
    pdb = CommonPlayerInfo(api_id).get_data_frames()[0]

    return render_template('advancedstatsregular.html', dict=dict, pdf_reg=pdf_reg, pdf1=pdf1, listStats=listStats, name=name, id=id, api_id=api_id, TF=TF, pdb=pdb)

if __name__ == "__main__":
    #db.create_all()
    app.run()
    # app.run(debug=True)