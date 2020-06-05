"""
Ansible Playbook Manager class that handles running various playbooks
AUTHOR: Jared Dyreson
INSTITUTION: Calfornia State University Fullerton
"""

import os
from TuffixLang.TuffixConstants import TuffixAnsibleTargetDir, TuffixTargetInstalledManifest
from natsort import natsorted, ns
from TuffixLang.Debug import dump_args

class PlaybookManager():
    def __init__(self, playbook_dir : str):
        self.playbook_dir = playbook_dir
        if(not os.path.exists(self.playbook_dir)):
          raise FileNotFoundError("[-] Cannot find path to playbooks at {}".format(self.playbook_dir))
        self.manifest = self.ObtainManifest()

    @dump_args
    def InstallTarget(self, target: str, install=True, override=False):
        """
        Run a target based on a dictionary mapping system
        Exception is raised there is not an associated playbook
        """

        if(install):
          if(self.IsInstalled(target=target) and not override):
            print("[-] Cannot proceed, {} is already installed".format(target))
          else:
            if(not self.IsValidTarget(target)):
              print("[-] Not valid target: {}".format(target))
            else:
              print("[+] Installing {} .....".format(target))
              with open(TuffixTargetInstalledManifest, "a")as fp:
                fp.write("{}\n".format(target))
        else:
          if(self.IsInstalled(target=target)):
            print("[+] Removing {}".format(target))
            contents = CurrentlyInstalled()
            contents.remove(target.upper())
            with open(TuffixTargetInstalledManifest, "w") as fp:
              fp.write('\n'.join(contents) + '\n')
          else:
            print("[-] Cannot remove {}, it is not installed".format(target))

    @dump_args
    def RemoveTarget(self, target : str):
        """
        Do the reverse of InstallTarget
        """

        self.InstallTarget(target, False) 

    def ReinstallTarget(self, target : str):
        """
        Re-run the specific playbook, regardless if it has been run before
        """
        if(target == "*"):
          print("[+] Reinstalling all targets")
          for target in CurrentlyInstalled():
            self.InstallTarget(target, install=True, override=True)
        else:
            self.InstallTarget(target, install=True, override=True)

    def ObtainManifest(self) -> dict:
        manifest = {}
        # https://stackoverflow.com/questions/15235823/how-to-ignore-hidden-files-in-python-functions
        for script in natsorted(os.listdir(self.playbook_dir), alg=ns.IC):
          if not script.startswith('.') and os.path.isfile(os.path.join(TuffixAnsibleTargetDir, script)):
            manifest[script.split("_")[0].lower()] = script
        return manifest

    def IsInstalled(self, target: str) -> bool:
        return target.upper() in CurrentlyInstalled() 

    def IsValidTarget(self, target: str) -> bool:
        return target.lower() in list(self.manifest.keys())

    def ShowAvailableTargets(self):
        for script in natsorted(os.listdir(TuffixAnsibleTargetDir), alg=ns.IC):
          if not script.startswith('.') and os.path.isfile(os.path.join(TuffixAnsibleTargetDir, script)):
            print("- {}".format(script.split("_")[0]))

def CurrentlyInstalled() -> list:
  with open(TuffixTargetInstalledManifest, "r") as fp:
    return fp.read().splitlines()

def CurrentlyInstalledFormatted() -> list:
    return [f'{"- ": >4}{element}' for element in natsorted(CurrentlyInstalled(), alg=ns.IC)]
