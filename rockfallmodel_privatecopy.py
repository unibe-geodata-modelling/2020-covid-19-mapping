#Example script for a simple rockfall model
#Andreas Zischg, 19.03.2020
#Seminar Geodata Analysis and Modelling, Spring Semseter 2020
#Private copy made
#imports
import numpy as np
import math
import matplotlib.pyplot as plt

#****************************************************
#functions
#****************************************************
def gridasciitonumpyarrayfloat(ingridfilefullpath):
    #this function reads a GRID-ASCII raster into a floating point numpy array
    #input is the full path to an ASCCI GRID file
    #output is the float numpy array, the number of columns, the number of rows, the x-coordinate of the lower left corner, y-coordinate of lower left corner, cellsize, NODATA value, and the full string of the ASCII GRID header
    i=0
    row=0
    headerstr=''
    infile=open(ingridfilefullpath, "r")
    for line in infile:
        if i==0:
            ncols=int(line.strip().split()[-1])
            headerstr+=line
        elif i==1:
            nrows=int(line.strip().split()[-1])
            headerstr += line
        elif i==2:
            xllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==3:
            yllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==4:
            cellsize=float(line.strip().split()[-1])
            headerstr += line
        elif i==5:
            NODATA_value=float(line.strip().split()[-1])
            arr=np.zeros((nrows, ncols), dtype=float)
            arr[:,:]=NODATA_value
            headerstr += line.replace("\n","")
        elif i > 5:
            col = 0
            while col < ncols:
                for item in line.strip().split():
                    arr[row, col] = float(item)
                    col += 1
            row += 1
        i += 1
    infile.close()
    return arr, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, headerstr
def gridasciitonumpyarrayint(ingridfilefullpath):
    #this function reads a GRID-ASCII raster into a floating point numpy array
    #input is the full path to an ASCCI GRID file
    #output is the integer numpy array, the number of columns, the number of rows, the x-coordinate of the lower left corner, y-coordinate of lower left corner, cellsize, NODATA value, and the full string of the ASCII GRID header
    i=0
    row = 0
    headerstr=''
    infile=open(ingridfilefullpath, "r")
    for line in infile:
        if i==0:
            ncols=int(line.strip().split()[-1])
            headerstr+=line
        elif i==1:
            nrows=int(line.strip().split()[-1])
            headerstr += line
        elif i==2:
            xllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==3:
            yllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==4:
            cellsize=float(line.strip().split()[-1])
            headerstr += line
        elif i==5:
            NODATA_value=float(line.strip().split()[-1])
            arr=np.zeros((nrows, ncols), dtype=int)
            arr[:,:]=NODATA_value
            headerstr += line.replace("\n","")
        elif i>5:
            col=0
            while col<ncols:
                for item in line.strip().split():
                    arr[row,col]=float(item)
                    col+=1
            row+=1
        i+=1
    infile.close()
    return arr, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, headerstr
def flowdirection_to_lowestcell(demarr, inrow, incolumn):
    #this function looks at the 8 neighboring cells of a selected cell with given coordinate (inrow, incolumn)
    #compares the z-coordinates of 8 adjacent neighbors with the z-coordinate of the center cell
    #returns the relative coordinates of the lowest adjacent cell
    z_center=demarr[inrow, incolumn]
    if inrow > 0 and inrow < np.shape(demarr)[0]-1 and incolumn >0 and incolumn<np.shape(demarr)[1]-1:
        zmin = z_center
        #check the minimum value of all 8 adjacent neighbors
        if demarr[inrow + 0, incolumn + 1] <= zmin:
            zmin = demarr[inrow + 0, incolumn + 1]
            flowdir = 1
        if demarr[inrow + 1, incolumn + 1] <= zmin:
            zmin = demarr[inrow + 1, incolumn + 1]
            flowdir = 2
        if demarr[inrow + 1, incolumn + 0] <= zmin:
            zmin = demarr[inrow + 1, incolumn + 0]
            flowdir = 4
        if demarr[inrow + 1, incolumn - 1] <= zmin:
            zmin = demarr[inrow + 1, incolumn - 1]
            flowdir = 8
        if demarr[inrow + 0, incolumn - 1] <= zmin:
            zmin = demarr[inrow + 0, incolumn - 1]
            flowdir = 16
        if demarr[inrow - 1, incolumn - 1] <= zmin:
            zmin = demarr[inrow - 1, incolumn - 1]
            flowdir = 32
        if demarr[inrow - 1, incolumn - 0] <= zmin:
            zmin = demarr[inrow - 1, incolumn - 0]
            flowdir = 64
        if demarr[inrow - 1, incolumn + 1] <= zmin:
            zmin = demarr[inrow - 1, incolumn + 1]
            flowdir = 128
    else:
        flowdir=0
    return flowdir

