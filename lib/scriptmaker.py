# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 12:39:51 2022

@author: Dr. Arndt Rohwedder
"""
import os
#import tifffile as tf

class scriptmaker:
    def __init__(self,direct,background,fitbody):
        self.dirname = direct
        self.mittel = os.path.sep
        self.bg = background
        self.fb = fitbody

    def __del__(self):
        x=0

    def makescript (self):
        #folder = self.dirname+self.mittel
        outfile = self.dirname+self.mittel+"script.txt"
        listOfFiles = list()
        tiflist = []
        fulllist = []
        endscript = open(outfile, "w" )
        for (dirpath, dirnames, filenames) in os.walk(self.dirname):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        for line in list(range(len(listOfFiles))):
            singlefile = listOfFiles[line]
            getrennt = singlefile.split(self.mittel)
            zwischen = getrennt[len(getrennt)-1]
            test = ('.tif' in zwischen)
            if test == True :
                tiflist.append(zwischen)
                fulllist.append(singlefile)
                print (singlefile)
        for single in list(range(len(tiflist))):
            fulllist[single] = fulllist[single].replace(self.mittel,'/')
            ausgabezeile = fulllist[single]+","+str(self.bg)+","+str(self.fb)+"\n"
            endscript.writelines(ausgabezeile)
        #ausgabezeile = "\n"
        endscript.writelines(ausgabezeile)
        endscript.close()
        text = "Script file generated: \n"+outfile
        return text

