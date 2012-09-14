#!/usr/bin/python

import logging
import inspect
import copy
import json
import os
import sys
import cgi###!c:/Python27/python.exe

from user_def import *
from plugin_mgr import *
from globalsManagers import *

import cgitb
cgitb.enable()

print "Content-Type: text/html" # HTML is following
print   # blank line, end of headers

val = ""
what = ""
whom = ""

def error(msg="error"):
   print (json.dumps(msg))
   sys.exit(0);


form = cgi.FieldStorage()
try:
   jsonData= json.loads(form['json'].value)
except Exception, e0:
   error('error loading POST val parameters : %s' %(e0))


try:
   meta = json.loads(form['meta'].value)
   what = meta['what']
   whom = meta['whom']
except Exception, e1:
   error('error loading POST meta parameters : %s' %(e1))

try:
   f = open("%s.json" %(whom),'w')
   try:
      f.write(json.dumps(jsonData))
   except Exception, e2:
      error("error writing file : %s" %(e2))
   finally:
      f.close()
except Exception, e3:
   error("error opening file : %s" %(e3))

print json.dumps("written %s for %s " %(what,whom));
