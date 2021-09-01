from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify, current_app, json
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
from nba_api.stats.endpoints.draftcombinestats import DraftCombineStats


app = Flask(__name__)      
app.secret_key = '3yxw?poY'
app.permanent_session_lifetime = timedelta(hours=2)


@app.route("/")
@app.route("/home/")
def home():
    return redirect(url_for('profile', name="LeBron James"))

@app.route("/player/profile/<name>")
def profile(name):
    # if request.method == "POST":
    #     return redirect(url_for('search', name=name))
    with open('nbanames.json', 'r') as file:
        nba_all = json.load(file)
    with open('dopple.json', "r") as file:
        dopple = json.load(file)

    dict1 = {}
    if(name.find("(") != -1):
        name1 = name.split(" (")[0]
        sub = name.split(" (")[1]
        find_player_name(name1, sub, dict1, nba_all, dopple)
        if(dict1):
            id1 = list(dict1.keys())[0]
            session['api_id'] = dict1[id1][4]
        else: 
            return render_template("fail.html")

    else:
        sub = "FINE"
        result = find_player_name(name, sub, dict1, nba_all, dopple)
        name1 = name
        if(dict1):
            id1 = list(dict1.keys())[0]
            session['api_id'] = dict1[id1][4]
        else:
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
    dictf = {}
    webscraper.find_profile_info(id1, dictf)
    pdb = dictf

    return render_template('profile.html',id = id1, name=name1, aw = aw, pers=personal, AllNBA = AllNBA, 
    amateur=amateur, list_yr = list_year, api_id=session['api_id'], TF=TF, pdb = dictf)



@app.route("/player/regularseasonstats/<id>")
def regular_stats(id):
    # if request.method == "POST":
    #     return redirect(url_for('search', name=name))
    
    name = Player(id).name
    api_id = session['api_id']
    TF = webscraper.image_TF(api_id)
    dict1 = {}
    c1 = {}

    if api_id != None:
        webscraper.find_reg_stats_scrape(id, dict1, c1)

    ls ={}
    pdb = webscraper.find_profile_info(id, ls)
    
    return render_template('regular_stats.html', name=name, dict=dict1, career=c1, id=id, api_id=api_id, TF=TF, pdb=pdb)

@app.route("/player/<id>/playoffstats")
def playoff_stats(id):
    # if request.method == "POST":
    #     return redirect(url_for('search', name=name))

    name = Player(id).name
    api_id = session['api_id']
    TF = webscraper.image_TF(api_id)
    dict1 = {}
    c1 = {}

    if api_id != None:
        webscraper.find_play_stats_scrape(id, dict1, c1)

    ls ={}
    pdb = webscraper.find_profile_info(id, ls)
    
    return render_template('playoffstats.html', name=name, dict=dict1, career=c1, id=id, api_id=api_id, TF=TF, pdb=pdb)

@app.route("/player/<id>/earnings/")
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

    d1 = {}
    pdb = webscraper.find_profile_info(id, d1)
    return render_template('earnings.html', name = name, dict=dict, labels1=labels, values=values, id=id, api_id = api_id, TF=TF, pdb=pdb)


@app.route("/player/<id>/advancedregular/")
def advanced_statistics_regular(id):
    # if request.method == "POST":
    #     return redirect(url_for('search', name=name))

    name = Player(id).name
    api_id = session['api_id']
    TF = webscraper.image_TF(api_id)

    dict = {}
    dict1= {}
    c1 = {}
    webscraper.advanced_statistics_r(id, dict)
    statDict = {}

    if api_id != None:
        if len(dict['Season'][-1]) != 0:
            webscraper.find_reg_stats_scrape(id, dict1, c1)
            statRankings.league_avg(dict, c1, statDict)
            
        else:
            dict = dict

    listStats = [statDict['SCR'], statDict['ASTRANK'], statDict['TSRANK'], statDict['3pEff'], statDict['RB_RANK']]
    #we got the average stats for the nba from 1974 to 2021
    ls = {}
    pdb = webscraper.find_profile_info(id, ls)

    return render_template('advancedstatsregular.html', dict=dict, listStats=listStats, name=name, id=id, api_id=api_id, TF=TF, pdb=pdb)

if __name__ == "__main__":
    #db.create_all()
    # app.run()
    app.run(debug=True)