// Creating the svg
var margin = {top:20, left:20, bottom:20, right:20},
    width = 960 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;
var svg = d3.select("body")
            .append("svg")
            .attr('height', height+margin.top+margin.bottom)
            .attr('width', width+margin.left+margin.right)
            .append("g")
            .attr('transform', "translate(" + margin.left + "," + margin.top + ")");

var numFormat = d3.format('.3s');
var mapScale = 90;

// Read in topojson for geo information
// Read in population infor
d3.queue()
    .defer(d3.json, "world_countries.json")
    .defer(d3.tsv, "world_population.tsv")
    .defer(d3.tsv, "literacy_rate.tsv")
    .await(ready);

function ready(error, geodata, popdata, literdata) {
  if (error) throw error;

  // Prepare the population data and literacy rate data of the country
  var popMap = new Map();
  for(var i=0; i<popdata.length; i++) {
    var coun = popdata[i];
    popMap.set(coun.id, coun.population);
  }
  var literMap = new Map();
  for(var i=0; i<literdata.length; i++) {
    var coun = literdata[i];
    literMap.set(coun.id, coun.Rate);
  }

  // Parse the data using topojson feature to get the raw geojson data and then get the features of the geojson obj
  var countries = geodata.features;
  for(var i=0; i<countries.length; i++) {
    countries[i].population = popMap.has(countries[i].id)? popMap.get(countries[i].id):"";
    countries[i].rate = literMap.has(countries[i].id)? literMap.get(countries[i].id):"";
  }

  drawMap(countries);
}

function drawMap(countries){
  // Create a projection using Mercator and center it
  var projection = d3.geo.mercator()
    .translate([width/2, height/2])
    .scale(mapScale)

  // Create a path using that projection
  var path = d3.geo.path()
    .projection(projection);

  // Assigning color to each path by their population
  var colorDomain =
  [ 889000, 3670000, 7780000, 27800000, 66700000, 189000000, 611000000 ],
    colorRange =
  [ '#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#99000d' ]

  var color = d3.scale.threshold()
  .domain(colorDomain)
  .range(colorRange);

  // Using tooltip for the prompting window
  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([0,0]) // [top, left]
    .html(function(d) { return promptFormat(d); })
    .direction('n') // Position the tooltip to the right (east) of a target element
    .style('font', '7px sans-serif')

  svg.call(tip)

  // Add a path for each country and assigning colors
  svg.selectAll('.country')
    .data(countries)
    .enter().append('path')
    .attr('class', 'country')
    .attr('id', function(d) { return d.id })
    .attr('d', path)
    .attr('fill', function(d) { return color(d.population) })
    .attr('stroke-width', '0.5')
    .on('mouseover', function(d) {
      d3.select(this).attr('stroke-width', '1.5')
      return tip.show(d) })
    .on('mouseout', function(d) {
      d3.select(this).attr('stroke-width', '0.5')
      return tip.hide(d) })

  // Adding a color legend to the graph
  var legendSetting = {
    width: 35,
    height: 5,
    x: 3*width/4,
    y: 60,
    text_dy: 2
  }

  // Add the legend
  var legend = svg.selectAll("rect")
    .data(colorDomain)
    .enter().append("rect") // legend box
    .attr("height", legendSetting.height)
    .attr('width', legendSetting.width)
    .attr("x", function(d,i) { return legendSetting.x + legendSetting.width*i; })
    .attr('y', legendSetting.y)
    .attr("fill", function(d) { return color(d); })

  // Add the text of legend
  var legnedText = svg.selectAll("text")
    .data(colorDomain)
    .enter().append("text")
    .text(function(d) { return numFormat(d) })
    .attr("x", function(d,i) { return legendSetting.x + legendSetting.width*i; })
    .attr('y', legendSetting.y - legendSetting.text_dy)
    .attr('stroke', 'black')
    .attr('opacity', 0.5)
    .attr('text-align', 'left')
    .style('font', "8px sans-serif")
    .style("text-anchor", "start")
}

function promptFormat(d) {
  var format = "<p><span style='color:red'><strong>Country:</strong></span> " + d.properties.name + "</p>"
    + "<p><span style='color:red'> <strong>Population:</strong></span> " + d3.format(',')(d.population) + "</p>"
    + "<p><span style='color:red'> <strong>Literacy Rate:</strong></span> " + d.rate + "</p>";
  return format;
}

function findThres(color){
  // Invert the function color to get the thresholds of each color
  var thresholds = color.range().map(function(d) {
      d = color.invertExtent(d);
      // console.log(d);
      return d;
    })

  return thresholds;
}