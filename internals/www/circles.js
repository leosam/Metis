(function($){

  var Circles = window.circles = {};

  Circles.gActionCircle = function(e, action, i, j) {   //draw a circle representing the Action
    action.centerx = (120+40)*i+80;
    action.centery = (120+40)*j+100;

    //FIXME: handle possible text erasing (if it's ever needed?)
    e.actionPaper.text(action.centerx,action.centery,action.name).attr({
      font:"15px Helvetica", 
      opacity: 1,
    });

    var c = e.actionPaper.circle(action.centerx, action.centery, 60);
    var commonAttr = {
      fill: "#0000FF",
      "fill-opacity": 0.2,
      stroke:"#ddd",
      "stroke-width": 10,
      "text": action.name,
      "text-anchor": "start",
      "font-size": 24,
      "title": action.name,
    };
    c.attr(commonAttr);
    c.node.onmouseover = function() {
      c.animate({fill: "#0000FF", stroke: "#FF0000", "stroke-width": 15, "font-size":240,r:60}, 500, "bounce");
    };
    c.node.onmouseout = function() {
      var myAttr = commonAttr;
      myAttr['r'] = 60;
      c.stop().animate(myAttr, 200);
    };
    this.gActionArgs(e,action);
    return c;
  }

  Circles.gBinding = function(e, binding) { //change appearance of bonded drawings
    if(! binding.hasOwnProperty('actionCircle')) {
      //from all actions, find the one that match the binding
      for ( var actionIdx in e.actions() ) {
        if ( e.actions()[actionIdx].name == binding.actionName ) {
          //then find the argument that is bound
          for (var argIdx in e.actions()[actionIdx].expectedArgs ) {
            if ( e.actions()[actionIdx].expectedArgs[argIdx].arg == binding.actionArgument ){
              //and change the circle's color to green
              circle = e.actions()[actionIdx].expectedArgs[argIdx].circle;
              circle.fillColor = "#0a0";
              circle.attr({ fill: circle.fillColor});
              binding.actionCircle = circle;
            }
          }
        }
      }
    }
    else {
      binding.actionCircle.fillColor = "#0a0";
      binding.actionCircle.attr({ fill: circle.fillColor});
    }

    if(! binding.hasOwnProperty('eventRect')) {
      //find the event param that is bound
      for (var paramIdx in e.parameterNames() ) {
        if ( e.parameterNames()[paramIdx].arg == binding.eventArgument ){
          //and change the rect's color to green
          rect = e.parameterNames()[paramIdx].rect;
          rect.fillColor = "#0a0";
          rect.attr({ fill: rect.fillColor});
          binding.eventRect = rect;
        }
      }
    }
    else {
      binding.eventRect.fillColor = "#0a0";
      binding.eventRect.attr({ fill: rect.fillColor});
    }
  }

  Circles.gEventArg = function(e, param, i, j, n) {   //draw a rect representing event's param
    var eventArg = {};
    eventArg.name = param.arg;
    eventArg.x = 20*i+50;
    eventArg.y = 30*j+(400-30*n)/2;

    eventArg.textDrawn = e.eventPaper.text(eventArg.x,eventArg.y,eventArg.name).attr({
      font:"15px Helvetica", 
      opacity: 1,
    });

    var wsize = eventArg.name.length * 11;
    var hsize = 22;
    var r = e.eventPaper.rect(eventArg.x - wsize/2, eventArg.y - hsize/2, wsize, hsize, 30);
    r.fillColor = "#0000FF";
    var commonAttr = {
      fill: r.fillColor,
      "fill-opacity": 0.2,
      stroke:"#add",
      "stroke-width": 1,
      "text": eventArg.name,
      "text-anchor": "start",
      "font-size": 24,
      "title": eventArg.name,
    };
    r.attr(commonAttr);
    r.node.onmouseover = function() {
      r.animate({stroke: "#FF0000", "stroke-width": 5}, 500, "bounce");
    };
    r.node.onmouseout = function() {
      var myattr = commonAttr;
      myattr['fill'] = r.fillColor;
      r.stop().animate(myattr, 200);
    };

    eventArg.rect = r;
    param.rect = r;
    return eventArg;
  }

  Circles.gEventArgs = function(e) {
    var i=0;
    for (var idx in e.parameterNames()) {
      //problem: parameterNames are plain names
      //TODO: make them objects so that we can keep a reference on their drawing
      this.gEventArg(e, e.parameterNames()[idx], 0, i, e.parameterNames().length);
      i++;
    }
  }

  Circles.__gActionArgsCircle = function(e,action, a, x, y, r) { //Circle represents the action's Argument
    var text = e.actionPaper.text(x,y, action.expectedArgs[a].arg[0]).attr({
      font:"15px Helvetica", 
      opacity: 1,
    });

    var c = e.actionPaper.circle(x, y, r);
    c.fillColor = "#c88";
    c.attr({
      fill: c.fillColor,
      "fill-opacity": 0.4,
      stroke:"#ddd",
      "stroke-width": 5,
      "title": action.expectedArgs[a].arg,
    });
    c.mycaption = text;
    c.node.onmouseover = function() {
      c.animate({fill: c.fillColor, r:30}, 500, "bounce");
    };
    c.node.onmouseout = function() {
      c.stop().animate({fill: c.fillColor, r:20}, 200);
    };
    return c;
  }

  Circles.gActionArgs = function(e,action) {
    //console.log("Action="+action);
    var l = action.expectedArgs.length;
    var t = 0;
    for (var a in action.expectedArgs) {
      var x = Math.sin(t)*60;
      var y = Math.cos(t)*60;
      //ASSERT action.expectedArgs[a].circle should be null at this point
      if(action.expectedArgs[a].circle != null) {
        console.log("WARNING circle not null (BUT SHOULD BE): "+action.expectedArgs[a].circle+" event: "+e.name+" .. "+action.expectedArgs[a].arg +"("+action.name+")");
      }
      else {
        //beware the scope of circle, we only want to affect ours
        action.addCircle(a, this.__gActionArgsCircle(
              e, action, a,
              action.centerx + x, action.centery + y, 20
              ));
        t += Math.PI*2/l;
      }
    }
  }

  Circles.gNewEvent = function(e) { 
    //e is the new event, actions are actions associated to this event, not global
    var myEventDiv = document.getElementById(e.name+'event');
    var myActionDiv = document.getElementById(e.name+'actions');
    //TODO: manage papers position and size nicely
    var eventPaper = Raphael(myEventDiv, 100, 400);
    if (e.eventPaper == null) {
      e.eventPaper = eventPaper;
      console.log("creating event paper for event params "+e.parameterNames() );
    }
    else {
      console.log("[WARNING] event paper not null : "+eventPaper);
    }

    var actionPaper = Raphael(myActionDiv, 420, 400);
    if (e.actionPaper == null) {
      e.actionPaper = actionPaper;
      console.log("creating paper for actions "+e.actions() );
    }
    else {
      console.log("[WARNING] action paper not null : "+actionPaper);
    }

    //draw available args to connect from
    this.gEventArgs(e);

    //draw available actions to connect to
    var i=0;
    var j=0;
    for (var idx in e.actions()) {
      this.gActionCircle(e, e.actions()[idx], i, j);
      i++;
      if (i >= 2) {
        i=0;
        j++;
      }
    }

    //draw existing bindings
    for (var b in e.bindings()) {
      this.gBinding(e,e.bindings()[b]);
    }
  }

}(jQuery));
