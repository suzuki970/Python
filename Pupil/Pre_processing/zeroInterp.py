import scipy.io
import numpy as np
import pandas as pd
from scipy import signal, interpolate

def zeroInterp(pupilData,interval,methods=None):

    for trials in np.arange(0,pupilData.shape[0]): 
#        np.arange(0,1):
#      
#        print(trials)
        zeroInd = np.argwhere(pupilData[trials,]==0).reshape(-1)
        
        if len(zeroInd) > pupilData.shape[1] / 2:
            continue
        # if there are 0 value in the obtained data
        if len(zeroInd) > 0:
            if zeroInd[0] == 1 and len(zeroInd) == 1:
                pupilData[trials,0] = pupilData[trials,1]
                continue
            
            if zeroInd[0] == pupilData.shape[1] and len(zeroInd) == 1:
                pupilData[trials,-1] = pupilData[trials,-2]
                continue
            
            if zeroInd[-1] == pupilData.shape[1] and len(zeroInd) == 1:
                continue
            
            if zeroInd[-1] == pupilData.shape[1] and zeroInd[-1] != zeroInd[-2] + 1:
                pupilData[trials,-1] = pupilData[trials,-2]
    
                zeroInd = np.delete(zeroInd, -1,0)
                
            else:
                if zeroInd[-1] > pupilData.shape[1] - interval:
                    endFlag = True
                    count = len(zeroInd)-1
                    rejInd=[]
    
                    while endFlag:
    
                        if count == 0:
                            rejInd.append(count)
                            break
                      
                        if zeroInd[count] == zeroInd[count - 1] + 1:
                           rejInd.append(count)
                           count=count - 1
    
                        else:
                            rejInd.append(count)
                            endFlag=False
                            
                    zeroInd = np.delete(zeroInd, rejInd,0)
                
        if len(zeroInd) == 0:
            continue
        
        ## return if 0 includes in the beginning or ending array
        if zeroInd[0] < interval:
            endFlag = True
            count=0
            rejInd=[]
            
            while endFlag:
    
                if count == len(zeroInd)-1:
                    break
                
                if len(zeroInd) == 0:
                    rejInd.append(count)
                    endFlag = False
                    
                else:
                    if zeroInd[count] == zeroInd[count + 1] - 1:
                       rejInd.append(count)
                       count=count + 1
                        
                    else:
                       rejInd.append(count)
                       endFlag=False
                       
            zeroInd = np.delete(zeroInd, rejInd,0)
                
        y = pupilData[trials,]
        diffOnOff = np.diff(zeroInd)
        diffOnOff = np.append(diffOnOff,10**5)
        diffOnOff = np.append(10**5,diffOnOff)
        count=0
        datOfblinkCood=[]
       
        for i in np.arange(1,len(diffOnOff)).reshape(-1):

            if diffOnOff[i] >= interval and diffOnOff[i - 1] >= interval:  #### one-shot noise
    #            datOfblinkCood[count,] = [zeroInd[i - 1],zeroInd[i - 1]]
                datOfblinkCood.append(np.array([zeroInd[i - 1],zeroInd[i - 1]]))
                count=count + 1
    
            elif diffOnOff[i] >= interval and diffOnOff[i - 1] <= interval:
    #                datOfblinkCood[count,2]=zeroInd[i - 1]
                datOfblinkCood[count][1] = zeroInd[i - 1]
#                datOfblinkCood.append(np.array([0,zeroInd[i - 1]]))
                count=count + 1
    
            elif diffOnOff[i] < interval and diffOnOff[i - 1] < interval:
                pass
            elif diffOnOff[i] < interval and diffOnOff[i - 1] >= interval:
    #            datOfblinkCood[count,1]=zeroInd[i - 1]
                datOfblinkCood.append(np.array([zeroInd[i - 1],0]))
#                datOfblinkCood[count][0]=zeroInd[i - 1]
         
        # adjust the onset and offset of the eye blinks
        for i in np.arange(0,len(datOfblinkCood)):
            # for onset
            while (y[datOfblinkCood[i][0]] - y[datOfblinkCood[i][0]-1]) <= 0:
    
                datOfblinkCood[i][0] = datOfblinkCood[i][0]-1
               
                if datOfblinkCood[i][0] == 0:
                    break
    
            # for offset
            while (y[datOfblinkCood[i][1]] - y[datOfblinkCood[i][1]+1]) <= 0:
    
                datOfblinkCood[i][1] = datOfblinkCood[i][1]+1
    
                if datOfblinkCood[i][1] == len(y)-1:
                    break
    
        for i in np.arange(0,len(datOfblinkCood)):
            onsetArray = datOfblinkCood[i][0]
            offsetArray = datOfblinkCood[i][1]
            
            if onsetArray == offsetArray:
              numX = np.arange(0,(onsetArray - 1))
              numX = np.append(numX,np.arange(offsetArray + 1,len(y)))
              numY = y[numX]
              yy = interpolate.PchipInterpolator(numX, numY)
            else:
                numX =  np.arange(0,onsetArray)
                numX = np.append(numX,np.arange(offsetArray,len(y)))
               
                numY = y[numX]
                yy = interpolate.PchipInterpolator(numX, numY)
            
            pupilData[trials,] = yy(np.arange(0,len(y)))
        
    return(pupilData)
   