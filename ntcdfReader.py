#NetCDF reader/converter
#John Connors

from netCDF4 import Dataset 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import matplotlib.cm as cm
import cmocean.cm as cmo 


class ncReader:

    #reads .nc files and can convert them into .csvs based on the variables selected. 
    def __init__(self, ct_filename = '', exp_filename = '', rp_1D = None, motu_1D = None, rf_1D = None):

        #Reads in files 
        self.ct_file = self.readFile(ct_filename)
        self.exp_file = self.readFile(exp_filename)
        self.profiles_1D = None
        if rp_1D != None:
            self.profiles_1D = [self.readFile(rp_1D), self.readFile(motu_1D), self.readFile(rf_1D)]

    def readFile(self, file, summary = False): #Reads the file and prints a summary if true
        output = Dataset(file, mode = 'r')
        if summary == True:
            print('Output File:\n', output)
        return output
    
    def timeVar(self, variable, data_file, mean = True): #Returns a variables from the .nc file, variable is a variable name, moves time to 3rd dimension
        var = data_file.variables[variable]
        var = np.array(var)
        k = np.abs(var) > 1e38 
        var[k] = None
        data = np.transpose(var, (1,2,0))
        if mean == True:
            testMean = np.mean(data[:,:,180:-180], axis=2) #Takes a measurement every 10 seconds, excluding 30 minutes would be the first and last 1800 seconds. 
            st_dev = np.nanstd(data[:,:,180:-180], axis=2)
        else:
            testMean = np.percentile(data[:,:,180:-180], 0.8, axis = 2)
            st_dev = np.nanstd(data[:,:,180:-180], axis=2)
        return testMean, st_dev #Returns time average and the standard deviation. 

    #Returns the non-Averaged time sets. 
    def rawData(self, variable, data_file):
        var = data_file.variables[variable]
        var = np.array(var)
        k = np.abs(var) > 1e38 
        var[k] = None
        data = np.transpose(var, (1,2,0))
        return data
    
    #Returns the dimensions of the grids. Usually used for x, y and time. 
    def dims(self, dims, data_file): 
        dim = data_file.variables[dims]
        dim = np.array(dim)
        k = np.abs(dim) > 1e36 
        dim[k] = None
        return dim

    #Gets the indices for the profiles to plot the border lines. 
    def getProfileInds(self, file = ''):
        inds = pd.read_csv(file, sep = ' ')
        XYlst = inds.to_numpy()
        x = XYlst[0:6:,2]
        x1 = np.vstack((x, x)).T
        x2 = np.vstack((np.zeros(x.shape[0]), np.ones(x.shape[0]))).T
        rd = XYlst[6:,2]
        rx = [x1[0][0], x1[1][0], x1[3][0]]
        ry = [float(XYlst[0:1,3][0]), float(XYlst[1:2,3][0]), float(XYlst[3:4,3][0])]
        return x1, x2, rd, rx, ry

    #Plots the quiver plots of each time step I select in subplots. 
    def qPlots2D_timeStep(self, df, x = [], y = [], rx = [], ry = [], v1 = '', v2 = '', nx = 2, ny = 2, xlab ='', ylab = '', plot_titles = [[]], fig_title = '', ts = [50, 100, 150, 200], rectDims = [], startInd = 75, stopInd = -30, skips = 2, fg = (15,15)):
        vars1R = self.rawData(v1, df)
        vars2R = self.rawData(v2, df)

        plot_titles = np.reshape(np.array(plot_titles), (nx, ny))
        fig, ax = plt.subplots(nx, ny, sharex=True, sharey=True, figsize = fg)
        for i in range(nx):
            for j in range(ny):
                reefFlat = ptc.Rectangle((rx[0], ry[0]), rectDims[1], rectDims[0], fill = False, ec = 'b')
                reefpit = ptc.Rectangle((rx[1], ry[1]), rectDims[3], rectDims[2], fill = False, ec = 'r')
                motu = ptc.Rectangle((rx[2], ry[2]), rectDims[5], rectDims[4], fill = False, ec = 'g')
                ax[i, j].quiver(x[::skips, startInd:stopInd:skips], y[::skips, startInd:stopInd:skips], vars1R[::skips, startInd:stopInd:skips,ts[i]], vars2R[::skips, startInd:stopInd:skips,ts[i]])
                ax[i, j].add_patch(reefFlat)
                ax[i, j].add_patch(reefpit)
                ax[i, j].add_patch(motu)
                ax[i, j].set_xlabel(xlab)
                ax[i, j].set_ylabel(ylab)
                ax[i, j].set_title(plot_titles[i, j])
        fig.suptitle(fig_title)

    #Plots quiver plots with a time average. 
    def timeAvg_Qplots(self, df, x = [], y = [], rx = [], ry = [], v1 = '', v2 = '', nx = 2, ny = 1, xlab ='', ylab = '', plot_titles = [], fig_title = '', rectDims = [], firstRow = 6, lastRow = 15, firstCol = 75, lastCol = -30, skips = 2, zoom1 = 100, zoom2 = 220, fg = (15,15)):
        vars1T = self.timeVar(v1, df)
        vars2T = self.timeVar(v2, df)
        fig, ax = plt.subplots(2, 1, sharex=False, sharey=False, figsize = fg)

        reefFlat = ptc.Rectangle((rx[0], ry[0]), rectDims[1], rectDims[0], fill = False, ec = 'b')
        reefpit = ptc.Rectangle((rx[1], ry[1]), rectDims[3], rectDims[2], fill = False, ec = 'r')
        motu = ptc.Rectangle((rx[2], ry[2]), rectDims[5], rectDims[4], fill = False, ec = 'g')

        ax[0].quiver(x[:, firstCol:lastCol:skips], y[:, firstCol:lastCol:skips], vars1T[:, firstCol:lastCol:skips], vars2T[:, firstCol:lastCol:skips])
        ax[0].add_patch(reefFlat)
        ax[0].add_patch(reefpit)
        ax[0].add_patch(motu)
        ax[0].set_xlabel(xlab)
        ax[0].set_ylabel(ylab)
        ax[0].set_title(plot_titles[0])

        reefpit1 = ptc.Rectangle((rx[1], ry[1]), rectDims[3], rectDims[2], fill = False, ec = 'r')

        ax[1].quiver(x[firstRow:lastRow, zoom1:zoom2:skips], y[firstRow:lastRow, zoom1:zoom2:skips], vars1T[firstRow:lastRow, zoom1:zoom2:skips], vars2T[firstRow:lastRow, zoom1:zoom2:skips])
        ax[1].add_patch(reefpit1)
        ax[1].set_xlabel(xlab)
        ax[1].set_ylabel(ylab)
        ax[1].set_title(plot_titles[1])
        fig.suptitle(fig_title)
    
    #Plots a profile with a variable and bathymetry. 
    def profiles(self, df, v,  axis, inds = [], xinds = [], xinds2 = [], title = '', xlab = '', ylab = '', legend = [], colors = [], dep = False, mean = True, startInd = 55, stopInd = 140,  ymin = 0, ymax = 1.5): 
        var, st_dev = self.timeVar(v, df, mean)
        bathy = self.rawData('zb', df)

        for i in range(len(inds)):
            plt.plot(axis[inds[i],startInd:stopInd], var[inds[i],startInd:stopInd])
            plt.plot(axis[inds[i],startInd:stopInd], bathy[inds[i],startInd:stopInd])
            plt.errorbar(axis[inds[i],startInd:stopInd], var[inds[i],startInd:stopInd], yerr=st_dev[inds[i], startInd:stopInd], fmt='none', ecolor=colors[i])

        if dep == False: 
            xinds2[:,1] = np.nanmax(var) + (np.nanmax(var)*0.1)
        else: 
            xinds2[:,1] = np.nanmin(var) + (np.nanmin(var)*0.1)

        for i in range(xinds.shape[0]):
            plt.plot(xinds[i], xinds2[i], '--', color = colors[i])

        plt.title(title)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.legend(legend)
        plt.ylim([ymin, ymax])
        plt.margins(x = 0, y = 0)

    #Creates a pcolor of the selected variable. 
    def pcolor(self, df, var, x, y, title = '', xlab = '', ylab = '', dep = True, mean = True):
        var = self.timeVar(var, df, mean)
        if dep == True: 
            plt.pcolor(x, y, var*-1)
        else: 
            plt.pcolor(x, y, var)
        plt.title(title)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.colorbar()
    
    #Creates profiles with the control and the experiment as subplots. 
    def ct_exp_profile(self, df_ct, df_exp, var, axis, profiles_1D = True, inds = [],  xinds = [], xinds2 = [], title = '', plot_titles = [], xlab = '', ylab = '', legend = [[]], colors = [], ctColors = [], expColors = [], p_1Dcolors = [], dep = False, mean = True, fg = (15,15), stopInd = 120, ymin = 0, ymax = 1.4):
        var_ct, ct_st = self.timeVar(var, df_ct)
        var_exVar, ex_st = self.timeVar(var, df_exp)

        fig, ax = plt.subplots(len(inds), 1, figsize = fg, sharey=True)
        
        if dep == False: 
            xinds2[:,1] = np.nanmax(var_exVar) + (np.nanmax(var_exVar)*0.1)
        else: 
            xinds2[:,1] = np.nanmin(var_exVar) + (np.nanmin(var_exVar)*0.1)

        for i in range(len(inds)):
            if self.profiles_1D != None: 
                list_1D = [self.timeVar(var, self.profiles_1D[0])[0].T, self.timeVar(var, self.profiles_1D[1])[0].T, self.timeVar(var, self.profiles_1D[2])[0].T]
                p_st = [self.timeVar(var, self.profiles_1D[0])[1].T, self.timeVar(var, self.profiles_1D[1])[1].T, self.timeVar(var, self.profiles_1D[2])[1].T]
                ax[i].plot(axis[inds[i],:stopInd], list_1D[i][0:stopInd])
                ax[i].errorbar(axis[inds[i],:stopInd], list_1D[i][0:stopInd], yerr = p_st[0:stopInd], fmt = 'none', ecolor = 'b')
            ax[i].plot(axis[inds[i],:stopInd], var_exVar[inds[i],:stopInd], color = expColors[i])
            ax[i].errorbar(axis[inds[i],:stopInd], var_exVar[inds[i],:stopInd], yerr = ex_st[inds[i],:stopInd], fmt = 'none', ecolor = expColors[i])
            ax[i].plot(axis[inds[i],:stopInd], var_ct[inds[i],:stopInd], '--', color = ctColors[i])
            ax[i].errorbar(axis[inds[i],:stopInd], var_ct[inds[i],:stopInd], yerr = ct_st[inds[i],:stopInd], fmt = 'none', ecolor = ctColors[i])
            ax[i].set_ylim([ymin, ymax])
            ax[i].set_xlabel(xlab)
            ax[i].set_ylabel(ylab)
            for j in range(xinds.shape[0]):
                ax[i].plot(xinds[j], xinds2[j], color = colors[j])
            ax[i].set_title(plot_titles[i])
            ax[i].legend(legend[i])
        
        fig.suptitle(title)
        plt.subplots_adjust(hspace=0.5)

    #Calculates the magnitude of the vectors input here. 
    def magnitude(self, df, var_X, var_Y):

        m_X = self.timeVar(var_X, df)
        m_Y = self.timeVar(var_Y, df)

        magnitude = np.sqrt(np.square(m_X) + np.square(m_Y))
        return magnitude

    #Calculates the % changes between the magnitude. 
    def m_Change(self, df_ct, df_exp, ct_X, ct_Y, exp_X, exp_Y):
        ct_mag = self.magnitude(df_ct, ct_X, ct_Y)
        exp_mag = self.magnitude(df_exp, exp_X, exp_Y)

        p_change = ((exp_mag - ct_mag)/ct_mag)*100
        return p_change

    #Plots quiver plots of the control, experiment and a p color of the % change. 
    def p_changePlots(self, df_ct, df_exp, x=[], y=[], ct_x='', ct_y='', exp_x='', exp_y='', plot_titles = [], fig_title = '', xlab = '', ylab = '', rx = [], ry = [], fg = (20,20), rectDims=[], fr=0, lr=0, fc=0, lc=0, skips = 2):
        ctVar_X = self.timeVar(ct_x, df_ct)
        ctVar_Y = self.timeVar(ct_y, df_ct)

        expVar_X = self.timeVar(exp_x, df_exp)       
        expVar_Y = self.timeVar(exp_y, df_exp)

        p_change = self.m_Change(df_ct, df_exp, ct_x, ct_y, exp_x, exp_y)

        reefFlat = ptc.Rectangle((rx[0], ry[0]), rectDims[1], rectDims[0], fill = False, ec = 'b')
        reefpit = ptc.Rectangle((rx[1], ry[1]), rectDims[3], rectDims[2], fill = False, ec = 'r')
        motu = ptc.Rectangle((rx[2], ry[2]), rectDims[5], rectDims[4], fill = False, ec = 'g')

        fig, ax = plt.subplots(3, 1, figsize = fg)
        ax[0].quiver(x[:, fc:lc:skips], y[:, fc:lc:skips], ctVar_X[:, fc:lc:skips], ctVar_Y[:, fc:lc:skips])
        ax[0].add_patch(reefFlat)
        ax[0].add_patch(reefpit)
        ax[0].add_patch(motu)
        ax[0].set_xlabel(xlab)
        ax[0].set_ylabel(ylab)
        ax[0].set_title(plot_titles[0])

        reefFlat1 = ptc.Rectangle((rx[0], ry[0]), rectDims[1], rectDims[0], fill = False, ec = 'b')
        reefpit1 = ptc.Rectangle((rx[1], ry[1]), rectDims[3], rectDims[2], fill = False, ec = 'r')
        motu1 = ptc.Rectangle((rx[2], ry[2]), rectDims[5], rectDims[4], fill = False, ec = 'g')

        ax[1].quiver(x[:, fc:lc:skips], y[:, fc:lc:skips], expVar_X[:, fc:lc:skips], expVar_Y[:, fc:lc:skips])
        ax[1].add_patch(reefFlat1)
        ax[1].add_patch(reefpit1)
        ax[1].add_patch(motu1)
        ax[1].set_xlabel(xlab)
        ax[1].set_ylabel(ylab)
        ax[1].set_title(plot_titles[1])

        ax[2].pcolor(x, y, p_change, cmap='cmo.thermal', shading = 'auto', vmin = 0, vmax = 0.9)
        ax[2].set_xlabel(xlab)
        ax[2].set_ylabel(ylab)
        ax[2].set_title(plot_titles[2])

        fig.colorbar(cm.ScalarMappable(norm=None, cmap='cmo.thermal'), ticks = [0, 0.25, 0.5, 0.75, 0.9], ax = ax[2])
        fig.suptitle(fig_title)            
        plt.subplots_adjust(hspace=0.5)

    #Plots the time average of the control and experiments next to eachother as subplots. 
    def ct_exp_Quivers(self, df_ct, df_exp, x=[], y=[], ct_x='', ct_y='', exp_x='', exp_y='', plot_titles = [], fig_title = '', xlab = '', ylab = '', rx = [], ry = [], fg = (15,15), rectDims=[], fr=0, lr=0, fc=0, lc=0, skips = 2, z1 = 100, z2 = 220):
       
        varlist = [self.timeVar(ct_x, df_ct), self.timeVar(ct_y, df_ct), self.timeVar(exp_x, df_exp), self.timeVar(exp_y, df_exp)]

        fig, ax = plt.subplots(2, 2, figsize = fg)

        reefFlat = ptc.Rectangle((rx[0], ry[0]), rectDims[1], rectDims[0], fill = False, ec = 'b')
        reefpit = ptc.Rectangle((rx[1], ry[1]), rectDims[3], rectDims[2], fill = False, ec = 'r')
        motu = ptc.Rectangle((rx[2], ry[2]), rectDims[5], rectDims[4], fill = False, ec = 'g')

        ax[0,0].quiver(x[:, fc:lc:skips], y[:, fc:lc:skips], varlist[0][:, fc:lc:skips], varlist[1][:, fc:lc:skips])
        ax[0,0].add_patch(reefFlat)
        ax[0,0].add_patch(reefpit)
        ax[0,0].add_patch(motu)
        ax[0,0].set_xlabel(xlab)
        ax[0,0].set_ylabel(ylab)
        ax[0,0].set_title(plot_titles[0])

        reefpit_ct = ptc.Rectangle((rx[1], ry[1]), rectDims[3], rectDims[2], fill = False, ec = 'r')

        ax[0,1].quiver(x[fr:lr, z1:z2:skips], y[fr:lr, z1:z2:skips], varlist[0][fr:lr, z1:z2:skips], varlist[1][fr:lr, z1:z2:skips])
        ax[0,1].add_patch(reefpit_ct)
        ax[0,1].set_xlabel(xlab)
        ax[0,1].set_ylabel(ylab)
        ax[0,1].set_title(plot_titles[1])

        reefFlat1 = ptc.Rectangle((rx[0], ry[0]), rectDims[1], rectDims[0], fill = False, ec = 'b')
        reefpit1 = ptc.Rectangle((rx[1], ry[1]), rectDims[3], rectDims[2], fill = False, ec = 'r')
        motu1 = ptc.Rectangle((rx[2], ry[2]), rectDims[5], rectDims[4], fill = False, ec = 'g')

        ax[1,0].quiver(x[:, fc:lc:skips], y[:, fc:lc:skips], varlist[2][:, fc:lc:skips], varlist[3][:, fc:lc:skips])
        ax[1,0].add_patch(reefFlat1)
        ax[1,0].add_patch(reefpit1)
        ax[1,0].add_patch(motu1)
        ax[1,0].set_xlabel(xlab)
        ax[1,0].set_ylabel(ylab)
        ax[1,0].set_title(plot_titles[2])

        reefpit2 = ptc.Rectangle((rx[1], ry[1]), rectDims[3], rectDims[2], fill = False, ec = 'r')

        ax[1,1].quiver(x[fr:lr, z1:z2:skips], y[fr:lr, z1:z2:skips], varlist[2][fr:lr, z1:z2:skips], varlist[3][fr:lr, z1:z2:skips])
        ax[1,1].add_patch(reefpit2)
        ax[1,1].set_xlabel(xlab)
        ax[1,1].set_ylabel(ylab)
        ax[1,1].set_title(plot_titles[3])

        fig.suptitle(fig_title)

