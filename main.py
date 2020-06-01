#!/usr/bin/env python3.8

from TuffixLang.TuffixParser import Parser
from TuffixLang.Lexer import Lexer
from TuffixLang.TuffixKeywords import TuffixTokenMap
from rply.errors import LexingError

"""
Driver code for the Tuffix Installer Prompt
AUTHOR: Jared Dyresonm
INSTITUTION: California State University Fullerton
"""

def tuffix_prompt():
  current_line = None 
  lexer = Lexer(TuffixTokenMap).get_lexer()
  pg = Parser(TuffixTokenMap)
  pg.parse()
  parser = pg.get_parser()

  while(True):
    current_line = input(">>> ")
    try:
      parser.parse(lexer.lex(current_line)).eval()
    except LexingError:
      print("[-] Invalid selection of {}, stop".format(current_line.strip()))

"""
Reading a file, simulating the instructions given to the interpreter
"""

def tuffix_script(path: str):

  current_line = None
  lexer = Lexer(TuffixTokenMap).get_lexer()
  with open(path, "r") as fp: content = fp.readlines()
  pg = Parser(TuffixTokenMap)
  pg.parse()
  parser = pg.get_parser()

  try:
      for line in content:
        current_line = line
        parser.parse(lexer.lex(line)).eval()
  except Exception as error:
      print("[-] Invalid selection of {} received, stop".format(current_line.strip()))
      pass

tuffix_script("tuffix_installer_script")
