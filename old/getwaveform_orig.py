#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tools for interfacing IRIS data, ObsPy, and SAC input/output.
"""
from __future__ import print_function

import os

import obspy
from obspy.clients.fdsn import Client
from scipy import signal

from util_write_cap import *

def run_get_waveform(c, event, idb, ref_time_place,
                     min_dist=20, max_dist=300, min_az=0, max_az=360, before=100, after=300,
                     network='*', station = '*', channel='BH*', 
                     ifresample = False, 
                     resample_freq=20, 
                     ifrotateRTZ=True, ifrotateUVW=False, 
                     ifCapInp=True, 
                     ifRemoveResponse=True,
                     ifDetrend=True, ifDemean=True, Taper=False, 
                     ifEvInfo=True,
                     scale_factor=10.0**2, ipre_filt = 1,
                     pre_filt=(0.005, 0.006, 10.0, 15.0),
                     icreateNull = 1,
                     ifFilter=False, fmin=.02, fmax=1, filter_type='bandpass', 
                     zerophase=False, corners=4, 
                     iplot_response = False, ifplot_spectrogram = False,
                     outformat = 'VEL', ifsave_sacpaz = False):
    """
    Get SAC waveforms for an event

    basic usage:
        run_get_waveform(event)

    event -       obspy Event object

    min_dist - minimum station distance (default = 20)
    max_dist - maximum station distance (default =300)
    before -   time window length before the event time (default= 100)
    after  -   time window length after the event time (default = 300)
    network -  network codes of potential stations (default=*)
    channel -  component(s) to get, accepts comma separated (default='BH*')
    ifresample_TF   - Boolean. Request resample or not. Default = False
    resample_freq   - sampling frequency to resample waveforms (default 20.0)
    ifrotate - Boolean, if true will output sac files rotated to baz
               unrotated sac files will also be written
    ifCapInp - Boolean, make weight files for CAP
    ifEvInfo - Boolean, output 'ev_info.dat' containg event info (True)
    ifRemoveResponse - Boolean, will remove response (True)
    ifDetrend - Boolean, will remove linear trend from data (True)
    ifDemean  - Boolean, will insult the data (True)
    scale_factor - scale all data by one value (10.0**2)
                    This usually puts the data in the units required by CAP
                    From m/s to cm/s
    pre_filt  - list, corner frequencies of filter to apply before deconv
                a good idea when deconvolving (ifRemoveResponse=True)
    """
    
    evtime = event.origins[0].time
    reftime = ref_time_place.origins[0].time

    if idb==1:
        print("Preparing request for IRIS ...")
        # BK network doesn't return data when using the IRIS client.
        # this option switches to NCEDC if BK is 
        if "BK" in network:
            client_name = "NCEDC"
            print("\nWARNING. Request for BK network. Switching to NCEDC client")
            c = Client("NCEDC")
        else:
            client_name = "IRIS" 

        print("Download stations...")
        stations = c.get_stations(network=network, station=station, 
                                  channel=channel,
                                  starttime=reftime - before, endtime=reftime + after,
                                  level="response")
        inventory = stations    # so that llnl and iris scripts can be combined
        print("Printing stations")
        print(stations)
        print("Done Printing stations...")
        sta_limit_distance(ref_time_place, stations, min_dist=min_dist, max_dist=max_dist, min_az=min_az, max_az=max_az)
        
        print("Downloading waveforms...")
        bulk_list = make_bulk_list_from_stalist(
            stations, reftime - before, reftime + after, channel=channel)
        stream_raw = c.get_waveforms_bulk(bulk_list)
            
    elif idb==3:
        client_name = "LLNL"
        print("Preparing request for LLNL ...")

        # Get event an inventory from the LLNL DB.
        event_number = int(event.event_descriptions[0].text)
        # event = llnl_db_client.get_obspy_event(event)
        inventory = c.get_inventory()
        
        print("--> Total stations in LLNL DB: %i" % (
                len(inventory.get_contents()["stations"])))
        sta_limit_distance(event, inventory, min_dist=min_dist, max_dist=max_dist, min_az=min_az, max_az=max_az)
        print("--> Stations after filtering for distance: %i" % (
                len(inventory.get_contents()["stations"])))

        stations = set([sta.code for net in inventory for sta in net])
        
        _st = c.get_waveforms_for_event(event_number)
        stream_raw = obspy.Stream()
        for tr in _st:
            if tr.stats.station in stations:
                stream_raw.append(tr)
    
    # set reftime
    stream = obspy.Stream()
    stream = set_reftime(stream_raw, evtime)

    print("--> Adding SAC metadata...")
    st2 = add_sac_metadata(stream,idb=idb, ev=event, stalist=inventory)

    # Do some waveform QA
    # - (disabled) Throw out traces with missing data
    # - log waveform lengths and discrepancies
    # - Fill-in missing data -- Carl request
    do_waveform_QA(st2, client_name, event, evtime, before, after)

    if ifDemean:
        st2.detrend('demean')

    if ifDetrend:
        st2.detrend('linear')

    if ifFilter:
        prefilter(st2, fmin, fmax, zerophase, corners, filter_type)

    if ifRemoveResponse:
        resp_plot_remove(st2, ipre_filt, pre_filt, iplot_response, scale_factor, stations, outformat)
    else:
        # output RAW waveforms
        decon=False
        print("WARNING -- NOT correcting for instrument response")

    if scale_factor > 0:
        amp_rescale(st2, scale_factor)
        if idb ==3:
            amp_rescale_llnl(st2, scale_factor)


    # Set the sac header KEVNM with event name
    # This applies to the events from the LLNL database
    # NOTE this command is needed at the time of writing files, so it has to
    # be set early
    st2, evname_key = rename_if_LLNL_event(st2, evtime)

    # Get list of unique stations + locaiton (example: 'KDAK.00')
    stalist = []
    for tr in st2.traces:
        #stalist.append(tr.stats.station)
        stalist.append(tr.stats.network + '.' + tr.stats.station +'.'+ tr.stats.location + '.'+ tr.stats.channel[:-1])

    # Crazy way of getting a unique list of stations
    stalist = list(set(stalist))

    # match start and end points for all traces
    st2 = trim_maxstart_minend(stalist, st2, client_name, event, evtime, ifresample, resample_freq, before, after)
    if len(st2) == 0:
        raise ValueError("no waveforms left to process!")

    if ifresample == True:
    # NOTE !!! tell the user if BOTH commands are disabled NOTE !!!
        if (client_name == "IRIS"):
            resample(st2, freq=resample_freq)
        elif (client_name == "LLNL"):
            resample_cut(st2, resample_freq, evtime, before, after)
    else:
        print("WARNING. Will not resample. Using original rate from the data")

    # save raw waveforms in SAC format
    path_to_waveforms = evname_key + "/RAW"
    write_stream_sac_raw(stream_raw, path_to_waveforms, evname_key, idb, event, stations=inventory)

    # Taper waveforms (optional; Generally used when data is noisy- example: HutchisonGhosh2016)
    # https://docs.obspy.org/master/packages/autogen/obspy.core.trace.Trace.taper.html
    # To get the same results as the default taper in SAC, use max_percentage=0.05 and leave type as hann.
    if Taper:
        st2.taper(max_percentage=Taper, type='hann',max_length=None, side='both')

    # save processed waveforms in SAC format
    path_to_waveforms = evname_key 
    write_stream_sac(st2, path_to_waveforms, evname_key)

    if ifrotateRTZ:
        rotate_and_write_stream(st2, evname_key, icreateNull, ifrotateUVW)

    if ifCapInp:
        write_cap_weights(st2, evname_key, client_name, event)

    if ifEvInfo:
        write_ev_info(event, evname_key)

    if ifplot_spectrogram:
        plot_spectrogram(st2, evname_key)

    if ifsave_sacpaz:
        write_resp(inventory,evname_key)

    # save station inventory as XML file
    xmlfilename = evname_key + "/stations.xml"
    stations.write(xmlfilename, format="stationxml", validate=True)