#These are the files paths to each 1D output file 
#If you did not make any 1D outputs comment these out and remove them from the parameters of the ncReader
#class below by deleting the rp_1D, motu_1D and rf_1D parameters. 
rp1D = r"""1D_Runs\1D_RP\xboutput.nc"""
motu1D = r"""1D_Runs\1D_Motu\xboutput.nc"""
rf1D = r"""1D_Runs\1D_RF\xboutput.nc"""

#The parameters here are the filepaths to the output files. Make sure to change the filepath in the ct_filename parameter to the correct filepath. 
n = ncReader(ct_filename=r"""ControlCase\xboutput.nc""", exp_filename="xboutput.nc", rp_1D = rp1D, motu_1D = motu1D, rf_1D = rf1D)
#Variable List ==== H, zb, zs, hh, E, D, zs0, Fx, Fy, Qb, taubx, tauby, ue, ve, urms, costh, sinth, thetamean ==== # Change this to the variables you have in your run to keep track. 

#These different files read in by the ncReader class. The useFile variable is the file that is going to be used in the individual plots. 
df_ct = n.ct_file
df_exp = n.exp_file
useFile = df_ct

#These are the dimensions of the grids. They are used in the quiver plots mostly. 
x = n.dims('globalx', df_ct)
y = n.dims('globaly', df_ct)
t = n.dims('globaltime', df_ct)

