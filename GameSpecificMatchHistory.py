# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 09:36:15 2018

@author: Erik
"""
import VooblyMatchHistory

def checkHistory(SKU, player, opponent, earliestDate, latestDate):
    if SKU == "AOE-SOLO-01":
        HistoryChecker = VooblyMatchHistory.VooblyScraper()
        winner = HistoryChecker.checkHistory(player, opponent, earliestDate, latestDate)
    return winner
