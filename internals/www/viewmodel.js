
/*
######
#here comes the eye-candy stuff
######
*/

var viewModel;



/*
var globalChart = Highcharts;
function eventChart(event) {
   //console.log('trying to chart :'+event.name+' HTML element is '+document.getElementById(event.name));
   var chart = new Highcharts.Chart({
      chart: {
         renderTo: event.name,
       plotBackgroundColor: null,
       plotBorderWidth: null,
       plotShadow: false,
      },
       title: {
          text: 'Actions for event '+event.name
       },
       tooltip: {
          pointFormat: '', //#FIXME: put Action's parameters here, maybe?
       },
       plotOptions: {
          pie: {
             allowPointSelect: true,
       cursor: 'pointer',
       events: {  //#events? or globalEvents?
          click: function(handle){
             //#here handle.point is directly the KO observable Action
             //console.log(handle.point);
             action = handle.point;
             action.selected = action.removed;
             action.removed(!action.removed());
             viewModel.save();
             //console.log(handle.point);
          }
       },
       dataLabels: {
          enabled: true,
          formatter: function() {
             return '<b>'+ this.point.name +'</b>';
          }
       },
       showInLegend: false,
       selected: true,
          }
               ,series: {
                  showCheckbox: true,
               }
       },
       series: [{
          type: 'pie',
          name: 'Actions',
          data: event.actions()
       }]
   });
}
*/


if(typeof(String.prototype.trim) === 'undefined')
{
   String.prototype.trim = function() 
   {
      return String(this).replace(/^\s+|\s+$/g, '');
   }
}

//call graphic procedures for new Event
function drawEvent(e) {
   //console.log(JSON.stringify(ko.toJS(e.actions), null, 2));
   circles.gNewEvent(e, e.actions());
}


/*
######
# backend part (view model)
######
*/