#Use xinds and xinds2 for profiles, use rx and ry for the rectangles in the 2D figures. 
xinds, xinds2, rectDims, rx, ry = n.getProfileInds('Exp1Bounds.txt')

#Figure Size
fg = (15,15)

#==== Profiles ==== #
'''Profile plots take a file, variable as a string, axis, specific indicies to plot the transects as a list of integers, the xinds[:4] and xinds2[:4] lists,
title as a string, x and y axis titles as strings, legend titles in the form of a list of strings, and colors in the form of a list of strings. To select a 
variable type the exact variable name from the bottom of params.txt into the second parameter spot in the function calls.'''

# plt.figure(1, figsize=fg)
'Format:   Filename, Var, axis, indices, xinds[:4], xinds2[:4],                  title,                  x axis label,      y axis label,                        legend labels,                                                                                          colors list'
# n.profiles(useFile, 'H', x, [11, 5, 2], xinds[:4], xinds2[:4], "Average Wave Height Across the Motu", 'Distance (m)', "Average Wave Height (m)", ['Reef Pit', 'Motu', 'Reef Flat', 'Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start'], ['black', 'magenta', 'magenta', 'green'])

# plt.figure(2, figsize=fg)
# n.profiles(useFile, 'zs', x, [11, 5, 2], xinds[:4], xinds2[:4], "Average Water Level", 'Distance (m)', "Average Water Level (m)", ['Reef Pit', 'Motu', 'Reef Flat', 'Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start'], ['black', 'magenta', 'magenta', 'green'], True)

