// Data source file
var dataFile = "wine_quality.csv"

// Setting window size for each svg
var w=800, h=600;
var padding = 60;
var symbolSize = 50;
var numTicks = 10;
var legendSize = 50;

d3.csv(dataFile, function(data) {
  // Changing from string to number
  data.forEach(function(d) {
    d.pH = +d.pH;
    d.free_sulfur_dioxide = +d.free_sulfur_dioxide;
    d.quality = +d.quality;
    d.residual_sugar = +d.residual_sugar;
    d.chlorides = +d.chlorides;
    d.total_sulfur_dioxide = +d.total_sulfur_dioxide;
    d.Density = +d.Density;
    d.sulphates = +d.sulphates;
    d.alcohol = +d.alcohol;
  });

  //Set up data for graphs
  var graph1Good = [];  // [Alcohol, pH] data for graph1
  var graph1Bad = [];
  var graph2Good = [];  // [Residual sugar, pH] data for graph2
  var graph2Bad = [];
  var graph3Good = []; // [Alcohol, pH] data for scaling graph3
  var graph3Bad = [];
  var graph3Product = [];
  var graph45Good = []; // [pH, Sulphates] data for graph4 $ 5
  var graph45Bad = [];

  data.forEach(function(d) {
    if (d.quality>5) {
      graph1Good.push([d.alcohol, d.pH]);
      graph2Good.push([d.residual_sugar, d.pH]);
      graph3Good.push([d.alcohol, d.pH]);
      graph45Good.push([d.pH, d.sulphates]);
    }
    else {
      graph1Bad.push([d.alcohol, d.pH]);
      graph2Bad.push([d.residual_sugar, d.pH]);
      graph3Bad.push([d.alcohol, d.pH]);
      graph45Bad.push([d.pH, d.sulphates]);
    }
    graph3Product.push(d.alcohol * d.pH)
  });

  var svg1 = plotGoodBad(graph1Good, graph1Bad, "pH vs. Alcohol");
  var svg2 = plotGoodBad(graph2Good, graph2Bad, "pH vs. Residual sugar");
  var svg3 = plotScale(graph3Good, graph3Bad, graph3Product, "pH vs. Alcohol (scaled symbols)")
  var svg4 = plotSqrt(graph45Good, graph45Bad, "Sulphates vs. pH (square-root-scaled)")
  var svg5 = plotLog(graph45Good, graph45Bad, "Sulphates vs. pH (log-scaled)")
});

function plotGoodBad(goodData, badData, title=null) {

  var x_max = Math.max( d3.max(badData, function(d) { return d[0]; }),
                        d3.max(goodData, function(d) { return d[0]; }) );
  var y_max = Math.max( d3.max(badData, function(d) { return d[1]; }),
                        d3.max(goodData, function(d) { return d[1]; }) );

  //Create SVG element
  var svg = d3.select("body")
              .append("svg")
              .attr("width", w)
              .attr("height", h);

  var xScale = d3.scale.linear()
             .domain([0, x_max])
             .range([padding, w-padding*2]);
  var yScale = d3.scale.linear()
             .domain([0, y_max])
             .range([h-padding, padding]);

  var crossSize = d3.svg.symbol().type('cross')
  .size(symbolSize);

  var cirSize = d3.svg.symbol().type('circle')
  .size(symbolSize);

  //Circles
  svg.append('g').selectAll('path')
    .data(badData)
    .enter()
    .append('path')
    .attr('d',cirSize)
    .attr('fill', "none")
    .attr('stroke', "red")
    .attr('stroke-width',1)
    .attr('transform',function(d,i){ return "translate("+xScale(d[0])+","+yScale(d[1])+")"; });

  //Crosses
  svg.append('g').selectAll('path')
    .data(goodData)
    .enter()
    .append('path')
    .attr('d',crossSize)
    .attr('fill', "none")
    .attr('stroke', "blue")
    .attr('stroke-width',1)
    .attr('transform',function(d,i){ return "translate("+xScale(d[0])+","+yScale(d[1])+")"; });

  //Define X axis
  var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient("bottom")
          .ticks(numTicks);

  //Create X axis
  svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + (h - padding) + ")")
    .call(xAxis);

  //Define Y axis
  var yAxis = d3.svg.axis()
          .scale(yScale)
          .orient("left")
          .ticks(numTicks);

  //Create Y axis
  svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(" + padding + ",0)")
      .call(yAxis);

  //Add title
  if (title != null){
    svg.append("svg:text")
      .attr("class", "title")
     .attr("x", w/2 - padding)
     .attr("y", padding)
     .attr("text-align", "center")
     .text(title);
  }

  //Add legend
  var legend = svg.append("g")
    .attr("class", "legend")
    .attr("x", w - padding)
    .attr("y", padding)
    .attr("height", 100)
    .attr("width", 100);

  //Add cross
  legend.append('g')
    .append('path')
    .attr('d',crossSize)
    .attr('fill', "none")
    .attr('stroke', "blue")
    .attr('stroke-width',1)
    .attr('transform', "translate("+ (w-3*padding) +","+ padding/3 +")");

  legend.append('g')
    .append('svg:text')
    .attr("x", w - 3*padding + padding/20)
    .attr("y", padding/3 + padding/20)
    .attr("text-align", "center")
    .attr("text-anchor", "center")
    .text("Good")

  //Add circle
  legend.append('g')
    .append('path')
    .attr('d',cirSize)
    .attr('fill', "none")
    .attr('stroke', "red")
    .attr('stroke-width',1)
    .attr('transform', "translate("+ (w-3*padding) +","+ 2*padding/3 +")");

  legend.append('g')
    .append('svg:text')
    .attr("x", w - 3*padding + padding/20)
    .attr("y", 2*padding/3 + padding/20)
    .attr("text-align", "center")
    .attr("text-anchor", "center")
    .text("Bad")


  return svg;
}

