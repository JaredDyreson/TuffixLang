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

def CPUInformation():
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

def ShellEnv():
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

def Host():
    return "{}@{}".format(os.environ["USER"], socket.gethostname())

def CurrentOperatingSystem():
    path = "/etc/os-release"
    _r_OS = r'NAME\=\"(?P<release>[a-zA-Z].*)\"'
    with open(path, "r") as fp: line = fp.readline()
    _OS = re.compile(_r_OS).match(line).group("release")
    return _OS

def Uname():
    path = "/proc/version"
    with open(path, "r") as fp:
        return fp.readline().split()[2]

def CurrentTime():
    return datetime.now().strftime("%a %d %B %Y %H:%M:%S")

def CurrentModel():
    product_name = "/sys/devices/virtual/dmi/id/product_name"
    product_family = "/sys/devices/virtual/dmi/id/product_family"
    with open(product_name, "r") as fp:
        name = fp.readline().strip('\n')
    with open(product_family, "r") as fp:
        family = fp.readline().strip('\n')
    return "{}{}".format(name, "" if name not in family else family)

# SOURCE - https://thesmithfam.org/blog/2005/11/19/python-uptime-script/
def CurrentUptime():
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

def MemoryInformation():
    formatting = lambda quantity, power: quantity/(1000**power) 
    path = "/proc/meminfo"
    with open(path, "r") as fp:
        contents = [int(line.split()[1]) for line in fp.readlines()[:3]]
    total, free, available = tuple(contents)
    return int(formatting(total, 2)), formatting(free, 2), formatting(available, 2), (round((free/available), 2))

def GraphicsInformation():
  """
  Use lspci to get the current graphics card in use
  Requires pciutils to be installed
  """

  # https://stackoverflow.com/questions/13867696/python-in-linux-obtain-vga-specifications-via-lspci-or-hal

  graphics_output =  subprocess.check_output("lspci | awk -F':' '/VGA|3D/ {print $3}'", shell=True, executable='/bin/bash').decode("utf-8").split("\n")
  primary_out = colored("{}".format(graphics_output[0].strip()), 'green')
  try:
    secondary_out = colored("{}".format(graphics_output[1].strip()))
  except IndexError:
    secondary_out = colored("NONE", 'red')
  return "{}\n{}".format(primary_out, secondary_out)

def GitConfiguration():
    git_config_output = subprocess.check_output("git config --list | grep -E 'user\..*' | cut -d '=' -f2", shell=True, executable='/bin/bash').decode("utf-8").split('\n')

    return tuple(git_config_output)

def HasInternet():
    # https://stackoverflow.com/questions/20913411/test-if-an-internet-connection-is-present-in-python/20913928
    SERVER = "1.1.1.1"
    try:
      host = socket.gethostbyname(SERVER)
      socket.create_connection((host, 80), 2).close()
      return True
    except Exception as e: 
      pass
    return False

def fetch():
  shell, editor, term = ShellEnv()
  physical, _, _, _ = MemoryInformation()
  git_conf = GitConfiguration()
  git_email, git_username = git_conf[0], git_conf[1]
  output_devices = GraphicsInformation().split("\n")
  primary, secondary = output_devices[0], output_devices[1]
  _fetched = """
{}
-----

OS: {}
Model: {}
Kernel: {}
Uptime: {}
Shell: {}
Editor: {}
Terminal: {}
CPU: {}
GPU:
  - Primary: {}
  - Secondary: {}
Memory: {} GB
Current Time: {}
Git Configuration:
  - Email: {}
  - Username: {}
Installed codewords:
  {}
Connected to Internet: {}

  """.format(
    Host(),
    CurrentOperatingSystem(),
    CurrentModel(),
    Uname(),
    CurrentUptime(),
    shell,
    editor,
    term,
    CPUInformation(),
    primary,
    secondary,
    physical,
    CurrentTime(),
    git_email,
    git_username,
    "HELLO WORLD\nANOTHER WORLD",
    "Yes" if HasInternet() else "No"
 )
  print(_fetched)
fetch()