def flowdirection_to_steepestpath(demarr, inrow, incolumn):
    #this function looks at the 8 neighboring cells of a selected cell with given coordinate (inrow, incolumn)
    #compares the z-coordinates of 8 adjacent neighbors with the z-coordinate of the center cell
    #returns the relative coordinates of the lowest adjacent cell
    z_center=demarr[inrow, incolumn]
    if inrow > 0 and inrow < np.shape(demarr)[0]-1 and incolumn >0 and incolumn<np.shape(demarr)[1]-1:
        slopetan = 0
        flowdir = 0
        #check the minimum value of all 8 adjacent neighbors
        if (z_center-demarr[inrow + 0, incolumn + 1])/cellsize >= slopetan:
            slopetan = (z_center - demarr[inrow + 0, incolumn + 1])/cellsize
            flowdir = 1
        if (z_center-demarr[inrow + 1, incolumn + 1])/(cellsize * math.sqrt(2)) >= slopetan:
            slopetan = (z_center - demarr[inrow + 1, incolumn + 1])/(cellsize * math.sqrt(2))
            flowdir = 2
        if (z_center - demarr[inrow + 1, incolumn + 0])/cellsize >= slopetan:
            slopetan = (z_center - demarr[inrow + 1, incolumn + 0])/cellsize
            flowdir = 4
        if (z_center - demarr[inrow + 1, incolumn - 1])/(cellsize * math.sqrt(2)) >= slopetan:
            slopetan = (z_center - demarr[inrow + 1, incolumn - 1])/(cellsize * math.sqrt(2))
            flowdir = 8
        if (z_center - demarr[inrow + 0, incolumn - 1])/cellsize >= slopetan:
            slopetan = (z_center - demarr[inrow + 0, incolumn - 1])/cellsize
            flowdir = 16
        if (z_center - demarr[inrow - 1, incolumn - 1])/(cellsize * math.sqrt(2)) >= slopetan:
            slopetan = (z_center - demarr[inrow - 1, incolumn - 1])/(cellsize * math.sqrt(2))
            flowdir = 32
        if (z_center - demarr[inrow - 1, incolumn - 0])/cellsize >= slopetan:
            slopetan = (z_center - demarr[inrow - 1, incolumn - 0])/cellsize
            flowdir = 64
        if (z_center - demarr[inrow - 1, incolumn + 1])/(cellsize * math.sqrt(2)) >= slopetan:
            slopetan = (z_center - demarr[inrow - 1, incolumn + 1])/(cellsize * math.sqrt(2))
            flowdir = 128
    else:
        flowdir=0
    return flowdir
#****************************************************
# end functions
#****************************************************


#**************************************************************************
#ENVIRONMENT variables - set workspace and names of input files
#**************************************************************************
#set environment and workspace
myworkspace = "/Users/evaammann/Dropbox/Eva Ammann - Universität/universität bern/Master/Geographie/FS 2020/Seminar Geodatenanalyse/inputdata2020" #change this to the directory you downloaded and extracted the input data
print("Workspace: " + myworkspace)

