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
  "ADD": r'(?i)add',
  "REMOVE": r'(?i)remove',
  "LIST_INSTALLED": r'(?i)installed',
  "LIST_AVAILABLE": r'(?i)available',
  "DESCRIBE": r'(?i)describe',
  "REKEY": r'(?i)rekey',
  "STATUS": r'(?i)(check)?status',
  "HELP": r'(?i)help',

  # syntax
  "COMMENT": r'^\#.*[a-zA-Z0-9]',

  # data types
  "TARGET": r'(?i:CPSC)\-(?P<course>[0-9]{3}[A-Z]?)'
}

