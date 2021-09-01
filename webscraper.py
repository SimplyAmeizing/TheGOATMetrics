import requests, string
from bs4 import BeautifulSoup, Comment
from flask import Blueprint, render_template, json, request
from sportsreference.nba.roster import Player
import re
from nba_api.stats.static.players import find_players_by_full_name
from nba_api.stats.endpoints.commonallplayers import CommonAllPlayers
from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
from unidecode import unidecode
import time
import requests
from urllib.request import Request, urlopen
from selenium import webdriver

custom_headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}


# webscraper = Blueprint("webscraper", __name__, static_folder ="static", template_folder="template")
# def find_every_player(dict, dopple):
#     d = {}
#     other = []
#     # db = CommonAllPlayers().get_data_frames()[0]
#     with open('nbanames.json', 'r') as file:
#         nba_all = json.load(file)
#     for x in nba_all:
#         dict[nba_all[x]] = {PlayerCareerStats(player_id=nba_all[x]).get_data_frames()[0]}
#     return dict


def image_TF(api_id):
    URL = 'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/' + api_id + '.png'
    r = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'html.parser')

    if soup.find('code') == None:
        return True

    return False

def find_profile_info(id, ls):
    URL = ("https://www.basketball-reference.com/players/")
    first_initial = id[0]
    r = requests.get(URL + first_initial + '/' + id + ".html")
    soup = BeautifulSoup(r.text, "html.parser")

    b = soup.find('div', itemtype = "https://schema.org/Person")
    count = 0

    for y in b.find_all('p'):
        if (y.get_text().find("Position") != -1):
            pos = y.get_text().split(' ▪')[0].replace("\n", "")
            pos = pos.replace('Position:', "")
            pos = pos.replace("   ", "")
            ls['position'] = pos
            
            continue
        elif (y.get_text().find("cm") != -1 and y.get_text().find("kg") != -1):
            ls['htwt'] = y.get_text().replace('\xa0', " ")
    
    c = soup.find('a', href=True, class_='poptip default')
    c = c.get_text().replace('\n', "")
    c = c.replace('     ', '')
    ls['number'] = c
    return ls



def find_player_name(name, sub, name_list, nl, d):
    URL = 'https://www.basketball-reference.com/search/search.fcgi?search='
  
    r = requests.get(URL + name)
    soup = BeautifulSoup(r.text, 'html.parser')

    p1 = soup.find('div', id='players', class_='current')
    if p1 == None:
        find_player_name_hard(name, name_list, nl)
        return None
    p = p1.find_all('div', {'class': 'search-item'})
    check = []
    # player_db = CommonPlayerInfo('203507').get_data_frames()[0]
    
    for name_filler in p:
        api_id = None
        api_full = []
        n = name_filler.find('a', href=True).get_text()
        id1 = name_filler.find('div',{'class':'search-item-url'})
        id = id1.get_text()[11:-5]
        current_status = name_filler.find('div',{'class':'search-item-team'})       

        if current_status != None:
            status1 = current_status.get_text()
            if status1.find("Last played for") == -1:
                status = status1.replace(":", "")
            else:
                status = "Retired"
        else:
            status = "Yet to play in the NBA" 

        if(n.find('(') != -1 ):
            first=n.find("(")
            sec = n.find(')')
            n1 = n.replace(n[first+1:sec], "")
            year = int(n[first+1:first+5])
            year = str(year -1)
            n1 = n1[:-3]

            
            if (n1 + "^" + sub[0:4]) in d:
                if(year == sub[0:4]):
                    api_id = d[name + "^" + year]
                    name_list.update({id:[n, None, None, status, api_id]})
                    break

            else:
                if(sub[0].isdigit() == False and n1.lower() == name.lower()):
                    api_id = nl[name]
                    name_list.update({id:[n, None, None, status, api_id]})    
                    break                    

                elif sub[0].isdigit() and n1.lower() == name.lower():
                    api_id = nl[name]
                    name_list.update({id:[n, None, None, status, api_id]})
                    break

                elif sub == "FINE" and (n1.lower() == name.lower() or n1.replace('.', "").lower() == name.lower()):
                    api_id = nl[name]
                    name_list.update({id:[n, None, None, status, api_id]})
                    break


