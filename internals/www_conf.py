#!/usr/bin/python

import logging
import inspect
import copy
import cgi###!c:/Python27/python.exe

from user_def import *
from plugin_mgr import *
from globalsManagers import *

import json
import cgitb
cgitb.enable()

print "Content-Type: text/html" # HTML is following
print   # blank line, end of headers

print "<html><head>"
print "<meta http-equiv='Content-type' content='text/html;charset=UTF-8'>"
print "<script type='text/javascript' src='jquery-1.8.1.min.js'></script>"
print "<script type='text/javascript' src='knockout-2.1.0.js'></script>"
#print "<script type='text/javascript' src='jquery-1.8.1.debug.js'></script>"
#print "<script type='text/javascript' src='knockout-2.1.0.debug.js'></script>"

 
print "<link rel='stylesheet' type='text/css' href='http://learn.knockoutjs.com/Content/App/coderunner.css'>"
print "<link rel='stylesheet' type='text/css' href='http://learn.knockoutjs.com//Content/TutorialSpecific/loadingsaving.css'>"
print "<link rel='stylesheet' type='text/css' href='http://learn.knockoutjs.com//Content/TutorialSpecific/webmail.css'>"

print "<script>"


print "</script>"
print "</head>"
print "<body>"


# frontend part (visualisation)

print "<body class='codeRunner'>"
print "   <h1>Availables</h1>"


print "   <h3>Users</h3>"
print "<ul class='folders' data-bind='foreach: users'>"
print "    <li data-bind=' text: $data.name"
print "                   ,css: { selected: $data == $root.chosenUserName() }"
print "                   ,click: $root.selectUser"
print "                   '></li>"
print "</ul>"


print "   <h3>Events</h3>"
print "   <ul data-bind='foreach: events, visible: events().length > 0'>"
print "      <li>"
print "      <input data-bind='value: name'/>"
print "      <a href='#' data-bind='click: $root.addEvent'>Add</a>"
#print "      <input data-bind='value: type'/>"
print "      </li> "
print "   </ul>"

"""
print "   <h3>Possible Actions List</h3>"
print "   <ul data-bind='foreach: globalActions, visible: globalActions().length > 0'>"
print "      <li>"
print "      <input data-bind='value: name'/>"
#print "      <a href='#' data-bind='click: $root.addAction'>Add</a>"
#print "      <input data-bind='value: type' />"
print "      </li> "
print "   </ul>"
"""

print "   <h1>Event Profiles</h1>"

print "   <h2>Events</h2>"
print "   <ul data-bind='foreach: userEvents, visible: userEvents().length > 0'>"
print "      <li>"
print "      <input data-bind='value: name'/>"

#print "<pre data-bind='text: JSON.stringify(ko.toJS($data), null, 2)'></pre>"   #USEFUL DEBUG!!

print "      <a href='#' data-bind='click: $root.removeEvent'>Delete</a>"

print "        <h3 data-bind='visible: actions().length > 0'>Associated Actions</h3>"
print "           <ul data-bind='foreach: actions, visible: actions().length > 0'>"
print "              <li>"
print "              <input data-bind='value: name, disable : removed'/>"
print "              <a href='#' data-bind='click: $parents[1].removeAction'>Delete</a>"
print "              <a href='#' data-bind='click: $parents[1].addAction'>Add</a>"
print "              </li> "
print "           </ul>"


print "      </li> "
print "   </ul>"

print "   <button data-bind='click: save'>Save</button>"
print "</body>"



# backend part (view model)



print "<script type='text/javascript'>"
print "  function Event(data) {"
print "    this.name = data.name; "
print "    this.type = data.type;"
print "    this.actions = ko.observableArray([]);"
print "    if(data.hasOwnProperty('actions')) {"
print "        this.actions(data.actions);"
print "    }"
print "  }"
print "  function User(data) {"
print "    this.name = data.name; "
print "  }"
print "  function Action(data) {"
print "    this.name = data.name; "
print "    this.type = data.type;"
print "    this.removed = ko.observable(true);"
print "    if(data.hasOwnProperty('removed')) {"
print "        this.removed(data.removed);"
print "    }"
#print "    return ko.observable(this);"
print "  }"
print "  function TaskListViewModel() {"
print "   // Data"
print "   var self = this;"
print "   self.defaultUser = new User({name:'Default'});"
print "   self.chosenUserName = ko.observable(self.defaultUser);"
print "   self.globalActions = ko.observableArray([]);"  #from Globals (=all actions available)
print "   self.events = ko.observableArray([]);"  #from Globals (=all events available)
print "   self.users = ko.observableArray([self.defaultUser]);"  #from Globals (=all users available)
print "   self.userEvents = ko.observableArray([]);"


