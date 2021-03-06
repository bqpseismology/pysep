import obspy
from getwaveform import *

def get_ev_info(ev_info,iex):
    if iex is 0:
        # Virginia earthquake
        # https://earthquake.usgs.gov/earthquakes/events/2011virginia/overview.php
        print('Extracting data for Virginia Earthquake')
        ev_info.idb = 1   # 
        ev_info.otime = obspy.UTCDateTime("2011-08-23T17:51:04")
        ev_info.min_dist = 35*111.19 
        ev_info.max_dist = 85*111.19
        ev_info.tbefore_sec = 10
        ev_info.tafter_sec = 41.2
        ev_info.network = 'II,IU,G'
        #ev_info.network = 'G'
        ev_info.channel = '*'
        ev_info.use_catalog = 1
        #ev_info.elat = 37.94
        #ev_info.elon = -77.93
        #ev_info.edep = 6000
        #ev_info.emag = 5.8
        ev_info.resample_TF = False
        
        # Shorter run
        ev_info.phase_window = True
        #ev_info.phases = ["P","S"] # Choosing time period with respect to P & S
        ev_info.phases = ["P","P"]
        ev_info.write_sac_phase = True
        #ev_info.max_dist =7000
        #ev_info.tafter_sec = 150
        ev_info.channel = 'BH?'

    return ev_info
