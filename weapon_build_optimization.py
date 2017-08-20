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
from Basic_Attack import *


"""
Weapon Optimization
"""

t3WP = ["Bonesaw","Breaking Point", "Tension Bow", "Tornado Trigger", "Tyrants Monocle", "Poisoned Shiv","Sorrowblade", "Serpents Mask"]

def optimize_WP_build(source, sLevel, target, tLevel, targetItems = [], slots = 3):
    combo_list = []
    for combo in itertools.combinations(t3WP, slots):
        time, autos = baFight(source, sLevel, target, tLevel, combo, targetItems)
        combo_list.append([combo, time, autos])
        
    combo_list.sort(key=itemgetter(1))
    return combo_list


if __name__ == "__main__":
    source = "Vox"
    sLevel = 12
    
    target = "Adagio"
    tLevel = 12
    targetItems = []
    
    
    build = optimize_WP_build(source, sLevel, target, tLevel, targetItems)
    
    
    for i in build[:3]:
        print(i[0],"time: %.2f" % i[1], ", ", i[2], "autos")
        
