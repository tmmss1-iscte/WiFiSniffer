# main.py
from configure_interfaces import pyw, configure_interfaces
from start_sniffing import start_sniffing
from env_variables import channels, sniffing_duration, starting_delay


# Start sniffer if there is more than 1 wireless interface 
# (which means that there is at least one external wi-fi dongle connected to the Raspberry Pi sniffer)
if len(pyw.winterfaces()) > 1:

    monitor_list = configure_interfaces(channels)
    print(monitor_list)
    start_sniffing(monitor_list, sniffing_duration, starting_delay)