function Event(data) {
   this.name = data.name; 
   this.actions = ko.observableArray([]);
   this.bindings = ko.observableArray([]);
   this.parameterNames = ko.observableArray([]);
   if(data.hasOwnProperty('bindings')) {
      this.bindings(data.bindings);
   }
   if(data.hasOwnProperty('actions')) {
      this.actions(data.actions);
   }
   if(data.hasOwnProperty('parameterNames')) {
      this.parameterNames(data.parameterNames);
   } else {
      //fill parameterNames using globals when not building globals
      //console.log("Event is "+this.name+" : "+JSON.stringify(ko.toJS(data), null, 2));
      var e = viewModel.getEvent(this.name);
      this.parameterNames(e.parameterNames());
   }
}
function User(data) {
   this.name = data.name; 
}
function Action(data) {
   this.name = data.name; 
   this.type = data.type;
   this.removed = ko.observable(true);
   //this.expectedArgs = ko.observableArray(data.expectedArgs);
   this.expectedArgs = data.expectedArgs;
   if(data.hasOwnProperty('removed')) {
      this.removed(data.removed);
   }
   /*
    * Here we do a transformation of data:
    * expectedArgs comes as a table of simple strings, and we want it to be a table of mapped objects
    * it is usefull to store graphical elements for each expectedArg (hence the additionnal "circle" member)
    */
   if(data.hasOwnProperty('expectedArgs')) {
      if (data.expectedArgs[0] != null && !data.expectedArgs[0].hasOwnProperty('circle')) {
         this.expectedArgs = $.map(data.expectedArgs, function(a) {
            var x = {"arg":a, "circle":null};
            return x;
         });
      }
   } else {
      //expectedArgs is not available in data, get them through globals
      /*
      this.expectedArgs = $.map(viewModel.getGlobalAction(data.name).expectedArgs, function(a) {
         var x = {"arg":a, "circle":null};
         return x;
      });
      */
      this.expectedArgs = $.map(viewModel.getGlobalAction(data.name).expectedArgs,function(a) {return a;});
   }
   //#### here's the specific part for chart UI (on each action) ###
   /*
   if (this.removed) {
      this.selected = false;
   }else {
      this.selected = true;
   }
   */
   //this.y = 100.0*1.0/viewModel.globalActions().length;
}
function Binding(data) {
   this.eventName = data.event;
   this.actionName = data.action;
   this.eventArgument = data.eventArgument;
   this.actionArgument = data.actionArgument;
}
function TaskListViewModel() {
   // Data
   var self = this;
   self.defaultUser = new User({name:'WWWDefault'});
   self.chosenUserName = ko.observable(self.defaultUser);
   self.globalActions = ko.observableArray([]); // #from Globals (=all actions available)
   self.globalEvents = ko.observableArray([]); // #from Globals (=all events available)
   //self.users = ko.observableArray([self.defaultUser]);  //#from Globals (=all users available)
   self.users = ko.observableArray([]);  //#from Globals (=all users available)
   self.userEvents = ko.observableArray([]);
   self.newUserName = ko.observable();

   self.newUser = function() { 
      var alreadyExists = false;
      var user;
      if ( self.newUserName() == undefined ) {
         Notifier.error('Empty user name is not allowed','User Creation');
         return;
      }
      var userName = self.newUserName().trim();
      if ( userName == '') {
         Notifier.error('Empty user name is not allowed','User Creation');
         return;
      }
      if ( userName == 'Globals') {
         Notifier.error('This user name is not allowed (reserved by system)','User Creation');
         return;
      }
      for (usrIdx in self.users()) {
         if( self.users()[usrIdx].name == userName ) {
            alreadyExists = true;
            user = self.users()[usrIdx];
            Notifier.warning('User name already exists','User Creation');
         }
      }
      if (!alreadyExists) {
         user = new User({name:userName});
         self.users.push( user );
         self.saveGlobals();
         Notifier.success('User successfully created','User Creation');
      }
      self.selectUser(user)
   }
   self.selectUser = function(user) {
      if (self.chosenUserName() && self.chosenUserName().name != '') {
            //            self.save(); //#DEBUG: TO REPUT IN PLACE
         }
      self.chosenUserName(user);
      if (self.chosenUserName().name != self.defaultUser.name) {
         self.loadUserPrefs();
      }
      //         self.save(); //#DEBUG 
   };
   self.removeEvent = function(item) { 
      self.userEvents.remove(item);
      self.save();
   };
   self.addEvent = function(item) {
      var alreadyExists = false;
      for (evIdx in self.userEvents()) {
         if( self.userEvents()[evIdx].name == item.name ) {
            alreadyExists = true;
         }
      }
      console.log('addEvent : '+alreadyExists);
      if (!alreadyExists) {
         mappedActions = $.map(self.globalActions(), function(a){ return new Action(a); });
         var e = new Event(item) ; e.actions(mappedActions);
         e.parameterNames(item.parameterNames);
         self.userEvents.push( e );
         drawEvent(e);
         self.save();
      }
   };
   self.removeAction = function(item) { 
      item.removed(true);
      self.save();
   };
   self.addAction = function(item) { 
      item.removed(false);
      self.save();
   };

   self.getEvent = function(name) {
      var res = null;
      for (evIdx in self.globalEvents()) {
         if( self.globalEvents()[evIdx].name == name ) {
            res = self.globalEvents()[evIdx];
         }
      }
      return res;
   }
   self.getUserAction = function(name) {
      var res = null;
      for (evIdx in self.userEvents().actions) {
         if( self.userEvents().actions[evIdx].name == name ) {
            res = self.userEvents()[evIdx];
         }
      }
      return res;
   }

   self.getGlobalAction = function(name) {
      var res = null;
      for (evIdx in self.globalActions()) {
         if( self.globalActions()[evIdx].name == name ) {
            res = self.globalActions()[evIdx];
         }
      }
      return res;
   }

   //Load initial state from server, convert it to instances, then populate self

   $.getJSON('Globals.json', function(allData) {
      var mappedUsers = $.map(allData['users'], function(item) { return new User(item) });
      self.users(mappedUsers);
      var mappedActions = $.map(allData['actionsAvailable'], function(item) { if (!item.hiddenFromUI) {return new Action(item)} });

      self.globalActions(mappedActions);
      var mappedEvents = $.map(allData['eventsAvailable'], function(item) { 
         if (!item.hiddenFromUI) {
            var e = new Event(item);
            e.actions([]);
            e.parameterNames(item.parameterNames);
            return e;
         }
      });
      self.globalEvents(mappedEvents);
   });
   self.saveGlobals = function() {
      $.ajax('save.py', {
         data: {
            meta: ko.toJSON({
               what: 'newUser',
               whom: 'Globals',
            }),
               json: ko.toJSON({
                  users: self.users(),
               actionsAvailable: self.globalActions(),
               eventsAvailable: self.globalEvents(),
               }),
         },
         type: 'POST',
         dataType: 'json',
         success: function(result) {
            ;//alert('message :'+result);
         },
         error: function(result) {
            if (result.statusText == 'OK') {
               alert('error  ' + result);
            }else {
               alert('error  ' + result.statusText);
               document.write(result.responseText);
            }
         },
      });
   };

   //save
   self.save = function() {
      //# now save the new EventProfile on server
      $.ajax('save.py', {
         data: {
            meta: ko.toJSON({
               what: 'EventProfile',
               whom: self.chosenUserName().name,
               whom: self.users()[0].name,
            }),
               json: ko.toJSON(
                        this.userEvents()
                        )
         },
         type: 'POST',
         dataType: 'json',
         success: function(result) {
            ;//alert('message :'+result);
         },
         error: function(result) {
            if (result.statusText == 'OK') {
               alert('error  ' + result);
            }else {
               alert('error  ' + result.statusText);
               document.write(result.responseText);
            }
         },
      });
   };
   self.loadUserPrefs = function() {
      $.ajax({
         type: 'GET',
         url: self.chosenUserName().name+'.json',
         dataType: 'json',
         success: function(allData) {
            var mappedEvents = new Array()
            mappedEvents = $.map(allData, function(item) {
               if (!item.hiddenFromUI) {
                  var e = new Event(item);
                  mappedActions = [];
                  //alert('Event:'+item.name+' has actions:'+JSON.stringify(item.actions));
                  mappedActions = $.map(viewModel.globalActions(), function(a){ if (!a.hiddenFromUI) {return new Action(a);} });
                  //TODO: tag removed actions properly depending on their presence in item.actions
                  e.actions(mappedActions);
                  mappedBindings = $.map(item.bindings, function(b){ return new Binding(b);});
                  e.bindings(mappedBindings);
                  return e;
               }
            });
            if (mappedEvents.length > 0) {
               self.userEvents(mappedEvents);
               for (evIdx in self.userEvents()) {
                  item = self.userEvents()[evIdx];
                  drawEvent(item);
               };
            } else {
               self.userEvents([]);
            }
         },
         error: function(allData) {
            if (self.chosenUserName() != self.defaultUser && allData.status != 200) {
               Notifier.warning('User '+ self.chosenUserName().name + ' does not have a profile yet', 'Preferences loading');
            }
            else if (allData.status != 404) {
               Notifier.error('Error loading profile for '+ self.chosenUserName().name, 'Preferences loading');
               console.log('error processing : '+JSON.stringify(ko.toJS(allData), null, 2));
            }
            self.userEvents([]);
         }
      });
   };
   self.selectUser(self.defaultUser);
}
var logEvent = function(event){
   console.log('seen '+event.name);
}

//$(document).ready(function(){
   viewModel = new TaskListViewModel()
   ko.applyBindings(viewModel);
//}

