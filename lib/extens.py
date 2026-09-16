

"""
Created on Sun Feb 14 11:03:17 2021

@author: Dr. Arndt Rohwedder, Core Facility Imaging, ZMF, JKU Linz
"""
import numpy as np

class extens:
    
    def __init__(self,fact,numparray):

        self.rx, self.ry, self.rz = fact[1]
        self.cx,self.cy,self.cz = fact[0]
        self.xdata = numparray[:, [0]]
        self.ydata = numparray[:, [1]]
        self.zdata = numparray[:, [2]]
        
        self.xdiffs = np.subtract(self.xdata,self.cx)
        self.ydiffs = np.subtract(self.ydata,self.cy)
        self.zdiffs = np.subtract(self.zdata,self.cz)

    def __del__(self):
        x=0

    def collect (self,hyp1,hyp2):
        
        posx = []
        posy = []
        posz = []
        
        for was in list(range(hyp1.shape[0])):
            if (hyp1[was])>(hyp2[was]):
                posx.append(self.xdata[was])
                posy.append(self.ydata[was])
                posz.append(self.zdata[was])
        left = np.column_stack((posx,posy,posz))
        leftclean = np.unique(left,axis=0)
        
        return leftclean
        
    def ellipext (self):

        orihypos = np.sqrt(np.square(self.xdiffs)+np.square(self.ydiffs)+np.square(self.zdiffs))

        cosu = self.xdiffs/np.sqrt(np.square(self.xdiffs)+np.square(self.ydiffs))
        cosv = np.sqrt(np.square(self.xdiffs)+np.square(self.ydiffs))/orihypos
        
        lambd = np.arccos(cosu)
        theta = np.arccos(cosv)
        
        x = np.multiply((np.multiply(np.cos(theta), np.cos(lambd))),self.rx)
        y = np.multiply((np.multiply(np.cos(theta), np.sin(lambd))),self.ry)
        z = np.multiply(np.sin(theta),self.rz)
        
        sqxsmdiffs = np.square(x)
        sqysmdiffs = np.square(y)
        sqzsmdiffs = np.square(z)
        
        calchypos = np.sqrt(sqxsmdiffs+sqysmdiffs+sqzsmdiffs)

        left = self.collect(orihypos,calchypos)

        self.cloudarray = []
        
        return left
    
    def paraext (self):

        orihypos = np.sqrt(np.square(self.xdiffs)+np.square(self.ydiffs)+np.square(self.zdata))
        cosu = self.xdiffs/np.sqrt(np.square(self.xdiffs)+np.square(self.ydiffs))
        cosv = np.sqrt(np.square(self.xdiffs)+np.square(self.ydiffs))/orihypos
    
        lambd = np.arccos(cosu)
        theta = np.arccos(cosv)

        x = np.multiply((np.multiply(np.cos(theta), np.cos(lambd))),self.ry)
        y = np.multiply(np.multiply(np.cos(theta), np.sin(lambd)),self.rx)
        z = np.multiply(np.sin(theta),self.rz*2.5)
    
        sqxsmdiffs = np.square(x)
        sqysmdiffs = np.square(y)
        sqzsmdiffs = np.square(z)
    
        calchypos = np.sqrt(sqxsmdiffs+sqysmdiffs+sqzsmdiffs)

        left = self.collect(orihypos,calchypos)

        self.cloudarray = []
    
        return left
    
    def torusext (self):
        
        firsthypos = np.hypot(self.xdiffs,self.ydiffs)
        
        thetas1 = np.arctan(self.xdiffs/self.ydiffs)
        
        rthetas1 = (self.rx*self.ry)/(np.sqrt(np.square(self.ry*np.cos(thetas1))+np.square(self.rx*np.sin(thetas1))))
        
        difs1 = rthetas1 - firsthypos
        
        newx = difs1 * np.sin(thetas1)
        
        thetas2 = np.arctan(newx/self.zdiffs)
        
        secondhypos = np.hypot(newx,self.zdiffs)
        
        rthetas2 = (self.rz*(self.ry/2))/(np.sqrt(np.square((self.ry/2)*np.cos(thetas2))+np.square(self.rz*np.sin(thetas2))))
        
        posx = []
        posy = []
        posz = []

        for was in list(range(secondhypos.shape[0])):
            if (secondhypos[was])>(rthetas2[was]):
                posx.append(self.xdata[was])
                posy.append(self.ydata[was])
                posz.append(self.zdata[was])
        
        for was in list(range(firsthypos.shape[0])):
            if (firsthypos[was])>(rthetas1[was]):
                posx.append(self.xdata[was])
                posy.append(self.ydata[was])
                posz.append(self.zdata[was])
                
        left = np.column_stack((posx,posy,posz))
        leftclean = np.unique(left,axis=0)
        self.cloudarray = []

        return leftclean

    
    def horcyext (self):
        
        firsthypos = np.hypot(self.zdiffs,self.xdiffs)
        
        thetas1 = np.arctan(self.zdiffs/self.xdiffs)
        
        rthetas1 = (self.rx*self.rz)/(np.sqrt(np.square(self.rz*np.cos(thetas1))+np.square(self.rx*np.sin(thetas1))))
        
        left = self.collect(firsthypos,rthetas1)
        
        self.cloudarray = []
        
        return left
    
    def vertcylext (self):
        
        firsthypos = np.hypot(self.xdiffs,self.ydiffs)
        
        thetas1 = np.arctan(self.xdiffs/self.ydiffs)
        
        rthetas1 = (self.rx*self.ry)/(np.sqrt(np.square(self.rx*np.cos(thetas1))+np.square(self.ry*np.sin(thetas1))))
        
        left = self.collect(firsthypos,rthetas1)
        
        self.cloudarray = []
        
        return left
    
    def spindleext (self):
        
        factxz = np.sqrt(self.zdata/(self.rz/np.square(self.rx)))
        factyz = np.sqrt(self.zdata/(self.ry/np.square(self.rx)))
        
        firsthypos = np.hypot(self.xdiffs,self.ydiffs)
        
        thetas1 = np.arctan(self.xdiffs/self.ydiffs)
        
        rthetas1 = (factxz*factyz)/(np.sqrt(np.square(factyz*np.cos(thetas1))+np.square(factxz*np.sin(thetas1))))
        
        left = self.collect(firsthypos,rthetas1)
        
        self.cloudarray = []
        
        return left        
        

#   Alternative        
#    def paraext (self):

#        rx, ry, rz = self.factors[1]
#        cx,cy,cz = self.factors[0]
#
#        xdata = self.cloudarray[:, [0]]
#        ydata = self.cloudarray[:, [1]]
#        zdata = self.cloudarray[:, [2]]
        
#        xdiffs = np.subtract(xdata,cx)
#        ydiffs = np.subtract(ydata,cy)
        
#        factx = np.sqrt(zdata/(rx/np.square(rz)))
#        facty = np.sqrt(zdata/(ry/np.square(rz)))
        
#        firsthypos = np.hypot(xdiffs,ydiffs)
        
#        thetas1 = np.arctan(xdiffs/ydiffs)
        
#        rthetas1 = (factx*facty)/(np.sqrt(np.square(facty*np.cos(thetas1))+np.square(factx*np.sin(thetas1))))
        
#        left = self.collect(firsthypos,rthetas1,xdata,ydata,zdata)
        
#        self.cloudarray = []
        
#        return left