import numpy as np
from open3d import geometry
#import lib.ioply
import lib.koerper3D

class fitproc:
    def __init__(self,filename,stcenter,plyhandle):
        self.fname = filename
        self.startcenter = stcenter
        self.plhandle = plyhandle

    def __del__(self):
        x=0

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
        return koerper3D

    def cloudsyn (self,cloud,index,coef):
        testcloud = geometry.PointCloud()
        testcloud = self.plhandle.fillpcd(testcloud,self.koerperarray(index,coef,self.startcenter,100))#200
        unterschied = geometry.PointCloud.compute_point_cloud_distance(cloud,testcloud)
        return unterschied
        
    def fitbody (self, cloud,index,coef):
        
        coef =(coef[0]*0.3,coef[1]*0.3,coef[2]*1.5)
        coef = list(coef)
        
        cloud2 = cloud.voxel_down_sample(voxel_size=0.1)

        for i in range (2):
            
            unterschied = self.cloudsyn(cloud2,index,coef)
            coef[i] = coef[i]+(np.median(unterschied)/10)
            unterschied1 = self.cloudsyn(cloud2,index,coef)
            transcoef = coef

            while (np.quantile(unterschied1,0.2)<np.quantile(unterschied,0.2)):
                
                transcoef = coef
                print (np.quantile(unterschied,0.2))
                coef[i] = coef[i]+(np.median(unterschied)/10)
                unterschied = unterschied1
                unterschied1 = self.cloudsyn(cloud,index,coef)

        outfile = self.fname+"_fit"
        transcloud = geometry.PointCloud()
        transcloud = self.plhandle.fillpcd(transcloud,self.koerperarray(index,transcoef,self.startcenter,400))
        transcloud.remove_duplicated_points()
        self.plhandle.saveply(transcloud,outfile)
        return transcoef
        
        
            
