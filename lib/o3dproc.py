# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:38:45 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""

from open3d import geometry
import numpy as np
import gc

import lib.orientation
import lib.volumeandsurface
import lib.koerper3D
import lib.extens
import lib.get_mean_center
import lib.bodygeofit

class o3dmeth:
    def __init__(self,namelist,plyhandle,res):
        self.filesinglename = namelist[1]
        self.results_folder = namelist[2]
        self.plhandle = plyhandle
        self.resolution = res
        self.resheader = (
        "PCL_max_x_size",#0
        "PCL_max_y_size",#1
        "PCL_ratio_YX_size",#2
        "PCL_ratio_YZ_size",#3
        "PCL_ratio_XZ_size",#4
        "PCL_shape_hint",#5
        "Sep_Comp_Count",#6
        "Spheroid_rotation_X",#7
        "Spheroid_rotation_Y",#8
        "Spheroid_rotation_Z",#9
        "Spheroid_max_x_size",#10
        "Spheroid_max_y_size",#11
        "Spheroid_ratio_YX_size",#12
        "Spheroid_ratio_YZ_size",#13
        "Spheroid_ratio_XZ_size",#14
        "Spheroid_surface_area",#15
        "Spheroid_Volume",#16
        "Spheroid_shape_hint",#17
        "Dev.Torus",#18
        "Dev.Ellipsoid",#19
        "Dev.Parabolid",#20
        "Dev.Hor. Cylinder",#21
        "Dev.Vert.Cylinder",#22"Dev.Spindle",#23
        "Med_Dist_Sph_to_Frag",#24
        "Av_Dist_Sph_to_Frag",#25
        "Var_Dist_Sph_to_Frag",#26
        "Max_Dist_Sph_to_Frag",#27
        "Med_Surf_of_Frag",#28
        "Av_Surf_of_Frag",#29
        "Var_Surf_of_Frag",#30
        "Max_Surf_of_Frag",#31
        "Med_Vol_of_Frag",#32
        "Av_Vol_of_Frag",#33
        "Var_Vol_of_Frag",#34
        "Max_Vol_of_Frag",#35
        'Ext_Count',#36
        'Ext_Max_Surface',#37
        'Ext_Av_Surface',#38
        'Ext_Med_Surface',#39
        'Ext_Surface_sum',#40
        'Ext_Max_length',#41
        'Ext_Av_length',#42
        'Ext_Med_length',#43
        'Ext_Av_Var_length',#44
        'Brim',#45
        'Narrow',#46
        'Broad',#47
        'Small',#48
        'Diff.to hull',#49
        "PixResol")#50
 
    def __del__(self):
        x=0
        
    def orientcalc (self,pcloud):
        
        box = pcloud.get_oriented_bounding_box()
        boxpunkte = np.asarray(box.get_box_points())
        ori = lib.orientation.orient(boxpunkte)
        (corr,angl) = ori.get_orientation()
        del ori
        gc.collect()

        return corr,angl
    
    def form (self, boxform):
        if ((boxform[0]/boxform[1])< 0.8) or ((boxform[0]/boxform[1])> 1.2):
            inter = "elongated or directed"
        else:
            inter = "round or even spread"
        return inter
    
    def rotatecloud (self,cloud,corrections):
        
        matrixwhat = cloud.get_axis_aligned_bounding_box()
        punkte = np.asarray(matrixwhat.get_box_points())
        box = geometry.PointCloud()
        box = self.plhandle.fillpcd(box,punkte)
        bigcenter = box.get_center()
        R = cloud.get_rotation_matrix_from_axis_angle(corrections)
        wolke = cloud.rotate(R,bigcenter)
        del matrixwhat
        del punkte
        del box
        del bigcenter
        del R
        gc.collect()
        return (wolke)
    
    def koerperarray(self,indexno,coefs,centers,punkte):
        
        kbase = lib.koerper3D.koerper(punkte)
        
        koerpersammlung = [
        kbase.torus(coefs,centers),
        kbase.ellipsoid(coefs,centers),
        kbase.parabolid(coefs,centers),
        kbase.horcylinder(coefs,centers),
        kbase.vertcylinder(coefs,centers)]
        
        koerper3D = koerpersammlung[indexno]
        del kbase
        gc.collect()
        return koerper3D
        
    def difftohull (self,cloud):
        downpcd = cloud.uniform_down_sample(every_k_points = 3)
        hull, _ = downpcd.compute_convex_hull()
        hull = hull.subdivide_loop(number_of_iterations=5)
        hullpoints = geometry.PointCloud()
        hullpoints.points = hull.vertices
        diff = np.mean(downpcd.compute_point_cloud_distance(hullpoints))
        return diff
    
    def shapetest (self, cloud, corrections,bcoef,bigcenter):
        
        namen = ['Torus','Ellipsoid','Parabolid','Hor. Cylinder','Vert. Cylinder']#,'Spindle'
        wolke = self.rotatecloud(cloud, corrections)
        bigform = wolke.get_max_bound()
        coef = (bcoef[0]/2,bcoef[1]/2,bcoef[2]/2)
        pcd = geometry.PointCloud()
        bestvekt = []
        for i in range(len(namen)):
            diff = wolke.compute_point_cloud_distance(self.plhandle.fillpcd(pcd,self.koerperarray(i,coef,bigcenter,100)))#200
            print (namen[i]," Difference -> ",np.mean(diff))
            diffvekt = np.sum(diff)
            bestvekt.append(diffvekt)
        alle = np.sum(bestvekt)
        prozentbest = []
        for i in range(len(namen)):
            prozentbest.append(bestvekt[i]/alle*100)

        bestfit = namen[np.argmin(bestvekt)]
        
        del wolke
        del namen
        del bigform
        del bigcenter
        del coef
        del pcd
        del bestvekt
        del diff
        del diffvekt
        del alle
        gc.collect()
        return prozentbest,bestfit
    
    def fullpcl (self, cloud,res,colorcloud):
                
        resultcoll = []
        wolkenform = cloud.get_max_bound()
        
        (correction,angles) = self.orientcalc(cloud)
        interpret = "Spread "+self.form(wolkenform)
        labels = np.array(cloud.cluster_dbscan(eps=2*res, min_points=10, print_progress=False))

        partcount = labels.max() + 1

        resultcoll.append(str(round((wolkenform[0]*res),4)))
        resultcoll.append(str(round((wolkenform[1]*res),4)))
        resultcoll.append(str(round((wolkenform[1]/wolkenform[0]),4)))
        resultcoll.append(str(round((wolkenform[1]/wolkenform[2]),4)))
        resultcoll.append(str(round((wolkenform[0]/wolkenform[2]),4)))
        resultcoll.append(interpret)
        resultcoll.append(str(partcount))

        for winkel in range(len(angles)):
            resultcoll.append(str(angles[winkel]))

        self.plhandle.savecolorply(cloud,labels,colorcloud)
        del wolkenform
        del correction
        del angles
        gc.collect()
        
        return (labels,partcount,resultcoll)

    def surfvolcalc (self,pcl, res):

        try:
            covex, _ = pcl.compute_convex_hull()
            surface = covex.get_surface_area()
            surface = surface*(res**2)        
            volume = covex.get_volume()
            volume = volume*(res**3)
            del covex
            gc.collect()
        except:
            surface = 0
            volume = 0
            pass
        
        return surface, volume
    
    def covexcentre (self,pcl):
        hull, _ = pcl.compute_convex_hull()
        hull = hull.subdivide_loop(number_of_iterations=4)
        hullpoints = geometry.PointCloud()
        hullpoints.points = hull.vertices
        hullnumbers = np.asarray(hullpoints.points)
        was = np.hsplit(hullnumbers,3)
        wasnb = was[0]
        wasnl = was[1]
        wasnh = was[2]
        oha =np.argmax(was[2])
        central = []
        a = wasnb[oha]
        b = wasnl[oha]
        c = wasnh[oha]
        central.append(a[0])
        central.append(b[0])
        central.append(c[0]/2)
        return central
    
    def bigpcl (self,cloud,labels,max_label,resultcoll, bigname,res):
        
        laenger = 0
        labpos = 0
        for gross in list(range(max_label + 1)):
            results2 = np.where(labels == gross)
            resultlist2 = list(results2[0])
            lang = len(resultlist2)
            if lang > laenger:
                laenger = lang
                labpos = gross
        result = np.where(labels == labpos)

        resultlist = list(result[0])

        bigone = cloud.select_by_index(resultlist)
        
        if int(max_label  +1 ) < 2:
            bigcloud = cloud
        else:
            bigcloud = bigone
        
        gmc = lib.get_mean_center.center(bigcloud)
        center,bcoef=gmc.centcalc()
        #central = self.covexcentre(bigcloud1)
        #center = central

        bigform = []
        for i in range(len(bcoef)):
            bigform.append(bcoef[i])#*2

        (correction,angles) = self.orientcalc(bigcloud)

        (surface,volume) = self.surfvolcalc(bigcloud,res)
        
        self.plhandle.saveply(bigcloud,bigname)
        
        resultcoll.append(str(round((bigform[0]*res),4)))
        resultcoll.append(str(round((bigform[1]*res),4)))
        resultcoll.append(str(round((bigform[1]/bigform[0]),4)))
        resultcoll.append(str(round((bigform[1]/bigform[2]),4)))
        resultcoll.append(str(round((bigform[0]/bigform[2]),4)))
        resultcoll.append(str(round(surface,4)))
        resultcoll.append(str(round(volume,4)))
        interpret = "Spheroid "+self.form(bigform)
        resultcoll.append(interpret)
        (prozentbest,bestfit) = self.shapetest(bigcloud,correction,bcoef,center)
        for shapeprozent in range(len(prozentbest)):
            resultcoll.append(str(round(prozentbest[shapeprozent],4)))
        print ('Best shape = ',bestfit)
        del laenger
        del gmc
        del labpos
        del results2
        del resultlist2
        del lang
        del result
        del resultlist
        del bigone
        del bigform
        del correction
        del angles
        del surface
        del volume
        del interpret
        gc.collect()
        return bigcloud,resultcoll,bestfit

    
    def surfcalc (self,pcl):
        try:
            pcl.estimate_normals()
            form = pcl.get_max_bound()
            sizeform = int(np.max(form))        
            distances = pcl.compute_nearest_neighbor_distance()
            avg_dist = np.mean(distances)
            radii = [10*avg_dist,10*avg_dist,10*avg_dist]
            covex, _ = pcl.compute_convex_hull()

            del pcl
            del form
            del sizeform
            del distances
            del avg_dist
            del radii
            gc.collect()
            surface = covex.get_surface_area()

        except:
            surface = 0
            
        return surface
    
            
    def extfract(self,extcloud,fitcloud,labels,max_label,partcount,outfile,indheader,resultscoll,res):
        types = ['Brim','Broad','Narrow','Small']
        brim = 0
        narrow = 0
        broad = 0
        small = 0
        
        sizevect = []
        medvect = []
        avvect = []
        varvect = []
        maxvect = []
        typearray = []
        
        fitarray = np.asarray(fitcloud.points)
        fitarraysize = fitarray.shape[0]
        arealimit = fitarraysize*0.02
        
        fitsize = fitcloud.get_max_bound()
        lengthlimit = (fitsize.max()/2)*0.15
        
        if int(partcount) >= 1:
            outfile = self.results_folder+self.filesinglename+"_ind_exten_results.csv"
            resfile = open( outfile , "w" )
            resfile.writelines(indheader)
            for gross in list(range(max_label+1)):
                results2 = np.where(labels == gross)
                resultlist2 = list(results2[0])
                testcloud = extcloud.select_by_index(resultlist2)
                extpointno = len(testcloud.points)
                if extpointno >= 10:
                    
                    distance =  testcloud.compute_point_cloud_distance(fitcloud)
                    distancearray = np.asarray(distance)
                    size = self.surfcalc(testcloud)*res*res
                    maxdist = np.max(distancearray)
                    avdist = np.average(distancearray)
                    mddist = np.median(distancearray)
                    vardist = np.var(distancearray)
                    maxdistextension =  distancearray.max()
                
                #Brim
                    if maxdistextension <= lengthlimit and size >= arealimit:
                        classification = types[0]
                #Broad
                    if maxdistextension > lengthlimit and size >= arealimit:
                        classification = types[1]
                #Narrow
                    if maxdistextension > lengthlimit and size < arealimit:
                        classification = types[2]
                #Small
                    if maxdistextension <= lengthlimit and size < arealimit:
                        classification = types[3]
                    if size > 0:
                        line = str(gross+1)+","+str(size)+","+str(maxdist)+","+classification+"\n"
                        sizevect.append(size)
                        maxvect.append(maxdist*res)
                        avvect.append(avdist*res)
                        medvect.append(mddist*res)
                        varvect.append(vardist*res)
                        typearray.append(classification)
                        resfile.writelines(line)
                    
                if extpointno < 10:
                    partcount = partcount-1
            resfile.close()
            del testcloud
            del distance
            del fitcloud
            del fitarray
            gc.collect()
                          
        
        if int(partcount) < 1:
            
            size = 0
            maxdistextension = 0
            maxdist = 0
            avdist = 0
            mddist = 0
            vardist = 0
            classification = 0
            
            sizevect.append(size)
            maxvect.append(maxdist)
            avvect.append(avdist)
            medvect.append(mddist)
            varvect.append(vardist)
            typearray.append(classification)
            
        for i in range(len(typearray)):
            if np.isin('Brim',typearray[i]) == True:
                brim += 1
            if np.isin('Narrow',typearray[i]) == True:
                narrow += 1
            if np.isin('Broad',typearray[i]) == True:
                broad += 1
            if np.isin('Small',typearray[i]) == True:
                small += 1

        maxsize = np.max(sizevect)
        avsize = np.average(sizevect)
        medsize = np.median(sizevect)
        sumsize = np.sum(sizevect)
        maxlength = np.max(maxvect)
        avlength = np.average(avvect)
        medlength = np.average(medvect)
        varlength = np.average(varvect)
        vectors = [partcount,maxsize,avsize,medsize,sumsize,maxlength,avlength,medlength,varlength,brim,narrow,broad,small]
        
        for res in range (len(vectors)):
            resultscoll.append(str(round((vectors[res]),4)))
            
        return resultscoll

    def pclfract(self,cloud,bigcloud,labels,max_label,partcount,outfile,indheader,resultcoll,res):
        
        distvectors =[]
        surfacevectors = []
        volumevectors = []
        medvect = 0
        avvect = 0
        varvect = 0
        maxvect = 0
        
        indsurfmed = 0
        indsurfav = 0
        indsurfvar = 0
        indsurfmax = 0
        
        indvolmed = 0
        indvolav = 0
        indvolvar = 0
        indvolmax = 0
        
        if int(partcount) > 1:
            outfile = self.results_folder+self.filesinglename+"_ind_parts_results.csv"
            resfile = open( outfile , "w" )
            resfile.writelines(indheader)
            for gross in list(range(max_label + 1)):
                results2 = np.where(labels == gross)
                resultlist2 = list(results2[0])
                testcloud = cloud.select_by_index(resultlist2)
                distance =  bigcloud.compute_point_cloud_distance(testcloud)
                distancearray = np.asarray(distance)
                extpointno = len(testcloud.points)
                if extpointno >= 10:
                    (indsurf,indvol) = self.surfvolcalc(testcloud,res)
                    surfarray = np.asarray(indsurf)
                    volarray = np.asarray(indvol)
                    size = indsurf
                    if (distancearray.mean()) > 1 and (indvol) > 0 and (indsurf) > 0:
                        distvectors.append(distancearray.mean())
                        surfacevectors.append(surfarray.mean())
                        volumevectors.append(volarray.mean())
                        line = str(gross+1)+","+str(size)+","+str(np.average(distancearray))+"\n"
                        resfile.writelines(line)
                if extpointno < 10:
                    partcount = partcount-1
            resfile.close()
            del testcloud
            del distance
            del distancearray
            del surfarray
            del volarray
            del cloud
            del bigcloud
            gc.collect()
            
            medvect = np.median(distvectors)
            avvect = np.average(distvectors)
            varvect = np.var(distvectors)
            maxvect = np.max(distvectors)
            
            indsurfmed = np.median(surfacevectors)
            indsurfav = np.average(surfacevectors)
            indsurfvar = np.var(surfacevectors)
            indsurfmax = np.max(surfacevectors)
            
            indvolmed = np.median(volumevectors)
            indvolav = np.average(volumevectors)
            indvolvar = np.var(volumevectors)
            indvolmax = np.max(volumevectors)
            
        vectmedavvar = [medvect,avvect,varvect,maxvect]
        vectsurfmedavvarmax = [indsurfmed,indsurfav,indsurfvar,indsurfmax]
        vectvolmedavvarmax = [indvolmed,indvolav,indvolvar,indvolmax]
        
        for medavvar in range(len(vectmedavvar)):
            resultcoll.append(str(round((vectmedavvar[medavvar]*res),4)))

        for surfmedavvarmax in range(len(vectsurfmedavvarmax)):
            resultcoll.append(str(round(vectsurfmedavvarmax[surfmedavvarmax],4)))

        for volmedavvarmax in range(len(vectvolmedavvarmax)):
            resultcoll.append(str(round(vectvolmedavvarmax[volmedavvarmax],4)))

        print ("Fragments calculated")
        return resultcoll

        
    def o3dcalcul (self,plfile):
        
        indheader = "no,size(surf),distance,\n"
        colorcloud = self.filesinglename+"_color"
        bigname = self.filesinglename+"_largest"
        outfile = self.results_folder+self.filesinglename+"_ind_parts_results.csv"
        
        resultcoll = []

        cloud = self.plhandle.openplyfile(plfile)
        (labels,partcount,resultcoll) = self.fullpcl(cloud,self.resolution,colorcloud)
        
        (bigcloud,resultcoll,bestfit) = self.bigpcl(cloud,labels,partcount-1,resultcoll,bigname,self.resolution)
        
        resultcoll = self.pclfract(cloud,bigcloud,labels,partcount-1,partcount,outfile,indheader,resultcoll,self.resolution)
        
        del cloud
        del colorcloud
        del bigcloud
        gc.collect()
        
        return resultcoll, bestfit
    
    def remainsarray(self,indexno,factors,cloudarray):
        
        excalc = lib.extens.extens(factors,cloudarray)
        
        if indexno == 0:
            koerper3D = excalc.torusext()
        elif indexno == 1:
            koerper3D = excalc.ellipext()
        elif indexno == 2:
            koerper3D =excalc.paraext()
        elif indexno == 3:
            koerper3D =excalc.horcyext()
        elif indexno ==4:
            koerper3D =excalc.vertcylext()
            
        del excalc
        gc.collect()
        return koerper3D
    
    
    def o3dextcalc (self, selindex,resultscoll):#selection
        
        indheader = "no,size(area),distance,type,\n"
        
        plyfile = self.filesinglename+"_largest"
        
        bigcloud = self.plhandle.openplyfile(plyfile)
        #wolke = self.plhandle.openplyfile(plyfile)
        
        (correction,angles) = self.orientcalc(bigcloud)
        
        wolke = self.rotatecloud(bigcloud, correction)
        
        (centerwolke,bcoef) = lib.get_mean_center.center(wolke).centcalc()
        
        cloudarray = np.asarray(wolke.points)

        coefs = lib.bodygeofit.fitproc(self.filesinglename,centerwolke,self.plhandle).fitbody(wolke,selindex,bcoef)
        print ("Selected shape fitted to spheroid")

        factors = centerwolke,coefs

        extension = self.remainsarray(selindex,factors,cloudarray)
        fitname = self.filesinglename+"_fit"
        fittedbody = self.plhandle.openplyfile(fitname)

        extpc = geometry.PointCloud()
        extpc = self.plhandle.fillpcd(extpc,extension)
        extfilename = self.filesinglename+"_extensions"
        self.plhandle.saveply(extpc,extfilename)
        labels = np.array(extpc.cluster_dbscan(eps=10, min_points=100, print_progress=False))
        max_label = 0
        partcount = 0
        outfile = self.results_folder+self.filesinglename+"_results.csv"
        if len(labels) != 0 : 
            max_label = labels.max()
            partcount = max_label + 1

        resultcoll = self.extfract(extpc,fittedbody,labels,max_label,partcount,outfile,indheader,resultscoll,self.resolution)
        
        differencetohull = self.difftohull(wolke)
        reldif = differencetohull/len(wolke.points)
        
        resultcoll.append(str(round((reldif*1000),4)))
        
        resultcoll.append(str(round((self.resolution),4)))
        
        del bigcloud
        del wolke
        del cloudarray
        del extension
        del fittedbody
        del extpc
        gc.collect()

        return resultcoll,self.resheader
