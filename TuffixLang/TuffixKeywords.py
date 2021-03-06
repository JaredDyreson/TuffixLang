#!/usr/bin/env python3.8

"""
This contains all of the keywords used in this language
AUTHOR: Jared Dyreson
INSTITUTION: California State University Fullerton
"""

from TuffixLang.Lexer import Lexer

TuffixTokenMap = {

  # builtin functions
  "INIT": r'(?i)init',
  "ADD": r'(?i)add|install',
  "REMOVE": r'(?i)delete|remove',
  "REINSTALL": r'(?i)reinstall',
  "LIST_INSTALLED": r'(?i)ls|installed',
  "LIST_AVAILABLE": r'(?i)available',
  "DESCRIBE": r'(?i)describe',
  "REKEY": r'(?i)rekey',
  "STATUS": r'(?i)check|status',
  "HELP": r'(?i)help',
  "QUIT": r'(?i)exit|quit',

  # syntax
  "COMMENT": r'^\#[^\!].*[a-zA-Z0-9]',
  "GLOB": r'\*|(?i:all)',

  # data types
  "TARGET": r'(?i:CPSC)\-(?P<course>[0-9]{3}[A-Z]?)',

  # environment variable  
  "ENV": r'^\#\!\/usr\/bin\/env\s(?P<env>.*)'
}

