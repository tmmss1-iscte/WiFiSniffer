# start_sniffing.py

import os
import subprocess
import time
from datetime import datetime
import pyshark
import sqlite3

def start_sniffing(monitor_list, sniffing_duration=1200, starting_delay=0):
    """
    This function prepares the data and report folders, starts the sniffing process
    in each interface, generates reports for each capture, and shuts down the sniffer device.
    """

    # manage dataset folders
    dataset_folder = "/home/kali/Desktop/Dataset"
    data_folder = f"{dataset_folder}/Data"
    reports_folder = f"{dataset_folder}/Reports"
    if not os.path.exists(dataset_folder):  
        os.makedirs(dataset_folder)
        os.makedirs(data_folder)
        os.makedirs(reports_folder)

    # manage capture reports database and text file
    reports_db = "CapturesReport.db"
    reports_filename = "captures_report.txt"
    conn, cursor, cap_id = manage_reports_db(f'{reports_folder}/{reports_db}')    
    f = open(f"{reports_folder}/{reports_filename}", "a")

    # starting delay
    print(f"Starting delay of {starting_delay} seconds...")
    time.sleep(starting_delay)

    # capture timestamp
    ts = datetime.now()
    cap_ts = datetime.strftime(ts, "%Y-%b-%d-h%H-m%M-s%S")
    start_ts = datetime.strftime(ts, "%d/%m/%Y-%H:%M:%S")
    print(f"Capture '{cap_id}' started at: {start_ts}")
    print(f"Capture duration: {int(sniffing_duration / 60)} minutes")

    # subprocesses list
    cap_sub = []

    for m_card_channel in monitor_list:
        m_card = m_card_channel[0]
        channel = m_card_channel[1]

        filename = f'{data_folder}/Capture{cap_id}-{cap_ts}-ch{channel}.pcap'

        # start the capture in a subprocess
        cap_sub.append(
            subprocess.Popen(['tcpdump',
                                '-i', m_card,           # Select the monitor interface
                                '-n',                   # Don't convert addresses
                                '-tt',                  # Timestamp seconds
                                '-e',                   # Link level header is printed out
                                '-w', filename,         # Save output
                                'type', 'mgt',          # Managament type frames
                                'subtype', 'probe-req', # get probe requests
                                ], stdout=subprocess.PIPE))

    # sleep while sub-processes make captures 
    time.sleep(sniffing_duration)

    for sub_proc in cap_sub:
        # terminate the subprocesses
        sub_proc.terminate()

    print("Capture ended.")

    # finish timestamp
    finish_ts = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")


    for m_card_channel in monitor_list:
        channel = m_card_channel[1]

        filename = f'{data_folder}/Capture{cap_id}-{cap_ts}-ch{channel}.pcap'

        # check if capture file exists
        if os.path.exists(filename):

            # get number of captured packets
            cap = pyshark.FileCapture(filename)
            cap.load_packets()
            pkts_count = len(cap)

            # save capture report on database
            cursor.execute("""INSERT INTO CapturesReport VALUES (?, ?, ?, ?, ?, ?, "Finished", ?)""", (cap_id, f"Capture{cap_id}-{cap_ts}.pcap", str(channel).zfill(2), int(sniffing_duration / 60), start_ts, finish_ts, pkts_count))

            # save capture report on text file
            f.write(f"|File: 'Capture{cap_id}-{cap_ts}.pcap' | Channel: {str(channel).zfill(2)} | Duration: {int(sniffing_duration / 60)} minutes | Start: {start_ts} | Finish: {finish_ts} | Status: 'Finished' | Packets: {pkts_count} packets\n")

    # close reports database
    conn.commit()
    cursor.close()
    conn.close()

    # close reports text file
    f.write(f"-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    f.close()


    # shutdown when finished
    os.system("sudo shutdown now")


# manage reports database
def manage_reports_db(db_filepath):
    """
    This function connects to the reports database and retrieves the capture ID.
    """

    # connect to database
    conn = sqlite3.connect(db_filepath, timeout=30)
    cursor = conn.cursor()
    
    table = cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='CapturesReport'""").fetchone()

    # check if table exists
    if table is None:

        # create table
        cursor.execute("""CREATE TABLE CapturesReport(
                                CaptureID TEXT,
                                Filename TEXT,
                                Channel TEXT,
                                Duration INTEGER,
                                Start DATETIME,
                                Finish DATETIME,
                                Status TEXT,
                                Packets INTEGER
                            );""").fetchone()
        
        # commit changes
        conn.commit()

    
    last_cap_id = cursor.execute("""SELECT CaptureID from CapturesReport ORDER BY CaptureID DESC LIMIT 1""").fetchone()

    # get capture ID
    if last_cap_id is None:
        cap_id = "A"
    else:
        cap_id = get_cap_id(last_cap_id[0])
        

    return conn, cursor, cap_id

    
# get capture ID from database
def get_cap_id(cap_id):
    """
    This function retrieves the next capture ID.
    """

    # Convert the input argument to a list of numbers where A=0, B=1, ..., Z=25
    numbers = [ord(c) - ord('A') for c in cap_id.upper()]
    
    # Add 1 to the rightmost number (last element)
    i = len(numbers) - 1
    while i >= 0:
        if numbers[i] < 25:
            # Increment and exit the loop if it's not a "Z"
            numbers[i] += 1
            break
        else:
            # If it's a "Z", change to "A" and continue to the next digit
            numbers[i] = 0
            i -= 1
    
    # If all letters were "Z", add an "A" at the beginning (e.g., Z -> AA)
    if i < 0:
        numbers.insert(0, 0)
    
    # Convert back to a string
    return ''.join(chr(n + ord('A')) for n in numbers)
