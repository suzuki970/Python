import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from zeroInterp import zeroInterp
from pre_processing import pre_processing

mat = scipy.io.loadmat('dataForPython.mat')
allPupilData = mat['PLR'] 
startTime = -1
endTime = 4

x = np.arange(startTime,endTime,((endTime - startTime) / (allPupilData.shape[1])))

plt.figure(figsize=(15.0, 3.0))
plt.subplot(1,3,1)
plt.plot(x,allPupilData.T)
plt.title('raw data',fontsize=14)
plt.xlabel('time[s]',fontsize=14)
plt.ylabel('pupil diameter [mm]',fontsize=14)

## blink interpolation
y = allPupilData

#y = allPupilData[np.arange(24,25),]
y = zeroInterp(y,10)
#y = y[np.arange(0,1),]
plt.subplot(1,3,2)
plt.plot(x,y.T)
plt.title('interpolated data',fontsize=14)
plt.xlabel('time[s]',fontsize=14)
plt.ylabel('pupil diameter [mm]',fontsize=14)
   
### pre-processing
SAMPLING_FREQENCY = 250
#pre_processing(pupil_data, sampling frequency, threshold, window for smoothing, time period of onset and offset)
y,rejctNum = pre_processing(y,SAMPLING_FREQENCY,0.05,30,
                            np.array([startTime,endTime]),1,np.array([.2,35]))

x = np.arange(startTime,endTime,((endTime - startTime) / (y.shape[1])))
#y = np.delete(y,rejctNum,axis=0)

plt.subplot(1,3,3)
plt.plot(x,y.T)
plt.title('baseline-corrected data',fontsize=14)
plt.xlabel('time[s]',fontsize=14)
plt.ylabel('pupil diameter [mm]',fontsize=14)

## sample.m:34
#subplot(1,3,3)
#hold('on')
#x=concat([arange(startTime,endTime,(endTime - startTime) / (size(y,2) - 1))])
## sample.m:36
#plot(x,y.T)
#title('baseline corrected data')
#xlabel('time[s]')
#ylabel('baseline corrected pupil changes [mm]')
#set(gca,'FontName','Times','FontSize',18)