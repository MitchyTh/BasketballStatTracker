# -*- coding: utf-8 -*-
from django.db import models

class Games(models.Model):
    game_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    class Meta:
        db_table = 'games'

class Teams(models.Model):
    team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'teams'

class Players(models.Model):
    player_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    team = models.ForeignKey(Teams, db_column='team_id', on_delete=models.CASCADE)
    class Meta:
        db_table = 'players'

class Shots(models.Model):
    shot_id = models.IntegerField(primary_key=True)
    points = models.IntegerField()
    shooting_foul_drawn = models.BooleanField()
    shot_loc_x = models.FloatField()
    shot_loc_y = models.FloatField()
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=25)
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    class Meta:
        db_table = 'shots'

class Passes(models.Model):
    pass_id = models.IntegerField(primary_key=True)
    completed_pass = models.BooleanField()
    potential_assist = models.BooleanField()
    turnover = models.BooleanField()
    ball_start_loc_x = models.FloatField()
    ball_start_loc_y = models.FloatField()
    ball_end_loc_x = models.FloatField()
    ball_end_loc_y = models.FloatField()
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=25)
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    class Meta:
        db_table = 'passes'

class Turnovers(models.Model):
    turnover_id = models.IntegerField(primary_key=True)
    tov_loc_x = models.FloatField()
    tov_loc_y = models.FloatField()
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=25)
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    class Meta:
        db_table = 'turnovers'
