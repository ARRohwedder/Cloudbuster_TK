# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:29:44 2023

@author: Dr. Arndt Rohwedder, Core Facility Imaging, ZMF, JKU Linz
"""
import os

class nameprep:

    def __init__(self,sep,file):
        self.mittel = sep
        self.fullpath = file

    def __del__(self):
        x=0
        
    def splitter (self):
        namelist = []
        
        getrenntarr = self.fullpath.split(self.mittel)
        fullname = getrenntarr[len(getrenntarr)-1]
        filename = fullname.split(".")[0]
        (results_folder,folder_3D,basefolder) = self.folders(fullname,filename)
        namelist.append(fullname)
        namelist.append(filename)
        namelist.append(results_folder)
        namelist.append(folder_3D)
        namelist.append(basefolder)

        return namelist

    def folders (self,fname,sname):

        basefolder = self.fullpath.replace(fname,"")
        results_folder = basefolder+sname+self.mittel+"results"+self.mittel
        folder_3D = basefolder+sname+self.mittel+"3D_files"+self.mittel
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)
        if not os.path.exists(folder_3D):
            os.makedirs(folder_3D)


        return results_folder, folder_3D, basefolder


