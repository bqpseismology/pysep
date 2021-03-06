import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================            
# MFFZ earthquakes for investigating the step response
# python run_getwaveform.py event_input_flats 0
    if iex == 0:
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0          # do not use event catalog for source parameters
        
        ievent = 14
        events_file = "/home/carltape/REPOSITORIES/manuscripts/carltape/papers/nennuc/clipping/data/MFFZ_step_response_obspy.txt"
        eids,otimes,elons,elats,edeps,emags = reof.read_events_obspy_file(events_file)

        ev_info_list = []
        for xx in range(ievent-1,ievent):
        #for xx in range(len(eids)):
            ev_info_temp = ev_info.copy()
            ev_info_temp.otime = obspy.UTCDateTime(otimes[xx])
            ev_info_temp.elat = elats[xx]
            ev_info_temp.elon = elons[xx]
            ev_info_temp.edep = edeps[xx]
            ev_info_temp.emag = emags[xx]
            ev_info_temp.eid = eids[xx]
            
            ev_info_temp.min_dist = 0
            ev_info_temp.max_dist = 300
            ev_info_temp.tbefore_sec = 200
            ev_info_temp.tafter_sec = 600
            ev_info_temp.network = 'AV,CN,AT,TA,AK,XV,II,IU,US'
            # ev_info_temp.network = 'XV,AK'
            ev_info_temp.channel = 'BH?,HH?'
            #ev_info_temp.scale_factor = 1
            ev_info_temp.resample_TF = False
            # for CAP
            # ev_info_temp.scale_factor = 10.0**2
            # ev_info_temp.resample_freq = 50 
        
            # to investigate step response
            ev_info_temp.isave_raw = True
            ev_info_temp.isave_raw_processed  = True
            ev_info_temp.rotateENZ = False
            ev_info_temp.rotateRTZ = False
            ev_info_temp.rotateUVW = True
            # filter options
            ev_info_temp.ifFilter = True
            ev_info_temp.zerophase = False    # causal
            # filter_type = 'lowpass'
            ev_info_temp.filter_type = 'bandpass'
            ev_info_temp.f1 = 1/100  # fmin
            ev_info_temp.f2 = 1/10  # fmax
            ev_info_temp.corners = 4
            # ev_info_temp.remove_response = False
            ev_info_temp.remove_response = True
            ev_info_temp.ipre_filt = 1
            ev_info_temp.demean = True
            ev_info_temp.detrend = True
            ev_info_temp.output_cap_weight_file = False
            # ev_info_temp.outformat = 'DISP'
            ev_info_temp.ifsave_sacpaz = True
            ev_info_temp.taper = 0.2

            # append getwaveform objects
            ev_info_list.append(ev_info_temp)
        
        # always return ev_info
        ev_info = ev_info_list
        
# NENNUC event (from Steve)
    if iex == 1:
        ev_info.idb = 1
        ev_info.use_catalog = 0          # manually enter AEC catalog parameters
        ev_info.otime = obspy.UTCDateTime("2016-01-14T19:04:10.727")
        ev_info.elat = 64.6827
        ev_info.elon = -149.2479
        ev_info.edep = 22663.7
        ev_info.emag = 3.8
        # -------------------------------------------------
        ev_info.otime = obspy.UTCDateTime("2015-09-12T03:25:12.711")
        ev_info.elat = 65.1207
        ev_info.elon = -148.6646
        ev_info.edep = 15556.8
        ev_info.emag = 2.6
        # -------------------------------------------------
        ev_info.otime = obspy.UTCDateTime("2013-03-12T07:39:50.214")
        ev_info.elat = 64.7161
        ev_info.elon = -148.9505
        ev_info.edep = 20000
        ev_info.emag = 2.1
            
        # For CAP
        ev_info.min_dist = 0
        ev_info.max_dist = 200
        ev_info.tbefore_sec = 500
        ev_info.tafter_sec = 2000
        ev_info.taper = 0.1
        ev_info.network = 'AV,CN,AT,TA,AK,XV,II,IU,US'
        # ev_info.network = 'AK,TA,II,IU,US'
        # ev_info.station = "-RAG"  # RAG has choppy data; gives error: Exception: Can't merge traces with same ids but differing sampling rates!
        ev_info.channel = 'BH?,HH?'
        ev_info.pre_filt = (0.0025, 0.003, 10.0, 15.0) # BH default
        ev_info.ipre_filt = 1

        # to investigate step response
        # ev_info.ev_info.tbefore_sec = 2000
        # ev_info.tafter_sec = 2000
        # ev_info.resample_freq = 0 
        # ev_info.scale_factor = 1
        # ev_info.ifFilter = True
        # ev_info.zerophase = False
        # ev_info.filter_type = 'bandpass'
        # ev_info.f1 = 1/100
        # ev_info.f2 = 1/20
        # ev_info.remove_response = True
        # ev_info.ipre_filt = 0
        # ev_info.demean = True
        # ev_info.detrend = True
        
