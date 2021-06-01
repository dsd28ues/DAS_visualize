import numpy as np
import obspy.core.trace 
import matplotlib.pyplot as plt
import pandas as pd
import scipy.fft as ft

def trace_spectrum(tr):
    spectrum = ft.fft(tr.data)
    frqBins = int(spectrum.size/2)
    # frequencies of interest
    NyquistFrq = tr.stats.sampling_rate/2.0 # the Nyquist frequency
    frqs = np.linspace(0,NyquistFrq,num=frqBins)

    plt.figure()
    plt.plot(frqs,np.absolute(spectrum[:frqBins]),'k')
    plt.xlabel('Frequency (Hz)',fontsize=12)
    plt.ylabel('Amplitude',fontsize=12)    
    plt.title('Amplitude spectrum at stations:' 
    + tr.stats.station 
    + '. distance: '
    + tr.stats.location
    + ' m')
    
    return

#Based on plotArraySpec function by Eileen Martin(Intro to DAS Data)
def stream_spectrum(dataArray, stations, freq, sampleRate,scale,cbar_lim):

    minCh = stations[0]
    maxCh = stations[-1]
    # figure out sample indices for time window of interest
    startTimeIdx =  0
    endTimeIdx = dataArray.shape[1]

    # calculate the amplitude spectrum (not amplitude symmetry for +/- frequencies)
    spectrum = ft.fft(dataArray[:,:],axis=-1) 
    nFrqBins = int(spectrum.shape[1]/2) # number of frequency bins 

    amplitudeSpec =np.absolute(spectrum[:,:nFrqBins])

    # calculate indices corresponding to the frequencies of interest
    minFrq = freq[0]
    maxFrq = freq[1]
    NyquistFrq = sampleRate/2.0 # the Nyquist frequency
    # make sure maxFrq doesn't exceed Nyquist  frequency
    if(maxFrq > NyquistFrq):
        print("ERROR in plotArraySpec inputs: maxFrq "+str(maxFrq)+" >= Nyquist frequency "+str(NyquistFrq)+" indicated by sampleRate "+str(sampleRate))
        maxFrq = NyquistFrq
    
    # convert frequencies to an index in the array
    HzPerBin = NyquistFrq/float(nFrqBins) 
    minFrqIdx =  int(minFrq/HzPerBin) 
    maxFrqIdx =  int(maxFrq/HzPerBin)
    frqs = np.linspace(minFrqIdx*HzPerBin,maxFrqIdx*HzPerBin,num=(maxFrqIdx-minFrqIdx+1))

    # actually do the plot
    plt.figure()
    if scale  == 'linear':
        plt.imshow(amplitudeSpec[:,minFrqIdx:maxFrqIdx],aspect='auto',interpolation='none',cmap='inferno',extent=(minFrq,maxFrq,maxCh,minCh)) 
    elif scale == 'log10':
        plt.imshow(np.log10(amplitudeSpec[:,minFrqIdx:maxFrqIdx]),aspect='auto',interpolation='none',cmap='inferno',extent=(minFrq,maxFrq,maxCh,minCh)) 
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Station')
    plt.clim(cbar_lim[0],cbar_lim[1])
    plt.colorbar()
    plt.title('Array amplitude spectrum')       
    return

def trace_specgram():
    #To be added
    return