def profile_info(id, list, personal, AllNBA, amateur):
    URL = ("https://www.basketball-reference.com/players/")
    first_initial = id[0]
    r = requests.get(URL + first_initial + '/' + id + ".html")
    soup = BeautifulSoup(r.text, "html.parser")

    a = soup.find('ul',{'id':'bling'})
    
    HOF = Champ = MVP = FMVP = AS = DPOY = ROY = ASMVP = ScChamp = StChamp = None
    AsChamp = RbChamp = BlkChamp = MIP = SMOY = All_Rookie = None
    
    if a != None:
        for x in a.find_all('li'):
            if x.get_text().find("Hall of Fame") != -1:
                HOF = x.get_text()
            elif x.get_text().find("NBA Champ") != -1:
                Champ = x.get_text()
            elif x.get_text().find("MVP") != -1 and x.get_text().find("AS MVP")==-1 and x.get_text().find("Finals MVP")==-1:
                MVP = x.get_text()
            elif x.get_text().find("Finals MVP") != -1:
                FMVP = x.get_text()
            elif x.get_text().find("All Star") != -1:
                AS = x.get_text()
            elif x.get_text().find("Def. POY") != -1:
                DPOY = x.get_text()
            elif x.get_text().find("ROY") != -1:
                ROY = x.get_text()
            elif x.get_text().find("AS MVP") != -1:
                ASMVP = x.get_text()
            elif x.get_text().find("Scoring Champ") != -1:
                ScChamp = x.get_text()
            elif x.get_text().find("STL Champ") != -1:
                StChamp = x.get_text()
            elif x.get_text().find("AST Champ") != -1:
                AsChamp = x.get_text()
            elif x.get_text().find("TRB Champ") != -1:
                RbChamp = x.get_text()
            elif x.get_text().find("BLK Champ") != -1:
                BlkChamp = x.get_text()
            elif x.get_text().find("Most Improved") != -1:
                MIP = x.get_text()
            elif x.get_text().find("Sixth Man") != -1:
                SMOY = x.get_text()
            elif x.get_text().find('All-Rookie') != -1:
                All_Rookie = x.get_text()

    list.extend([HOF, Champ, MVP, FMVP, DPOY, AS, ROY, ASMVP, ScChamp, AsChamp, RbChamp, BlkChamp, StChamp, MIP, SMOY])
        
    b = soup.find('div', itemtype = "https://schema.org/Person")
    count = 0
    if b == None:
        return "Ins"

    for y in b.find_all('p'):
        if (count == 1 and y.get_text().find("Position") != -1):
            personal.append("None")
            personal.append(y.get_text())
            continue
        if(y.get_text().find("Pronunciation") != -1):
            continue
        elif(y.get_text().find("Relatives") != -1):
            continue
        elif(y.get_text().find("NBA Debut") != -1):
            continue
        elif(y.get_text().find("Hall of Fame") != -1):
            continue
        elif(y.get_text().find("Career Length") != -1 or y.get_text().find("Experience") != -1 ):
            continue
        elif(y.get_text().find("Recruiting Rank") != -1):
            continue 
        elif(y.get_text().find("born") != -1):
            continue    
        count += 1
        personal.append(y.get_text())

    c = soup.find('div',{'class':'leaderboard_wrapper','id':'all_leaderboard'})

    a_count1 = a_count2 = a_count3 = 0
    d_count1 = d_count2 = 0
    r_count1 = r_count2 = 0
    MVP_yr_list = []
    FMVP_yr_list = []
    DPOY_yr_list = []
    SMOY_yr_list = []
    champ_yr_list = []
    
    if c!= None:
        for comment in c(text=lambda text: isinstance(text, Comment)):
            if('div class="data_grid"' in comment.string):
                tag = BeautifulSoup(comment, 'html.parser')
                comment.replace_with(tag)
                break

        c4 = c.find('div', id="leaderboard_championships")
        if c4 != None:
            for z3 in c4.find_all('td', class_='single'):
                if(z3.get_text().find('NBA') != -1):
                    champ_yr_list.append(z3.get_text()[0:4])


        c1 = c.find('div',id="leaderboard_notable-awards")
        if c1 != None:
            for z in c1.find_all('td', class_='single'):
                s = z.get_text()
                if(s.find('Sporting News') != -1):
                    continue
                elif(s.find('All-Star') == -1 and s.find('Finals') == -1 and s.find('Most Valuable Player') != -1):
                    MVP_yr = s[0:2] + s[5:7]
                    MVP_yr_list.append(MVP_yr)
                elif(s.find('Finals Most Valuable Player') != -1):
                    FMVP_yr = s[0:4]
                    FMVP_yr_list.append(FMVP_yr)
                elif(s.find('Defensive Player of the Year') != -1):
                    DPOY_yr = s[0:2] + s[5:7]
                    DPOY_yr_list.append(DPOY_yr)
                elif(s.find('Sixth Man of the Year') != -1):
                    SMOY_yr = s[0:2] + s[5:7]
                    SMOY_yr_list.append(SMOY_yr)
        

        c2 = c.find('div', id='leaderboard_all_league')
        if c2 != None:
            for z1 in c2.find_all('td',class_="single"):
                sel = z1.get_text()
                if(sel.find("All-NBA (1st)") != -1):
                    a_count1 += 1
                elif(sel.find("All-NBA (2nd)") != -1):
                    a_count2 += 1
                elif(sel.find("All-NBA (3rd)") != -1):
                    a_count3 += 1
                elif(sel.find("All-NBA (3rd)") != -1):
                    a_count3 += 1
                elif(sel.find("All-Defensive (1st)") != -1):
                    d_count1 += 1
                elif(sel.find("All-Defensive (2nd)") != -1):
                    d_count2 += 1
                elif(sel.find("All-Rookie (1st)") != -1):
                    r_count1 += 1
                elif(sel.find("All-Rookie (2nd)") != -1):
                    r_count2 += 1

        c3 = c.find('div', id="leaderboard_amateur-honors")
        if c3 != None:
            for z2 in c3.find_all('td', class_='single'):
                amateur.append(z2.get_text())
        
    AllNBA.extend([a_count1, a_count2, a_count3, d_count1, d_count2, All_Rookie, r_count1, r_count2])
    list.extend([champ_yr_list, MVP_yr_list, FMVP_yr_list, DPOY_yr_list, SMOY_yr_list,])


