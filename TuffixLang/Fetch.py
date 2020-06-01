#!/usr/bin/env python3.8

"""
Neofetch clone written in Python
AUTHOR: Jared Dyreson
INSTITUTION: California State University Fullerton
"""

import re
import os
import subprocess
import socket
from datetime import datetime
import sys
from termcolor import colored

def cpu_information():
  path = "/proc/cpuinfo"
  _r_cpu_core_count = re.compile("cpu family.*(?P<count>[0-9].*)")
  _r_general_model_name = re.compile("model name.*\:(?P<name>.*)")
  with open(path, "r") as fp:
    contents = fp.readlines()

  cores = None
  name = None

  for line in contents:
    core_match = _r_cpu_core_count.match(line)
    model_match = _r_general_model_name.match(line)
    if(core_match and cores is None):
      cores = core_match.group("count")
    elif(model_match and name is None):
      name = model_match.group("name").strip()
    elif(cores and name):
      break
  return "{} ({} cores)".format(name, cores)

def shell_env():
  _r_shell = r'(?P<shell>[a-z].*sh\s[0-9].*\.[0-9])'

  out, _ = subprocess.Popen([os.environ["SHELL"], '--version'],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT).communicate()

  current_shell_running = re.compile(_r_shell).match(out.decode("utf-8")).group("shell")
  try:
    current_editor = os.environ["EDITOR"]
  except KeyError as error:
    print("[-] Editor has not been defined")

  return current_shell_running, current_editor, os.environ["TERM"]

def host():
    return "{}@{}".format(os.environ["USER"], socket.gethostname())

def current_operating_system():
    path = "/etc/os-release"
    _r_OS = r'NAME\=\"(?P<release>[a-zA-Z].*)\"'
    with open(path, "r") as fp: line = fp.readline()
    _OS = re.compile(_r_OS).match(line).group("release")
    return _OS

def uname():
    path = "/proc/version"
    with open(path, "r") as fp:
        return fp.readline().split()[2]

def current_time():
    return datetime.now().strftime("%a %d %B %Y %H:%M:%S")

def current_model():
    path = "/sys/devices/virtual/dmi/id/product_name"
    with open(path, "r") as fp:
        return fp.readline().strip('\n')

# SOURCE - https://thesmithfam.org/blog/2005/11/19/python-uptime-script/
def current_uptime():
    path = "/proc/uptime"
    with open(path, 'r') as f:
        total_seconds = float(f.readline().split()[0])

    MINUTE  = 60
    HOUR    = MINUTE * 60
    DAY     = HOUR * 24

    days    = int( total_seconds / DAY )
    hours   = int( ( total_seconds % DAY ) / HOUR )
    minutes = int( ( total_seconds % HOUR ) / MINUTE )
    seconds = int( total_seconds % MINUTE )

    uptime = ""
    if days > 0:
       uptime += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
    if len(uptime) > 0 or hours > 0:
       uptime += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
    if len(uptime) > 0 or minutes > 0:
       uptime += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
    uptime += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )

    return uptime

def memory_information():
    formatting = lambda quantity, power: quantity/(1000**power) 
    path = "/proc/meminfo"
    with open(path, "r") as fp:
        contents = [int(line.split()[1]) for line in fp.readlines()[:3]]
    total, free, available = tuple(contents)
    return int(formatting(total, 2)), formatting(free, 2), formatting(available, 2), (round((free/available), 2))

def graphics_information():
  """
  Use lspci to get the current graphics card in use
  Requires pciutils to be installed
  """

  # https://stackoverflow.com/questions/13867696/python-in-linux-obtain-vga-specifications-via-lspci-or-hal

  graphics_output =  subprocess.check_output("lspci | awk -F':' '/VGA|3D/ {print $3}'", shell=True, executable='/bin/bash').decode("utf-8").split("\n")
  primary_out = colored("-{} [PRIMARY OUTPUT DEVICE]".format(graphics_output[0].strip()), 'green')
  try:
    secondary_out = colored("-{} [SECONDARY OUTPUT DEVICE]".format(graphics_output[1].strip()))
  except IndexError:
    secondary_out = colored("NONE: [SECONDARY OUTPUT DEVICE]", 'red')
  return "\n\t{}\n\t{}".format(primary_out, secondary_out)


def fetch():
  shell, editor, term = shell_env()
  physical, _, _, _ = memory_information()
  _fetched = """
OS: {}
Host: {}
Kernel: {}
Uptime: {}
Shell: {}
Editor: {}
Terminal: {}
CPU: {}
GPU: {}
Memory: {} GB
Current Time: {}
  """.format(
    current_operating_system(),
    current_model(),
    uname(),
    current_uptime(),
    shell,
    editor,
    term,
    cpu_information(),
    graphics_information(),
    physical,
    current_time()
 )
  print(_fetched)


fetch()
