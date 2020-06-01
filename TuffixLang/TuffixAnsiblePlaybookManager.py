"""
Ansible Playbook Manager class that handles running various playbooks
AUTHOR: Jared Dyreson
INSTITUTION: Calfornia State University Fullerton
"""

import os

TuffixPlaybookDir = "/tmp/playbooks"

class PlaybookManager():
    def __init__(self, manifest : dict, playbook_dir : str):
        self.manifest = manifest
        self.playbook_dir = playbook_dir
        if(not os.path.exists(self.playbook_dir)):
          raise FileNotFoundError("[-] Cannot find path to playbooks at {}".format(self.playbook_dir))

    def run_target(self, target: str, remove=False):
        """
        Run a target based on a dictionary mapping system
        Exception is raised there is not an associated playbook
        """

        try:
          if(remove):
            print("we are removing the target {}".format(target))
          print("[+] Running {}/{}".format(self.playbook_dir, self.manifest[target]))
        except KeyError:
          raise KeyError("[-] There is no current ansible playbook for {}".format(target))

    def remove_target(self, target : str):
        """
        Do the reverse of run_target
        """

        self.run_target(target, True) 


TuffixAnisblePlaybooks = {
  "cpsc-120": "CPSC_120_AnsiblePlaybook.ansible"
}

# Manager = PlaybookManager(TuffixAnisblePlaybooks, TuffixPlaybookDir)
# Manager.run_target("cpsc-120", True)
