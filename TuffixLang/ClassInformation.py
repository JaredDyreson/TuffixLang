"""
Get the CS catalog for CSUF 2020
AUTHOR: Jared Dyreson
INSTITUTION: California State University Fullerton
"""

import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint as pp
import json
from datetime import datetime
import os

"""
This contains all the information about the computer science classes
"""

# set to conf dir but relative path is okay right now
TuffixCacheDir = "cache"
if(not os.path.isdir(TuffixCacheDir)):
  os.mkdir(TuffixCacheDir)
class_cache = "{}/California_State_University_CS_Catalog_{}.json".format(TuffixCacheDir, datetime.now().year)

def scrape_page():
  url = "https://catalog.fullerton.edu/preview_program.php?catoid=61&poid=28640&returnto=7392"
  _r_valid_class = re.compile(r'(?P<courseId>CPSC\s[0-9]{3}[A-Z]?)\s\-(?P<courseDescription>.*)\([0-9]\)', flags = re.M)

  content = requests.get(url).content
  soup = BeautifulSoup(content, features="lxml")

  classes = soup.find('div', attrs = {'class': 'custom_leftpad_20'}).find_all('li', class_="acalog-course")
  class_manifest = [element.text for element in classes]
  ClassInformationMap = {}
  for c in class_manifest:
    check = _r_valid_class.match(c)
    if(check):
      course_title, course_description = check.group("courseId").replace(" ", "-").lower(), check.group("courseDescription").strip()
      ClassInformationMap[course_title] = course_description

  with open(class_cache, "w") as fp:
      json.dump(ClassInformationMap, fp)

  return ClassInformationMap

if(os.path.exists(class_cache)):
  with open(class_cache, "r") as fp:
    ClassInformationMap = json.load(fp)
else:
  ClassInformationMap = scrape_page()
