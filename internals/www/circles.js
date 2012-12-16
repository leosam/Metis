(function($){

   var Circles = window.circles = {};

   Circles.gActionCircle = function(e, action, i, j) {   //draw a circle representing the Action
      action.centerx = (120+40)*i+80;
      action.centery = (120+40)*j+80;
      var c = e.paper.circle(action.centerx, action.centery, 60).attr({
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
         c.animate({fill: "#0000FF", stroke: "#FF0000", "stroke-width": 40, "font-size":240,r:70}, 500, "bounce");
      };
      c.node.onmouseout = function() {
         c.stop().animate({fill: "#0000FF", stroke: "#aaaaaa", "stroke-width": 20, r:60}, 200);
      };
      this.gActionArgs(e,action);
      return c;
   }

   Circles.gBinding = function(e, binding) {  //
      ;//TODO
   }

   Circles.gEventArgs = function(e) {  //
      ;//TODO
   }

   Circles.__gActionArgsCircle = function(e,action, a, x, y, r) {
      //console.log(action.expectedArgs[a].arg);
      return e.paper.circle(x, y, r).attr({
             fill: "#000",
             stroke:"#aaa",
             "stroke-width": 5,
             "title": action.expectedArgs[a].arg,
      });
   }
   Circles.gActionArgs = function(e,action) {
      //console.log("Action="+action);
      var l = action.expectedArgs.length;
      var t = 0;
      for (a in action.expectedArgs) {
         var x = Math.sin(t)*60;
         var y = Math.cos(t)*60;
         //ASSERT action.expectedArgs[a].circle should be null at this point
         //CURRENT PROBLEM : grosse fouge sur les variables de circle, qui sont réutilisées à tout va, même entre deux papers
         console.log(action.expectedArgs[a].circle);
         action.expectedArgs[a].circle = this.__gActionArgsCircle(
             e, action, a,
             action.centerx + x, action.centery + y, 20
         );
         console.log(action.expectedArgs[a].arg);
         action.expectedArgs[a].circle.node.onmouseover = function() {
            console.log("Action="+action);
            action.expectedArgs[a].circle.animate({fill: "#F00", r:40}, 500, "bounce");
         };
         action.expectedArgs[a].circle.node.onmouseout = function() {
            action.expectedArgs[a].circle.stop().animate({fill: "#000", r:20}, 200);
         };
         t += Math.PI*2/l;
      }
   }

   Circles.gNewEvent = function(e, actions) { //e is the new event, actions are all global actions availables in the system
      var mydiv = document.getElementById(e.name);
      var paper = Raphael(mydiv, 520, 400);
      e.paper = e.paper == null ? paper : e.paper;

      //draw available args to connect from
      this.gEventArgs(e);

      //draw available actions to connect to
      var i=0;
      var j=0;
      for (idx in actions) {
         this.gActionCircle(e, actions[idx], i, j);
         i++;
         if (i >= 2) {
            i=0;
            j++;
         }
      }

      //draw existing bindings
      for (b in e.bindings) {
         this.gBinding(e,b);
      }
   }

}(jQuery));