print "   self.selectUser = function(user) { "
print "        if (self.chosenUserName() && self.chosenUserName().name != ''"
print "                 ) {"
#print "           self.save();" #DEBUG: TO REPUT IN PLACE
print "        }"
print "        self.chosenUserName(user);"
print "        self.loadUserPrefs();"
#print "        self.save();" #DEBUG 
print "   };"
print "   self.removeEvent = function(item) { "
print "        self.userEvents.remove(item);"
print "        self.save();"
print "   };"
print "   self.addEvent = function(item) { "
print "      mappedActions = $.map(self.globalActions(), function(a){ return new Action(a); });"
print "      var e = new Event(item) ; e.actions(mappedActions);"
print "      self.userEvents.push( e );"
print "      self.save();"
print "   };"
print "   self.removeAction = function(item) { "
print "        item.removed(true);"
print "        self.save();"
print "   };"
print "   self.addAction = function(item) { "
print "        item.removed(false);"
print "        self.save();"
print "   };"

print "   //Load initial state from server, convert it to instances, then populate self"

print "   $.getJSON('Globals.json', function(allData) {"
print "        var mappedUsers = $.map(allData['users'], function(item) { return new User(item) });"
print "        self.users(mappedUsers);"
print "        self.users.push(self.defaultUser);"
print "        var mappedActions = $.map(allData['actionsAvailable'], function(item) { return new Action(item) });"
print "        self.globalActions(mappedActions);"
print "        var mappedEvents = $.map(allData['eventsAvailable'], function(item) { "
print "                 var e = new Event(item);"
print "                 e.actions([]);"
print "                 return e;"
print "        });"
print "        self.events(mappedEvents);"
print "    });"

print "   //save"
print "   self.save = function() {"
# now save the new EventProfile on server
print "     $.ajax('save.py', {"
print "         data: {"
print "            meta: ko.toJSON({"
print "                     what: 'EventProfile',"
print "                     whom: self.chosenUserName().name,"
#print "                     whom: self.users()[0].name,"
print "                  }),"
print "            json: ko.toJSON("
print "               this.userEvents()"
print "            )"
print "            },"
print "         type: 'POST',"
print "         dataType: 'json',"
print "         success: function(result) {"
print "            ;//alert('message :'+result);"
print "         },"
print "         error: function(result) {"
print "           if (result.statusText == 'OK') {"
print "              alert('error  ' + result);"
print "           }else {"
print "              alert('error  ' + result.statusText);"
print "              document.write(result.responseText);"
print "           }"
print "         },"
print "     });"
print "   };"
print "   self.loadUserPrefs = function() {"
print "      $.ajax({"
print "          type: 'GET',"
print "          url: self.chosenUserName().name+'.json',"
print "          dataType: 'json',"
print "          success: function(allData) {"
print "              var mappedEvents = $.map(allData, function(item) { "
print "                          var e = new Event(item);"
print "                          mappedActions = [];"
#print "      alert('Event:'+item.name+' has actions:'+JSON.stringify(item.actions));"
print "                          mappedActions = $.map(item.actions, function(a){ return new Action(a); });"
print "                          e.actions(mappedActions);"
print "                          return e; });"
print "              self.userEvents(mappedEvents);"
print "          },"
print "          error: function(allData) {"
print "              if (self.chosenUserName() != self.defaultUser) {"
print "                 alert('New Profile for '+self.chosenUserName().name);"
print "              }"
print "              self.userEvents([]);"
print "          }"
print "      });"
print "   };"
print "   self.selectUser(self.defaultUser);"
print "}"
print "ko.applyBindings(new TaskListViewModel());"


print "</script>"


print "</body>"
print "</html>"
