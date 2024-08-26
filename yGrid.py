#Y Grid
#07/09/2020

import gridCreation1D as grdC
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

class Ygrid: #Creates the 2D grid 

    #This class will generate the X.grd, Y.grd and Z.dep files, as well as the indices of the start of each geographic feature. 
    #It will create 3 different Z files, one with everything (reef pit, motu, reef flat), one with only the motu and reef flat, and one with just the reef flat. 
    #The files required to run this class are: 
        #Inputs2D.txt

    def __init__(self, filename = '', files = []): 
        #Params Description: 
            #filename is the name of the Inputs2D.txt or another inputs file
            #files is the names of the 3 output files of the 3 Z files. 
            #Please see the readme file to see how the inputs should be entered. 
        
        data = pd.read_csv(filename, delimiter= ' ', header = None)
        self.inputs = np.reshape(data[2].to_numpy(), (data[2].to_numpy().shape[0], 1))

        self.Xdata = self.inputs[:17]
        Xres = self.inputs[22:]
        self.Xdata = np.concatenate([self.Xdata, Xres])

        self.ytotal = np.sum(self.inputs[17:20])
        self.filenames = files #List of names of the output Z files. 
        self.xGrids = []
        self.zGrids = []
        self.totalrfWid = 0
        self.rflatLen = self.inputs[17,0]
        self.rpLen = self.inputs[18,0]
        self.motuLen = self.inputs[19,0] 
        self.Ymin = self.inputs[20,0]
        self.Ymax = self.inputs[21,0]

        self.Ygrd = None

        self.rf1 = (self.rflatLen*0.5) - (self.motuLen*0.5)
        self.motu1 = self.rf1 + (self.motuLen*0.5) - (self.rpLen*0.5)
        self.rp1 = self.motu1 + (self.rpLen*0.5)
        self.rp2 = self.rp1 + (self.rpLen*0.5)
        self.motu2 = self.rp2 + (self.motuLen*0.5) - (self.rpLen*0.5)

        self.Xinds = [0]*6
        self.Yinds = ['Nan']*6

    def Xfiles(self):
        #This is the function that creates the 3 Z file outputs. 
        xdc = self.Xdata
        ZpInputs = xdc
        ZpFile = np.savetxt(self.filenames[0], ZpInputs, delimiter=' ')

        xdc[6, 0] = xdc[4, 0]
        xdc[7, 0] = 0
        ZmInputs = xdc
        ZmFile = np.savetxt(self.filenames[1], ZmInputs, delimiter=' ')

        xdc[11, 0] = 0
        ZrInputs = xdc
        ZrFile = np.savetxt(self.filenames[2], ZrInputs, delimiter=' ')
        return ZpFile, ZmFile, ZrFile

    def createGrids(self): #Creates the X and Z grids from the 3 output files, and some of the inputs from the Inputs2D.txt file. 
        XZ = grdC.XZgrid()
        for i in range(len(self.filenames)):
            grids = XZ.create(self.filenames[i])
            self.xGrids.append(grids[0])
            self.zGrids.append(grids[1]) 
            self.totalrfWid = grids[2]
            self.Xinds = grids[3]
        return self.xGrids[0]
    
    def resolution(self, start, distance, res): #Tells the function when there should be a point on the graph. 
        points = np.arange(start, distance, res) 
        return points
    
    def concatenate(self, Y, origin, end, resInd): #Conojoins the lists together. Returns the last point of Y that is appended and the new Y list. 
        Ya = self.resolution(origin, (origin + end) + 1, resInd)
        Y = np.concatenate([Y, Ya])
        origin = origin + end
        return Y, origin

    def createY(self, motuPlace = None):
        Ygrd = np.array([])  

        #motuPlace is the distance the motu is from the bottom of the reef flat (bottom of the graph, closer to the x axis)
        self.Yinds[0] = 0
        if motuPlace == None: #center everything
            Ygrd, origin = self.concatenate(Ygrd, 0, (self.rflatLen*0.5) - (self.motuLen*0.5), self.Ymax)
            self.Yinds[3] = origin
            Ygrd, origin = self.concatenate(Ygrd, origin, (self.motuLen*0.5) - (self.rpLen*0.5), self.Ymax*.25)
            self.Yinds[1] = origin
            Ygrd, origin = self.concatenate(Ygrd, origin, (self.rpLen*0.5), self.Ymin)
            Ygrd, origin = self.concatenate(Ygrd, origin, (self.rpLen*0.5), self.Ymin)
            Ygrd, origin = self.concatenate(Ygrd, origin, (self.motuLen*0.5) - (self.rpLen*0.5), self.Ymax*.25)
            Ygrd, origin = self.concatenate(Ygrd, origin, (self.rflatLen*0.5) - (self.motuLen*0.5), self.Ymax)
            Ygrd = np.append(Ygrd, self.rflatLen)

        #place the motu a distance away from the edge of the reef flat relative to the x axis. 
        #This value must not be 0.
        #EX: If the value is 200 the motu will be 200 meters away from the x axis. 
        else:  
            self.rf1 = motuPlace
            self.motu1 = self.rf1 + (self.motuLen*0.5) - (self.rpLen*0.5)
            self.rp1 = self.motu1 + (self.rpLen*0.5)
            self.rp2 = self.rp1 + (self.rpLen*0.5)
            self.motu2 = self.rp2 + (self.motuLen*0.5) - (self.rpLen*0.5)

            Ygrd, origin = self.concatenate(Ygrd, 0, motuPlace + 1, self.Ymax)
            self.Yinds[3] = origin
            Ygrd, origin = self.concatenate(Ygrd, origin, (self.motuLen*0.5) - (self.rpLen*0.5) + 1, self.Ymax*.25)
            self.Yinds[1] = origin
            Ygrd, origin = self.concatenate(Ygrd, origin, (self.rpLen*0.5)+1, self.Ymin)
            Ygrd, origin = self.concatenate(Ygrd, origin, (self.rpLen*0.5)+1, self.Ymin)
            Ygrd, origin = self.concatenate(Ygrd, origin, (self.motuLen*0.5) - (self.rpLen*0.5) + 1, self.Ymax*.25)
            Ygrd, origin = self.concatenate(Ygrd, origin, (self.rflatLen - origin) + 1, self.Ymax)
            Ygrd = np.append(Ygrd, self.rflatLen)

        Ygrd = np.unique(Ygrd)
        self.Ygrd = Ygrid
        
        return Ygrd
    
    #Creates the x y mesh grid. 
    def mesh(self, X, Y): 
        x, y = np.meshgrid(X, Y)
        return x, y
    
    #Creates 3 z grids all the same size as Y. 
    def z2dGrd(self, X, Y):
        Zp = np.ones((Y.shape[0], X.shape[0]))
        Zp[0:] = self.zGrids[0]

        Zm = np.ones((Y.shape[0], X.shape[0]))
        Zm[0:] = self.zGrids[1]

        Zr = np.ones((Y.shape[0], X.shape[0]))
        Zr[0:] = self.zGrids[2]

        return Zp, Zm, Zr

    #Puts Z into one list, the same size as Y, varying in depth. 
    def combineZ(self, X, Y):
        Z = np.zeros((Y.shape[0], X.shape[0]))

        Z[np.where(Y <= self.rf1)] = self.zGrids[2]
        Z[np.where(Y >= self.rf1)] = self.zGrids[1]
        Z[np.where(Y >= self.motu1)] = self.zGrids[0]
        Z[np.where(Y >= self.rp1)] = self.zGrids[0]
        Z[np.where(Y >= self.rp2)] = self.zGrids[1]
        Z[np.where(Y >= self.motu2)] = self.zGrids[2]
        return(Z)

    #Gets the X and Y indices of the geographic features and their dimensions to be used in the plots. 
    def createRects(self): 
        m = np.vstack((self.Xinds, self.Yinds))
        rowLabels = ['Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start', 'Motu End', 'Reef Flat End']
        m = np.vstack((rowLabels, m)).T

        rectDims = [['Reef Flat Length', self.rflatLen, 'Nan'], 
                            ['Reef Flat Width', self.totalrfWid, 'NaN'],
                            ['Reef Pit Length', self.rpLen, 'Nan'],
                            ['Reef Pit Width', self.Xinds[2] - self.Xinds[1], 'Nan'], 
                            ['Motu Length', self.motuLen, 'Nan'], 
                            ['Motu Width', self.Xinds[4] - self.Xinds[3], 'Nan']]
        rectDims = np.array(rectDims)
        m = np.vstack((m, rectDims))
        return m