# Kyle Nenana basin earthquakes for basin amplification
    if iex == 2:
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0          # do not use event catalog for source parameters
        # AEC source parameters
        ev_info.otime = obspy.UTCDateTime("2015-11-20T10:53:48.168") 
        ev_info.elat = 64.6210
        ev_info.elon = -149.4024
        ev_info.edep = 17113.4
        ev_info.emag = 2.67
        # subset of stations
        ev_info.min_dist = 0
        ev_info.max_dist = 200
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 400
        ev_info.network = 'AK,AT,II,IU,US,XM,XV,XZ,TA'  # no CN,AV,YV,ZE
        ev_info.channel = 'BH?,HH?'
        # ev_info.resample_freq = 0        # no resampling
        # ev_info.scale_factor = 1         # no scale factor
        # For CAP moment tensor
        ev_info.resample_freq = 50         # same as greens function 
        ev_info.scale_factor = 100         # change from m/s to cm/s
        # ev_info.ipre_filt = 0
        ev_info.remove_response = True
        # ev_info.demean = False
        # ev_info.detrend = False

# gets waveforms from M 8.3 Chile event with stations centered in Minto
    if iex == 3:
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0
        ev_info.otime = obspy.UTCDateTime("2015-09-16T22:54:33.000")
        ev_info.elat = -31.5695
        ev_info.elon = -71.6543
        ev_info.edep = 22400.0
        ev_info.emag = 8.30
        ev_info.rlat = 64.7716
        ev_info.rlon = -149.1465
        ev_info.rtime = obspy.UTCDateTime("2015-09-16T23:09:15.000")
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 200
        ev_info.min_dist = 0
        ev_info.max_dist = 100
        ev_info.network = 'AK,AT,II,IU,US,XM,XV,XZ,TA'  # no CN,AV,YV,ZE
        ev_info.channel = 'BH?,HH?'
        ev_info.resample_freq = 0        
        ev_info.scale_factor = 1        
        ev_info.remove_response = True

# gets a ???
    if iex == 4:
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0
        ev_info.otime = obspy.UTCDateTime("2016-06-06T00:00:00.000")
        ev_info.elat = 64.6130
        ev_info.elon = -149.0992
        ev_info.edep = 0
        ev_info.emag = 0.00
        # ev_info.rlat = 64.7716
        # ev_info.rlon = -149.1465
        # ev_info.rtime = obspy.UTCDateTime("2015-09-16T23:09:15.000")
        ev_info.tbefore_sec = 0
        ev_info.tafter_sec = 3600
        ev_info.min_dist = 0
        ev_info.max_dist = 100
        ev_info.network = 'XV,AK,TA'  # no CN,AV,YV,ZE
        ev_info.channel = 'HH?,BH?'
        ev_info.resample_freq = 0        
        ev_info.scale_factor = 1        
        ev_info.remove_response = True
        ev_info.rotateRTZ = False
        # ev_info.pre_filt=(f0*0.001, f1*0.001, f2*1000, f3*1000)
        # ev_info.ipre_filt = 2
        ev_info.ipre_filt = 0

# Chatnika earthquake
    if iex == 5:
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0          # do not use event catalog for source parameters
        # GCMT source parameters
        # the otime is the centroid time and accounts for tshift
        ev_info.otime = obspy.UTCDateTime("2017-05-08T05:09:02.000") 
        ev_info.elat = 65.2643
        ev_info.elon = -146.922
        ev_info.edep = 9000
        ev_info.emag = 3.8
        
        # subset of stations
        ev_info.min_dist = 0
        ev_info.max_dist = 500
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 500
        ev_info.network = 'AV,CN,ZE,AT,TA,AK,XV,II,IU,US' 
        ev_info.channel = 'BH?,HH?'
        ev_info.resample_freq = 50        # no resampling
        ev_info.scale_factor = 100         # no scale factor
            
# NE Nenana earthquake
    if iex == 6:
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0          # do not use event catalog for source parameters
        # GCMT source parameters
        # the otime is the centroid time and accounts for tshift
        ev_info.otime = obspy.UTCDateTime("2017-06-28T12:58:52") 
        ev_info.elat = 64.7569
        ev_info.elon = -148.8883
        ev_info.edep = 18000
        ev_info.emag = 3.5
        
        # subset of stations
        ev_info.min_dist = 0
        ev_info.max_dist = 500
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 500
        ev_info.network = 'AV,CN,ZE,AT,TA,AK,XV,II,IU,US' 
        ev_info.channel = 'BH?,HH?'
        ev_info.resample_freq = 50        
        ev_info.scale_factor = 100 

