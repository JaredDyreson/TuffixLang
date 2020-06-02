#!/usr/bin/env python3.8

from TuffixLang.TuffixParser import Parser
from TuffixLang.Lexer import Lexer
from TuffixLang.TuffixKeywords import TuffixTokenMap
from rply.errors import LexingError

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
  while(True):
    try:
      CurrentLine = input(">>> ")
      if(not CurrentLine):
        continue
      Parser.parse(lexer.lex(CurrentLine)).eval()
    except LexingError as error:
      print("[-] Invalid selection of {}, stop".format(CurrentLine.strip()))
      print(error)
    except (EOFError, KeyboardInterrupt):
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
  except Exception as error:
      print("[-] Invalid selection of {} received, stop".format(CurrentLine.strip()))
      print(error)
      pass

TuffixScript("tuffix_installer_script")
