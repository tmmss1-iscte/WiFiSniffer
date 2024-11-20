# configure_interfaces.py

import subprocess
import os
import pyric.pyw as pyw
import pyric.utils.channels as pych



# configure interfaces in monitor mode and set each to a specific channel
def configure_interfaces(channels=None):

    # kill interfering processes and stop network managers
    subprocess.call(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # set default channels, if not defined
    if channels is None:
        channels = [1, 6, 11]

    # check all wireless interfaces
    for w_id in pyw.winterfaces():

        # get info of interface
        # ex: Card(phy=0, dev='wlan0', ifindex=2)
        w_card = pyw.getcard(w_id)

        # check if it supports monitor mode and has a known driver
        if "monitor" in pyw.devmodes(w_card) and pyw.ifinfo(w_card)["driver"] != "Unknown":

            # check if it is not in monitor mode
            if pyw.devinfo(w_card)["mode"] != "monitor":

                # set wireless interface in monitor mode
                set_monitor_mode(w_card.dev)


    # list of tuples of monitor interfaces and channels
    # [ ('wlan_id', channel), ...]
    monitor_list = []
    
    # check all wireless interfaces
    # **NOTE**: A second iteration of the wireless interfaces must be executed since the 
    # 'airmon-ng' utility may create a wireless interface with a different name.
    # ex: manager mode -> 'wlan0'; monitor mode -> 'wlan0mon'.
    for w_id in pyw.winterfaces():

        # get info of interface
        # ex: Card(phy=0, dev='wlan0', ifindex=2)
        w_card = pyw.getcard(w_id)

        if pyw.devinfo(w_card)["mode"] == "monitor":

            # set channel on monitor interface
            set_interface_channel(w_card.dev, channels[0])

            # verify channel on monitor interface
            if verify_card_channel(w_card, channels[0]):
                
                # add tuple ('wlan_id', channel) to list and remove channel
                w_card_channel = (w_card.dev, channels[0])
                monitor_list.append(w_card_channel)
                channels.pop(0)

    return monitor_list



# set wireless interface in monitor mode
def set_monitor_mode(interface):
    """
    This function sets the interface to monitor mode using airmon-ng.
    """
    subprocess.call(["sudo", "airmon-ng", "start", str(interface)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


# set wireless interface channel
def set_interface_channel(interface, channel):
    """
    This function sets a channel to wireless interface using iwconfig.
    """

    subprocess.call(["sudo", "iwconfig", str(interface), "channel", str(channel)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


# verify wireless interface channel
def verify_card_channel(w_card, channel):
    """
    This function verifies if a channel was set to a wireless interface.
    """
    
    ch_freq = pych.ch2rf(channel)
    device_freq = pyw.devinfo(w_card).get('CF', None)

    if ch_freq != device_freq:
        return False
    else:
        return True






        