def find_player_name_hard(name, name_list, nl):
    n1 = name.split(" ")
    if len(n1[1]) > 5:
        if n1[1].find("-") != -1:
            n1[1] = n1[1].replace("-", "")
        if n1[0].find("-") != -1:
            n1[0] = n1[0].replace("-", "")
        if n1[1].find('.') != -1:
            n1[0] = n1[1].replace(".", "")
        if n1[0].find('.')!= -1:
            n1[0] = n1[0].replace(".", "")
        id = n1[1][0:5] + n1[0][0:2] + "01"
    else:
        if n1[1].find("-")!= -1:
            n1[1] = n1[1].replace("-", "")
        if n1[0].find("-")!= -1:
            n1[0] = n1[0].replace("-", "")
        if n1[1].find('.')!= -1:
            n1[1] = n1[1].replace(".", "")
        if n1[0].find('.')!= -1:
            n1[0] = n1[0].replace(".", "")
        id = n1[1] + n1[0][0:2] + "01"

    id = id.lower()
    api_id = nl[name]
    name_list.update({id:[name, None, None, None, api_id]})


def career_earnings_contract(id, dict):
    URL = ("https://www.basketball-reference.com/players/")
    first_initial = id[0]
    r = requests.get(URL + first_initial + '/' + id + ".html")
    soup = BeautifulSoup(r.text, "html.parser")
    dict.update({'year':[], 'team':[], 'salary':[], 'curyear':[], 'curteam':[], 'cursalary':[]})

    for comments in soup.find_all(text=lambda text:isinstance(text, Comment)):
        comments_soup = BeautifulSoup(comments, "html.parser")
        com = comments_soup.find(id='div_all_salaries')
        com1 = comments_soup.find(id='div_contract')
        if com != None:
            if(com.find_all('tr') != None):
                for c in com.find_all('tr'):
                    if(c.find('th',{'scope':'row','class':'left','data-stat':'season'}) != None):
                        dict['year'].append(c.find('th',{'scope':'row','class':'left','data-stat':'season'}).get_text())
                    if(c.find('td',{'data-stat':'team_name'}) != None):
                        dict['team'].append(c.find('td',{'data-stat':'team_name'}).get_text())
                    if(c.find('td',{'data-stat':'salary'}) != None):
                        dict['salary'].append(c.find('td',{'data-stat':'salary'}).get_text())
        if com1 != None:
            c1 = com1.find('table', class_=True)
            if(c1 != None):
                for c2 in c1.find_all('th'):
                    if(c2.get_text() != "Team"):
                        dict['curyear'].append(c2.get_text())
                for c3 in c1.find_all('td'):
                    if(c3.find('span', class_=True)):
                        dict['cursalary'].append(c3.get_text())
                    elif c3.find('a', href=True):
                        dict['curteam'].append(c3.get_text())
        
    return dict

