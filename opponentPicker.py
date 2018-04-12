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
import SpreadSheet

class OpponentPicker():
    def __init__(self):
        self.allParticipants = []
        self.d = []
        self.SS = SpreadSheet.SSWriter()

    def pickOpponents(self,filename):
        try:
            allParticipants = self.SS.readSheet(filename)
        except:
            allParticipants = []
        numParticipants = len(allParticipants)
        if numParticipants == 0:
            print("NO PARTICIPANTS HERE!")
            return
        pairs = {}
        for participant in allParticipants:
            print(allParticipants)
            if participant["username"] not in pairs.keys():
                p = participant["username"]
                print(numParticipants)
                n = np.random.randint(numParticipants)
                opp = allParticipants[n]["username"]
                print(p + "'s opponent should be: " + opp)                
                while opp == p:
                    n = np.random.randint(numParticipants)
                    opp = allParticipants[n]["username"]
                pairs[p] = opp
                pairs[opp] = p
        for participant in allParticipants:
            
            p = participant["username"]
            opp = pairs[p]
            participant["opponent"] = ",".join([participant["opponent"],opp])
        self.SS.writeSheet(filename, allParticipants)

                
        
'''
    def pickOpponents(self,filename):
        with open(filename, 'r') as f:
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
        with open(filename, 'w') as f:
            for user in self.d:
                userSplit = user.split(",")
                userSplit[3] = self.pairs[userSplit[0]]
                line = ",".join(str(x) for x in userSplit) + "\n"
                f.write(line)


'''
