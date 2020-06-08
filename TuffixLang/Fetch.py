#!/usr/bin/env python3

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
import json
from natsort import natsorted, ns

TuffixStatePath = "/var/lib/tuffix/state.json"

def CPUInformation() -> str:
  """
  Goal: get current CPU model name and the amount of cores
  """

  path = "/proc/cpuinfo"
  _r_cpu_core_count = re.compile("cpu cores.*(?P<count>[0-9].*)")
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
      name = model_match.group("name")
    elif(cores and name):
      break
  return "{} ({} cores)".format(' '.join(name.split()), cores)

def CurrentNonRootUser() -> str:
    """
    Goal: Attempt to get the current user who is not root
    """

    return os.listdir("/home")[0]

def Host() -> str:
    """
    Goal: get the current user logged in and the computer they are logged into
    """

    return "{}@{}".format(CurrentNonRootUser(), socket.gethostname())

def CurrentOperatingSystem() -> str:
    """
    Goal: get current Linux distribution name
    """

    path = "/etc/os-release"
    _r_OS = r'NAME\=\"(?P<release>[a-zA-Z].*)\"'
    with open(path, "r") as fp: line = fp.readline()
    return re.compile(_r_OS).match(line).group("release")

def CurrentKernelRevision() -> str:
    """
    Goal: get the current kernel version
    """

    path = "/proc/version"
    with open(path, "r") as fp:
        return fp.readline().split()[2]

def CurrentTime() -> str:
    """
    Goal: return the current date and time
    """

    return datetime.now().strftime("%a %d %B %Y %H:%M:%S")

def CurrentModel() -> str:
    """
    Goal: retrieve the current make and model of the host
    """

    product_name = "/sys/devices/virtual/dmi/id/product_name"
    product_family = "/sys/devices/virtual/dmi/id/product_family"
    with open(product_name, "r") as fp:
        name = fp.readline().strip('\n')
    with open(product_family, "r") as fp:
        family = fp.readline().strip('\n')
    return "{}{}".format(name, "" if name not in family else family)

def CurrentUptime() -> str:
    """
    Goal: pretty print the contents of /proc/uptime
    Source: https://thesmithfam.org/blog/2005/11/19/python-uptime-script/
    """

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

def MemoryInformation() -> int:
    """
    Goal: get total amount of ram on system
    """
    
    formatting = lambda quantity, power: quantity/(1000**power) 
    path = "/proc/meminfo"
    with open(path, "r") as fp:
        total = int(fp.readline().split()[1])
    return int(formatting(total, 2))

def GraphicsInformation() -> str:
  """
  Use lspci to get the current graphics card in use
  Requires pciutils to be installed (seems to be installed by default on Ubuntu)
  Source: https://stackoverflow.com/questions/13867696/python-in-linux-obtain-vga-specifications-via-lspci-or-hal 
  """

  graphics_output =  tuple(subprocess.check_output("lspci | awk -F':' '/VGA|3D/ {print $3}'", shell=True, executable='/bin/bash').decode("utf-8").split("\n"))
  one, two = graphics_output

  return colored(one, 'green'), colored("None" if not two else two, 'red')


def GitConfiguration() -> str:
    """
    Retrieve Git configuration information about the current user
    """

    command = "sudo -H -u {} bash -c 'git config --list | grep -E 'user\.' | cut -d '=' -f2'".format(CurrentNonRootUser())
    git_config_output = subprocess.check_output(command, shell=True, executable='/bin/bash').decode("utf-8").split('\n')[:2]

    return tuple(git_config_output)

def HasInternet() -> bool:
    """
    GOAL: Check if there is an internet connection by attempting to open a socket to Google.
    If a connection cannot be established, it will return false.
    SOURCE: https://stackoverflow.com/questions/20913411/test-if-an-internet-connection-is-present-in-python/20913928
    """

    SERVER = "1.1.1.1"
    try:
      host = socket.gethostbyname(SERVER)
      socket.create_connection((host, 80), 2).close()
      return True
    except Exception as e: 
      pass
    return False

def CurrentlyInstalledTargets() -> list:
  """
  GOAL: list all installed codewords in a formatted list
  """

  try:
    with open(TuffixStatePath, "r") as fp:
      content = json.load(fp)["installed"]
    return [f'{"- ": >4}{element}' for element in natsorted(content, alg=ns.IC)]
  except FileNotFoundError as error:
    # raise proper exception defined in TuffixLib
    print("[INFO] Please initalize tuffix")
    return None
  

def Fetch() -> str:
  """
  GOAL: Driver code for all the components defined above
  """

  GitEmail, GitUsername = GitConfiguration()
  Primary, Secondary = GraphicsInformation()
  InstalledTargets = CurrentlyInstalledTargets()

  _Fetched = """
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
    CurrentKernelRevision(),
    CurrentUptime(),
    SystemShell(),
    SystemEditor(),
    SystemTerminalEmulator(),
    CPUInformation(),
    Primary,
    Secondary,
    MemoryInformation(),
    CurrentTime(),
    GitEmail,
    GitUsername,
    '\n'.join(InstalledTargets).strip() if (len(InstalledTargets) !=  0) else "None",
    "Yes" if HasInternet() else "No"
 )
  print(_Fetched)

def SystemShell():
  path = "/etc/passwd"
  cu = CurrentNonRootUser()
  _r_shell = re.compile("^{}.*\:\/home\/{}\:(?P<path>.*)".format(cu, cu))
  with open(path, "r") as fp:
    contents = fp.readlines()

  shell = None

  for line in contents:
    shell_match = _r_shell.match(line)
    if(shell_match and not shell):
      shell_path = shell_match.group("path")
      version, _ = subprocess.Popen([shell_path, '--version'],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT).communicate()
      shell_out = re.compile("(?P<shell>[a-z]?.*sh)\s(?P<version>[0-9].*\.[0-9])").match(version.decode("utf-8"))
      return "{} {}".format(shell_out.group("shell"), shell_out.group("version"))

  return None

def SystemTerminalEmulator() -> str:
    return os.environ["TERM"]

def SystemEditor() -> str:
    return os.environ["EDITOR"]