def advanced_statistics_r(id, dict):
    URL = ("https://www.basketball-reference.com/players/")
    first_initial = id[0]
    r = requests.get(URL + first_initial + '/' + id + ".html")
    soup = BeautifulSoup(r.text, "html.parser")

    dict.update({'Season':[], 'Age':[],'Team':[],'GP':[],'PER':[], 'TS':[], 'ORB':[], 'DRB':[], 'TRB':[], 'AST':[], 'STL':[], 'BLK':[], 'TOV':[], 'USG':[], 'OWS':[], 'DWS':[], 'WS':[],
    'OBxPM':[], 'DBxPM':[], 'BxPM':[], 'VORP':[]})
    
    a = soup.find('div', id="all_advanced-playoffs_advanced")
    b = a.find('table',class_="stats_table sortable row_summable", id='advanced')
    for ad in b.find('tbody').find_all('tr'):
        if ad.find('th', {'data-stat':'season'}):
            dict['Season'].append(ad.find('th', {'data-stat':'season'}).get_text())
        if ad.find('td', {'data-stat':'age'}):
            dict['Age'].append(ad.find('td', {'data-stat':'age'}).get_text())
        if ad.find('td', {'data-stat':'team_id'}):
            dict['Team'].append(ad.find('td', {'data-stat':'team_id'}).get_text())
        if ad.find('td', {'data-stat':'g'}):
            dict['GP'].append(ad.find('td', {'data-stat':'g'}).get_text())
        if ad.find('td',{'data-stat':'per'}):
            dict['PER'].append(ad.find('td',{'data-stat':'per'}).get_text())
        if ad.find('td',{'data-stat':'ts_pct'}):
            dict['TS'].append(ad.find('td',{'data-stat':'ts_pct'}).get_text())
        if ad.find('td',{'data-stat':'orb_pct'}):
            dict['ORB'].append(ad.find('td',{'data-stat':'orb_pct'}).get_text())
        if ad.find('td',{'data-stat':'drb_pct'}):
            dict['DRB'].append(ad.find('td',{'data-stat':'drb_pct'}).get_text())
        if ad.find('td',{'data-stat':'trb_pct'}):
            dict['TRB'].append(ad.find('td',{'data-stat':'trb_pct'}).get_text())
        if ad.find('td',{'data-stat':'ast_pct'}):
            dict['AST'].append(ad.find('td',{'data-stat':'ast_pct'}).get_text())
        if ad.find('td',{'data-stat':'stl_pct'}):
            dict['STL'].append(ad.find('td',{'data-stat':'stl_pct'}).get_text())
        if ad.find('td',{'data-stat':'blk_pct'}):
            dict['BLK'].append(ad.find('td',{'data-stat':'blk_pct'}).get_text())
        if ad.find('td',{'data-stat':'tov_pct'}):
            dict['TOV'].append(ad.find('td',{'data-stat':'tov_pct'}).get_text())
        if ad.find('td',{'data-stat':'usg_pct'}):
            dict['USG'].append(ad.find('td',{'data-stat':'usg_pct'}).get_text())
        if ad.find('td',{'data-stat':'ows'}):
            dict['OWS'].append(ad.find('td',{'data-stat':'ows'}).get_text())
        if ad.find('td',{'data-stat':'dws'}):
            dict['DWS'].append(ad.find('td',{'data-stat':'dws'}).get_text())    
        if ad.find('td',{'data-stat':'ws'}):
            dict['WS'].append(ad.find('td',{'data-stat':'ws'}).get_text())
        if ad.find('td',{'data-stat':'obpm'}):
            dict['OBxPM'].append(ad.find('td',{'data-stat':'obpm'}).get_text())
        if ad.find('td',{'data-stat':'dbpm'}):
            dict['DBxPM'].append(ad.find('td',{'data-stat':'dbpm'}).get_text())
        if ad.find('td',{'data-stat':'bpm'}):
            dict['BxPM'].append(ad.find('td',{'data-stat':'bpm'}).get_text())
        if ad.find('td',{'data-stat':'vorp'}):
            dict['VORP'].append(ad.find('td',{'data-stat':'vorp'}).get_text())
    
    ad2 = b.find('tfoot')
    ad1 = ad2.find('tr')
    if(ad1.find('td', {'data-stat':'g'})):
        dict['GP'].append(ad1.find('td',{'data-stat':'g'}).get_text())
    if(ad1.find('td', {'data-stat':'per'})):
        dict['PER'].append(ad1.find('td',{'data-stat':'per'}).get_text())
    if ad1.find('td',{'data-stat':'ts_pct'}):
        dict['TS'].append(ad1.find('td',{'data-stat':'ts_pct'}).get_text())
    if ad1.find('td',{'data-stat':'orb_pct'}):
        dict['ORB'].append(ad1.find('td',{'data-stat':'orb_pct'}).get_text())
    if ad1.find('td',{'data-stat':'drb_pct'}):
        dict['DRB'].append(ad1.find('td',{'data-stat':'drb_pct'}).get_text())
    if ad1.find('td',{'data-stat':'trb_pct'}):
        dict['TRB'].append(ad1.find('td',{'data-stat':'trb_pct'}).get_text())
    if ad1.find('td',{'data-stat':'ast_pct'}):
        dict['AST'].append(ad1.find('td',{'data-stat':'ast_pct'}).get_text())
    if ad1.find('td',{'data-stat':'stl_pct'}):
        dict['STL'].append(ad1.find('td',{'data-stat':'stl_pct'}).get_text())
    if ad1.find('td',{'data-stat':'blk_pct'}):
        dict['BLK'].append(ad1.find('td',{'data-stat':'blk_pct'}).get_text())
    if ad1.find('td',{'data-stat':'tov_pct'}):
        dict['TOV'].append(ad1.find('td',{'data-stat':'tov_pct'}).get_text())
    if ad1.find('td',{'data-stat':'usg_pct'}):
        dict['USG'].append(ad1.find('td',{'data-stat':'usg_pct'}).get_text())
    if ad1.find('td',{'data-stat':'ows'}):
        dict['OWS'].append(ad1.find('td',{'data-stat':'ows'}).get_text())
    if ad1.find('td',{'data-stat':'dws'}):
        dict['DWS'].append(ad1.find('td',{'data-stat':'dws'}).get_text())    
    if ad1.find('td',{'data-stat':'ws'}):
        dict['WS'].append(ad1.find('td',{'data-stat':'ws'}).get_text())
    if ad1.find('td',{'data-stat':'obpm'}):
        dict['OBxPM'].append(ad1.find('td',{'data-stat':'obpm'}).get_text())
    if ad1.find('td',{'data-stat':'dbpm'}):
        dict['DBxPM'].append(ad1.find('td',{'data-stat':'dbpm'}).get_text())
    if ad1.find('td',{'data-stat':'bpm'}):
        dict['BxPM'].append(ad1.find('td',{'data-stat':'bpm'}).get_text())
    if ad1.find('td',{'data-stat':'vorp'}):
        dict['VORP'].append(ad1.find('td',{'data-stat':'vorp'}).get_text())

    return None

