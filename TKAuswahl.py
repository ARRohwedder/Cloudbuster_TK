# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 11:50:13 2025

@author: Dr. Arndt Rohwedder, Core Facility Imaging, ZMF, JKU Linz
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import lib.stackprep
import lib.names
import lib.ioply
import lib.o3dproc
import lib.scriptmaker
import lib.statistics
import gc
import numpy as np
import matplotlib.pyplot as plt

backgrounds =['black','white']
bodies = ['Torus','Ellipsoid','Parabolid','Hor. Cylinder','Vert. Cylinder']

class SingleDialog:

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.imagelabel = tk.Label(top, text='Load a stack image')
        self.imagelabel.pack()
        self.button_imagestack = tk.Button(top,text = "Image Stack:",command=self.browsefiles)
        self.button_imagestack.pack()
        self.xdimlabel = tk.Label(top, text='X pixel dimensions:')
        self.xdimlabel.pack()
        self.xdimentryBox = tk.Entry(top)
        self.xdimentryBox.pack()
        self.ydimlabel = tk.Label(top, text='Y pixel dimensions:')
        self.ydimlabel.pack()
        self.ydimentryBox = tk.Entry(top)
        self.ydimentryBox.pack()
        self.zdimlabel = tk.Label(top, text='Z pixel dimensions:')
        self.zdimlabel.pack()
        self.zdimentryBox = tk.Entry(top)
        self.zdimentryBox.pack()
        self.mySubmitButton = tk.Button(top, text='Start Analysis', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        self.top.destroy()
        
    def browsefiles(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select image stack",filetypes = (("tif files","*.tif*"),("all files","*.*")))
        self.stackobj = lib.stackprep.imprep()
        self.im,fehler,self.xvalue,self.yvalue,self.zvalue = self.stackobj.openfile(self.filename)
        self.xdimentryBox.insert(0,self.xvalue)
        self.ydimentryBox.insert(0,self.yvalue)
        self.zdimentryBox.insert(0,self.zvalue)
        makemax = np.max(self.im,axis=0)
        transfer = plt.imshow(makemax)
        plt.show()
        

class ScriptDialog:

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.geometry("200x100")
        self.imagelabel = tk.Label(top, height = 2, width = 20, text='Make a script file for \n high throughput analysis')
        self.imagelabel.pack()
        self.button_imagefolder = tk.Button(top,height = 1, width = 20, text = "Image Folder:",command=self.browsefolder)
        self.button_imagefolder.pack()
        self.mySubmitButton = tk.Button(top,height = 1, width = 20,bg = 'SpringGreen',text='Start Script Generation', command=self.send)
        self.mySubmitButton.pack()

    def browsefolder(self):
        self.foldername = filedialog.askdirectory()

    def send(self):
        self.top.destroy()

class MassDialog:

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.geometry("200x100")
        self.imagelabel = tk.Label(top, height = 2, width = 20,text='Load a script file to process')
        self.imagelabel.pack()
        self.button_imagefolder = tk.Button(top,height = 1, width = 20,text = "Script file:",command=self.browsefile)
        self.button_imagefolder.pack()
        self.mySubmitButton = tk.Button(top,height = 1, width = 20,bg = 'SpringGreen', text='Start Analysis', command=self.send)
        self.mySubmitButton.pack()

    def browsefile(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select image stack",filetypes = (("txt files","*.txt*"),("all files","*.*")))

    def send(self):
        self.top.destroy()

class AccuDialog:

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.geometry("200x100")
        self.acculabel = tk.Label(top, height = 2, width = 30, text='Collect and combine results from  \n different locations')
        self.acculabel.pack()
        self.button_accufolder = tk.Button(top,height = 1, width = 20,text = "Main Results Folder:",command=self.browsefolder)
        self.button_accufolder.pack()
        self.mySubmitButton = tk.Button(top, height = 1, width = 20,bg = 'SpringGreen',text='Start Collecting Results', command=self.send)
        self.mySubmitButton.pack()        

    def browsefolder(self):
        self.foldername = filedialog.askdirectory()

    def send(self):
        self.top.destroy()

class AnaDialog:

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.geometry("300x100+100+100")
        self.imagelabel = tk.Label(top, text='Load a results file to process')
        self.imagelabel.pack()
        self.button_imagefolder = tk.Button(top,height = 1, width = 20,text = "Results file:",command=self.browsefile)
        self.button_imagefolder.pack()
        self.mySubmitButton = tk.Button(top, height = 1, width = 20,bg = 'SpringGreen', text='Start Analysis', command=self.send)
        self.mySubmitButton.pack()

    def browsefile(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select image stack",filetypes = (("csv files","*.csv*"),("all files","*.*")))

    def send(self):
        self.top.destroy()


class BodyDialog:

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.bchoicelabel = tk.Label(top, text='Choose geom. body to fit:')
        self.bchoicelabel.pack()
        self.bchoicename = tk.StringVar(top)
        self.bchoicename.set(bodies[0])
        self.bchoicemenu = tk.OptionMenu(top, self.bchoicename, *bodies)
        self.bchoicemenu.pack()
        self.mySubmitButton = tk.Button(top, text='OK', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        self.top.destroy()

class BgDialog:

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.bgchoicelabel = tk.Label(top, text='Choose image background color:')
        self.bgchoicelabel.pack()
        self.bgchoicename = tk.StringVar(top)
        self.bgchoicename.set(backgrounds[0])
        self.bgchoicemenu = tk.OptionMenu(top, self.bgchoicename, *backgrounds)
        self.bgchoicemenu.pack()
        self.mySubmitButton = tk.Button(top, text='OK', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        self.top.destroy()

class ColumnchoiceDialog:

    def __init__(self, parent,pars,textpart):
        top = self.top = tk.Toplevel(parent)
        self.columnchoicelabel = tk.Label(top, text=textpart)
        self.columnchoicelabel.pack()
        self.columnchoicename = tk.StringVar(top)
        self.columnchoicemenu = tk.Listbox(top, selectmode = "multiple")
        self.columnchoicemenu.pack(padx = 10, pady = 10, expand = True, fill = "both")

        for item in range(len(pars)):
        	self.columnchoicemenu.insert(0,pars[item])
        	self.columnchoicemenu.itemconfig(item, bg="#bdc1d6")
        
        self.mySubmitButton = tk.Button(top, text='OK', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        self.excludelist = []
        cname = self.columnchoicemenu.curselection()
        for i in cname:
            op = self.columnchoicemenu.get(i)
            self.excludelist.append(op)
        self.top.destroy()


def singlestack():
    
    dimensions = []
    mittel = "/"
    inputDialog = SingleDialog(window)
    window.wait_window(inputDialog.top)
    namepreps = lib.names.nameprep(mittel, inputDialog.filename)
    namelist = namepreps.splitter()
    del namepreps
    
    bgchoiceDialog = BgDialog(window)
    window.wait_window(bgchoiceDialog.top)
    bgvalue = bgchoiceDialog.bgchoicename.get()
    if bgvalue == 'black':
        bg = 0.0
    else:
        bg = 1.0

    dimensions.append(inputDialog.xvalue)
    dimensions.append(inputDialog.yvalue)
    dimensions.append(inputDialog.zvalue)
    
    (wolke,res) = inputDialog.stackobj.arrayprep(inputDialog.im,float(dimensions[0]),float(dimensions[1]),float(dimensions[2]),bg)
    plyhandle = lib.ioply.ioplynow(namelist[3])
    plyhandle.saveplynow(wolke,namelist[1])
    del inputDialog.stackobj
    gc.collect
    
    o3dwork = lib.o3dproc.o3dmeth(namelist,plyhandle,res)
    (resultcoll, bestfit) = o3dwork.o3dcalcul(namelist[1])
    
    messagebox.showinfo("Closest shape: ", bestfit+'\n')

    bchoiceDialog = BodyDialog(window)
    window.wait_window(bchoiceDialog.top)
    shapevalue = bchoiceDialog.bchoicename.get()

    selindex = bodies.index(shapevalue)
    
    print ("Fitting process...")

    results = o3dresults(o3dwork,selindex,namelist,res,resultcoll,plyhandle)

    res1 = "Extension of entire cloud:  X = "+results[0]+" Y = "+results[1]
    res2 = "Extension of central spheroid:  X = "+results[10]+" Y = "+results[11]
    res3 = "Hint: "+results[17]
    res4 = "Number of separated parts = "+results[6]
    res5 = "Dist. from spheroid: Average = "+results[24]+" Average size of separated parts = "+results[28]
    res6 = "Number of extensions = "+results[35]+" Av. length of extensions = "+results[41]
            
    collres = res1 + "\n" + res2 + "\n" + res3 + "\n" + res4 + "\n" + res5 + "\n" + res6
    messagebox.showinfo("Some Key Features:", collres)
    messagebox.showinfo("Results saved in file:", namelist[2]+namelist[1]+".CSV")
    frage = messagebox.askquestion('3D Results', 'Display resulting 3D model?')
    if frage =='yes':
        threeDfile = namelist[1]+"_color"        
        wolke =plyhandle.openplyfile(threeDfile)
        plyhandle.showpcd(wolke)
    else:
        print ('Done')

def scriptprep():
    inputDialog = ScriptDialog(window)
    window.wait_window(inputDialog.top)
    dirname = inputDialog.foldername
    
    bgchoiceDialog = BgDialog(window)
    window.wait_window(bgchoiceDialog.top)
    bgvalue = bgchoiceDialog.bgchoicename.get()

    if bgvalue == 'black':
        bg = 0.0
    else:
        bg = 1.0
    
    bchoiceDialog = BodyDialog(window)
    window.wait_window(bchoiceDialog.top)
    shapevalue = bchoiceDialog.bchoicename.get()
    selindex = bodies.index(shapevalue)

    scriptobj = lib.scriptmaker.scriptmaker(dirname,bg,selindex)
    try:
        text = scriptobj.makescript()
        print (text)
        messagebox.showinfo("Success", text)
    except:
        messagebox.showinfo("Scriptmaker", "No folder selected")
    del scriptobj
    gc.collect()

def mass():
    inputDialog = MassDialog(window)
    window.wait_window(inputDialog.top)
    fname = inputDialog.filename
    mittel = "/"
    scriptfile = open(fname,'r')
    scriptzeilen = scriptfile.readlines()
    namenarray = []
    bgarray = []
    boarray = []
    scriptnamearr = fname.split(mittel)
    scriptfilename = scriptnamearr[len(scriptnamearr)-1]
    scriptfilefolder = fname.replace(scriptfilename,"")
    docname = scriptfilefolder+"failsdoc.txt"
    fails = open(docname,'w')
    fails.writelines("Following files could not be analysed:\n")
    
    for i in list(range(len(scriptzeilen))):#-1
        lineparts = scriptzeilen[i].split(',')
        namenarray.append(lineparts[0])
        bgarray.append(lineparts[1])
        boarray.append(lineparts[2])
    scriptfile.close()
    
    for i in range(len(namenarray)):
        try:
            namepreps = lib.names.nameprep(mittel, namenarray[i])
            namelist = namepreps.splitter()
            del namepreps
          
            print(namelist[1])

            stackobj = lib.stackprep.imprep()
            im,fehler,xvalue,yvalue,zvalue = stackobj.openfile(namenarray[i])
            (wolke,res) = stackobj.arrayprep(im,float(xvalue),float(yvalue),float(zvalue),float(bgarray[i]))
            plyhandle = lib.ioply.ioplynow(namelist[3])
            plyhandle.saveplynow(wolke,namelist[1])
            del stackobj
            gc.collect()
            o3dwork = lib.o3dproc.o3dmeth(namelist,plyhandle,res)
            (resultcoll, bestfit) = o3dwork.o3dcalcul(namelist[1])
            
            print ("Fitting process...")

            selindex = int(boarray[i])
            results = o3dresults(o3dwork,selindex,namelist,res,resultcoll,plyhandle)
        except:
            failtext = namelist[1]+"\n"
            fails.writelines(failtext)
            continue
            
    fails.close()
    messagebox.showinfo("Multiple Image Analysis :", "Process finished. See failsdoc.txt for skipped files.")

def accumulate():
    import lib.sammler
    inputDialog = AccuDialog(window)
    window.wait_window(inputDialog.top)
    dirname = inputDialog.foldername
    try:
        collectobj = lib.sammler.sammler(dirname)
        text = collectobj.collect()
        print (text)
        messagebox.showinfo("Success", text)
    except:
        messagebox.showinfo("Accumulation :", "No folder selected")
    del collectobj
    gc.collect()

def analyse():
    inputDialog = AnaDialog(window)
    window.wait_window(inputDialog.top)
    fname = inputDialog.filename
    datafile = open(fname,'r')
    dataline = datafile.readline()
    namelist = dataline.split(',')
    transcolons = dataline.split(',')
    datafile.close()
    samplenames = []
    gc.collect()
    namelist.reverse()
    
    ### select specific parameters
    
    inputDialog = ColumnchoiceDialog(window,namelist,"Choose parameter containing sample names")
    window.wait_window(inputDialog.top)
    samplenames = inputDialog.excludelist[0]
    namelist.remove(samplenames)
    ### filenames removed
    
    #message: Remove text containing parameters
    text = "Make sure to remove all parameters containing text data"
    messagebox.showinfo("Notice: ", text, icon='info')
    
    
    inputDialog = ColumnchoiceDialog(window,namelist,"Choose parameters to exclude from analysis")
    window.wait_window(inputDialog.top)
    exparmvalue = inputDialog.excludelist
    for i in range(0,len(exparmvalue)):
        namelist.remove(exparmvalue[i])
    ### excluded parameters removed

    #try:
    calculation = lib.statistics.statistics(fname,namelist,samplenames,transcolons)
    text = calculation.compute()
    messagebox.showinfo("Results :", text, icon='info')
    del calculation
    gc.collect()
    #except:
     #   messagebox.showinfo("Analysis :", "Process failed", icon='error')
    
def o3dresults(o3dwork,selindex,namelist,resolution,resultcoll,plyhandle):
    resultsfile = namelist[2]+namelist[1]+"_final_results.csv"
    (results,resheader) = o3dwork.o3dextcalc(selindex,resultcoll)
    f = open(resultsfile,"w")
    outline = (','.join(resheader))+'\n'
    f.writelines(outline)
    outline = (','.join([str(x) for x in results]))+'\n'
    f.writelines(outline)
    f.close
    del o3dwork
    gc.collect
    return results

window = tk.Tk()
window.title('Cloudbuster tk')
window.geometry("400x300+300+200")

frame=tk.Frame(window)
frame.pack()


labelinfo = tk.Label(frame, text="Attention: Does not work with multichannel stacks!")
labelinfo.pack()

labelsingle = tk.Label(frame, text="Analyse a single image stack")
labelsingle.pack()

button_single = tk.Button(frame, height = 1, width = 100,bg = 'SpringGreen',text = "Single stack analysis",command=singlestack)
button_single.pack()

labelmulti = tk.Label(frame, text="Analyse multiple image stacks\n Build scriptfile first:")
labelmulti.pack()

button_script = tk.Button(frame,height = 1, width = 100,bg = 'Cyan',text = "Script Maker",command=scriptprep)
button_script.pack()

button_multi = tk.Button(frame,height = 1, width = 100,bg = 'SpringGreen',text = "Multiple cloud analysis",command=mass)
button_multi.pack()

labelcombi = tk.Label(frame, text="Combine results in folders to table")
labelcombi.pack()

button_combi = tk.Button(frame,height = 1, width = 100,bg = 'Cyan',text = "Results accumulation",command=accumulate)
button_combi.pack()

labelstat = tk.Label(frame, text="Data analysis from results table")
labelstat.pack()

button_stat = tk.Button(frame,height = 1, width = 100,bg = 'Gold',text = "Data analysis",command=analyse)
button_stat.pack()

button_quit = tk.Button(frame,text = "Quit",command=window.destroy)
button_quit.pack()

window.mainloop()
