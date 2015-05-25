#!/usr/bin/env python

# Imports
import datetime
import os
#import shlex
import subprocess
import sys
import time

# Variable. This will be used as unique identifier for a pcap file name.
today = datetime.datetime.now().strftime("%Y-%m-%d--%H:%M")


def how_to():
  print("Usage:")
  print("  Simply run")
  print("    \"python packetnoid.py\"")
  print("[-0--<^_^>--0-]")


# Simmple function which uses subprocess to send nmap a command to 
# find all live hosts in the newtork. It then greps to find the line
# which contain an IP address, cutting only to get the IP address.
# The IPs are then converted into a list.
def get_hosts():
  try:
    print("[+] Finding the live hosts in your network!")
    cmd_1 = 'nmap -sP 192.168.1.1-254 | grep "report" | cut -d" " -f5'
    
    # Perform the actual nmap command.
    p1 = subprocess.Popen(cmd_1, stdout=subprocess.PIPE, stderr=\
      subprocess.STDOUT, shell=True)
    
    # Take the first returned value of communicate and split the lines.
    p1_list = p1.communicate()[0].splitlines()

    print("[+] Done!")
    print("[+] Here is what I found:\n")
    
    # Print live hosts found (for information only).
    for ip in p1_list:
      print("  " + ip)

    # Return IPs in a list.
    return p1_list

  except Exception:
    sys.exit("[-] Problem finding your live hosts!")


# This funtion takes the list of IPs created by get_hosts()
# and spits out a new list, formatted for tcpdump.
def preparer(p1_list):
  try:
    print("[+] Trying to prepare the command for tcpdump.")
    new_ip_list = []

    # The aim here is to ascertain the indeces of each list element.
    # There are three possibilities:
    #   1) if the index is zero, then we prefix the IP with the string "host";
    #   2) if the index is not of the last list element, append "or \"; and
    #   3) if the index is that of the last element, add "&" to the command
    for ip in p1_list:
      if p1_list.index(ip) == 0:
        new_ip_list.append("host " + ip + " or ")
      elif p1_list.index(ip) in range(1, (len(p1_list) - 1)):
        new_ip_list.append(ip + " or ")
      elif p1_list.index(ip) == (len(p1_list) - 1):
        new_ip_list.append(ip + " &")

    ip_str = ''.join(new_ip_list)

    raw_cmd = "/usr/sbin/tcpdump -i wlan0 -lenx -X -s 0 -w "\
      + os.getcwd() + "/tcpdump-" + today + ".pcap " + ip_str
    
    print("[+] Done!")
    print("[+] Here is the command:\n")
    print("  " + raw_cmd)

    # Return the command as a string. "shell=True" must be passed 
    # as a subprocess' argument.
    return raw_cmd

  except Exception:
    sys.exit("[-] Could not prepare the IP list for tcpdump.")


def monitore(raw_cmd):
  #while True:
    try:
      f_name = os.getcwd() + "/tcpdump-" + today + ".pcap"

      f_handle = open(f_name, 'wb')

      print("[+] Firing tcpdump now.")
      p2 = subprocess.Popen(raw_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, \
                         stderr=subprocess.STDOUT, shell=True)

      # Putting the script to sleep for 24 hours whilst tcpdump
      # runs on the background.
      # time.sleep(86400)
      time.sleep(5)
      p2.terminate()
      f_handle.close()
      
      # try:
      #   print("[+] Zipping pcap file.")
      #   p3 = subprocess.Popen(gzip, stdout=subprocess.PIPE, shell=True)
      #   #p3.terminate()
      #   print("[+] Done!\n")
      # except Exception:
      #   sys.exit("[-] I have managed to run tcpdump, but could not zip the file")

    except Exception:
        sys.exit("[-] Could not run the actual tcpdump command.") 


def main():
  if len(sys.argv) > 1:  
    sys.exit(how_to())

  print("The default network to be scanned is:")
  print("  192.168.1.0/24")
  print("\n----------------------------------------------------")
  
  try:
    p1_list = get_hosts()
  except Exception:
    sys.exit("[-] Main function could not get the return of get_hosts().")
  
  print("\n----------------------------------------------------")
  try:
    raw_cmd = preparer(p1_list)
  except Exception:
    sys.exit("[-] Main function could not get the return of preparer().")

  print("\n----------------------------------------------------")
  try:
    monitore(raw_cmd)
  except Exception:
    sys.exit("[-] Main function could not call monitore().")

if __name__ != "__main__":
  sys.exit("[!] NO WAY!")
else:  
  main()