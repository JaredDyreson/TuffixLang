#!/usr/bin/env python3.8

from TuffixLang.version import __version__ as version
from TuffixLang.TuffixParser import Parser
from TuffixLang.Lexer import Lexer
from TuffixLang.TuffixKeywords import TuffixTokenMap
from rply.errors import LexingError
import readline # this makes our lives SOOO much easier
import os
import platform

"""
Driver code for the Tuffix Installer Prompt
AUTHOR: Jared Dyreson
INSTITUTION: California State University Fullerton
"""

CurrentLine = None
lexer = Lexer(TuffixTokenMap).get_lexer()
PG = Parser(TuffixTokenMap)
PG.parse()
Parser = PG.get_parser()
BeenInitialized = False

def TuffixPrompt():
  Preamble = """Tuffix {}
[Python {}] on Linux
Type "help", "credits" for more information
""".format(version, platform.python_version())

  os.system('clear')
  print(Preamble)

  while(True):
    try:
      CurrentLine = input(">>> ").strip()
      if(not CurrentLine):
        continue
      Parser.parse(lexer.lex(CurrentLine)).eval()
    except LexingError as error:
      print("[-] Invalid selection of {}, stop".format(CurrentLine))
    except (EOFError, KeyboardInterrupt):
      quit()
    except Exception as error:
      print("[INFO] An error has occurred, exiting\n{}".format(error))
      quit()

"""
Reading a file, simulating the instructions given to the interpreter
"""

def TuffixScript(path: str):
  with open(path, "r") as fp: content = fp.readlines()

  try:
      for line in content:
        CurrentLine = line
        Parser.parse(lexer.lex(line)).eval()
  except LexingError as error:
    print("[-] Invalid selection of {}, stop".format(CurrentLine.strip()))
    print(error)
  except (EOFError, KeyboardInterrupt):
    quit()

# TuffixScript("tuffix_installer_script")
TuffixPrompt()
