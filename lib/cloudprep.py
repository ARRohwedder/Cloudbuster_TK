# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:05:42 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""

import numpy as np

class wolke:
    
    def __init__(self):
        x=0
        
    def __del__(self):
        x=0
    
    def combined (self,stack):

        wolkenstack = np.empty(3, dtype=object)
        bild = 0
        for bild in list(range(stack.shape[0])):
            zwert = 0
            positions = []
            zeile = []
            poswert = 0
            wolke = []
            positive = stack[bild]
            for zwert in list(range(len(positive))):
                positions = positive[zwert]
                for poswert in list(range(len(positions))):
                    zeile.append(positions[poswert][1])
                    zeile.append(positions[poswert][0])
                    zeile.append(zwert)
                    wolke.append(zeile)
                    zeile = []
            wolkenstack[bild] = wolke
        return wolkenstack
    
    def addingup (self,sammelwolke):

        ordnung = [[0,2,1],[1,2,0]]
        wowert = 0
        count = 0
        gesamt = []
        zwischena = []
        zeile = []
        gesamt = sammelwolke[0]
        for count in range(0,2):
            for wowert in list(range(len(sammelwolke[count+1]))):
                zwischena = sammelwolke[count+1][wowert]
                zeile.append(zwischena[ordnung[count][0]])
                zeile.append(zwischena[ordnung[count][1]])
                zeile.append(zwischena[ordnung[count][2]])
                gesamt.append(zeile)
                zeile = []
            zwischena=[]
        sauber = np.unique(gesamt,axis=0)
        return sauber
    
    def carrayprep(self,stack):
        wolkenstack = self.combined(stack)
        clean = self.addingup(wolkenstack)
        return clean
            
            