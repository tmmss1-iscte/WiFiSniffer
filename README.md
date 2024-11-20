# Wi-Fi Sniffer
This repository contains the software of a Wi-Fi sniffer to capture Wi-Fi probe request messages on multiple channels simultaneously during a given period of time and save the collected data into .pcap files.

The software was designed to create a dataset of mobile device messages containing captures of individual devices in an environment isolated from electromagnetic radiation (e.g., inside an anechoic chamber room or inside a Faraday cage), in which the only equipment present are the sniffer and the mobile device to be examined, in order to study the ground truth of various mobile devices.

The purpose of this study is to develop an accurate people counting algorithm based on probe request messages, mitigating the issue of MAC address randomization that is performed in the large majority of recent [Android](https://source.android.com/docs/core/connect/wifi-mac-randomization-behavior) and [iOS](https://support.apple.com/pt-pt/guide/security/secb9cb3140c/web) devices.

This Wi-Fi sniffer was designed to perform all its tasks completely autonomously, i.e., without resorting to any human interaction since the booting of the sniffer. As so, all tasks have been duly automated so that the sniffer, in general, autonomously performs the following tasks since its boot:

  0. (Sniffer Boot)
  1. Set wireless interfaces in monitor mode (```configure_interfaces.py```);
  2. Start sniffing probe requests during a pre-defined period of time, writing out the captured data to .pcap files (```start_sniffing.py```);
  4. Generate reports/logs of each capture (```start_sniffing.py```);
  5. (Sniffer shutdown).

The algorithm sets wireless interfaces and creates .pcap capture files of Wi-Fi probe request messages simultaneously on different channels (by default it selects the non-overlapping channels 1, 6, and 11).

This simple script can be used to capture Wi-Fi packets via interfaces that support [monitor mode](https://en.wikipedia.org/wiki/Monitor_mode).

The captured files are named with the capture ID, timestamp, and channel (e.g., _CaptureA-2024-Nov-19-h12-m45-s32-ch-1._).

Reports of each capture are stored in a database as well in a text file for keeping track of each capture.

Superuser privileges are needed to run the sniffer (```sudo -E python3 main.py```).

This software is based on another [WiFi-Sniffer](https://github.com/luciapintor/WiFi-Sniffer), with some changes and updates to its software.

***IMPORTANT NOTES:*** 
 - The current software version of this project was designed and is very directed to be run on a specific device (Raspberry Pi). As so, this software may not run as intended on other devices, and it was not tested in other devices other than a Raspberry Pi.
 - This is not the finished version of this project, as it may be subject to changes in the future.

## Configure interfaces
The 'configure_interpfaces.py' file is responsible for configuring the wireless interfaces and preparing them to sniff data.

As so, the functions in the 'configure_interfaces.py' file do the following steps:
1. kill possible interfering processes and stop network managers (```sudo airmon-ng check kill```);
2. get the names of the wireless interfaces;
3. set the wireless interfaces in monitor mode;
4. set a specific channel for each monitor interface.

***NOTE:*** Some Wi-Fi interfaces do not support all channels, so there is a loop to try to assign all of them correctly.

## Start sniffing
The 'start_sniffing file.py' file is responsible for sniffing probe request messages, saving the collected data into structured .pcap files, and generating reports of each capture.

As so, the functions in the 'start_sniffing.py' file do the following steps:
1. create a folder for the captured data (if it not exists);
2. create a folder for the reports of each capture (if it not exists);
3. create the reports files in the reports folder (if not exists);
4. show the capture ID, followed by the timestamp of the capture start and its duration;
5. prepare the capture filename structure (```Capture{capture_id}-{timestamp}-ch{channel}.pcap```);
6. start a sniffing subprocess in each assigned channel during the specified duration;
7. terminate all sniffing processes;
8. generate a report for each capture, and insert them into the report files;
9. shutdown the sniffer;

Each sniffing subprocess created in step 5) uses the [tcpdump](https://www.tcpdump.org/) utility with the following arguments:
* '-i' - to specify the wireless monitor interface for capture;
* '-n' - to do not convert addresses;
* '-tt' - to show the timestamp in seconds;
* '-e' - to print the link layer headers;
* '-w' - to define the output file format (. files followed by the filename);
* 'type' 'mgt' and 'subtype' ' probe-req' - to only capture management probe request messages.

The captured .pcap files are saved in a directory called 'Data'. 

The report files are saved in a directory called 'Reports'.

***NOTE:*** The sniffer may take some time (in the order of seconds) from steps 8) and 9). This is due to the analysis of counting the number of captured packets in each .pcap file, which sometimes may take longer depending on the amount of collected data.


## Environment requirements
The file 'env_variables_example.py' is an example of how the env_variables.py file should look like. The example file is meant to be copied and renamed correctly (env_variables.py), in order to change the values of the input variables as desired.

## Main
To run the Wi-Fi sniffer, simply run the 'main.py' file with superuser privileges (```sudo -E python3 main.py```).

***NOTE:*** The sniffer will only start sniffing if there are at least two wireless interfaces on the sniffer, which means that there is at least one external Wi-Fi dongle connected to the Raspberry Pi. This mechanism was implemented to allow the normal operation of the Raspberry Pi when no Wi-Fi dongle is connected to it, which sometimes was intended during the test phase of this project.

### Crontab
As the sniffer was designed to autonomously perform all its tasks since its boot, instead of executing the 'main.py' script manually, the crontab utility can be used for this purpose.



For this, load the 'crontab.txt' file to crontab using the following command: ```crontab crontab.txt```.  This will replace the current crontab file with the 'crontab.txt', in which the last line has a scheduled task to run the 'main.py' script on boot.

 
***NOTE:*** The task on the 'crontab.txt' file assumes that the 'main.py' script is located at '/home/kali/Desktop/WiFiSniffer'. You may need to change this location according to your needs.


## Faraday cage

The [faraday_cage](https://github.com/tmmss1-iscte/WiFiSniffer/tree/main/faraday_cage) directory contains some information about the custom-made faraday cage purposefully created for this project. This directory contains another two sub-directories: images and isolation_tests. 

* The [images](https://github.com/tmmss1-iscte/WiFiSniffer/tree/main/faraday_cage/images) sub-directory contains images of the final version of the faraday cage, along with a description of its dimensions, construction, and equipments.

* The [isolation_tests](https://github.com/tmmss1-iscte/WiFiSniffer/tree/main/faraday_cage/isolation_tests) sub-direcorty contains the isolation tests prosecuted to test and validate the isolation from outside eletromagnetic and radio interference.

## Pre-requisites
This project requires the installation of the ```pyric```, ```scapy```, and ```pyshark``` libraries through pip, and the ```wireless-tools```, ```cron```, ```tcpdump```, and ```sqlite3``` packages from apt repository.

```pip install pyric```

```pip install scapy```

```pip install pyshark```

```sudo apt-get install wireless-tools```

```sudo apt-get install cron```

```sudo apt-get install tcpdump -y```

```sudo apt-get install sqlite3 libsqlite3-dev```
