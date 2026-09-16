# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 11:23:29 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""

import numpy as np

from skimage import io
from skimage import transform
from skimage.draw import rectangle_perimeter
from skimage import filters
from skimage import feature

#from skimage import measure

class imprep:
    
    def __init__(self,):
        x=0
        
    def __del__(self):
        x = 0

    def openfile (self,fname):
        self.file = fname
        xvalue = 0
        yvalue = 0
        zvalue = 0
        zhelp = ""
        xstrarray = []
        ystrarray = []
        zstrarray = []
        try:
            im = io.imread(self.file)

            import tifffile
            with tifffile.TiffFile(self.file) as tif:
                tif_tags = {}
                for tag in tif.pages[0].tags.values():
                    name, value = tag.name, tag.value

                    if "spacing" in str(value):
                        zhelp = str(value)
                        zstrarray = zhelp.split("\n")
                        for i in range(len(zstrarray)):
                           if "spacing" in zstrarray[i]:
                               zvalue = zstrarray[i].split("=")[1]
                    if "XResolution" in name:
                        xstrarray = list(value)
                        xvalue = xstrarray[1]/xstrarray[0]

                    if "YResolution" in name:
                        ystrarray = list(value)
                        yvalue = ystrarray[1]/ystrarray[0]

        except:
            fehler = "-1"
            return im,fehler,xvalue,yvalue,zvalue
        else:
            fehler = "0"
            return im,fehler,xvalue,yvalue,zvalue
        
    def imratio (self,im,x,y,z):

        largest = 0
        ratio = 0
        zxratio = 0
        dimensions = []
        largest = np.max(im.shape)
        ratio = 750/largest

        zxratio = z/x

        dimensions.append(zxratio*ratio)
        dimensions.append(ratio)
        dimensions.append(ratio)
        
        return dimensions
    
    def sortscale (self,im,x,y,z,hinter):
        
        imscale = []
        bild = []
        bild2 = []

        bild2 = transform.rescale(im, (z,y,x),mode="edge",preserve_range=False)
        start = (1, 1)
        for slide in range(bild2.shape[0]-1):
            einzelbild = bild2[slide]
            endx = (einzelbild.shape[0])-2
            endy = (einzelbild.shape[1])-2
            end = (endx, endy)
            rr, cc = rectangle_perimeter(start, end, shape=einzelbild.shape)
            einzelbild[rr, cc] = hinter
            bild2[slide] = einzelbild
        bild = np.full((1,bild2.shape[1], bild2.shape[2]), hinter)
        imscale = np.concatenate([bild,bild2,bild])

        return imscale
    
    def threshold (self,im):

        thresh = filters.threshold_li(im)
        binary = im > thresh
        return binary
    
    def rotate (self,im):

        a = np.empty(3, dtype=object)
        a[0] = im
        a[1] = np.transpose(a[0], (1, 0, 2))
        a[2] = np.transpose(a[0], (1, 2, 0))
        return a

#edgedetection based
    def positions (self,im):

        edgestack = np.empty(3, dtype=object)
        bild = 0
        for bild in list(range(im.shape[0])):
            edges = []
            result = []
            positionsarray = []
            poscollect = []
            zwert = 0
            image = im[bild]
            for zwert in list(range(image.shape[0])):
                edges = feature.canny(image[zwert],sigma=2)#,sigma=2 sigma bislang nicht verwendet
                result = np.where(edges == True)

                positionsarray = np.asarray(list(zip(result[0], result[1])))
                poscollect.append(positionsarray)

            edgestack[bild] = poscollect
        return edgestack

    
    def calibration (self,im,xvalue,yvalue,zvalue):
        largest = np.max(im.shape)
        fullrangeo = largest * xvalue
        pixelres = fullrangeo/750
        
        return pixelres
        
    
    def arrayprep (self,im,xvalue,yvalue,zvalue,bg):

        resolution = self.calibration(im,xvalue,yvalue,zvalue)
        print('resolution calibration calculation completed')
        transfer = self.imratio(im,xvalue,yvalue,zvalue)
        print('ratio factors transmission completed')
        finalscale = self.sortscale(im,transfer[2],transfer[1],transfer[0],bg)
        print('scaling application completed')
        binary =self.threshold(finalscale)
        print('threshold completed')
        rotated = self.rotate(binary)
        print('rotation completed')
        kanten = self.positions(rotated)
        print('point extraction completed')
        import lib.cloudprep
        cloudobj = lib.cloudprep.wolke()
        wolkenstack = cloudobj.carrayprep(kanten)
        print('point cloud preparation completed')
        return (wolkenstack,resolution)


#contourdetection based
#    def positions (self,im):
#
#        edgestack = np.empty(3, dtype=object)
#        bild = 0
#        for bild in list(range(im.shape[0])):
#
#            positionsarray = []
#            poscollect = []
#            zwert = 0
#            image = im[bild]
#            for zwert in list(range(image.shape[0])):
#
#                kak = []
#                kak2 = []
#            
#                contours = measure.find_contours(image[zwert])
#                for contour in contours:
#    
#                    res = np.hsplit(contour, 2)
#                    a = res[0]
#                    b = res[1]
#
#                    for j in range (len(a)):
#                       
#                        kak.extend(a[j])
#                        kak2.extend(b[j])
#
#                positionsarray = np.asarray(list(zip(kak,kak2)))
#                poscollect.append(positionsarray)
#
#            edgestack[bild] = poscollect
#            
#        return edgestack
    