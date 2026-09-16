# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 15:44:44 2025

@author: Dr. Arndt Rohwedder, Core Facility Imaging, ZMF, JKU Linz
"""

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

class mydbscan:
    def __init__(self,one,two):
        self.first = one
        self.second = two
    
    def __del__(self):
        x=0
        
    def Dbscancalc (self):
        dbsdf = pd.DataFrame({'First': self.first,'Second': self.second}, columns=['First','Second'])
        dbsdfarray = np.asarray(dbsdf)
        dbsdf_scalar = StandardScaler().fit(dbsdfarray)
        dbsdf_rescaled = dbsdf_scalar.transform(dbsdfarray)
        db = DBSCAN(eps=0.05, min_samples=5).fit(dbsdf_rescaled)
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)

        return n_clusters_,n_noise_
