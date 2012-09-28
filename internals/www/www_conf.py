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


print "<script src='http://code.highcharts.com/highcharts.js'></script>"
print "<script src='http://code.highcharts.com/modules/exporting.js'></script>"
 
#TODO: make our own styles

print "<link rel='stylesheet' type='text/css' href='http://learn.knockoutjs.com/Content/App/coderunner.css'>"
print "<link rel='stylesheet' type='text/css' href='http://learn.knockoutjs.com//Content/TutorialSpecific/loadingsaving.css'>"
print "<link rel='stylesheet' type='text/css' href='http://learn.knockoutjs.com//Content/TutorialSpecific/webmail.css'>"

print "<script>"


print "</script>"
print "</head>"
print "<body>"


# frontend part (list visualisation)

"""
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
"""

# frontend part (graph visualisation)
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
print "      </li> "
print "   </ul>"

print "   <h1>Event Profiles</h1>"

print "   <table border = 0>"
print "   <tr data-bind='foreach: userEvents, visible: userEvents().length > 0' >"

#print "      <td data-bind='value: name'>"
#print "<pre data-bind='text: JSON.stringify(ko.toJS($data), null, 2)'></pre>"   #USEFUL DEBUG!!
#print "      <div class='eventNameBox' data-bind='text: name' /> "
#print "      </td> "
print "      <td data-bind='value: name' id=graphContainerTD>"
print "      <div data-bind='attr: {\"id\": name}, text: name' style='min-width: 500px; min-height: 300px; margin: 0 auto;' ></div>"
print "      <div style='text-align: center;'>"
print "        <a href='#' data-bind='click: $root.removeEvent' >Skip from EventProfile (remove all actions associated)</a>"
print "      </div>"
print "      </td> "

print "   </ul>"

print "   <button data-bind='click: save'>Save</button>"
print "</body>"

print "<script type='text/javascript'>"
print "  var viewModel;"
print "var globalChart = Highcharts;"
print "  function eventChart(event) {"
#print "console.log('trying to chart :'+event.name+' HTML element is '+document.getElementById(event.name));"
print "      var chart = new Highcharts.Chart({"
print "         chart: {"
print "                renderTo: event.name,"
print "                plotBackgroundColor: null,"
print "                plotBorderWidth: null,"
print "                plotShadow: false,"
print "            },"
print "            title: {"
print "                text: 'Actions for event '+event.name"
print "            },"
print "            tooltip: {"
print "                pointFormat: ''," #FIXME: put Action's parameters here, maybe?
print "            },"
print "            plotOptions: {"
print "                pie: {"
print "                    allowPointSelect: true,"
print "                    cursor: 'pointer',"
print "                    events: {"
print "                       click: function(handle){"
                                 #here handle.point is directly the KO observable Action
#print "                          console.log(handle.point);"
print "                          action = handle.point;"
print "                          action.selected = action.removed;"
print "                          action.removed(!action.removed());"
print "                          viewModel.save();"
#print "                          console.log(handle.point);"
print "                       }"
print "                    },"
print "                    dataLabels: {"
print "                        enabled: true,"
print "                        formatter: function() {"
print "                            return '<b>'+ this.point.name +'</b>';"
print "                        }"
print "                    },"
print "                    showInLegend: false,"
print "                    selected: true,"
print "                }"
print "            },"
print "            series: [{"
print "                type: 'pie',"
print "                name: 'Actions',"
print "                data: event.actions()"
print "            }]"
print "        });"
print "  }"
print "</script>"

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
      #### here's the specific part for chart UI (on each action) ###
print "      if (this.removed) {"
print "         this.selected = false;"
print "      }else {"
print "        this.selected = true;"
print "      }"
print "      this.y = 100.0*1.0/viewModel.globalActions().length;"
print "  }"
print "  function TaskListViewModel() {"
print "   // Data"
print "   var self = this;"
print "   self.defaultUser = new User({name:'WWWDefault'});"
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
print "      var alreadyExists = false;"
print "      for (evIdx in self.userEvents()) {"
print "        if( self.userEvents()[evIdx].name == item.name ) {"
print "           alreadyExists = true;"
print "        }"
print "      }"
#print "      console.log('addEvent : '+alreadyExists);"
print "      if (!alreadyExists) {"
print "        mappedActions = $.map(self.globalActions(), function(a){ return new Action(a); });"
print "        var e = new Event(item) ; e.actions(mappedActions);"
print "        self.userEvents.push( e );"
print "        eventChart(e);"
print "        self.save();"
print "      }"
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
#print "                 eventChart(e);" #ONLY for graphic UI!!
print "                 return e;"
print "        });"
print "        self.events(mappedEvents);"
#print "        self.userEvents(mappedEvents);" #ONLY for graphic UI!!
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
print "              var mappedEvents = new Array()"
print "              mappedEvents = $.map(allData, function(item) { "
print "                          var e = new Event(item);"
print "                          mappedActions = [];"
#print "      alert('Event:'+item.name+' has actions:'+JSON.stringify(item.actions));"
print "                          mappedActions = $.map(item.actions, function(a){ return new Action(a); });"
print "                          e.actions(mappedActions);"
print "                          return e; });"
print "              if (mappedEvents.length > 0) {"
print "                 self.userEvents(mappedEvents);"
print "                 for (evIdx in self.userEvents()) {"
print "                    item = self.userEvents()[evIdx];"
print "                    eventChart(item);"
print "                 };"
print "              } else {"
print "                 self.userEvents([]);"
print "              }"
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
print "var logEvent = function(event){"
print "      console.log('seen '+event.name);"
print "      }"
print "viewModel = new TaskListViewModel()"
print "ko.applyBindings(viewModel);"

print "</script>"

print "</body>"
print "</html>"