function plotScale(goodData, badData, prodData, title=null) {

  var x_max = Math.max( d3.max(badData, function(d) { return d[0]; }),
                        d3.max(goodData, function(d) { return d[0]; }) );
  var y_max = Math.max( d3.max(badData, function(d) { return d[1]; }),
                        d3.max(goodData, function(d) { return d[1]; }) );
  var prod_max = d3.max(prodData);
  var prod_min = d3.min(prodData);

  //Create SVG element
  var svg = d3.select("body")
              .append("svg")
              .attr("width", w)
              .attr("height", h);

  var xScale = d3.scale.linear()
             .domain([0, x_max])
             .range([padding, w-padding*2]);
  var yScale = d3.scale.linear()
             .domain([0, y_max])
             .range([h-padding, padding]);
  var sScale = d3.scale.linear()
                     .domain([prod_min, prod_max])
                     .range([100, 1]);

  var crossSize = d3.svg.symbol().type('cross')
  .size(function(d){ return sScale(d); });

  var cirSize = d3.svg.symbol().type('circle')
  .size(function(d){ return sScale(d); });

  //Circles
  svg.append('g').selectAll('path')
    .data(badData)
    .enter()
    .append('path')
    .attr('d',function(d,i) { return cirSize(prodData[i]); })
    .attr('fill', "none")
    .attr('stroke', "red")
    .attr('stroke-width',1)
    .attr('transform',function(d,i){ return "translate("+xScale(d[0])+","+yScale(d[1])+")"; });

  //Crosses
  svg.append('g').selectAll('path')
    .data(goodData)
    .enter()
    .append('path')
    .attr('d',function(d,i) { return crossSize(prodData[i]); })
    .attr('fill', "none")
    .attr('stroke', "blue")
    .attr('stroke-width',1)
    .attr('transform',function(d,i){ return "translate("+xScale(d[0])+","+yScale(d[1])+")"; });

  //Define X axis
  var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient("bottom")
          .ticks(numTicks);

  //Create X axis
  svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + (h - padding) + ")")
    .call(xAxis);

  //Define Y axis
  var yAxis = d3.svg.axis()
          .scale(yScale)
          .orient("left")
          .ticks(numTicks);

  //Create Y axis
  svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(" + padding + ",0)")
      .call(yAxis);

  //Add title
  if (title != null){
    svg.append("svg:text")
      .attr("class", "title")
     .attr("x", w/2 - padding)
     .attr("y", padding)
     .attr("text-align", "center")
     .text(title);
  }

  //Add legend
  var legend = svg.append("g")
    .attr("class", "legend")
    .attr("x", w - 2*padding)
    .attr("y", padding)
    .attr("height", 100)
    .attr("width", 100);

  //Add cross
  var crossLegendSize = d3.svg.symbol().type('cross')
  .size(legendSize);
  legend.append('g')
    .append('path')
    .attr('d',crossLegendSize)
    .attr('fill', "none")
    .attr('stroke', "blue")
    .attr('stroke-width',1)
    .attr('transform', "translate("+ (w-3*padding) +","+ padding/3 +")");

  legend.append('g')
    .append('svg:text')
    .attr("x", w - 3*padding + padding/20)
    .attr("y", padding/3 + padding/20)
    .attr("text-align", "center")
    .attr("text-anchor", "center")
    .text("Good")

  //Add circle
  var cirLegendSize = d3.svg.symbol().type('circle')
  .size(legendSize);

  legend.append('g')
    .append('path')
    .attr('d',cirLegendSize)
    .attr('fill', "none")
    .attr('stroke', "red")
    .attr('stroke-width',1)
    .attr('transform', "translate("+ (w-3*padding) +","+ 2*padding/3 +")");

  legend.append('g')
    .append('svg:text')
    .attr("x", w - 3*padding + padding/20)
    .attr("y", 2*padding/3 + padding/20)
    .attr("text-align", "center")
    .attr("text-anchor", "center")
    .text("Bad")


  return svg;
}