# plt.figure(3, figsize=fg)
# n.profiles(useFile, 'E', x, [11, 5, 2], xinds[:4], xinds2[:4], "Average Wave Energy", 'Distance (m)', "Average Wave Energy (m)", ['Reef Pit', 'Motu', 'Reef Flat', 'Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start'], ['black', 'magenta', 'magenta', 'green'])

# plt.figure(4, figsize=fg)
# n.profiles(useFile, 'ue', x, [11, 5, 2], xinds[:4], xinds2[:4], "Average Eularian Velocity (X)", 'Distance (m)', "Average EU", ['Reef Pit', 'Motu', 'Reef Flat', 'Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start'], ['black', 'magenta', 'magenta', 'green'])

# plt.figure(5, figsize=fg)
# n.profiles(useFile, 've', x, [11, 5, 2], xinds[:4], xinds2[:4], "Average Eularian Velocity (Y)", 'Distance (m)', "Average EU", ['Reef Pit', 'Motu', 'Reef Flat', 'Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start'], ['black', 'magenta', 'magenta', 'green'], False, True)

# plt.figure(6, figsize=fg)
# n.profiles(useFile, 'Fx', x, [11, 5, 2], xinds[:4], xinds2[:4], "Average Wave Force (X)", 'Distance (m)', "Average Force", ['Reef Pit', 'Motu', 'Reef Flat', 'Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start'], ['black', 'magenta', 'magenta', 'green'])

