# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:38:45 2022

@author: Dr. Arndt Rohwedder, Johannes Keppler University, Linz
"""

from open3d import utility
from open3d import io
from open3d import visualization
from open3d import geometry
import matplotlib.pyplot as plt


class ioplynow:
    def __init__(self,filename):
        self.folder_3D = filename
        
    def __del__(self):
        x=0

    def saveplynow (self,nparray,name):
        pcd = geometry.PointCloud()
        pcd.points = utility.Vector3dVector(nparray)
        savefile = self.folder_3D+name+".ply"
        io.write_point_cloud(savefile, pcd)

    def savefromemptyply (self,pcd,nparray,name):
        pcd.points = utility.Vector3dVector(nparray)
        savefile = self.folder_3D+name+".ply"
        io.write_point_cloud(savefile, pcd)

    def saveply (self,pcd,name):
        savefile = self.folder_3D+name+".ply"
        io.write_point_cloud(savefile, pcd)

    def savecolorply (self,pcd,labels,name):
        colors = plt.get_cmap("tab20")(labels / (labels.max() if labels.max() > 0 else 1))
        colors[labels < 0] = 0
        pcd.estimate_normals()
        pcd.colors = utility.Vector3dVector(colors[:, :3])
        savefile = self.folder_3D+name+".ply"
        io.write_point_cloud(savefile, pcd)

    def openplyfile (self,name):
        openfile = self.folder_3D+name+".ply"
        cloud = io.read_point_cloud(openfile)
        return cloud

    def fillpcd (self,pcd,nparray):
        pcd.points = utility.Vector3dVector(nparray)
        return pcd

    def showpcd (self,name):
        pcd = name
        pcd.estimate_normals()
        visualization.draw_geometries([pcd],window_name='Point Cloud',width=750,height=750)
