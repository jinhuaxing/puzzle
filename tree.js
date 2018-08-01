// p5.js script for L-system tree generator

function generate(axiom, rules) {
  var r = [];
  Array.from(axiom).forEach(function (a) {
    var rule = rules[a];
    if (rule) {
      r = r.concat(Array.from(rule));
    } else {
      r.push(a);
    }
  });
  return r;
}

function generateN(n, axiom, rules) {
  var a1 = axiom;
  for (var i = 0; i < n; i++) {
    a1 = generate(a1, rules);
  }
  return a1;
}

function drawShape(x, y, intialAngle, turtle, length, deltaAngle) {
  const forwardCommands = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const colorCommands = "0123456789";
  var x1 = x;
  var y1 = y;
  var stack = [];
  var ca = [color("rgba(140, 80, 60, 1)"), color("rgba(24, 180, 24, 1)"), color("rgba(48, 220, 48, 0.5)")];
  var currentColor = "0";
  stroke(ca[parseInt(currentColor)]);
  angle = intialAngle;
  var weight = 15.0;
  //var weight = 1.0;
  strokeWeight(weight);
  for (var i = 0; i < turtle.length; i++) {
    var cmd = turtle[i];
    if (forwardCommands.includes(cmd)) {
      x2 = x1 + length*cos(angle);
      y2 = y1 + length*sin(angle);
      line(x1, y1, x2, y2);
      x1 = x2;
      y1 = y2;
    } else if (cmd === "+") {
      angle += deltaAngle;
    } else if (cmd === "-") {
      angle -= deltaAngle;
    } else if (cmd === "f") {
      x1 = x1 + length*cos(angle);
      y1 = y1 + length*sin(angle);        
    } else if (cmd === "[") {
      stack.push({"x1":x1, "y1":y1, "angle": angle, "currentColor": currentColor, "weight":weight});
    } else if (cmd === "s") {
      weight = weight / 2.0 * 1.3;
      strokeWeight(weight);      
    } else if (cmd === "t") {
      weight = weight / 2.0 * 1.95;
      strokeWeight(weight);      
    }
    else if (cmd === "]") {
      var p = stack.pop();
      x1 = p.x1;
      y1 = p.y1;
      angle = p.angle;
      currentColor = p.currentColor;
      stroke(ca[parseInt(currentColor)]);
      weight = p.weight;
      strokeWeight(weight);
    } else if (colorCommands.includes(cmd)) {
      currentColor = cmd;
      stroke(ca[parseInt(currentColor)]);
    } else {
      console.log("Unknown command: " + cmd);
    }
  }
}

function setup() {
  
  var rules = [];

  //var axiom = "F-F-F-F", startX = 300, startY = 600, intialAngle = 0, lineSize = 4, angle = PI/2, interation = 3;
  //rules["F"] = "F-F+F+FF-F-F+F";
  
  //var axiom = "-F", startX = 300, startY = 600, intialAngle = 0, lineSize = 4, angle = PI/2, interation = 4;
  //rules["F"] = "F+F-F-F+F";
  
  //var axiom = "F-F-F-F", startX = 300, startY = 600, intialAngle = 0, lineSize = 4, angle = PI/2, interation = 2;
  //rules["F"] = "F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF";
  //rules["f"] = "ffffff";
  
  //var w = "-F";
  //var pF = "F+G+";
  //var pf;
  //var pG = "-F-G";
  
  //var w = "F";
  //var pF = "G+F+G";
  //var pf;
  //var pG = "F-G-F";
  
  //var axiom = "F", startX = 100, startY = 300, intialAngle = PI/2, lineSize = 5, angle = PI/2, interation = 5;
  //rules["F"] = "F+G++G-F--FF-G+";
  //rules["G"] = "-F+GG++G+F--F-G";
  
  //var axiom = "F", startX = 300, startY = 600, intialAngle = -PI / 2, lineSize = 8, angle = PI / 9, interation = 5;
  //rules["F"] = "F[+F]F[-F][F]";
  
  var axiom = "F", startX = 100, startY = 580, intialAngle = -PI/2, lineSize = 10, angle = PI/8, interation = 3;
  rules["F"] = "t0FF-[s0-F+F+F]+[ss0+F-F-F]";
  
  createCanvas(800, 600);
  //colorMode(HSL);
  background(255, 255, 255);
	noFill();
  
  //drawShape(startX, startY, intialAngle, generateN(interation, axiom, rules), lineSize, angle)
  // for tree
  drawShape(50, startY, intialAngle, generateN(1, axiom, rules), lineSize, angle);  
  drawShape(150, startY, intialAngle, generateN(2, axiom, rules), lineSize, angle);  
  drawShape(300, startY, intialAngle, generateN(3, axiom, rules), lineSize, angle);
  drawShape(600, startY, intialAngle, generateN(4, axiom, rules), lineSize, angle);
  
  noLoop();
}