#read the input rasters: dem = digital elevation model, startarr=raster with starting points (cells) for rockfall
dem=gridasciitonumpyarrayfloat(myworkspace+"/"+"clipdem.asc")
demarr=dem[0]
demcols=dem[1]
demrows=dem[2]
cellsize=dem[5]
headerstr=dem[7]
plt.imshow(demarr)
print("raster dimension: "+str(demcols)+ " columns and "+ str(demrows)+" rows")
print("cellsize:", cellsize)
#import startpoint raster as numpy array. Input is a raster dataset with values = 1 for starting points of rockfall processes
#startarr=gridasciitonumpyarrayint(myworkspace+"/"+"start1.asc")[0] #
startarr=gridasciitonumpyarrayint(myworkspace+"/"+"startpointsall.asc")[0]
#visualize the raster
plt.imshow(demarr)
plt.imshow(startarr)

#**************************************************************************
#Model Parameter (slope angle, parameter that determines stop condition of a rockfall process
slopeangleparameter=0.455#0.58 #% = 30 grad
#Learning curve:
#0.4: trajectory too long
#0.5: trajectory too short
#0.45: nearly perfect (one pixel too long)
#0.46: nearly perfect (one pixel too short)
#**************************************************************************


#create output array for writing outraster
rows=int(np.shape(demarr)[0])
cols=int(np.shape(demarr)[1])
#create an array for output (with the same dimensions as dem array)
outarr=np.zeros((rows, cols), dtype=int)
plt.imshow(outarr)

i=0
j=0
count=0
#first (outer) loop through all rows in dem array
while i <rows:
    j=0
    #second loop through all colums in row
    while j<cols:
        #check if cell is a starting point of rockfall prrocess
        if startarr[i,j]==1:
            #read out the z-coordinate of starting point
            z0 = demarr[i, j]
            #print("row: " + str(i) + "/" + "col: " + str(j))
            #print("rockfall starts ...")
            # start inner loop of rockfall trajectory
            #set initial conditions
            flowlength=0.0
            stopcondition = 0
            slope=0.0
            #x and y are the rows/column indices for the inner loop (trajectory modelling of a rockfall)
            x=i
            y=j
            #each pixel passed by the rockfall is set to value = 1
            outarr[i, j] += 1
            flowdir=flowdirection_to_steepestpath(demarr, x, y)
            #check the next cell of the trajectory
            while x>=0 and x<rows and y>=0 and y<cols and stopcondition == 0:
                flowdir = flowdirection_to_steepestpath(demarr, x, y)
                if flowdir==1:
                    y+=1
                    flowlength+=cellsize
                elif flowdir==2:
                    x+=1
                    y+=1
                    flowlength += cellsize * math.sqrt(2)
                elif flowdir==4:
                    x+=1
                    flowlength += cellsize
                elif flowdir==8:
                    x+=1
                    y-=1
                    flowlength += cellsize * math.sqrt(2)
                elif flowdir==16:
                    y-=1
                    flowlength += cellsize
                elif flowdir==32:
                    x-=1
                    y-=1
                    flowlength += cellsize * math.sqrt(2)
                elif flowdir==64:
                    x-=1
                    flowlength += cellsize
                elif flowdir==128:
                    x-=1
                    y+=1
                    flowlength += cellsize * math.sqrt(2)
                else:
                    stopcondition=1
                    break
                #z-coordinate of the actual cell
                z1=demarr[x,y]
                #compute condition for continuing/stopping the process
                if flowlength>0:
                    slope=(z0-z1)/flowlength
                else:
                    stopcondition=1
                if slope < slopeangleparameter:
                    stopcondition = 1
                #write the trajectory to the output raster
                outarr[x,y]=1
                #make a snapshot of the actual process
                #plt.imsave(myworkspace+"/"+"step"+str(count)+".png", outarr) #comment this line out if you don't want to write an image file for each step
                count+=1
        j+=1
    i+=1
print("loop done ...")
#display results
plt.imshow(outarr)
#write the output to a raster file
print("now write the output array ...")
np.savetxt(myworkspace+"/"+"rockfallhazardzone_steepestpath_all_v2.asc", outarr, fmt="%i", delimiter=" ", newline="\n", header=headerstr, comments="")
print("output array written")
print("This should be commitable")



