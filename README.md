# Wi-Fi Sniffer
This repository contains the software of a Wi-Fi sniffer to capture Wi-Fi probe request messages on multiple channels simoultaneously during a given period of time. 

The software was designed to create a dataset of mobile device messages containing captures of individual devices in an environment isolated from eletromagnetic radiation (e.g., inside an anechoic chamber room or inside a Faraday cage), in order to study the ground truth of various mobile devices.

In order to obtain the digital signature of each examined mobile device, the captures must be procecuted in an isolated ennvironment in which the only equipment present are the sniffer and the mobile device to be examined, so that the captures only contain the probe request messages emitted by the latter.

The purpose of this study is to develop accurate people counting algorithms based on probe request messages, mitigating the issue of MAC address randomization that is performed in the large majority of recent [Android](https://source.android.com/docs/core/connect/wifi-mac-randomization-behavior) and [iOS](https://support.apple.com/pt-pt/guide/security/secb9cb3140c/web) devices.

This algorithm sets wireless interfaces and creates pcap capture files of Wi-Fi probe request messages simultaneously on different channels (by default it selects the non-overlapping channels 1, 6 and 11).

This simple script can be used to capture Wi-Fi packets via interfaces that support [monitor mode](https://en.wikipedia.org/wiki/Monitor_mode).

This algorithm configures the sniffing interfaces, starts the sniffing in each interface and saves collected data in files.

The captured files are named with the capture ID, timestamp, and channel (i.e. _CaptureA-2024-Nov-19-h12-m45-s32-ch-1.pcap_).

Superuser privileges are needed to run this script (```sudo -E python3 main.py```).

***NOTE 1:*** This software is based on another [Wi-Fi Sniffer](https://github.com/luciapintor/WiFi-Sniffer), with some changes and updates to its software.

***NOTE 2:*** This is not the finished version of this project, as it may be subtile to changes in the future.

## Configure interfaces


## Start sniffing


## Environment requirements


## Main


## Requirements


 






