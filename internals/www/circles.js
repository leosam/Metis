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
      var c = e.paper.circle(x, y, r).attr({
         fill: "#000",
          stroke:"#aaa",
          "stroke-width": 5,
          "title": action.expectedArgs[a].arg,
      });
      console.log("Circle for : " + action.expectedArgs[a].arg +"("+a+") event:"+e.name);
      c.node.onmouseover = function() {
         //console.log("Action="+action);
         c.animate({fill: "#F00", r:40}, 500, "bounce");
      };
      c.node.onmouseout = function() {
         c.stop().animate({fill: "#000", r:20}, 200);
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
            console.log("WARNING circle not null: "+action.expectedArgs[a].circle+" event: "+e.name+" .. "+action.expectedArgs[a].arg +"("+action.name+")");
         }
         else {
            //we can't affect directly, it affects all instances in all papers....
            //all hail javascript.... :'(
        /*
            action.expectedArgs[a].circle = this.__gActionArgsCircle(
                  e, action, a,
                  action.centerx + x, action.centery + y, 20
                  );
                  */
            action.addCircle(a, this.__gActionArgsCircle(
                  e, action, a,
                  action.centerx + x, action.centery + y, 20
                  ));
            t += Math.PI*2/l;
         }
      }
   }

   Circles.gNewEvent = function(e, actions) { 
      //e is the new event, actions are actions associated to this event, not global
      var mydiv = document.getElementById(e.name);
      var paper = Raphael(mydiv, 520, 400);
      if (e.paper == null) {
         e.paper = paper;
         console.log("creating paper for actions "+actions);
      }
      else {
         console.log("paper not null : "+paper);
      }

      //draw available args to connect from
      this.gEventArgs(e);

      //draw available actions to connect to
      var i=0;
      var j=0;
      for (var idx in actions) {
         this.gActionCircle(e, actions[idx], i, j);
         i++;
         if (i >= 2) {
            i=0;
            j++;
         }
      }

      //draw existing bindings
      for (var b in e.bindings) {
         this.gBinding(e,b);
      }
   }

}(jQuery));
