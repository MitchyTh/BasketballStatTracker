import json
import os
import random
import django

from app.dbmodels.models import Players, Teams, Shots, Games, Passes, Turnovers
from django.db.models import Sum, Count
from rest_framework.response import Response


def get_player_summary_stats(player_id: str):
    #creates django objects for a certain player's information depending on the playerId provided
    player = Players.objects.get(player_id = player_id)
    shots = Shots.objects.filter(player_id = player)
    passes = Passes.objects.filter(player_id = player)
    turnovers = Turnovers.objects.filter(player_id = player)

    #general data querying
    totalAttempts = shots.count()
    totalPoints = shots.aggregate(Sum('points'))['points__sum'] or 0
    totalPasses = passes.count()
    totalPotAssists = passes.filter(potential_assist = True).count()
    totalTurnovers = turnovers.count()
    totalPassTurnovers = passes.filter(turnover = True).count()
    
    #pick and roll play querying
    pickAndRollShots = shots.filter(action_type = "pickAndRoll")
    pickAndRollPasses = passes.filter(action_type = "pickAndRoll")
    pickAndRollTurnovers = turnovers.filter(action_type = "pickAndRoll")

    pickShotAttempts = pickAndRollShots.count()
    pickPoints = pickAndRollShots.aggregate(Sum('points'))['points__sum'] or 0
    pickPassCount = pickAndRollPasses.count()
    pickPotAssists = pickAndRollPasses.filter(potential_assist = True).count()
    pickTurnoverCount = pickAndRollTurnovers.count()
    pickTotal = pickShotAttempts + pickPassCount + (pickTurnoverCount - pickAndRollPasses.filter(turnover = True).count()) #gets accurate measure of plays by subtracting previously counted pass turnovers from turnovers

    #isolation querying
    isoShots = shots.filter(action_type = "isolation")
    isoPasses = passes.filter(action_type = "isolation")
    isoTurnovers = turnovers.filter(action_type = "isolation")

    isoShotAttempts = isoShots.count()
    isoPoints = isoShots.aggregate(Sum('points'))['points__sum'] or 0
    isoPassCount = isoPasses.count()
    isoPotAssists = isoPasses.filter(potential_assist = True).count()
    isoTurnoverCount = isoTurnovers.count()
    isoTotal = isoShotAttempts + isoPassCount + (isoTurnoverCount - isoPasses.filter(turnover = True).count()) #gets accurate measure of plays by subtracting previously counted pass turnovers from turnovers

    #post up querying
    postShots = shots.filter(action_type = "postUp")
    postPasses = passes.filter(action_type = "postUp")
    postTurnovers = turnovers.filter(action_type = "postUp")

    postShotAttempts = postShots.count()
    postPoints = postShots.aggregate(Sum('points'))['points__sum'] or 0
    postPassCount = postPasses.count()
    postPotAssists = postPasses.filter(potential_assist = True).count()
    postTurnoverCount = postTurnovers.count()
    postTotal = postShotAttempts + postPassCount + (postTurnoverCount - postPasses.filter(turnover = True).count()) #gets accurate measure of plays by subtracting previously counted pass turnovers from turnovers

    #off ball screen querying
    offBallScreenShots = shots.filter(action_type = "offBallScreen")
    offBallScreenPasses = passes.filter(action_type = "offBallScreen")
    offBallScreenTurnovers = turnovers.filter(action_type = "offBallScreen")

    offBallScreenShotAttempts = offBallScreenShots.count()
    offBallScreenPoints = offBallScreenShots.aggregate(Sum('points'))['points__sum'] or 0
    offBallScreenPassCount = offBallScreenPasses.count()
    offBallScreenPotAssists = offBallScreenPasses.filter(potential_assist = True).count()
    offBallScreenTurnoverCount = offBallScreenTurnovers.count()
    offBallScreenTotal = offBallScreenShotAttempts + offBallScreenPassCount + (offBallScreenTurnoverCount - offBallScreenPasses.filter(turnover = True).count()) #gets accurate measure of plays by subtracting previously counted pass turnovers from turnovers

    data = {
        "name": player.name,
        "playerId": player.player_id,
        "totalShotAttempts": totalAttempts, 
        "totalPoints": totalPoints, 
        "totalPasses": totalPasses, 
        "totalPotentialAssists": totalPotAssists, 
        "totalTurnovers": totalTurnovers, 
        "totalPassingTurnovers": totalPassTurnovers, 
        "pickAndRollCount": pickTotal, 
        "isolationCount": isoTotal, 
        "postUpCount": postTotal, 
        "offBallScreenCount": offBallScreenTotal, 

        "pickAndRoll": {
            "totalShotAttempts": pickShotAttempts, 
            "totalPoints": pickPoints,
            "totalPasses": pickPassCount, 
            "totalPotentialAssists": pickPotAssists, 
            "totalTurnovers": pickTurnoverCount, 

            "shots": [],
            "passes": [],
            "turnovers": []
        },

        "isolation": {
            "totalShotAttempts": isoShotAttempts, 
            "totalPoints": isoPoints, 
            "totalPasses": isoPassCount, 
            "totalPotentialAssists": isoPotAssists, 
            "totalTurnovers": isoTurnoverCount, 

            "shots": [],
            "passes": [],
            "turnovers": []
        },

        "postUp": {
            "totalShotAttempts": postShotAttempts, 
            "totalPoints": postPoints, 
            "totalPasses": postPassCount, 
            "totalPotentialAssists": postPotAssists, 
            "totalTurnovers": postTurnoverCount, 

            "shots": [],
            "passes": [],
            "turnovers": []
        },

        "offBallScreen": {
            "totalShotAttempts": offBallScreenShotAttempts, 
            "totalPoints": offBallScreenPoints, 
            "totalPasses": offBallScreenPassCount, 
            "totalPotentialAssists": offBallScreenPotAssists, 
            "totalTurnovers": offBallScreenTurnoverCount, 

            "shots": [],
            "passes": [],
            "turnovers": []
        },
    }

    #LOADING SHOTS, PASSES AND TURNOVERS INTO EMPTY DICTIONARY LISTS PER PLAY
    #PICK AND ROLLS
    for shot in pickAndRollShots:
        data["pickAndRoll"]["shots"].append({
            "loc": [shot.shot_loc_x, shot.shot_loc_y],
            "points": shot.points
        })
    
    for pass_ in pickAndRollPasses:
        data["pickAndRoll"]["passes"].append({
            "startLoc": [pass_.ball_start_loc_x, pass_.ball_start_loc_y],
            "endLoc": [pass_.ball_end_loc_x, pass_.ball_end_loc_y],
            "isCompleted": pass_.completed_pass,
            "potentialAssist": pass_.potential_assist,
            "isTurnover": pass_.turnover
        })

    for turnover in pickAndRollTurnovers:
        data["pickAndRoll"]["turnovers"].append({
            "loc": [turnover.tov_loc_x, turnover.tov_loc_y]
        })

    #ISOLATION
    for shot in isoShots:
        data["isolation"]["shots"].append({
            "loc": [shot.shot_loc_x, shot.shot_loc_y],
            "points": shot.points
        })
    
    for pass_ in isoPasses:
        data["isolation"]["passes"].append({
            "startLoc": [pass_.ball_start_loc_x, pass_.ball_start_loc_y],
            "endLoc": [pass_.ball_end_loc_x, pass_.ball_end_loc_y],
            "isCompleted": pass_.completed_pass,
            "potentialAssist": pass_.potential_assist,
            "isTurnover": pass_.turnover
        })

    for turnover in isoTurnovers:
        data["isolation"]["turnovers"].append({
            "loc": [turnover.tov_loc_x, turnover.tov_loc_y]
        })

    #POSTUP
    for shot in postShots:
        data["postUp"]["shots"].append({
            "loc": [shot.shot_loc_x, shot.shot_loc_y],
            "points": shot.points
        })
    
    for pass_ in postPasses:
        data["postUp"]["passes"].append({
            "startLoc": [pass_.ball_start_loc_x, pass_.ball_start_loc_y],
            "endLoc": [pass_.ball_end_loc_x, pass_.ball_end_loc_y],
            "isCompleted": pass_.completed_pass,
            "potentialAssist": pass_.potential_assist,
            "isTurnover": pass_.turnover
        })

    for turnover in postTurnovers:
        data["postUp"]["turnovers"].append({
            "loc": [turnover.tov_loc_x, turnover.tov_loc_y]
        })

    #OFFBALLSCREEN
    for shot in offBallScreenShots:
        data["offBallScreen"]["shots"].append({
            "loc": [shot.shot_loc_x, shot.shot_loc_y],
            "points": shot.points
        })
    
    for pass_ in offBallScreenPasses:
        data["offBallScreen"]["passes"].append({
            "startLoc": [pass_.ball_start_loc_x, pass_.ball_start_loc_y],
            "endLoc": [pass_.ball_end_loc_x, pass_.ball_end_loc_y],
            "isCompleted": pass_.completed_pass,
            "potentialAssist": pass_.potential_assist,
            "isTurnover": pass_.turnover
        })

    for turnover in offBallScreenTurnovers:
        data["offBallScreen"]["turnovers"].append({
            "loc": [turnover.tov_loc_x, turnover.tov_loc_y]
        })

    return data


def get_ranks(player_id: str, player_summary: dict):
    # TODO: replace with your implementation of get_ranks

    all_players = Players.objects.all()
    
    stat_keys = [
        "totalShotAttempts",
        "totalPoints",
        "totalPasses",
        "totalPotentialAssists",
        "totalTurnovers",
        "totalPassingTurnovers",
        "pickAndRollCount",
        "isolationCount",
        "postUpCount",
        "offBallScreenCount"
    ]

    category_totals = {key: [] for key in stat_keys}
    for player in all_players:
        summary_response = get_player_summary_stats(player.player_id)

        summary = getattr(summary_response, "data", summary_response) #extracts the dict from the response object

        if not isinstance(summary, dict): #ignores if data is missing
            continue

        for key in stat_keys:
            value = summary.get(key, 0)
            category_totals[key].append((player.player_id, value))

    ranks = {}
    for key, values in category_totals.items():
        #sorts in descending order
        sorted_values = sorted(values, key=lambda x: x[1], reverse=True)

        #assigns ranks for each player
        for rank, (pid, _) in enumerate(sorted_values, start=1):
            if str(pid) == str(player_id): 
                ranks[key + "Rank"] = rank
                break
        else:
            ranks[key + "Rank"] = None

    return ranks

