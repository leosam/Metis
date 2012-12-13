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
      /*
      c.node.onmouseover = function() {
         c.animate({fill: "#0000FF", stroke: "#FF0000", "stroke-width": 80}, 500, "bounce");
      };
      c.node.onmouseout = function() {
         c.stop().animate({fill: "#0000FF", stroke: "#aaaaaa", "stroke-width": 20, r:60}, 200);
      };
      */
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
         return e.paper.circle(x, y, r).attr({
            fill: "#000",
            stroke:"#aaa",
            "stroke-width": 5,
            "title": action.expectedArgs()[a],
         });
   }
   Circles.gActionArgs = function(e,action) {
      var l = action.expectedArgs().length;
      var t = 0;
      for (a in action.expectedArgs()) {
         var x = Math.sin(t)*60;
         var y = Math.cos(t)*60;
         /*
          * i don't understand javascript...this works fine (but useless as c is overwritten with each pass of the loop) :
         c = this.__gActionArgsCircle(

          * and this just doesn't work (TypeError: action.expectedArgs()[a].circle is undefined) when executing next 'mouseover' line
          * parce que action.expectedArgs()[a] est une string et pas un objet...
         action.expectedArgs()[a].circle = this.__gActionArgsCircle(
         */
               e, action, a,
               action.centerx + x, action.centery + y, 20
               );
         action.expectedArgs()[a].circle.node.onmouseover = function() {
            action.expectedArgs()[a].circle.animate({fill: "#00F", r:50}, 500, "bounce");
         };
         action.expectedArgs()[a].circle.node.onmouseout = function() {
            action.expectedArgs()[a].circle.stop().animate({fill: "#000", r:20}, 200);
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
