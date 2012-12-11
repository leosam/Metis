#!/usr/bin/python

import logging
import inspect
import copy
import cgi  ###!c:/Python27/python.exe

import json
import cgitb
cgitb.enable()

print "Content-Type: text/html" # HTML is following
print   # blank line, end of headers

print "<html><head>"
print "<meta http-equiv='Content-type' content='text/html;charset=UTF-8'>"

#TODO: decide a policy for includes : local or distant?

#print "<script type='text/javascript' src='jquery-1.8.1.min.js'></script>"
#print "<script type='text/javascript' src='knockout-2.1.0.js'></script>"
print "<script type='text/javascript' src='jquery-1.8.1.debug.js'></script>"
print "<script type='text/javascript' src='knockout-2.1.0.debug.js'></script>"


print "<script src='notifier.js'></script>"

#print "<script src='http://code.highcharts.com/highcharts.js'></script>"
#print "<script src='http://code.highcharts.com/modules/exporting.js'></script>"

"""
print "<script src='strathausen-dracula-5ff039e/vendor/raphael.js'></script>"
print "<script src='strathausen-dracula-5ff039e/vendor/Curry-1.0.1.js'></script>"
print "<script src='strathausen-dracula-5ff039e/js/dracula_graffle.js'></script>"
print "<script src='strathausen-dracula-5ff039e/js/dracula_graph.js'></script>"
print "<script src='strathausen-dracula-5ff039e/js/dracula_algorithms.js'></script>"
"""

#print "<script src='arbor-v0.92/lib/arbor.js'></script>"
#print "<script src='arbor-v0.92/lib/arbor-tween.js'></script> "


#TODO: make our own styles

print "<link rel='stylesheet' type='text/css' href='http://learn.knockoutjs.com/Content/App/coderunner.css'>"
print "<link rel='stylesheet' type='text/css' href='http://learn.knockoutjs.com//Content/TutorialSpecific/loadingsaving.css'>"
print "<link rel='stylesheet' type='text/css' href='http://learn.knockoutjs.com//Content/TutorialSpecific/webmail.css'>"


print "</head>"
p = open('presentation.html','r')
for l in p.readlines():
   print l
p.close()

print "<script src='viewmodel.js'></script>"

print "</html>"