# plt.figure(7, figsize=fg)
# n.profiles(useFile, 'Fy', x, [11, 5, 2], xinds[:4], xinds2[:4], "Average Wave Force (Y)", 'Distance (m)', "Average Force", ['Reef Pit', 'Motu', 'Reef Flat', 'Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start'], ['black', 'magenta', 'magenta', 'green'])

# plt.figure(8, figsize=fg)
# n.profiles(useFile, 'taubx', x, [11, 5, 2], xinds[:4], xinds2[:4], "Average Bed Shear Stress (X)", 'Distance (m)', "Average Bed Shear Stress", ['Reef Pit', 'Motu', 'Reef Flat', 'Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start'], ['black', 'magenta', 'magenta', 'green'], True)

# plt.figure(9, figsize=fg)
# n.profiles(useFile, 'tauby', x, [11, 5, 2], xinds[:4], xinds2[:4], "Average Bed Shear Stress (Y)", 'Distance (m)', "Average Bed Shear Stress", ['Reef Pit', 'Motu', 'Reef Flat', 'Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start'], ['black', 'magenta', 'magenta', 'green'])

# plt.figure(10, figsize=fg)
# n.profiles(useFile, 'urms', x, [11, 5, 2], xinds[:4], xinds2[:4], 'Average Orbital Velocity', 'Distance (m)', 'Orbital Velocity', ['Reef Pit', 'Motu', 'Reef Flat', 'Reef Flat Start', 'Reef Pit Start', 'Reef Pit End', 'Motu Start'], ['black', 'magenta', 'magenta', 'green'])