# Loop over multiple event       
    if iex == 7:
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0          # do not use event catalog for source parameters
        
        events_file = "/home/ksmith/REPOSITORIES/manuscripts/kyle/papers/basinresp/data/basinamp_obspy.txt"
        eids,otimes,elons,elats,edeps,emags = reof.read_events_obspy_file(events_file)

        ev_info_list = []
        for xx in range(0,3):
            ev_info_temp = ev_info.copy()
            ev_info_temp.otime = obspy.UTCDateTime(otimes[xx])
            ev_info_temp.elat = elats[xx]
            ev_info_temp.elon = elons[xx]
            ev_info_temp.edep = edeps[xx]
            ev_info_temp.emag = emags[xx]
            ev_info_temp.eid = eids[xx]
            
            # subset of stations
            ev_info_temp.min_dist = 0
            ev_info_temp.max_dist = 200 #500
            ev_info_temp.tbefore_sec = 100
            ev_info_temp.tafter_sec = 500
            ev_info_temp.network = 'AV,CN,ZE,AT,TA,AK,XV,II,IU,US' 
            ev_info_temp.channel = 'BH?,HH?'
            ev_info_temp.resample_freq = 50        
            ev_info_temp.scale_factor = 100 

            # append getwaveform objects
            ev_info_list.append(ev_info_temp)
        
        # always return ev_info
        ev_info = ev_info_list

    if iex == 8:
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0          # do not use event catalog for source parameters
        
        events_file = "/home/ksmith/REPOSITORIES/manuscripts/kyle/misc/F2TN_events_near_out.txt"
        eids,otimes,elons,elats,edeps,emags = reof.read_events_obspy_file(events_file)
        ev_info_temp.tafter_sec = 500
        ev_info_temp.network = 'AK,XV' 
        ev_info_temp.channel = 'BH?,HH?'
        ev_info_temp.resample_freq = 50        
        ev_info_temp.scale_factor = 100 

        # append getwaveform objects
        ev_info_list.append(ev_info_temp)
        
        # always return ev_info
        ev_info = ev_info_list

    if iex == 9:
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0          # do not use event catalog for source parameters
        # GCMT source parameters
        # the otime is the centroid time and accounts for tshift
        ev_info.otime = obspy.UTCDateTime("2018-05-27T10:40:00") 
        ev_info.elat = 64.613
        ev_info.elon = -149.0992
        ev_info.edep = 000
        ev_info.emag = 0
        ev_info.rotateRTZ = False
        # subset of stations
        ev_info.min_dist = 0
        ev_info.max_dist = 15
        ev_info.tbefore_sec = 1800
        ev_info.tafter_sec = 3600
        ev_info.network = 'XV' 
        ev_info.channel = 'HH?'
        ev_info.resample_freq = 50        
        ev_info.scale_factor = 100 

    if iex == 10:     
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0          # do not use event catalog for source parameters
	# GCMT source parameters
	# the otime is the centroid time and accounts for tshift
        
	# FNN1 outage 
	#ev_info.otime = obspy.UTCDateTime("2018-07-15T19:30:00") 
        #ev_info.elat = 64.5716
        #ev_info.elon = -149.2179

	# FTGH outage
        #ev_info.otime = obspy.UTCDateTime("2018-07-23T23:30:00")
        #ev_info.elat = 64.6917
        #ev_info.elon = -148.8278
      
	# FNN1 out again 
        ev_info.otime = obspy.UTCDateTime("2018-07-18T10:00:00")  
        ev_info.elat = 64.5716
        ev_info.elon = -149.2179
        
        ev_info.edep = 000
        ev_info.emag = 0
        ev_info.rotateRTZ = False
        # subset of stations
        ev_info.min_dist = 0
        ev_info.max_dist = 5 
        ev_info.tbefore_sec = 0 
        ev_info.tafter_sec = 3600
        ev_info.network = 'XV' 
        ev_info.channel = 'HH?'
        ev_info.resample_freq = 50        
        ev_info.scale_factor = 100 

    if iex == 11:     
        
        # Manley event
        ev_info.idb = 1
        ev_info.overwrite_ddir = 1       # delete data dir if it exists
        ev_info.use_catalog = 0          # do not use event catalog for source parameters
	
        # FNN1 out again 
        ev_info.otime = obspy.UTCDateTime("2018-08-28T15:18:44")  
        ev_info.elat = 65.1778
        ev_info.elon = -150.4964
        
        ev_info.edep = 16000
        ev_info.emag = 4.8 
        ev_info.rotateRTZ = True 
    
        # subset of stations
        ev_info.min_dist = 0
        ev_info.max_dist = 500
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 500
        ev_info.network = 'AV,CN,ZE,AT,TA,AK,XV,II,IU,US' 
        ev_info.channel = 'BH?,HH?'
        ev_info.resample_freq = 50        
        ev_info.scale_factor = 100 
 
    return(ev_info)

#=================================================================================
# END EXAMPLES
#=================================================================================
