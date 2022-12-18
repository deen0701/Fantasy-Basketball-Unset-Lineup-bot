from flask import Blueprint, render_template, jsonify
from espn_api.basketball import League
from datetime import datetime

views = Blueprint(__name__, "views")
league = league = League(league_id=98658036, year=2023, espn_s2='AECnRz00UuzGLrbuSrG8olijR4AX2%2B%2BQZeYd8DGnCimEbRv%2FSYziPcgicTDXD0Ro25jZJUFXTOsLZ13pzAuAb%2F0Mk1nbZniXOdwG4Jav7O9AKz5DD20WR%2BwfPA0RcXOuImdlUtft1siEQ358cPoD44%2Fga6vDwwpKoNXMvb4nLEWOheCB32HeYBlo5EBsmlBeQSLf5l5CSIZJp9bS1uou1%2Bee4NNiugws5coP8dw7aayHmwtCBIXGJgG%2Ft22vRDRcGoMofzD6ZtNMToc%2B5i1ZzRn6NTeY2lxIjtfSOKUiW4l4Aw%3D%3D',
                swid='{7E1AD19D-1AD7-452E-B400-761EE5F02035}')

class Managers:
    def __init__(self, name, count):
        self.name = name
        self.count = count


unsetLineup = []
def isSet():
    for i in range(len(league.teams)):
        setlineup = True
        for j in range(len(league.teams[i].roster)):
            player = league.teams[i].roster[j]
            current = league.scoringPeriodId
            playstoday = False
            if str(current) in player.schedule:
                month = player.schedule[str(current)]["date"].month
                day = player.schedule[str(current)]["date"].day
                year = player.schedule[str(current)]["date"].year
                day2 = datetime.today().day
                month2 = datetime.today().month
                year2 = datetime.today().year
                if month == month2 and day == day2 and year == year2:
                    #print("This person plays today")
                    playstoday = True
                if(player.lineupSlot == 'BE' and playstoday == True and player.injuryStatus == "ACTIVE"):
                    setlineup = False

        if(setlineup == False):
            unsetLineup.append(league.teams[i].team_name)
            return unsetLineup



@views.route("/")
def home():
    teamList = []

    for i in range(len(league.teams)):
        manager = Managers(league.teams[i].team_name, 0)
        teamList.append(manager)
    isSet()
    if datetime.today().hour == 23:
        if len(unsetLineup) == 0:
            print("everyone has set their lineups")
        else:
            for i in range(len(unsetLineup)):
                for j in range(len(teamList)):
                    if teamList[j].name == unsetLineup[i]:
                        print(teamList[j].name, unsetLineup[i])
                        teamList[j].count += 1
                        print(teamList[j].count, "\n")

    teamList.sort(key=lambda x: x.count, reverse=True)
    return render_template("index.html", name="Team Ana Soori", teamList=teamList)



# @views.route("/json")
# def get_json():
#     return jsonify({'name':'time', 'coolness':10})
