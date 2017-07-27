import obspy
import copy
import util_helpers
import shutil   # only used for deleting data directory
import os
import sys
from getwaveform import *
from obspy.clients.fdsn import Client
from obspy.core.event import Event, Origin, Magnitude, Catalog

ev_info = getwaveform()
ev_info.min_dist = 0 
ev_info.max_dist = .1 # hoping there is no other station within 100 mt radius 
ev_info.tbefore_sec = 100
ev_info.tafter_sec = 300

# event selection info
clat = 66.160507
clon = -153.369141
starttime = obspy.UTCDateTime("2010-01-01T00:00:00.000Z")
endtime = obspy.UTCDateTime("2011-01-01T00:00:00.000Z")
ev_minradius = 80
ev_maxradius = 120
minmagnitude = 7

# station selection info
network = 'AK'
channel = 'BH?'
station = ''
st_minradius = ev_minradius
st_maxradius = ev_maxradius

client = Client("IRIS")

# extract catalog of all events around the CENTER
cat = client.get_events(starttime = starttime, endtime = endtime, 
                        minradius = ev_minradius, maxradius = ev_maxradius, 
                        latitude = clat, longitude = clon, minmagnitude  = minmagnitude)
print(cat)

# get stations
inventory = client.get_stations(network = network, station = station, channel = channel,
                    starttime = starttime, endtime = endtime, level="response")
print(inventory)

# Loop over networks
for ii in range(0,len(inventory)):
    ev_info.network = inventory[ii].code
    # Loop over stations
    for jj in range(0,len(inventory[ii])):
        ev_info.station = inventory[ii][jj].code
        ev_info.channel = channel # same as above

        ev_info.rlat = inventory[ii][jj].latitude
        ev_info.rlon = inventory[ii][jj].longitude
        ev_info.rtime

        # subset_events = Find events common in alaska centroid ring (cat_0) and station ring (cat_ij)
        cat_subset = Catalog()
        for kk in range(0,len(cat)):
            dist = obspy.geodetics.base.locations2degrees(ev_info.rlat,ev_info.rlon,cat[kk].origins[0].latitude,cat[kk].origins[0].longitude)
            if dist >= st_minradius and dist <= st_maxradius:
                cat_subset.append(cat[kk])
        print(cat_subset)

        # Create station directory
        sta_dir = './' + ev_info.network + '_' + ev_info.station
        if not os.path.exists(sta_dir):
            os.makedirs(sta_dir)

        # Loop over subset_events
        for kk in range(0,len(cat_subset)):
            ev_info.otime = cat_subset[kk].origins[0].time
            ev_info.elat = cat_subset[kk].origins[0].latitude
            ev_info.elon = cat_subset[kk].origins[0].longitude
            ev_info.edep = cat_subset[kk].origins[0].depth
            ev_info.emag = cat_subset[kk].magnitudes[0].mag
            ev_info.rtime = cat_subset[kk].origins[0].time
            ev_info.ev = cat_subset[kk]      # get event object
            ev_info.reference_time_place()   # get stations around a reference origin (rlat, rlon - each station in this case)
            
            ev_info.use_catalog = 0
            ev_info.overwrite_dir = 0

            # Delete existing data directory
            eid = util_helpers.otime2eid(ev_info.ev.origins[0].time)
            ddir = './'+ eid
            if ev_info.overwrite_ddir and os.path.exists(ddir):
                print("WARNING. %s already exists. Deleting ..." % ddir)
                shutil.rmtree(ddir)

            # Get waveforms for this event-reciever pair
            try:
                ev_info.run_get_waveform()
            except:
                "WARNING: NO WAVEFORMS COULD BE EXTRACTED" # you might want to save this event and station info
                continue

            # move contents from event directory to station directory
            new_path =  sta_dir + '/' + eid
            if ev_info.overwrite_ddir and os.path.exists(new_path):
                print("WARNING. %s already exists. Deleting ..." % new_path)
                shutil.rmtree(new_path)
            
            if os.path.exists(ddir):    
                os.rename(ddir, new_path)
            
