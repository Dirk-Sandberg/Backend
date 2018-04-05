# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 14:19:16 2018

@author: Erik
"""

'''
Program to randomly select opponents from list of participants
Creates a new column in the "Participants" table for opponents

'''
import numpy as np

class OpponentPicker():
    def __init__(self):
        self.allParticipants = []
        self.d = []
        pass
    
    def pickOpponents(self,file):
        with open(file, 'r') as f:
            d = f.read().splitlines()
        for user in d:
            self.allParticipants.append(user.split(",")[0])
            self.d.append(user)
        numParticipants = len(self.allParticipants)
        self.pairs = {}
        for p in self.allParticipants:
            if p not in self.pairs.keys():
                n = np.random.randint(numParticipants)
                opp = self.allParticipants[n]
                while opp == p:
                    n = np.random.randint(numParticipants)
                    opp = self.allParticipants[n]
                self.pairs[p] = opp
                self.pairs[opp] = p
        # ---- Rewrite to table
        with open(file, 'w') as f:
            for user in self.d:
                userSplit = user.split(",")
                userSplit[3] = self.pairs[userSplit[0]]
                line = ",".join(str(x) for x in userSplit) + "\n"
                f.write(line)


