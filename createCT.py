#Creates Control Case
#John Connors 
#7/28/2020

import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

'''This file is used to create the control case for the Experiment model. It takes the grids from the original yGrid.py run 
and creates a grid without a reefpit or motu.'''


class Control: 

    #Needs the .grd files, input files and bounds file. 
    def __init__(self, X, Z, expInputs, controlInputs, boundsfile): 

        X = pd.read_csv(X, delimiter= ' ', header = None)
        Z =  pd.read_csv(Z, delimiter= ' ', header = None)
        bounds = pd.read_csv(boundsfile, delimiter= ' ', header=None)
        self.bounds = bounds.to_numpy()
        self.xgrd = X.to_numpy()
        self.zdep = Z.to_numpy()

        exp =  pd.read_csv(expInputs, delimiter= ' ', header = None)
        ct =  pd.read_csv(controlInputs, delimiter= ' ', header = None)
        exp = exp.to_numpy()
        ct = ct.to_numpy()

        self.ExpFile = exp[:,2]
        self.ctFile = ct[:,2]

    #Gets the differences between the 2 files, experiment and control. 
    def getDiffs(self):
        ct_dep = self.ctFile[np.where(self.ExpFile != self.ctFile)]
        return ct_dep

    #Removes the motu
    def removeMotu(self, filename): 
        ct_dep = self.getDiffs()
        rfInds = np.where(self.zdep == ct_dep[0])
        dists = self.xgrd[rfInds]

        sne = []
        sne.append(dists[0])
        sne.append(dists[len(dists) - 1])

        zCopy = self.zdep
        zCopy[np.where((self.xgrd >= sne[0]) & (self.xgrd <= sne[1]))] = ct_dep[0]
        ctDepFile = np.savetxt(filename, zCopy, delimiter=' ')
        return ctDepFile

    #Removes the reef pit. 
    def removeRP(self, filename): 
        rpBounds = self.bounds[2:4,2].astype(float)
        ct_dep = self.getDiffs()

        zCopy = self.zdep
        zCopy[np.where((self.xgrd >= rpBounds[0]) & (self.xgrd <= rpBounds[1]))] = ct_dep[0]
        ctDepFile = np.savetxt(filename, zCopy, delimiter=' ')     
        return ctDepFile

# The files needed to run this code are: 
    #The original .grd files from the yGrid.py run so yGrid.py needs to be run first! 
    #If you have already ran yGrid.py the next files needed are the .dep file 
    #ANOTHER inputs file created for the control case.
    #the original inputs file from the yGrid.py run. 
    #The Bounds file generated from the yGrid.py run. 

ct = Control('Exp1X.grd', 'Exp1Z.dep', 'Inputs2D.txt', 'ct_Inputs.txt', 'Exp1Bounds.txt')
ct.getDiffs()

#Uncomment ONE of the below function calls. They cannot both be uncommented at the same time. 
    #One removes the motu, the other removes the Reef pit. 
    #The parameter in the () is the name of the out put file. To avoid overwriting your file: 
    #name the new .dep file something different. It will generate the control .dep file. 

# ct.removeMotu('noMotuZ.dep')
# ct.removeRP('ctZ.dep')
