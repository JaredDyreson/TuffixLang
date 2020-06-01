from rply.token import BaseBox
from ClassInformation import class_information_map
from Fetch import fetch
from TuffixAnsiblePlaybookManager import TuffixAnisblePlaybooks

"""
TODO:

- All functionality of the program should be here
- The functions Kevin writes should be imported into this file and assigned correctly
"""

class Target(BaseBox):
    def __init__(self, target):
        self.target = target

    def eval(self):
        """
        Simply display the selected target
        """

        print("Target: {}".format(self.target))
        return self.target

class Install(Target):
    def eval(self):
      """
      Run the corresponding Ansible target
      Naming scheme example should be:
      CPSC_121_AnsiblePlaybook.ansible
      """

      print("[+] Installing {}".format(self.target))
      print("[+] Running {}_AnisblePlaybook.ansible".format(self.target.replace("-", "_")))

class Remove(Target):
    def eval(self):
      """
      Remove the corresponding Ansible target
      Naming scheme example should be:
      CPSC_121_AnsiblePlaybook.ansible
      """

      print("[+] Removing {}".format(self.target))

class Describe(Target):
    def eval(self):
      """
      Grab information about a current class
      It will complain if you request a class that does not exist
      """

      try:
          print("[+] Information about {}".format(self.target))
          print(class_information_map[self.target.lower()])
      except KeyError as error:
          print("[-] Cannot retrieve information about {}".format(self.target))

class Ignore(Target):
    def eval(self):
        """
        Ignore comments and continue program flow
        """
        pass

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

        print("Listing installed packages.....")

class ListAvailable(Target):
    def eval(self):
        print("----- All avaialble codewords -----")
        for target in TuffixAnisblePlaybooks.keys():
          print("- Class: {}".format(target.upper()))

class Rekey(Target):
    def eval(self):
        print("Starting rekey process")

class Status(Target):
    def eval(self):
       print("----- BEGIN Information about host -----")
       fetch()
       print("----- END Information about host -----")
