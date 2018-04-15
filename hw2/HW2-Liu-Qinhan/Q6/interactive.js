// Data
var data = [
{franchise:'Harry Potter', revenue: {1:974, 2:878, 3:796, 4:896, 5:942, 6:935, 7:960, 8:1341 }},
{franchise:'Transformers', revenue: {1:708, 2:836, 3:1123, 4:1104, 5:603 }},
{franchise:'Mission Impossible', revenue: {1:457, 2:549, 3:397, 4:694, 5:700 }},
{franchise:'Fast and the Furious', revenue: {1:206, 2:236, 3:363, 4:363, 5:629, 6:789, 7:1516, 8:1237 }},
{franchise:'Hunger Games', revenue: {1:677, 2:864, 3:766, 4:650 }},
{franchise:'Pirates of the Caribbean', revenue: {1:634, 2:1066, 3:963, 4:1045, 5:794 }}
];

var w = 900,
    h = 550;

var original = '#0283AF',
    highlight = 'red';

var row_len = 40;
var franchises= [];
var revenues = [];

franchises.push("");
data.forEach(function(d) {
  franchises.push(d.franchise);
  var total=0;
  for (var key in d.revenue) {
    total += d.revenue[key];
  }
  revenues.push(total);
});

var grid = d3.range(25).map(function(i){
  return {'x1':0,'y1':0,'x2':0,'y2':row_len*franchises.length};
});

var tickVals = grid.map(function(d,i){
  if(i>0){ return i*10; }
  else if(i===0){ return "100";}
});

var x_max = Math.max.apply(Math, revenues),
    x_min = Math.min.apply(Math, revenues);

var xscale = d3.scale.linear()
        .domain([x_min,x_max])
        .range([w/3,w/2]);

var yscale = d3.scale.linear()
        .domain([0,franchises.length])
        .range([0,row_len*franchises.length]);


var svg = d3.select('body')
        .append('svg')
        .attr('id', 'canvas')
        .attr({'width':w,'height':h});



var xAxis = d3.svg.axis()
    .orient('bottom')
    .scale(xscale)
    .tickValues(tickVals);

var yAxis = d3.svg.axis();
  yAxis
    .orient('left')
    .scale(yscale)
    .tickSize(0)
    .tickFormat(function(d,i){ return franchises[i]; })
    .tickValues(d3.range(17));

var y_xis = svg.append('g')
          .attr("transform", "translate(150,0)")
          .attr('id','yaxis')
          .call(yAxis);

var chart = svg.append('g')
          .attr("transform", "translate(150,0)")
          .attr('id','bars')
          .selectAll('rect')
          .data(revenues)
          .enter()
          .append('rect')
          .attr('height',19)
          .attr({'x':0,'y':function(d,i){ return yscale(i)+30; }})
          .style('fill', original)
          .attr('width',function(d){ return 0; })
          .on('mouseover', show)
          .on('mouseout', cancel)


var transit = d3.select("svg").selectAll("rect")
            .data(revenues)
            .transition()
            .duration(1000)
            .attr("width", function(d) {return xscale(d); });

var transitext = d3.select('#bars')
          .selectAll('text')
          .data(revenues)
          .enter()
          .append('text')
          .attr({'x':function(d) {return xscale(d)-200; },'y':function(d,i){ return yscale(i)+45; }})
          .text(function(d){ return d+"$"; }).style({'fill':'#fff','font-size':'14px'});


// Show the line chart of revenues
function show(d,i){
  d3.select(this).style('fill', highlight);

  var dataObj = data[i].revenue;
  var movie = [];
  var reves = [];

  // reves.push("");
  for (var key in dataObj){
    if (dataObj.hasOwnProperty(key)){
      movie.push(key);
      reves.push(dataObj[key]);
    }
  }

  var svg = d3.select("#canvas"),
    margin = {top: 0, right: 20, bottom: h/2, left: 3*w/4},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    linechart = svg.append("g")
                  .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                  .attr('id', 'linechart');


  var x = d3.scale.linear()
      .domain(d3.extent(movie, function(d) { return d }))
      .range([1, width]);

  var y = d3.scale.linear()
      .domain(d3.extent(reves))
      .rangeRound([height, 0]);

  var line = d3.svg.line()
      .x(function(d,i) {
        // verbose logging to show what's actually being done
        //console.log('Plotting X value for data point: ' + d + ' using index: ' + i + ' to be at: ' + x(i) + ' using our xScale.');
        // return the X coordinate where we want to plot this datapoint
        return x(i+1);
      })
      .y(function(d) {
        // verbose logging to show what's actually being done
        //console.log('Plotting Y value for data point: ' + d + ' to be at: ' + y(d) + " using our yScale.");
        // return the Y coordinate where we want to plot this datapoint
        return y(d);
      });

  // Add the line path.
  linechart.append("path")
      .datum(reves)
      .attr("class", "line")
      .attr("d", function(d) {
        return line(d) })

  // Define the axes
  var xAxis = d3.svg.axis().scale(x)
  .orient("bottom").tickFormat(function(d) { return d3.format("d")(d) });

  var yAxis = d3.svg.axis().scale(y)
  .orient("left").ticks(5);

  // Add the X Axis
  linechart.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);
  // Add the X Label
  linechart.append('text')
    .attr("y", height)
    .attr("x", width/2)
    .attr("dy", "30")
    .style("text-anchor", "middle")
    .text("Movie");

  // Add the Y Axis
  linechart.append("g")
      .attr("class", "y axis")
      .call(yAxis);
  // Add the Y Label
  linechart.append('text')
    .attr("y", 0)
    .attr("x", -height/2)
    .attr("dy", "-40")
    .attr('transform', "rotate(-90)") // Rotates everything
    .style("text-anchor", "middle")
    .text("Revenue");
}

// Cancel the line chart
function cancel(d,i){
  d3.select(this).style('fill', original)
  d3.select('#linechart').remove();
}