#==== Pcolor Plots ====#
'''Pcolor plots take a file, variable x and y, title and x and y labels. '''

# plt.figure(11, figsize=fg)
'''Format: filename var, x, y,      title,              x label,        y label'''
# n.pcolor(useFile, 'hh', x, y, 'Water Depth (m)', 'Distance in X', 'Distance in Y')

# plt.figure(12, figsize=fg)
# n.pcolor(useFile, 'zb', x, y, 'Bathymetry', 'Distance in X', 'Distance in Y', False)

# plt.figure(13, figsize=fg)
# n.pcolor(useFile, 'E', x, y, 'Wave Energy', 'Distance in X (m)', 'Distance in Y (m)', False)

# plt.figure(14, figsize=fg)
# n.pcolor(useFile, 'D', x, y, 'Wave Dissapation', 'Distance in X (m)', 'Distance in Y (m)', False, False)

# plt.figure(15, figsize=fg)
# n.pcolor(useFile, 'zs0', x, y, 'Water Level - Tides Included', 'Distance in X (m)', 'Distance in Y (m)', False, False)

# plt.figure(16, figsize=fg)
# n.pcolor(useFile, 'urms', x, y, 'Orbital Velocity', "X Distance", 'Y Distance', False)

#==== Quiver Plots ====#
'''The quiver plots take a file, x, y, , rx and ry (which are points for the rectangles of the features to be drawn from)a variable that has an x and y 
such as ue (x) and ve (y), the number of plots in x and the number of plots in y, an x label, a y label, titles for different plots, a title for the entire
figure, the rectdims list (a list of dimensions and coordinates for the features), and the start, stop and zoom indices. There are 2 types of these plots, time 
step and time average. The time average has 2 subplots, one of the entire reefflat and another of just the reef pit. The time step has the entire reef flat at 
different time steps with 4 subplots. They each have different parameters which will be shown in the format. '''

