#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 21:09:02 2017

@author: phypoh
"""
import numpy as np
import math
from initialize import *


"""
Main Fight Simulator
"""

def baFight(source, sLevel, target, tLevel, sourceItems = [], targetItems = [], stutter = False):
    
    source = hStats[source]
    target = hStats[target]
    
    maxHealth = targetHealth(target, tLevel, targetItems)
    
    period = baTime(source, sLevel, sourceItems)
    #print("Period:", period)
    
    tHealth = maxHealth
    time = 0
    autos = 0
    totalDmg = 0
    
    stacksBS = 0
    stacksBP = 0
    stacksBM = 0
    tbowTime = 0
    
    
    shield = target.defense[tLevel-1]
    for item in targetItems:
        shield += iStats[item].shield
    
    armor = target.defense[tLevel-1]
    for item in targetItems:
        armor += iStats[item].armor

    wpPierce = 0    
    for item in sourceItems:
        wpPierce += iStats[item].wpPierce
    
    cpPierce = 0
    for item in sourceItems:
        cpPierce += iStats[item].cpPierce
    
    while tHealth > 0:
        rawWP, rawCP = baDmg(source, sLevel, target, tLevel, sourceItems, targetItems, stacksBP)
        
        newArmor = armor - stacksBS * armor * 0.05
        if newArmor < 0:
            newArmor = 0    

        #Account for Perk        
        perkWP = 0
        perkCP = 0
        if source.name in pStats:
            if pStats[source.name].remarks == "Spell":
                perkWP, perkCP = perkDmg(source, sLevel, target, tLevel, sourceItems, targetItems, stacksBP)
                if source.name == "Lyra":                
                    heavyWP, heavyCP = perkDmg(source, sLevel, target, tLevel, sourceItems, targetItems, stacksBP, True)
                    perkWP += heavyWP
                    perkCP += heavyCP

            elif pStats[source.name].remarks == "Alternate" and autos%2 == 1:
                perkWP, perkCP = perkDmg(source, sLevel, target, tLevel, sourceItems, targetItems, stacksBP)
                
        rawWP += perkWP
        rawCP += perkCP
        
        #Account for Tension Bow
        if "Tension Bow" in sourceItems:
            tbowTime = time - period
            if time == 0 or (tbowTime%6) > (time%6):
                rawWP += 180
                #print("Tension Bow proced")
        
        dmgWP = raw2received(rawWP, wpPierce, newArmor)
        
        dmgCP = raw2received(rawCP, cpPierce, shield)
        
        #Account for Broken Myth
        if "Broken Myth" in sourceItems:
            stacksBM = np.floor(time)
            if stacksBM > 9:
                stacksBM = 9
            dmgCP += 0.04*stacksBM*dmgCP
        
        tHealth -= (dmgWP + dmgCP)
        
        totalDmg += dmgWP + dmgCP      
        
        #print(int(totalDmg), stacksBP, stacksBS)
        
        #Account for Breaking Point 
        #Gain 10 Weapon Power for every 140 damage done to enemy heroes, +5/10 (Melee/Ranged) damage needed for each stack thereafter. 20 stacks max. Decays 3 stacks per second after you've stopped attacking for 2.5 seconds
        if "Breaking Point" in sourceItems:
            if source.range < 5:   #if melee hero
                a = 5
                b = 135
                c = -totalDmg
                stacksBP = np.floor((- b + math.sqrt(b**2 - 4*a*c))/(2*a))
        
            elif source.range >= 5: #if ranged hero 
                a = 5/2
                b = 275/2
                c = -totalDmg
                stacksBP = np.floor((- b + math.sqrt(b**2 - 4*a*c))/(2*a))
            
            if stacksBP > 20:
                stacksBP = 20
                
        #Account for Bonesaw
        if ("Bonesaw" in sourceItems) and (stacksBS < 8):
            stacksBS += 1
            
        time += period
        autos += 1
    
    return time, autos


"""
Damage after Defense
"""
def raw2received(raw_dmg, pierce, defense):
    received = raw_dmg * pierce + raw_dmg * (1-pierce)/(1+defense/100)
    return received

"""
Target Health
"""
def targetHealth(target, tLevel, targetItems):    
    health = target.health[tLevel-1]
    for item in targetItems:
        health += iStats[item].health
    
    return health

"""
Basic Attack Damage
"""
def baDmg(source, sLevel, target, tLevel, sourceItems = [], targetItems = [], stacksBP = 0):
    
    #Weapon
    baseWP = source.weapon[sLevel-1]
    bonusWP = 0
    for item in sourceItems:
        bonusWP += iStats[item].weapon
    
    rawWP = baseWP + bonusWP

    dmgWP = rawWP + stacksBP*10
    
    #Crystal
    dmgCP = 0
    rawCP = 0
    
    for item in sourceItems:
        rawCP += iStats[item].crystal
    
    if "Alternating Current" in sourceItems:
        dmgCP += 70/100/2*rawCP    
        
    return dmgWP, dmgCP

"""
Perk Damage
"""
def perkDmg(source, sLevel, target, tLevel, sourceItems = [], targetItems = [], stacksBP = 0, Lyra = False):
    
    #Weapon
    baseWP = source.weapon[sLevel-1]
    bonusWP = 0
    for item in sourceItems:
        bonusWP += iStats[item].weapon
    
    rawWP = baseWP + bonusWP

    dmgWP = rawWP + stacksBP*10
    
    #Crystal
    dmgCP = 0
    rawCP = 0
    
    for item in sourceItems:
        rawCP += iStats[item].crystal
    

    tHealth = targetHealth(target, tLevel, targetItems)
    
    if Lyra == False:    
        dmg, dmgType = pStats[source.name].damage(sLevel, rawWP, rawCP, tHealth)
    elif Lyra == True:
        dmg, dmgType = pStats["Lyra (Heavy)"].damage(sLevel, rawWP, rawCP, tHealth)
    
    if dmgType == "Weapon":
        return dmg, 0
    elif dmgType == "Crystal":
        return 0, dmg

"""
Basic Attack Time
"""

def baTime(source, sLevel, sourceItems = [], stutter = False):
    
    if stutter == True:
        BAT = source.ACD + source.ADelay
    elif stutter == False:
        BAT = source.ACD + source.ADelay + source.stutterBonus
    
    #Base Attack Speed
    baseAS = source.AS[sLevel-1]
    
    #Bonus Attack Speed
    bonusAS = 0
    for item in sourceItems:
        bonusAS += iStats[item].AS
    
    #Attack Speed Modifier
    ASMod = source.ASMod
    
    #Time Taken for one basic attack
    time = BAT/(baseAS + bonusAS * ASMod)
    
    return time

if __name__ == "__main__":
    source = "Ringo"
    sLevel = 12
    target = "Adagio"
    tLevel = 12
    sourceItems = ["Breaking Point", "Sorrowblade", "Bonesaw"]
    targetItems = []
    
    
    time, autos = baFight(source, sLevel, target, tLevel, sourceItems, targetItems)
    
    print(source)
    print(sourceItems)
    print("Time to kill", target +":", time)
    print("Number of Autos:", autos)