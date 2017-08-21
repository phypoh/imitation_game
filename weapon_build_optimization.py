#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 21:09:02 2017

@author: phypoh
"""
import numpy as np
import math
import itertools
from operator import itemgetter
from basic_attack import *


"""
Weapon Optimization
"""

t3WP = ["Bonesaw","Breaking Point", "Tension Bow", "Tornado Trigger", "Tyrants Monocle", "Poisoned Shiv","Sorrowblade", "Serpents Mask"]

def optimize_WP_build(source, sLevel, target, tLevel, targetItems = [], slots = 3):
    combo_list = []
    for combo in itertools.combinations_with_replacement(t3WP, slots):
    #for combo in itertools.product(t3WP, repeat = slots):
        time, autos = baFight(source, sLevel, target, tLevel, combo, targetItems)
        combo_list.append([combo, time, autos])
        
    combo_list.sort(key=itemgetter(1))
    return combo_list


if __name__ == "__main__":
    source = "Vox"
    sLevel = 12
    
    target = "Glaive"
    tLevel = 12
    targetItems = []
    
    
    build = optimize_WP_build(source, sLevel, target, tLevel, targetItems)
    print("Source:", source + ", Level:", sLevel)
    print("Target:", target + ", Level:", tLevel)
    print("Target Inventory: ", targetItems)
    
    
    for i in build[:5]:
        print(i[0],"time: %.2f" % i[1], ", ", i[2], "autos")
    """
    
    for i in build:
        if "Poisoned Shiv" in i[0]:
            print(i)
    """    
    
