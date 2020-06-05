"""
All options mapped to a description
AUTHOR: Jared Dyreson
INSTITUTION: California State University Fullerton
"""

import inspect
# from TuffixLang import TuffixAST

# def initial_idea():
  # # https://stackoverflow.com/questions/22578509/python-get-only-classes-defined-in-imported-module-with-dir/22578562
  # classes = [m[0] for m in inspect.getmembers(TuffixAST, inspect.isclass) if m[1].__module__  == TuffixAST.__name__]
  # for c in classes:
    # print(getattr(TuffixAST, c)("filler_target").info("Message"))

HelpMessageMap = {
  "add, install [CODEWORD]": "install fundamental packages and guides you through the necessary steps to have a fully configured version of Ubuntu",
  "available": "list all available classes that have required software and according configuration files",
  "check, status": "the status of the host computer such as hardware information and software configurations",
  "delete, remove [CODEWORD]": "remove the required software for a given class, but preserves work done",
  "describe [CODEWORDS]": "give a brief summary of what the given class is",
  "ls": "list all installed codewords",
  "rekey": "regenerate SSH and/or GPG key"
}
