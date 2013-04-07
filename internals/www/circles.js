(function($){

  var Circles = window.circles = {};

  Circles.gActionCircle = function(e, action, i, j) {   //draw a circle representing the Action
    action.centerx = (120+40)*i+80;
    action.centery = (120+40)*j+100;
    var c = e.paper.circle(action.centerx, action.centery, 60);
    c.attr({
      fill: "#0000FF",
      "fill-opacity": 0.4,
      stroke:"#aaa",
      "stroke-width": 20,
      "text": action.name,
      "text-anchor": "start",
      "font-size": 24,
      "title": action.name,
    });
    c.node.onmouseover = function() {
      c.animate({fill: "#0000FF", stroke: "#FF0000", "stroke-width": 30, "font-size":240,r:60}, 500, "bounce");
    };
    c.node.onmouseout = function() {
      c.stop().animate({fill: "#0000FF", stroke: "#aaaaaa", "stroke-width": 20, r:60}, 200);
    };
    this.gActionArgs(e,action);
    return c;
  }

  Circles.gBinding = function(e, binding) {
    //from all actions, find the one that match
    for ( var actionIdx in e.actions() ) {
      if ( e.actions()[actionIdx].name == binding.actionName ) {
        //then find the argument that is bound
        for (var argIdx in e.actions()[actionIdx].expectedArgs ) {
          if ( e.actions()[actionIdx].expectedArgs[argIdx].arg == binding.actionArgument ){
            //and change the circle's color to green
            circle = e.actions()[actionIdx].expectedArgs[argIdx].circle;
            circle.fillColor = "#0a0";
            circle.attr({ fill: circle.fillColor});
          }
        }
      }
    }
  }

  Circles.gEventArgs = function(e) {  //
    ;//TODO
  }

  Circles.__gActionArgsCircle = function(e,action, a, x, y, r) { //Circle represents the action's Argument
    var c = e.paper.circle(x, y, r);
    c.fillColor = "#000";
    c.attr({
      fill: c.fillColor,
      stroke:"#aaa",
      "stroke-width": 5,
      "title": action.expectedArgs[a].arg,
    });
    console.log("Circle for : " + action.expectedArgs[a].arg +"("+a+") event:"+e.name);
    c.node.onmouseover = function() {
      //console.log("Action="+action);
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
        //console.log("WARNING adding circle: "+action.expectedArgs[a].circle+" event: "+e.name+" .. "+action.expectedArgs[a].arg +"("+action.name+")");
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
    var mydiv = document.getElementById(e.name);
    var paper = Raphael(mydiv, 320, 400);
    if (e.paper == null) {
      e.paper = paper;
      console.log("creating paper for actions "+e.actions() );
    }
    else {
      console.log("paper not null : "+paper);
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