function plotSqrt(goodData, badData, title=null) {

  var x_max = Math.max( d3.max(badData, function(d) { return d[0]; }),
                        d3.max(goodData, function(d) { return d[0]; }) );
  var y_max = Math.max( d3.max(badData, function(d) { return d[1]; }),
                        d3.max(goodData, function(d) { return d[1]; }) );
  var y_min = Math.max( d3.min(badData, function(d) { return d[1]; }),
                        d3.min(goodData, function(d) { return d[1]; }) );

  //Create SVG element
  var svg = d3.select("body")
              .append("svg")
              .attr("width", w)
              .attr("height", h);

  var xScale = d3.scale.linear()
             .domain([0, x_max])
             .range([padding, w-padding*2]);
  var yScale = d3.scale.sqrt()
             .domain([y_min, y_max])
             .range([h-padding, padding]);

  var crossSize = d3.svg.symbol().type('cross')
  .size(symbolSize);

  var cirSize = d3.svg.symbol().type('circle')
  .size(symbolSize);

  //Circles
  svg.append('g').selectAll('path')
    .data(badData)
    .enter()
    .append('path')
    .attr('d',cirSize)
    .attr('fill', "none")
    .attr('stroke', "red")
    .attr('stroke-width',1)
    .attr('transform',function(d,i){ return "translate("+xScale(d[0])+","+yScale(d[1])+")"; });

  //Crosses
  svg.append('g').selectAll('path')
    .data(goodData)
    .enter()
    .append('path')
    .attr('d',crossSize)
    .attr('fill', "none")
    .attr('stroke', "blue")
    .attr('stroke-width',1)
    .attr('transform',function(d,i){ return "translate("+xScale(d[0])+","+yScale(d[1])+")"; });

  //Define X axis
  var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient("bottom")
          .ticks(numTicks);

  //Create X axis
  svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + (h - padding) + ")")
    .call(xAxis);

  //Define Y axis
  var yAxis = d3.svg.axis()
          .scale(yScale)
          .orient("left")
          .ticks(numTicks);

  //Create Y axis
  svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(" + padding + ",0)")
      .call(yAxis);

  //Add title
  if (title != null){
    svg.append("svg:text")
      .attr("class", "title")
     .attr("x", w/2 - 2*padding)
     .attr("y", padding)
     .attr("text-align", "center")
     .attr("text-anchor", "center")
     .text(title);
  }

  //Add legend
  var legend = svg.append("g")
    .attr("class", "legend")
    .attr("x", w - padding)
    .attr("y", padding)
    .attr("height", 100)
    .attr("width", 100);

  //Add cross
  legend.append('g')
    .append('path')
    .attr('d',crossSize)
    .attr('fill', "none")
    .attr('stroke', "blue")
    .attr('stroke-width',1)
    .attr('transform', "translate("+ (w-3*padding) +","+ padding/3 +")");

  legend.append('g')
    .append('svg:text')
    .attr("x", w - 3*padding + padding/20)
    .attr("y", padding/3 + padding/20)
    .attr("text-align", "center")
    .attr("text-anchor", "center")
    .text("Good")

  //Add circle
  legend.append('g')
    .append('path')
    .attr('d',cirSize)
    .attr('fill', "none")
    .attr('stroke', "red")
    .attr('stroke-width',1)
    .attr('transform', "translate("+ (w-3*padding) +","+ 2*padding/3 +")");

  legend.append('g')
    .append('svg:text')
    .attr("x", w - 3*padding + padding/20)
    .attr("y", 2*padding/3 + padding/20)
    .attr("text-align", "center")
    .attr("text-anchor", "center")
    .text("Bad")


  return svg;
}

