(function($){

  var Circles = window.circles = {};
  var EventsToActions = {};
  EventsToActions.x = 120;
  EventsToActions.y = 0;

  Circles.gActionCircle = function(e, action, i, j) {   //draw a circle representing the Action
    action.centerx = (120+40)*i+80;
    action.centery = (120+40)*j+100;

    //FIXME: handle possible text erasing (if it's ever needed?)
    var t = e.actionPaper.text(action.centerx,action.centery,action.name).attr({
      font:"15px Helvetica", 
      opacity: 1,
    });
    this.transformAction(t);

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
    this.transformAction(c);
    c.node.onmouseover = function() {
      c.animate({fill: "#0000FF", stroke: "#aaf", "stroke-width": 15, "font-size":240,r:60}, 500, "bounce");
    };
    c.node.onmouseout = function() {
      var myAttr = commonAttr;
      myAttr['r'] = 60;
      c.stop().animate(myAttr, 200);
    };
    this.gActionArgs(e,action);
    return c;
  }

  Circles.BindTogether = function(e, binding, circle, rect) {
    originx = rect.attrs.x + rect.attrs.width;
    originy = rect.attrs.y + rect.attrs.height/2;
    destx = circle.attrs.cx + EventsToActions.x;
    desty = circle.attrs.cy + EventsToActions.y;
    var s = "M"+originx+","+originy+"Q"+originx+","+originy+","+destx+","+desty;

    var path = e.eventPaper.path(s);
    this.transformEvent(path);
    var commonAttr = {
      //fill: "#0000FF",
      //"fill-opacity": 0.2,
      stroke:"#f00",
      "text": "binding",
      //"text-anchor": "start",
      //"font-size": 24,
      "stroke-width": 5,
      "title": "binding",
    };
    path.attr(commonAttr);
    path.s = s;
    return path;
  }

  Circles.gBinding = function(e, binding) { 
    if (binding.actionArgument == "ignored" || binding.eventArgument == "ignored") {
      //ignore binding with at least one "ignored" argument
      //shall we really do that? (maybe we should change their appearance as well?)
      console.log("binding: "+binding.eventName+" and "+binding.actionName+" with "+binding.eventArgument+" and "+binding.actionArgument);
    } else {
      /*
       * change appearance of bonded drawings
       */
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

      /*
       * Create binding representation
       */
      console.log("seen binding between"+binding.actionName+"("+binding.actionArgument+") and"+binding.eventName+"("+binding.eventArgument+")");
      binding.drawing = this.BindTogether(e, binding, binding.actionCircle, binding.eventRect);
      binding.drawing.hide(); //we show it when appropriate item is selected, or hovered on
      if (binding.actionCircle.bindings == undefined) 
        binding.actionCircle.bindings = [];
      if (binding.eventRect.bindings == undefined) 
        binding.eventRect.bindings = [];
      binding.eventRect.bindings.push(binding.drawing);
      binding.actionCircle.bindings.push(binding.drawing);
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
    this.transformEvent(eventArg.textDrawn);

    var wsize = eventArg.name.length * 11;
    var hsize = 22;
    var r = e.eventPaper.rect(eventArg.x - wsize/2, eventArg.y - hsize/2, wsize, hsize, 30);
    this.transformEvent(r);
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
      for (i in r.bindings) {
        r.bindings[i].show();
      }
      r.toFront();
    };
    r.node.onmouseout = function() {
      var myattr = commonAttr;
      myattr['fill'] = r.fillColor;
      r.stop().animate(myattr, 200);
      for (i in r.bindings) {
        r.bindings[i].hide();
      }
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
    this.transformAction(text);

    var c = e.actionPaper.circle(x, y, r);
    c.fillColor = "#c88";
    c.attr({
      fill: c.fillColor,
      "fill-opacity": 0.4,
      stroke:"#ddd",
      "stroke-width": 5,
      "title": action.expectedArgs[a].arg,
    });
    this.transformAction(c);
    c.mycaption = text;
    c.node.onmouseover = function() {
      c.animate({fill: c.fillColor, r:30}, 500, "bounce");
      for (i in c.bindings) {
        c.bindings[i].show();
      }
      c.toFront();
    };
    c.node.onmouseout = function() {
      c.stop().animate({fill: c.fillColor, r:20}, 200);
      for (i in c.bindings) {
        c.bindings[i].hide();
      }
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

  Circles.transformEvent = function(e) {
    e.transform("");
  }
  Circles.transformAction = function(a) {
    a.transform("t"+EventsToActions.x+","+EventsToActions.y);
  }

  Circles.gNewEvent = function(e) { 
    //e is the new event, actions are actions associated to this event, not global
    var myEventDiv = document.getElementById(e.name+'event');
    var myActionDiv = document.getElementById(e.name+'actions');
    //TODO: adjust size nicely depending on e.actions().length
    var eventPaper = Raphael(myEventDiv, 450, 350);
    
    if (e.eventPaper == null) {
      e.eventPaper = eventPaper;
      console.log("creating event paper for event "+e.name );
    }
    else {
      console.log("[WARNING] event paper not null : "+eventPaper);
    }

    //var actionPaper = Raphael(myActionDiv, 420, 400);
    var actionPaper = eventPaper;
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
