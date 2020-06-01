#!/usr/bin/env python3.8

"""
This contains all of the keywords used in this language
AUTHOR: Jared Dyreson
INSTITUTION: California State University Fullerton
"""

from Lexer import Lexer

cpsc_regex = r'CPSC\-(?P<course>[0-9]{3}[A-Z]?)'

TuffixTokenMap = {

  # builtin functions
  "INIT": r'(?i)init',
  "ADD": r'(?i)add.*CPSC\-(?P<course>[0-9]{3}[A-Z]?)',
  "REMOVE": r'(?i)remove.*CPSC\-(?P<course>[0-9]{3}[A-Z]?)',
  "LIST_INSTALLED": r'(?i)installed',
  "LIST_AVAILABLE": r'(?i)available',
  "DESCRIBE_TARGET": r'(?i)describe.*CPSC\-(?P<course>[0-9]{3}[A-Z]?)',
  "REKEY": r'(?i)rekey',
  "STATUS": r'(?i)status',
  "TARGET": cpsc_regex,

  # syntax
  "COMMENT": r'^\#.*[a-zA-Z0-9]',

}