function plotLog(goodData, badData, title=null) {

  var x_max = Math.max( d3.max(badData, function(d) { return d[0]; }),
                        d3.max(goodData, function(d) { return d[0]; }) );
  var y_max = Math.max( d3.max(badData, function(d) { return d[1]; }),
                        d3.max(goodData, function(d) { return d[1]; }) );
  var y_min = Math.max( d3.min(badData, function(d) { return d[1]; }),
                        d3.min(goodData, function(d) { return d[1]; }) );

  //Create SVG element
  var svg = d3.select("body")
              .append("svg")
              .attr("width", w)
              .attr("height", h);

  var xScale = d3.scale.linear()
             .domain([0, x_max])
             .range([padding, w-padding*2]);
  var yScale = d3.scale.log()
             .domain([y_min, y_max])
             .range([h-padding, padding]);

  var crossSize = d3.svg.symbol().type('cross')
  .size(symbolSize);

  var cirSize = d3.svg.symbol().type('circle')
  .size(symbolSize);

  //Circles
  svg.append('g').selectAll('path')
    .data(badData)
    .enter()
    .append('path')
    .attr('d',cirSize)
    .attr('fill', "none")
    .attr('stroke', "red")
    .attr('stroke-width',1)
    .attr('transform',function(d,i){ return "translate("+xScale(d[0])+","+yScale(d[1])+")"; });

  //Crosses
  svg.append('g').selectAll('path')
    .data(goodData)
    .enter()
    .append('path')
    .attr('d',crossSize)
    .attr('fill', "none")
    .attr('stroke', "blue")
    .attr('stroke-width',1)
    .attr('transform',function(d,i){ return "translate("+xScale(d[0])+","+yScale(d[1])+")"; });

  //Define X axis
  var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient("bottom")
          .ticks(numTicks);

  //Create X axis
  svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + (h - padding) + ")")
    .call(xAxis);

  //Define Y axis
  var yAxis = d3.svg.axis()
          .scale(yScale)
          .orient("left")
          .ticks(numTicks);

  //Create Y axis
  svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(" + padding + ",0)")
      .call(yAxis);

  //Add title
  if (title != null){
    svg.append("svg:text")
      .attr("class", "title")
     .attr("x", w/2 - 2*padding)
     .attr("y", padding)
     .attr("text-align", "center")
     .attr("text-anchor", "center")
     .text(title);
  }

  //Add legend
  var legend = svg.append("g")
    .attr("class", "legend")
    .attr("x", w - padding)
    .attr("y", padding)
    .attr("height", 100)
    .attr("width", 100);

  //Add cross
  legend.append('g')
    .append('path')
    .attr('d',crossSize)
    .attr('fill', "none")
    .attr('stroke', "blue")
    .attr('stroke-width',1)
    .attr('transform', "translate("+ (w-3*padding) +","+ padding/3 +")");

  legend.append('g')
    .append('svg:text')
    .attr("x", w - 3*padding + padding/20)
    .attr("y", padding/3 + padding/20)
    .attr("text-align", "center")
    .attr("text-anchor", "center")
    .text("Good")

  //Add circle
  legend.append('g')
    .append('path')
    .attr('d',cirSize)
    .attr('fill', "none")
    .attr('stroke', "red")
    .attr('stroke-width',1)
    .attr('transform', "translate("+ (w-3*padding) +","+ 2*padding/3 +")");

  legend.append('g')
    .append('svg:text')
    .attr("x", w - 3*padding + padding/20)
    .attr("y", 2*padding/3 + padding/20)
    .attr("text-align", "center")
    .attr("text-anchor", "center")
    .text("Bad")


  return svg;
}



