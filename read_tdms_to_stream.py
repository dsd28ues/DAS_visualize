from obspy.core.utcdatetime import UTCDateTime
import obspy
import obspy.core.trace 
import obspy.core.stream
from tdms_reader import TdmsReader
import numpy as np

def read_tdms_to_stream(filename, das_channels,sampling):

    tdms = TdmsReader(filename)
    props = tdms.get_properties()

    zero_offset = props.get('Zero Offset (m)') 
    channel_spacing = props.get('SpatialResolution[m]') * props.get('Fibre Length Multiplier')
    n_channels = tdms.fileinfo['n_channels']
    depth = zero_offset + np.arange(n_channels) * channel_spacing
    fs = props.get('SamplingFrequency[Hz]')
        
    #COnverting to obspy stream 
    #Note: Obspy channel referes to component. 
    st = obspy.Stream()
    stations = das_channels
    for channel in stations:
        first_time_sample = 0
        last_time_sample = tdms._channel_length
        trace_data = tdms.get_data(channel,channel,first_time_sample, last_time_sample).reshape(-1)
        trace = obspy.Trace()

        #trace properties
        trace.stats.sampling_rate = fs
        trace.stats.delta = 1/fs
        trace.stats.npts = tdms.channel_length + 1
        trace.stats.network = 'OU_DAS_2021'
        location = depth[channel]
        trace.stats.location = f'{location:5.2f}'
        trace.stats.station = str(channel)
        trace.stats.channel = 'C' #arbitrary name for single component
        trace.stats.starttime = UTCDateTime(props.get('GPSTimeStamp'))

        #trace data
        trace.data = trace_data

        #resampling to save space
        trace = trace.resample(sampling) #change resampling
        st.append(trace)
    print('traces in stream : '+ str(len(st)))
    return st
