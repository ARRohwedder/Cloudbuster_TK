# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 11:06:19 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""


import pandas as pd
#from pandas import set_option
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale
import re
import numpy as np


class statistics:
    
    def __init__(self,fname,namelist,samplenames,transcolons):
        self.filename = fname
        self.selected = namelist
        self.samples = samplenames
        self.allcolons = transcolons

        
    def __del__(self):
        x=0
        
    def compute (self):
        import lib.names
        mittel = "/"
        namepreps = lib.names.nameprep(mittel, self.filename)
        folderlist = namepreps.splitter()
        basefolder = folderlist[4]
        
        Sphdata = pd.read_csv(self.filename, names=self.allcolons)

        samplefiles = Sphdata[self.samples]
        samplelist = Sphdata[self.samples].tolist()
        samplelist.remove(self.samples)
        Sphdata.drop(index=Sphdata.index[0], axis=0, inplace=True)

        #parameters = list(Sphdata.columns)
        
        notnumeric = []
        
        #Sphdata = Sphdata.apply(lambda x: pd.to_numeric(x, errors = 'ignore'))
        
        for i in range(len(self.selected)):#-1
            wasndas = str(Sphdata.dtypes[self.selected[i]])
            if wasndas == 'object':
                notnumeric.append(self.selected[i])
        
        for i in range(len(notnumeric)):
            self.selected.remove(notnumeric[i])
        
        Reddata = Sphdata[self.selected]

        Reddata[self.selected] = Reddata[self.selected].apply(pd.to_numeric)
            
        #PCA
        import lib.pcacalc
        calcpca = lib.pcacalc.pcacalc(Reddata,basefolder,Sphdata[self.samples].tolist())
        pcares = calcpca.calcul()
        pca_topten = pcares[0]
        pca_topten_txt = pcares[1]
        pcadf_scaled = pcares[2]

        shortdata = Reddata[pca_topten]
        
        remains = self.selected
        
        for i in range(len(pca_topten)):
            remains.remove(pca_topten[i])

        remaindata = Reddata[remains]
        Redarray = remaindata.values
        Redarrayscaled = minmax_scale(Redarray,feature_range=(-1, 1), axis=0)
        Redmean = Redarrayscaled.mean(axis=1)
        
        shortarray = shortdata.values
        shortarrayscaled = minmax_scale(shortarray,feature_range=(-1, 1), axis=0)
        shortmean = shortarrayscaled.mean(axis=1)

        maximavalues = []
        
        for m in range(len(pca_topten)):
            maxwert = Reddata[pca_topten[m]].max()
            maximavalues.append(maxwert)
        
        testsub = Reddata[pca_topten]
        testsub.insert(0, "Samplenames", samplefiles)

        for m in range(len(pca_topten)):
            testsub[pca_topten[m]]=Reddata[pca_topten[m]].div(float(maximavalues[m])).abs()

        boxplot = testsub.boxplot(column=pca_topten, by="Samplenames",layout=(len(pca_topten), 1), rot=90, fontsize=6, figsize=(50,30))

        kfig = basefolder+"grouped_data.svg"
        plt.savefig(kfig)

        #Correlation
        import lib.corcalc

        correl = lib.corcalc.corcalc(shortdata,pca_topten,pcadf_scaled, basefolder)
        pcacor = correl.correlcalc()

        # For grouped data
        datacount = len(shortdata)
        if datacount > 10:
            #DBSCAN Clustering
            import lib.dbscan

            dbsinit1 = lib.dbscan.mydbscan(Redmean,shortmean)
            dbclusters1 = dbsinit1.Dbscancalc()
            
            #K-means clustering
            import lib.kmeans

            kminit1 = lib.kmeans.myKMeans(samplelist,Redmean,shortmean,basefolder,dbclusters1[0])
            clusters1 = kminit1.KMeanscalc()
            
        #plotting
        import lib.figplot

        if datacount > 10:
            plotting = lib.figplot.figplot(pcares[3],pcacor[0],pca_topten,pcacor[3],pcacor[4],clusters1[0],basefolder,len(pca_topten),datacount)
            
        if datacount <= 10:
            plotting = lib.figplot.figplot(pcares[3],pcacor[0],pca_topten,pcacor[3],pcacor[4],pcacor[3],basefolder,len(pca_topten),datacount)#pcacor[3],
            
        plotting.FigPlot()
        
        if datacount > 10:
            text = "PCA : Most relevant (85% of variances) parameters= \n"+pca_topten_txt+"\n\n"+"K-Means Clustering:\n"+str(dbclusters1[0])+" Clusters Identified"+" \n\n"+"Detailed results stored as .csv files and graphs as .svg files in folder: \n"+basefolder
        if datacount <= 10:
            text = "PCA : Most relevant (85% of variances) parameters= \n"+pca_topten_txt+"\n\n"+" \n\n"+"Detailed results stored as .csv files and graphs as .svg files in folder: \n"+basefolder

        return text
