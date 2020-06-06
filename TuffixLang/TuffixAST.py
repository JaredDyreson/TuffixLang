from rply.token import BaseBox
from TuffixLang.ClassInformation import ClassInformationMap
from TuffixLang.Fetch import Fetch
from TuffixLang.TuffixAnsiblePlaybookManager import PlaybookManager, CurrentlyInstalled, CurrentlyInstalledFormatted
from TuffixLang.TuffixConstants import TuffixAnsibleTargetDir
from TuffixLang.TuffixHelpMessage import HelpMessageMap
import os
from natsort import natsorted, ns
import itertools

"""
TODO:

- All functionality of the program should be here
- The functions Kevin writes should be imported into this file and assigned correctly
"""

Manager = PlaybookManager(TuffixAnsibleTargetDir)

class Target(BaseBox):
    def __init__(self, target):
        self.target = target

    def eval(self):
        """
        Simply display the selected target
        """

        print("Target: {}".format(self.target))

    # def info(self, message : str):
      # return "{0: <32} {1}".format(type(self).__name__+":", message)

class Install(Target):
    def eval(self):
      """
      Run the corresponding Ansible target
      Naming scheme example should be:
      CPSC-121_AnsiblePlaybook.yml
      """
      Manager.InstallTarget(target=self.target, install=True)

class Remove(Target):
    def eval(self):
      """
      Remove the corresponding Ansible target
      Naming scheme example should be:
      CPSC-121_AnsiblePlaybook.yml
      """

      Manager.InstallTarget(target=self.target, install=False)

class Reinstall(Target):
   def eval(self):
      """
      Re-run the specific playbook, regardless if it has been run before
      """

      Manager.ReinstallTarget(target=self.target)

class Describe(Target):
    def eval(self):
      """
      Grab information about a current class
      It will complain if you request a class that does not exist
      """

      try:
          print("[+] Information about {}".format(self.target))
          print(ClassInformationMap[self.target.lower()])
      except KeyError as error:
          print("[-] Cannot retrieve information about {}".format(self.target))


class Ignore(Target):
    def eval(self):
        """
        Ignore comments and continue program flow
        """
        pass

class PrintEnv(Target):
    def eval(self):
        """
        Print environment variable
        """
        print("[INFO] Current runtime environment is {}".format(self.target))

class Die(Target):
    """
    A way to kill current interpreter process
    """

    def eval(self):
      raise EOFError("[+] Killing process!")

class Initialize(Target):
    def eval(self):
        """
        - Install fundamental packages (git, python, ansible, wget, etc.)
        - Add Tuffix PPA to /etc/apt/sources.list.d
        - Add Tuffix PPA gpg key
        - Walk student through git configuration
        - Walk student through ssh key generation
        - Walk student through gpg key generation
        - Send public key to Tuffix HQ
        - Prompt student to enter GitHub account, prompt to create account otherwise
        - Mark Tuffix as initialized
        """

        print("Initializing......")

class ListInstalled(Target):
    def eval(self):
        """
        List all of the installed packages
        Read from configuration file
        """
        print("----- All installed targets -------")
        for target in CurrentlyInstalledFormatted():
          print(target)
        print("-----------------------------------")

class ListAvailable(Target):
    def eval(self):
        print("----- All avaialble codewords -----")
        Manager.ShowAvailableTargets()
        print("-----------------------------------")

class Rekey(Target):
    def eval(self):
        print("Starting rekey process")

class Status(Target):
    def eval(self):
       print("----- BEGIN Information about host -----")
       Fetch()
       print("----- END Information about host -----")

class Help(Target):
    def eval(self):
      for option, body in HelpMessageMap.items():
        print(f'{option: <45}{body}')