# # Figure 9
'''Format Time Step:filename  x, y,  rx , ry, x var yvar, num plots x, num plots y,    xlabel,          ylabel,                         plot titles,                                        Figure title,                      time step indicies,  rectdims, Start ind, stop ind,    skip (in this case take every second measurement)'''
# n.qPlots2D_timeStep(useFile, x, y, rx,  ry, "ue", "ve",      2,           2,     'Distance (m)', 'Distance in Y', [['Time Step 50', 'Time Step 100', 'Time Step 150', 'Time Step 200']], 'Eularian Velocity (m/s) Time Steps', [50, 100, 150, 200], rectDims,    75,         -30,    2)

# # Figure 10 
'''Format Time Avg:filename  x, y,  rx , ry, x var yvar, num plots x, num plots y, xlabel,          ylabel,            plot titles,                            Figure title,          rectdims, first row, last row, first column, last column, skip (in this case take every second measurement), zoom1, zoom2'''
# n.timeAvg_Qplots(useFile, x, y,   rx,  ry, "ue", "ve",     2,            1,     'Distance (m)', 'Distance in Y', ['Entire Reef Flat', 'Reef Pit'], 'Time Averaged Elarian Velocity', rectDims,     40,       60,       75,           -30,        2,                                                95,   130)

# # Figure 11
# n.qPlots2D_timeStep(useFile, x, y, rx, ry, "taubx", "tauby", 2, 2, 'Distance (m)', 'Distance in Y', [['Time Step 50', 'Time Step 100', 'Time Step 150', 'Time Step 200']], 'Bed Shear Stress Time Steps', [50, 100, 150, 200], rectDims, False, 75, -30, 2)

# # Figure 12
# n.timeAvg_Qplots(useFile, x, y, rx, ry, "taubx", "tauby", 2, 1, 'Distance (m)', 'Distance in Y', ['Entire Reef Flat', 'Reef Pit'], 'Time Averaged Bed Shear Stress', rectDims,  40, 60, 75, -30, 2, 95, 130)

