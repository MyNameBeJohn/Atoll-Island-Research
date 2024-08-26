#Grid Generator
#6/25/2020
#John Connors 

import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
#Things to fix: 
#========================================================================# 

#========================================================================#

class XZgrid: 

    def __init__(self):
        
        #List of X points at each area with a slope: 
        self.numRP = []
        self.numMtS = []
        self.xDif = []
        self.Xtrace = []

    def updateNumRp(self, xDif, Z, val): 
        self.numRP = [val]*xDif
        Z = np.concatenate([Z, self.numRP])
        return Z

    def updateNumMtS(self, xDif, Z, val): 
        self.numMtS = [val]*xDif
        Z = np.concatenate([Z, self.numMtS])
        return Z

    def line(self, dep1, dep2, m, res, x1s): #Returns a list of points after pluging in a slope and depth 
        deltaX = np.abs((dep2 - dep1)/m)
        x1 = x1s
        y1 = dep1
        Xnum = deltaX/res
        Xslope = []
        Yslope = []
        for i in range(int(Xnum)):
            x2 = x1 + res
            deltaY = (x2 - x1)*m
            y2 = deltaY + y1
            y1 = y2
            x1 = x2
            Xslope.append(x2)
            Yslope.append(y2)
        return Xslope, Yslope

    def resolution(self, start, distance, res): #Tells the function when there should be a point on the graph. <-Fix
        points = np.arange(start, distance, res) 
        return points
    
    def concatenate(self, X, Z, origin, end, resInd, val):
        Xa = self.resolution(origin, (origin + end) + 1, resInd)
        X = np.concatenate([X, Xa])
        Za = np.full(Xa.shape[0], val)
        Z = np.concatenate([Z, Za])
        origin = origin + end 
        return X, Z, origin
    
    def conSlope(self, X, Z, dep1, dep2, slope, resInd, origin):
        Xslope, Yslope = self.line(dep1, dep2, slope, resInd, origin) #i is the resolution index
        X = np.concatenate([X, Xslope])
        Z = np.concatenate([Z, Yslope])
        origin = Xslope[len(Xslope) - 1]
        return X, Z, origin

    def create(self, filename = ''):
        '''
        Variables: 
            waterDep is the initial offshore depth, measured from sea level 
            reefdep is the depth of the reef flat, measured from sea level 
            rpd is the depth of the reef pit from sea level
            lm is the height of the motu above sea level
            lgDep is the lagoon depth from sea level 
            offShoreSlope is the reef slope leading up to the reef flat. 
            mtm is the slope from the reef flat to the motu. 
            backM is the backslop of the lagoon
        '''
        d = pd.read_csv(filename, header = None)
        data = d.to_numpy()
        inputs = np.reshape(data, (data.shape[0], 1))

        #Marks where each feature starts in meters --> you do not have to change mW, mts, and bcksl. 
        deepWater = inputs[0,0] #sets length of the off shore water depth
        offShoreDep = inputs[1,0] #Depth off shore
        offshoreSlope = inputs[2,0] #sets length of the reef slope
        dto = inputs[3,0] #sets length of the reef flat from the distance to the ocean to the start of the reef pit. 
        reefdep = inputs[4,0] #Depth of the reef
        rpWid = inputs[5,0] #sets length of the reef pit
        rpdep = inputs[6,0] #Depth of the reef pit
        rpsl = inputs[7,0] #Slope of the reef pit
        dtm = inputs[8,0] #sets the distance the reef pit is from the motu. 
        motuWid = inputs[9,0] #Width of the motu 
        landElev = inputs[10,0] #Elevation of the land
        motuSlope = inputs[11,0] #Distance of motu slope
        lgWid = inputs[12,0] #Width of included lagoon.
        lgdep = inputs[13,0] #Depth of the lagoon 
        backslope = inputs[14,0] #the distance of the backslope of the lagoon
        Xmax = inputs[15,0] #Max X resolution 
        Xmin = inputs[16,0] #Min X resolution

        totalDist = 0 #Total length of profile --> gets set after X is created. 

        #Resolutions 
        rpRes = inputs[17,0]
        motuRes = inputs[18,0]
        rfRes = inputs[19,0]
        offshoreRes = inputs[20,0]
        lagoonRes = inputs[21, 0]
        reefslopeRes = inputs[22,0]
        motuSlpRes = inputs[23,0]
        backslopeRes = inputs[24,0]

        #List of resolutions for each part of the model, same order as XZlst. 
        resLst = [Xmax, reefslopeRes, rfRes, rpRes, rfRes, motuSlpRes, motuRes, backslopeRes, lagoonRes] 

        #Returns X and Z arrays.
        Z = np.array([]) #Motu and reef pit
        X = np.array([]) #X grid 
        origin = 0
        Xinds = []
        #The numbers here are the default values of resolution for each part of the profile. 

        #off shore water and depth 
        X, Z, origin = self.concatenate(X, Z, 0, deepWater, resLst[0], offShoreDep)

        #Reef slope
        X, Z, origin = self.conSlope(X, Z, offShoreDep, reefdep, offshoreSlope, resLst[1], origin)
        rfStart = origin
        Xinds.append(rfStart)

        #Distance to ocean
        X, Z, origin = self.concatenate(X, Z, origin, dto, resLst[2], reefdep)
        xp = X.shape[0] #previous shape of X
        Xinds.append(origin)
        if rpsl != 0:
            #Reef pit slope going down 
            X, Z, origin = self.conSlope(X, Z, reefdep, rpdep, rpsl*-1, resLst[3], origin)
            #Bottom of the reef pit
            X, Z, origin = self.concatenate(X, Z, origin, rpWid, resLst[3], rpdep)
            #Reef pit slope going up 
            X, Z, origin = self.conSlope(X, Z, rpdep, reefdep, rpsl, resLst[3], origin)
            self.xDif.append(X.shape[0] - xp)
            self.Xtrace.append(X)
            Xinds.append(origin)
        else:
            X = self.Xtrace[0]
            Z = self.updateNumRp(self.xDif[0], Z, reefdep)
            origin = X[X.shape[0] - 1]
            Xinds.append(origin)
        
        #Reef flat after the pit
        X, Z, origin = self.concatenate(X, Z, origin, dtm, resLst[4], reefdep)
        xp = X.shape[0] #previous shape of X
        Xinds.append(origin)

        #Motu Slope
        if motuSlope != 0: 
            X, Z, origin = self.conSlope(X, Z, reefdep, landElev, motuSlope, resLst[3], origin)
            self.xDif.append(X.shape[0] - xp)
            self.Xtrace.append(X)
        else:
            X = self.Xtrace[1]
            Z = self.updateNumMtS(self.xDif[1], Z, reefdep)
            origin = X[X.shape[0] - 1]

        #The motu 
        X, Z, origin = self.concatenate(X, Z, origin, motuWid, resLst[6], landElev)
        xp = X.shape[0] #previous shape of X
        Xinds.append(origin)

        #Back Slope 
        rfEnd = origin
        if motuSlope != 0: 
            X, Z, origin = self.conSlope(X, Z, landElev, lgdep, backslope, resLst[7], origin)
            self.Xtrace.append(X)
            Xinds.append(origin)
        else:
            X, Z, origin = self.conSlope(X, Z, landElev, lgdep, backslope, resLst[7], origin)
            X = self.Xtrace[2]
            Z[np.where(Z > reefdep)] = reefdep
            Xinds.append(origin)

        #Lagoon Depth
        X, Z, origin = self.concatenate(X, Z, origin, lgWid, resLst[8], lgdep)

        Xnew, Xind = np.unique(X, return_index=True)
        Znew = Z[Xind]
        totalDist = Xnew[Xnew.shape[0] - 1]
        totalrfWid = rfEnd - rfStart
        return Xnew, Znew, totalrfWid, Xinds

class toCsv: #Turns the X and Z arrays into grid and dep files. 
    
    def __init__(self, X, Z):
        self.Xgrd = X.reshape(1, X.shape[0])
        self.Zdep = Z.reshape(1, Z.shape[0])
    
    def write(self, names = []):
        Xgrd = np.savetxt(names[0], self.Xgrd, delimiter=' ')
        Zdep = np.savetxt(names[1], self.Zdep, delimiter=' ')
        return Xgrd, Zdep

# XZ = XZgrid(filename="test1D.txt")
# X, Z = XZ.create()

# print(X.shape)
# print(Z.shape)

# CSV = toCsv(X, Z)
# CSV.write(['X2.grd', 'Z2.dep'])

# plt.plot(X, Z, '-o')
# plt.show()
