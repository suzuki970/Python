
import numpy as np
import numpy.matlib
from band_pass_filter import butter_bandpass_filter

def getNearestValue(in_y, num):
    idx = np.abs(np.asarray(in_y) - num).argmin()
    return idx

def moving_avg(in_y,windowL):
    np_y_conv=[]
    if len(in_y) > 1:
        for trials in np.arange(0,in_y.shape[0]): 
            np_y_conv.append(np.convolve(in_y[trials,], np.ones(windowL)/float(windowL), mode='valid'))
#            out_x_dat = np.linspace(np.min(in_x), np.max(in_x), np.size(np_y_conv))
    else:
        np_y_conv.append(np.convolve(in_y[0,], np.ones(3)/float(3), mode='valid'))
#        out_x_dat = np.linspace(np.min(in_x), np.max(in_x), np.size(np_y_conv))

    return np.array(np_y_conv)

def pre_processing(y,fs,thres,windowL,timeLen,method,filt):

    # filtering
    if len(filt) > 0:
        ave = np.mean(y,axis=1)
        y = y - np.tile(ave, (1,y.shape[1])).reshape(y.shape[1],y.shape[0]).T
        y = butter_bandpass_filter(y, filt[0], filt[1], fs, order=4)
        y = y + np.tile(ave, (1,y.shape[1])).reshape(y.shape[1],y.shape[0]).T
        
    
    ## Smoothing
    y = moving_avg(y,windowL)
    
    ## baseline(-200ms - 0ms)
    startTime=timeLen[0]
    endTime=timeLen[1]
    x = np.arange(startTime,endTime,((endTime - startTime) / (y.shape[1])))

#    baselineData = concat([knnsearch(x.T,- 0.2),knnsearch(x.T,0)])
    baselineData = np.array([getNearestValue(x,-0.2),getNearestValue(x,0)])
    baselinePLR = y[:,np.arange(baselineData[0],baselineData[1])]
    baselinePLR = np.mean(baselinePLR,axis=1)
    baselinePLR = np.tile(baselinePLR, (1,y.shape[1])).reshape(y.shape[1],y.shape[0]).T
    
    if method == 1:
        y = y - baselinePLR
    elif method == 2:
        y = y / baselinePLR
#    else:
#        y=(y - repmat(mean(y(arange(),arange(baselineData(1),baselineData(2))),2),1,size(y,2))) / repmat(std(y(arange(),arange(baselineData(1),baselineData(2))).T).T,1,size(y,2))
    
    ## reject trials when the velocity of pupil change is larger than threshold
    rejctNum=[]
    fx = np.diff(y, n=1)
    for trials in np.arange(0,y.shape[0]):
#        ind = np.argwhere(abs(fx[trials,np.arange(baselineData[1],y.shape[1]-1)]) > thres)
        ind = np.argwhere(abs(fx[trials,:]) > thres)
        if len(ind) > 0:
            rejctNum.append(trials)
    
    ## reject trials when the NAN includes
#    for j in arange(0,y.shape[0]):
#        if sum(isnan(y(j,arange()))) > 0:
#            rejctNum.append(j)
#    
#    ## reject trials when number of 0 > 50#
#    for j in arange(0,y.shape[0]):
#        if numel(find(y(j,arange()) == 0)) > size(y,2) / 2:
#             rejctNum.append(j)
    
#    rejctNum = unique(rejctNum)
#    set(rejctNum)
    return y,rejctNum
