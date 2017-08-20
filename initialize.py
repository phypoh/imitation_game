#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initializing values. Run this before all else!
"""
import pandas as pd
import numpy as np


hero_stats = pd.read_csv("hero_stats.csv")
item_stats = pd.read_csv("item_stats.csv")
perk_stats = pd.read_csv("perk_stats.csv")


class hero_stat:
    def __init__(self, row, perk = None):
        self.name = row.iloc[0]
        self.health = np.linspace(row.loc["Health (Level 1)"],row.loc["Health (Level 12)"],12) 
        self.defense = np.linspace(row.loc["Armour/Shield (Level 1)"],row.loc["Armour/Shield (Level 12)"],12) 
        self.energy = np.linspace(row.loc["Energy (Level 1)"],row.loc["Energy (Level 12)"],12) 
        self.weapon = np.linspace(row.loc["Weapon (Level 1)"],row.loc["Weapon (Level 12)"],12) 
        self.AS = np.linspace(row.loc["Attack Speed (Level 1)"],row.loc["Attack Speed (Level 12)"],12) 
        self.ACD = row.loc["Attack Cooldown"]
        self.ADelay = row.loc["Attack Delay"]
        self.stutterBonus = row.loc["Stutterstep Bonus"]
        self.ASMod = row.loc["Attack Speed Modifier"]
        self.range = row.loc["Range"]
            
    def __repr__(self):
        return self.name + "'s stats"

class item_stat:
    def __init__(self,row):
        self.name = row.iloc[0]
        self.weapon = row.loc["Weapon Power"]
        self.wpLifesteal = int(row.loc["Weapon Lifesteal"].strip('%'))/100
        self.wpPierce = int(row.loc["Armor Pierce"].strip('%'))/100
        self.AS = int(row.loc["Attack Speed"].strip('%'))/100
        self.critChance = int(row.loc["Critical Chance"].strip('%'))/100
        self.critDamage = int(row.loc["Critical Damage"].strip('%'))/100
        self.crystal = row.loc["Crystal Power"]
        self.cpLifesteal = int(row.loc["Crystal Lifesteal"].strip('%'))/100
        self.cpPierce = int(row.loc["Shield Pierce"].strip('%'))/100
        self.CD = int(row.loc["Cooldown"].strip('%'))/100
        self.maxEnergy = row.loc["Max Energy"]
        self.eRecharge = row.loc["Energy Recharge"]
        self.TrueDamage = np.linspace(row.loc["True Damage (Level 1)"],row.loc["True Damage (Level 12)"],12) 
        self.shield = row.loc["Shield"]
        self.armor = row.loc["Armor"]
        self.health = row.loc["Health"]
        self.cost = row.loc["Cost"]
        self.description = row.loc["Description"]
    
    def __repr__(self):
        return self.name + ": " + self.description

class perk_stat:
    def __init__(self,row):
        self.name = row.iloc[0]
        self.baseDamage = np.linspace(row.loc["Base Damage (Level 1)"],row.loc["Base Damage (Level 12)"],12) 
        self.cpRatio = int(row.loc["Crystal Ratio"].strip('%'))/100
        self.wpRatio = int(row.loc["Weapon Ratio"].strip('%'))/100
        self.type = row.loc["Type"]
        self.remarks = row.loc["Remarks"]
        self.description = row.loc["Description"]
        
    def __repr__(self):
        return self.description
        
    def damage(self, level, weapon=0, crystal=0, targetHealth=0):
        dmg = self.baseDamage[level-1]
        
        dmgType = self.type
        
        if dmgType == "Crystal":
            dmg += self.cpRatio*crystal
        elif dmgType == "Weapon":
            dmg += self.wpRatio*weapon
        elif dmgType == "Skaarf":
            dmg += targetHealth* ((int(self.remarks).strip('%'))+self.cpRatio*crystal)/100
            dmgType = "Crystal"
        return dmg, dmgType



hStats = {}
iStats = {}
pStats = {}

for i in range(len(hero_stats)):
    hero = hero_stat(hero_stats.iloc[i])
    hStats[hero.name] = hero


for i in range(len(item_stats)):
    item = item_stat(item_stats.iloc[i])
    iStats[item.name] = item    

for i in range(len(perk_stats)):
    perk = perk_stat(perk_stats.iloc[i])
    pStats[perk.name] = perk

if __name__ == "__main__":
    print("Hero stats initialized.")
    print("Item stats initialized.")
    print("Perk stats initialized.")
    
    #hero = "Adagio"
    #print( not perk_stats[perk_stats["Hero"].isin([hero])].empty)
    
    
    

    