class toCsv: #Turns the X, Y, and Z arrays into grid and dep files. 
    
    def __init__(self, X, Y, Z):
        self.Xg = X
        self.Yg = Y
        self.Zdep = Z
    
    #Creates the files for X, Y and Z. 
    def write(self, names = []):
        Xgrd = np.savetxt(names[0], self.Xg, delimiter=' ')
        Ygrd = np.savetxt(names[1], self.Yg, delimiter= ' ')
        Zdep = np.savetxt(names[2], self.Zdep, delimiter=' ')
        return Xgrd, Ygrd, Zdep

    #Writers the files for the X and Y indicies along with the rectangle dimensions. 
    def indsWriter(self, filename, markers):
        marker = pd.DataFrame(markers, columns=['Labels', 'x', 'y'])
        indsCSV = marker.to_csv(filename, sep = " ")
        return indsCSV

#Creates the 2D grid creator object. #These output files are used in the gridCreation1D.py file. 

Yc = Ygrid('Inputs2D.txt', files=['Exp1Z1.txt', 'Exp1Z2.txt', 'Exp1Z3.txt'])

#Creates Y, X, and the depth files. 
Y = Yc.createY() #To move the motu around on the reef flat put a number in here. The number represents the distance the motu is from the bottom of the reef flat (near the x axis) 
Yc.Xfiles()
X = Yc.createGrids()
Zp, Zm, Zr = Yc.z2dGrd(X, Y)

#Meshes the files together 
x, y = Yc.mesh(X, Y)
z = Yc.combineZ(X, Y)

#Generates the lists of 
m = Yc.createRects()

#This will print out the shape of the x, y and z files. These should all be the same. 
#Make sure to note what they are because you will need to enter in the nx and 
#ny paramters in the params.txt. 
print(x.shape)
print(y.shape)
print(z.shape)

csv = toCsv(x, y, z)

#This function call need to be uncommented to create the .grd and .dep files. 
#The inputs here are the names of the output files. To avoid overwriting other files
#please change the names if you want a different grid each run. 
csv.write(['exampleX.grd', 'exampleY.grd', 'exampleZ.dep'])

#This function call created the files that contains all the bounds for the features 
#in the model. Please have bound included in the naming scheme of this file to avoid 
#confusion. 
csv.indsWriter('ExampleBounds.txt', m)