# # Figure 13
# n.qPlots2D_timeStep(useFile, x, y, rx, ry, "Fx", "Fy", 2, 2, 'Distance (m)', 'Distance in Y', [['Time Step 50', 'Time Step 100', 'Time Step 150', 'Time Step 200']], 'Wave Force (m/s) Time Steps', [50, 100, 150, 200], rectDims, False, 75, -30, 2)

# # Figure 14
# n.timeAvg_Qplots(useFile, x, y, rx, ry, "Fx", "Fy", 2, 1, 'Distance (m)', 'Distance in Y', ['Entire Reef Flat', 'Reef Pit'], 'Time Averaged Wave Force', rectDims,  40, 60, 75, -30, 2, 95, 130)


#======================= Uses both the control files and the experiment files =================================#

#Profiles =================#
'''These profiles use the control case and the experiment case. They take the control filename, the experiment filename, the variable name, a setting if 1D plots were used, the axis, a list of indicies
the xinds[:4] and xinds2[:4] lists, a title, plot titles, an x and y label, legend titles for each subplot, colors for each plot and line, a stop index and a minimum and maximum y 
value.'''
# plt.figure(23, figsize=fg)
'Format:           ct file, exp file, Var, axis, 1D?   indices,    xinds[:4], xinds2[:4],    title,              plot titles,                x axis label,  y axis label                                                                                                    legend labels,                                                                                                                                                                  colors list for legend          color list for different datasets    1D plot colors    stopIndex      ymin         ymax'
# n.ct_exp_profile(df_ct,    df_exp,   'H', x, True, [43, 30, 2], xinds[:4], xinds2[:4], 'Wave Height', ['Reef Pit', 'Motu', 'Reef Flat'], 'Distance (m)', 'Wave Height (m)',  [['Exp RP', 'CT RP', '1D RP', 'RF Start', 'RP Start', 'RP End', 'Motu Start'], ['Exp Motu', 'CT Motu', '1D Motu', 'RF Start', 'RP Start', 'RP End', 'Motu Start'], ['Exp RF', 'CT RF', '1D RF', 'RF Start', 'RP Start', 'RP End', 'Motu Start']], ['black', 'magenta', 'magenta', 'green', 'green', 'black'], ['k', 'g', 'm'],               ['c', 'y', 'orange'], stopInd = 150, ymin = 0.6, ymax = 1.3)

#Quiver Plots ============#
'''These quiver plots are similar to the quiver plots that take one variable. The difference is that these use two file names instead of 
one and make a figure with an entire reef flat and a zoom in of the reef pit for the control file and experiment file. ''' 
# #Figure 24
'''Format:        ct file, exp file, x, y, ct xvar, ct yvar, exp x var, exp y var,                                      plot titles,                                                    fig title,      xlabel,         y label, rx, ry, fig size, rectdims, first row,     last row    first col   last col    skip,   z1,          z2'''
# n.ct_exp_Quivers(df_ct, df_exp,    x, y,  'ue',   've',      'ue',       've', ['CT Eularian Velocity', 'CT EU (Reef Pit Area)', 'Exp Eularian Velocity', 'Exp EU (Reef Pit)'], 'Time Averaged EU', 'Dist in X', 'Dist in Y', rx, ry,     fg, rectDims,       40,         60,         75,         -30,        2,      95,         130)

#% change plots ==========#
'''This figure shows a quiver plot of the entire reef flat for each file and shows a p color plot of the % change in magnitude
of the variables between the control case and the experiment case. '''
# #Figure 25
'''Format:        ct file, exp file, x, y, ct xvar, ct yvar, exp x var, exp y var,                                      plot titles,                   fig title,          xlabel,         y label,   rx, ry, fig size, rectdims, first row,     last row    first col   last col    skip'''
# n.p_changePlots(df_ct, df_exp,     x, y, 'ue',     've',   'ue',        've', ['CT Eularian Velocity', 'Exp Eularian Velocity', 'Percent Change'], 'Time Averaged EU', 'Dist in X',    'Dist in Y', rx, ry, fg,       rectDims,    40,            60,         75,         -30,        2)

plt.show()