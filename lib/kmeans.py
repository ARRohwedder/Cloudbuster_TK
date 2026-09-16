#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 13:00:37 2021

@author: Dr. Arndt Rohwedder
"""
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

class myKMeans:
    def __init__(self,smpls,one,two,fold,dbcount):
        self.samples = smpls
        self.first = one
        self.second = two
        self.basefolder = fold
        self.number = dbcount

    def __del__(self):
        x=0

    def KMeanscalc (self):
        kmdf = pd.DataFrame({'First': self.first,'Second': self.second}, columns=['First','Second'])
        kmdfarray = np.asarray(kmdf)
        kmdf_scalar = StandardScaler().fit(kmdfarray)
        kmdf_rescaled = kmdf_scalar.transform(kmdfarray)
        
        
        kmeans_kwargs = {"init": "random","n_init": 10,"max_iter": 300,"random_state": 42,}
        sse = []
        if self.number < 3:
            self.number = 3
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
            kmeans.fit(kmdf_rescaled)
            sse.append(kmeans.inertia_)

        finalkmeans = KMeans(n_clusters=self.number, random_state=0).fit(kmdf_rescaled)
        order = finalkmeans.labels_

        kmdf_complete = pd.DataFrame(kmdf_rescaled,columns=["High variable data","Low variable data"])
        kmdf_complete.insert(2,'clusters',order,True)

        kmoutdf = pd.DataFrame(self.samples,columns=["samples"])
        kmoutdf.insert(1,'clusters',order,True)

        kmdf_name = self.basefolder+"K_Means_clu.csv"

        kmoutdf.to_csv(kmdf_name)

        kmdf_name = self.basefolder+"K_Means_raw.csv"

        kmdf_complete.to_csv(kmdf_name)
        return kmdf_complete,order
