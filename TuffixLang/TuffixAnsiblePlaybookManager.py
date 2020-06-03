"""
Ansible Playbook Manager class that handles running various playbooks
AUTHOR: Jared Dyreson
INSTITUTION: Calfornia State University Fullerton
"""

import os
from TuffixLang.TuffixConstants import TuffixAnsibleTargetDir, TuffixTargetInstalledManifest
from natsort import natsorted, ns

class PlaybookManager():
    def __init__(self, playbook_dir : str):
        self.playbook_dir = playbook_dir
        if(not os.path.exists(self.playbook_dir)):
          raise FileNotFoundError("[-] Cannot find path to playbooks at {}".format(self.playbook_dir))
        self.manifest = self.ObtainManifest()

    def InstallTarget(self, target: str, install=True):
        """
        Run a target based on a dictionary mapping system
        Exception is raised there is not an associated playbook
        """

        with open(TuffixTargetInstalledManifest, "r") as fp:
            contents = fp.read().splitlines()
        if(install):
          if(self.IsInstalled(target=target)):
            print("[-] Cannot proceed, {} is already installed".format(target))
          else:
            print("[+] Installing {} .....".format(target))
            with open(TuffixTargetInstalledManifest, "w+") as fp:
              fp.write(target)
        else:
          if(self.IsInstalled(target=target)):
            print("[+] Removing {}".format(target))
            contents.remove(target.upper())
            with open(TuffixTargetInstalledManifest, "w") as fp:
              fp.writelines(contents)
          else:
            print("[-] Cannot remove {}, it is not installed".format(target))

    def RemoveTarget(self, target : str):
        """
        Do the reverse of InstallTarget
        """

        self.InstallTarget(target, False) 

    def ObtainManifest(self) -> dict:
        manifest = {}
        # https://stackoverflow.com/questions/15235823/how-to-ignore-hidden-files-in-python-functions
        for script in natsorted(os.listdir(self.playbook_dir), alg=ns.IC):
          if not script.startswith('.') and os.path.isfile(os.path.join(TuffixAnsibleTargetDir, script)):
            manifest[script.split("_")[0].lower()] = script
        return manifest

    def IsInstalled(self, target: str) -> bool:
       with open(TuffixTargetInstalledManifest, "r") as fp:
         return target.upper() in fp.read().splitlines()

    def IsValidTarget(self, target: str) -> bool:
        return target.lower() in list(self.manifest.keys())

    def ShowAvailableTargets(self):
        for script in natsorted(os.listdir(TuffixAnsibleTargetDir), alg=ns.IC):
          if not script.startswith('.') and os.path.isfile(os.path.join(TuffixAnsibleTargetDir, script)):
            print("- {}".format(script.split("_")[0]))