def find_reg_stats_scrape(id, dict, c1):
    URL = ("https://www.basketball-reference.com/players/")
    first_initial = id[0]
    r = requests.get(URL + first_initial + '/' + id + ".html")
    soup = BeautifulSoup(r.text, "html.parser")

    a = soup.find('div', id="all_per_game-playoffs_per_game")
    b = a.find('div', class_="table_container", id='div_per_game')

    dict.update({'Season':[], 'Age':[], 'Team':[], 'GP':[], 'GS':[], 'MP':[], 'FGM':[], 'FGA':[], 'FG_PCT':[], 'FG3M':[], 'FG3A':[], 'FG3_PCT':[],
    'FTM':[], 'FTA':[], 'FT_PCT':[], 'OREB':[], 'DREB':[], 'REB':[], 'AST':[], 'STL':[],'BLK':[], 'TOV':[], 'PF':[], 'PTS':[]})

    c1.update({'GP':[], 'GS':[], 'MP':[], 'FGM':[], 'FGA':[], 'FG_PCT':[], 'FG3M':[], 'FG3A':[], 'FG3_PCT':[],
    'FTM':[], 'FTA':[], 'FT_PCT':[], 'OREB':[], 'DREB':[], 'REB':[], 'AST':[], 'STL':[],'BLK':[], 'TOV':[], 'PF':[], 'PTS':[]})

    for reg in b.find('tbody').find_all('tr'):
        if reg.find('th', {'data-stat':'season'}):
            dict['Season'].append(reg.find('th', {'data-stat':'season'}).get_text())
        if reg.find('td', {'data-stat':'age'}):
            dict['Age'].append(reg.find('td', {'data-stat':'age'}).get_text())
        if reg.find('td', {'data-stat':'team_id'}):
            dict['Team'].append(reg.find('td', {'data-stat':'team_id'}).get_text())
        if reg.find('td', {'data-stat':'g'}):
            dict['GP'].append(reg.find('td', {'data-stat':'g'}).get_text())
        if reg.find('td', {'data-stat':'gs'}):
            dict['GS'].append(reg.find('td', {'data-stat':'gs'}).get_text())
        if reg.find('td', {'data-stat':'mp_per_g'}):
            dict['MP'].append(reg.find('td', {'data-stat':'mp_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fg_per_g'}):
            dict['FGM'].append(reg.find('td', {'data-stat':'fg_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fga_per_g'}):
            dict['FGA'].append(reg.find('td', {'data-stat':'fga_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fg_pct'}):
            dict['FG_PCT'].append(reg.find('td', {'data-stat':'fg_pct'}).get_text())
        if reg.find('td', {'data-stat':'fg3_per_g'}):
            dict['FG3M'].append(reg.find('td', {'data-stat':'fg3_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fg3a_per_g'}):
            dict['FG3A'].append(reg.find('td', {'data-stat':'fg3a_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fg3_pct'}):
            dict['FG3_PCT'].append(reg.find('td', {'data-stat':'fg3_pct'}).get_text())
        if reg.find('td', {'data-stat':'ft_per_g'}):
            dict['FTM'].append(reg.find('td', {'data-stat':'ft_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fta_per_g'}):
            dict['FTA'].append(reg.find('td', {'data-stat':'fta_per_g'}).get_text())
        if reg.find('td', {'data-stat':'ft_pct'}):
            dict['FT_PCT'].append(reg.find('td', {'data-stat':'ft_pct'}).get_text())
        if reg.find('td', {'data-stat':'orb_per_g'}):
            dict['OREB'].append(reg.find('td', {'data-stat':'orb_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'drb_per_g'}):
            dict['DREB'].append(reg.find('td', {'data-stat':'drb_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'trb_per_g'}):
            dict['REB'].append(reg.find('td', {'data-stat':'trb_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'ast_per_g'}):
            dict['AST'].append(reg.find('td', {'data-stat':'ast_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'stl_per_g'}):
            dict['STL'].append(reg.find('td', {'data-stat':'stl_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'blk_per_g'}):
            dict['BLK'].append(reg.find('td', {'data-stat':'blk_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'tov_per_g'}):
            dict['TOV'].append(reg.find('td', {'data-stat':'tov_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'pf_per_g'}):
            dict['PF'].append(reg.find('td', {'data-stat':'pf_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'pts_per_g'}):
            dict['PTS'].append(reg.find('td', {'data-stat':'pts_per_g'}).get_text()) 

    reg2 = b.find('tfoot')
    reg1 = reg2.find('tr')

    if reg1.find('td', {'data-stat':'g'}):
        c1['GP'].append(reg1.find('td', {'data-stat':'g'}).get_text())
    if reg1.find('td', {'data-stat':'gs'}):
        c1['GS'].append(reg1.find('td', {'data-stat':'gs'}).get_text())
    if reg1.find('td', {'data-stat':'mp_per_g'}):
        c1['MP'].append(reg1.find('td', {'data-stat':'mp_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fg_per_g'}):
        c1['FGM'].append(reg1.find('td', {'data-stat':'fg_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fga_per_g'}):
        c1['FGA'].append(reg1.find('td', {'data-stat':'fga_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fg_pct'}):
        c1['FG_PCT'].append(reg1.find('td', {'data-stat':'fg_pct'}).get_text())
    if reg1.find('td', {'data-stat':'fg3_per_g'}):
        c1['FG3M'].append(reg1.find('td', {'data-stat':'fg3_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fg3a_per_g'}):
        c1['FG3A'].append(reg1.find('td', {'data-stat':'fg3a_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fg3_pct'}):
        c1['FG3_PCT'].append(reg1.find('td', {'data-stat':'fg3_pct'}).get_text())
    if reg1.find('td', {'data-stat':'ft_per_g'}):
        c1['FTM'].append(reg1.find('td', {'data-stat':'ft_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fta_per_g'}):
        c1['FTA'].append(reg1.find('td', {'data-stat':'fta_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'ft_pct'}):
        c1['FT_PCT'].append(reg1.find('td', {'data-stat':'ft_pct'}).get_text())
    if reg1.find('td', {'data-stat':'orb_per_g'}):
        c1['OREB'].append(reg1.find('td', {'data-stat':'orb_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'drb_per_g'}):
        c1['DREB'].append(reg1.find('td', {'data-stat':'drb_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'trb_per_g'}):
        c1['REB'].append(reg1.find('td', {'data-stat':'trb_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'ast_per_g'}):
        c1['AST'].append(reg1.find('td', {'data-stat':'ast_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'stl_per_g'}):
        c1['STL'].append(reg1.find('td', {'data-stat':'stl_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'blk_per_g'}):
        c1['BLK'].append(reg1.find('td', {'data-stat':'blk_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'tov_per_g'}):
        c1['TOV'].append(reg1.find('td', {'data-stat':'tov_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'pf_per_g'}):
        c1['PF'].append(reg1.find('td', {'data-stat':'pf_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'pts_per_g'}):
        c1['PTS'].append(reg1.find('td', {'data-stat':'pts_per_g'}).get_text())

    return None

def find_play_stats_scrape(id, dict, c1):
    URL = ("https://www.basketball-reference.com/players/")
    first_initial = id[0]
    r = requests.get(URL + first_initial + '/' + id + ".html")
    soup = BeautifulSoup(r.text, "html.parser")

    a = soup.find('div', id="all_per_game-playoffs_per_game")
    b = a.find('div', class_="table_container", id='div_playoffs_per_game')

    dict.update({'Season':[], 'Age':[], 'Team':[], 'GP':[], 'GS':[], 'MP':[], 'FGM':[], 'FGA':[], 'FG_PCT':[], 'FG3M':[], 'FG3A':[], 'FG3_PCT':[],
    'FTM':[], 'FTA':[], 'FT_PCT':[], 'OREB':[], 'DREB':[], 'REB':[], 'AST':[], 'STL':[],'BLK':[], 'TOV':[], 'PF':[], 'PTS':[]})

    c1.update({'GP':[], 'GS':[], 'MP':[], 'FGM':[], 'FGA':[], 'FG_PCT':[], 'FG3M':[], 'FG3A':[], 'FG3_PCT':[],
    'FTM':[], 'FTA':[], 'FT_PCT':[], 'OREB':[], 'DREB':[], 'REB':[], 'AST':[], 'STL':[],'BLK':[], 'TOV':[], 'PF':[], 'PTS':[]})

    for reg in b.find('tbody').find_all('tr'):
        if reg.find('th', {'data-stat':'season'}):
            dict['Season'].append(reg.find('th', {'data-stat':'season'}).get_text())
        if reg.find('td', {'data-stat':'age'}):
            dict['Age'].append(reg.find('td', {'data-stat':'age'}).get_text())
        if reg.find('td', {'data-stat':'team_id'}):
            dict['Team'].append(reg.find('td', {'data-stat':'team_id'}).get_text())
        if reg.find('td', {'data-stat':'g'}):
            dict['GP'].append(reg.find('td', {'data-stat':'g'}).get_text())
        if reg.find('td', {'data-stat':'gs'}):
            dict['GS'].append(reg.find('td', {'data-stat':'gs'}).get_text())
        if reg.find('td', {'data-stat':'mp_per_g'}):
            dict['MP'].append(reg.find('td', {'data-stat':'mp_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fg_per_g'}):
            dict['FGM'].append(reg.find('td', {'data-stat':'fg_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fga_per_g'}):
            dict['FGA'].append(reg.find('td', {'data-stat':'fga_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fg_pct'}):
            dict['FG_PCT'].append(reg.find('td', {'data-stat':'fg_pct'}).get_text())
        if reg.find('td', {'data-stat':'fg3_per_g'}):
            dict['FG3M'].append(reg.find('td', {'data-stat':'fg3_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fg3a_per_g'}):
            dict['FG3A'].append(reg.find('td', {'data-stat':'fg3a_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fg3_pct'}):
            dict['FG3_PCT'].append(reg.find('td', {'data-stat':'fg3_pct'}).get_text())
        if reg.find('td', {'data-stat':'ft_per_g'}):
            dict['FTM'].append(reg.find('td', {'data-stat':'ft_per_g'}).get_text())
        if reg.find('td', {'data-stat':'fta_per_g'}):
            dict['FTA'].append(reg.find('td', {'data-stat':'fta_per_g'}).get_text())
        if reg.find('td', {'data-stat':'ft_pct'}):
            dict['FT_PCT'].append(reg.find('td', {'data-stat':'ft_pct'}).get_text())
        if reg.find('td', {'data-stat':'orb_per_g'}):
            dict['OREB'].append(reg.find('td', {'data-stat':'orb_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'drb_per_g'}):
            dict['DREB'].append(reg.find('td', {'data-stat':'drb_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'trb_per_g'}):
            dict['REB'].append(reg.find('td', {'data-stat':'trb_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'ast_per_g'}):
            dict['AST'].append(reg.find('td', {'data-stat':'ast_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'stl_per_g'}):
            dict['STL'].append(reg.find('td', {'data-stat':'stl_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'blk_per_g'}):
            dict['BLK'].append(reg.find('td', {'data-stat':'blk_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'tov_per_g'}):
            dict['TOV'].append(reg.find('td', {'data-stat':'tov_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'pf_per_g'}):
            dict['PF'].append(reg.find('td', {'data-stat':'pf_per_g'}).get_text()) 
        if reg.find('td', {'data-stat':'pts_per_g'}):
            dict['PTS'].append(reg.find('td', {'data-stat':'pts_per_g'}).get_text()) 

    reg2 = b.find('tfoot')
    reg1 = reg2.find('tr')

    if reg1.find('td', {'data-stat':'g'}):
        c1['GP'].append(reg1.find('td', {'data-stat':'g'}).get_text())
    if reg1.find('td', {'data-stat':'gs'}):
        c1['GS'].append(reg1.find('td', {'data-stat':'gs'}).get_text())
    if reg1.find('td', {'data-stat':'mp_per_g'}):
        c1['MP'].append(reg1.find('td', {'data-stat':'mp_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fg_per_g'}):
        c1['FGM'].append(reg1.find('td', {'data-stat':'fg_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fga_per_g'}):
        c1['FGA'].append(reg1.find('td', {'data-stat':'fga_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fg_pct'}):
        c1['FG_PCT'].append(reg1.find('td', {'data-stat':'fg_pct'}).get_text())
    if reg1.find('td', {'data-stat':'fg3_per_g'}):
        c1['FG3M'].append(reg1.find('td', {'data-stat':'fg3_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fg3a_per_g'}):
        c1['FG3A'].append(reg1.find('td', {'data-stat':'fg3a_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fg3_pct'}):
        c1['FG3_PCT'].append(reg1.find('td', {'data-stat':'fg3_pct'}).get_text())
    if reg1.find('td', {'data-stat':'ft_per_g'}):
        c1['FTM'].append(reg1.find('td', {'data-stat':'ft_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'fta_per_g'}):
        c1['FTA'].append(reg1.find('td', {'data-stat':'fta_per_g'}).get_text())
    if reg1.find('td', {'data-stat':'ft_pct'}):
        c1['FT_PCT'].append(reg1.find('td', {'data-stat':'ft_pct'}).get_text())
    if reg1.find('td', {'data-stat':'orb_per_g'}):
        c1['OREB'].append(reg1.find('td', {'data-stat':'orb_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'drb_per_g'}):
        c1['DREB'].append(reg1.find('td', {'data-stat':'drb_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'trb_per_g'}):
        c1['REB'].append(reg1.find('td', {'data-stat':'trb_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'ast_per_g'}):
        c1['AST'].append(reg1.find('td', {'data-stat':'ast_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'stl_per_g'}):
        c1['STL'].append(reg1.find('td', {'data-stat':'stl_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'blk_per_g'}):
        c1['BLK'].append(reg1.find('td', {'data-stat':'blk_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'tov_per_g'}):
        c1['TOV'].append(reg1.find('td', {'data-stat':'tov_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'pf_per_g'}):
        c1['PF'].append(reg1.find('td', {'data-stat':'pf_per_g'}).get_text()) 
    if reg1.find('td', {'data-stat':'pts_per_g'}):
        c1['PTS'].append(reg1.find('td', {'data-stat':'pts_per_g'}).get_text())
        
    return None


# def scrape_stats():


#     fgt =  fg3t = ftt = orbt = drbt = trbt = astt = ptst = 0
#     totalg = fg3g = 0
#     for x in range(1974, 2021):

#         URL = ("https://www.basketball-reference.com/leagues/NBA_" + str(x) + "_per_game.html")
#         r = requests.get(URL)
#         soup = BeautifulSoup(r.text, "html.parser")

#         a = soup.find(id='all_per_game_stats').find('tbody')

#         for ad in a.find_all('tr', class_='full_table'):
#             g = int(ad.find('td',{'data-stat':'g'}).get_text())
#             if ad.find('td',{'data-stat':'fg_pct'}).get_text() != "": 
#                 fgpct = float(ad.find('td',{'data-stat':'fg_pct'}).get_text())
#                 fgav = (g) * (fgpct)
#                 fgt += fgav

#             if ad.find('td',{'data-stat':'fg3_pct'}).get_text() != "" and ad.find('td',{'data-stat':'fg3_pct'}).get_text() != ".000": 
#                 fg3_pct = float(ad.find('td',{'data-stat':'fg3_pct'}).get_text())
#                 fg3_av = g * fg3_pct
#                 fg3t += fg3_av
#             else:
#                 fg3g -= g

#             if ad.find('td',{'data-stat':'ft_pct'}).get_text() != "": 
#                 ft_pct = float(ad.find('td',{'data-stat':'ft_pct'}).get_text())
#                 ft_av = g * ft_pct
#                 ftt += ft_av

#             if ad.find('td',{'data-stat':'orb_per_g'}).get_text() != "": 
#                 orb = float(ad.find('td',{'data-stat':'orb_per_g'}).get_text())
#                 orb_av = g * orb
#                 orbt += orb_av

#             if ad.find('td',{'data-stat':'drb_per_g'}).get_text() != "": 
#                 drb = float(ad.find('td',{'data-stat':'drb_per_g'}).get_text())
#                 drb_av = g * drb
#                 drbt += drb_av

#             if ad.find('td',{'data-stat':'trb_per_g'}).get_text() != "": 
#                 trb = float(ad.find('td',{'data-stat':'trb_per_g'}).get_text())
#                 trb_av = g * trb
#                 trbt += trb_av

#             if ad.find('td',{'data-stat':'ast_per_g'}).get_text() != "": 
#                 ast = float(ad.find('td',{'data-stat':'ast_per_g'}).get_text())
#                 ast_av = g * ast
#                 astt += ast_av

#             if ad.find('td',{'data-stat':'pts_per_g'}).get_text() != "": 
#                 pts = float(ad.find('td',{'data-stat':'pts_per_g'}).get_text())
#                 pts_av = g * pts
#                 ptst += pts_av
#             totalg += g
#             fg3g += g

#     print('fg%')
#     print(fgt / totalg)
#     print('3p%')
#     print(fg3t / fg3g)
#     print('ft%')
#     print(ftt / totalg)
#     print('orb')
#     print(orbt / totalg)
#     print('drb')
#     print(drbt / totalg)
#     print('trb')
#     print(trbt / totalg)
#     print('ast')
#     print(astt / totalg)
#     print('pts')
#     print(ptst / totalg)

# fg%
# 0.4571849037664385
# 3p%
# 0.32191134453906667
# ft%
# 0.737586960658112
# orb
# 1.2364785680585733
# drb
# 2.9959304842840258
# trb
# 4.231191595362775
# ast
# 2.281550687410316
# pts
# 10.07008304064271




# def scrape_advanced_averagestats(dict):
#     totalg = orbt = drbt = trbt = astt = 0
#     totalt = 0

#     for x in range(1974, 2021):

#         URL = ("https://www.basketball-reference.com/leagues/NBA_" + str(x) + "_advanced.html")
#         r = requests.get(URL)
#         soup = BeautifulSoup(r.text, "html.parser")

#         a = soup.find(id='all_advanced_stats').find('tbody')

#         for ad in a.find_all('tr', class_='full_table'):
#             g = int(ad.find('td',{'data-stat':'g'}).get_text())
#             if ad.find('td',{'data-stat':'ts_pct'}).get_text() != "": 
#                 tspct = float(ad.find('td',{'data-stat':'ts_pct'}).get_text())
#                 av = (g) * (tspct)
#                 totalt += av

#             if ad.find('td',{'data-stat':'orb_pct'}).get_text() != "": 
#                 orb_pct = float(ad.find('td',{'data-stat':'orb_pct'}).get_text())
#                 orb_av = g * orb_pct
#                 orbt += orb_av

#             if ad.find('td',{'data-stat':'drb_pct'}).get_text() != "": 
#                 drb_pct = float(ad.find('td',{'data-stat':'drb_pct'}).get_text())
#                 drb_av = g * drb_pct
#                 drbt += drb_av

#             if ad.find('td',{'data-stat':'trb_pct'}).get_text() != "": 
#                 trb_pct = float(ad.find('td',{'data-stat':'trb_pct'}).get_text())
#                 trb_av = g * trb_pct
#                 trbt += trb_av

#             if ad.find('td',{'data-stat':'ast_pct'}).get_text() != "": 
#                 ast_pct = float(ad.find('td',{'data-stat':'ast_pct'}).get_text())
#                 ast_av = g * ast_pct
#                 astt += ast_av

#             totalg += (g)
#     print('orb%')
#     print(orbt / totalg)
#     print('drb%')
#     print(drbt  / totalg)
#     print('trb%')
#     print(trbt  / totalg)
#     print('ast%')
#     print(astt  / totalg)
#     print('ts%')
#     print(totalt  / totalg)

# #     orb%
# # 6.026131882597581
# # drb%
# # 14.049571497080924
# # trb%
# # 10.038912802471188
# # ast%
# # 13.828653875650646
# # ts%
# # 0.5242884259555871


# def find_all_star(p_id):
#     first = p_id[0]
#     url1 = 'https://www.basketball-reference.com/players/'
#     req = requests.get(url1 + first + '/' + p_id + '.html')
#     s = BeautifulSoup(req.text, 'html.parser')

#     all_s = s.find('li', {'class':'all_star'})

#     if all_s == None:
#         return "0x All Star"
    
#     return all_s.get_text()