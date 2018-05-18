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
        # What to do if an odd number of players? One has to get a buy? commented May 6, 2018 
        try:
            allParticipants = self.SS.readSheet(filename)
        except:
            allParticipants = []
        numParticipants = len(allParticipants)
        if numParticipants == 0:
            print("NO PARTICIPANTS HERE!")
            return
        if numParticipants == 1:
            # Can't assign participant to one person
            print("No opponents available!")
            return
        pairs = {}
        for participant in allParticipants:
            if (participant['needsOpponent'] == "Yes"):  
                if participant["username"] not in pairs.keys():
                    p = participant["username"]
                    print("number of participants: ", numParticipants)
                    n = np.random.randint(numParticipants)
                    opp = allParticipants[n]["username"]
                    while (opp == p ) or ( allParticipants[n]['needsOpponent'] == "No" ) or (opp in pairs.keys()) :
                        # Try to pick opponent again if the player is either himself or doesn't need an opponent
                        n = np.random.randint(numParticipants)
                        opp = allParticipants[n]["username"]
                    pairs[p] = opp
                    pairs[opp] = p
                    print(p + "'s opponent should be: " + opp)                
        self.test = pairs
        for participant in allParticipants:
            if (participant['needsOpponent'] == "Yes"):
                p = participant["username"]
                opp = pairs[p]
                participant["opponent"] = ",".join([participant["opponent"],opp])
        self.test2 = allParticipants
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
