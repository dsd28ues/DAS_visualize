#Based on plotSpaceTime function by Eileen Martin(Intro to DAS Data)
import numpy as np
import obspy.core.trace 
import matplotlib.pyplot as plt
import pandas as pd
import scipy.fft as ft

def stream_amplitude(stream_data,stations,time,sampleRate,amp):
    minCh = stations[0]
    maxCh = stations[-1]
    # Basic error checking
    minSec = time[0]
    maxSec = time[-1]


    # turn time range (in seconds) to indices
    minSecID = int(minSec*sampleRate) 
    maxSecID = int(maxSec*sampleRate) 

    plt.figure()
    plt.imshow(stream_data[:,minSecID:maxSecID],aspect='auto',interpolation='none',cmap='seismic',extent=(minSec,maxSec,maxCh,minCh))
    plt.xlabel('time (s)',fontsize=12)
    plt.ylabel('Station',fontsize=12)
    plt.title('Array amplitudes',fontsize=14)
    plt.colorbar()
    plt.clim(-amp,amp)
    return

def stream_RMS(stream_data,stations,time,sampleRate,win,step,amp):
    twinSize = win
    tstepSize = step
    t0 = time[0] +win/2
    t1 = time[-1] - win/2

    n0 = int(t0*sampleRate)
    n1 = int(t1*sampleRate)
    nwinSize = int(twinSize*sampleRate)
    nstepSize = int(tstepSize*sampleRate)
    nL = int(1 - nwinSize/2);
    nR = int(nwinSize/2);

    winRMS = np.arange(n0,n1+1,nstepSize)

    RMS = np.zeros((len(stations),winRMS.size),dtype=float)
    for iwin in range(0,winRMS.size):
        RMS[:,iwin] = np.sqrt(np.mean(np.square(stream_data[:,winRMS[iwin]+nL:winRMS[iwin]+nR]),axis=1))

    chSt = 0
    chEd = np.size(RMS,0) - 1
    minWin = winRMS[0]/sampleRate;
    maxWin = winRMS[-1]/sampleRate;
    # plt.imshow(RMS[chSt:chEd,winRMS[0]:winRMS[-1]],aspect='auto',interpolation='none',cmap='jet',extent=(minWin,maxWin,chSt,chEd))
    plt.figure
    plt.imshow(RMS,aspect='auto',interpolation='none',cmap='jet',extent=(minWin,maxWin,max(stations),min(stations)))
    plt.title("RMS in " + str(twinSize) + "s window",fontsize=14)
    plt.xlabel('time (s)',fontsize = 12)
    plt.ylabel('Station',fontsize=12)
    plt.colorbar()
    plt.clim(0,amp)
    #print(minWin)
    #print(maxWin)
    #print(chEd)
    #print(RMS.shape)
    #print(winRMS)
    #print(nstepSize)
    return