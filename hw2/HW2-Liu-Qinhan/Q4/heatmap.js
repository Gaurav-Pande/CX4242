// The data source file
var dataFile = "heatmap.csv"

// Define the variables
var seasonNum = 1;
var names = ["Baratheon","Greyjoy","Lannister","Stark","Targaryen","Tyrell"];
var order = {"Baratheon":1,"Greyjoy":2,"Lannister":3,"Stark":4,"Targaryen":5,"Tyrell":6};
var episodes = [1,2,3,4,5,6,7,8,9,10];

var margin = { top: 50, right: 0, bottom: 100, left: 30 },
    width = 960 - margin.left - margin.right,
    height = 800 - margin.top - margin.bottom,
    grid = { height:50, width:50, rx:'5', ry:'5', padding: 1,
            dx:90, dy:10, top:margin.top, left:margin.left, bottom:800-margin.bottom-350 }
    rect = { height:grid.height-2*grid.padding, width:grid.width-2*grid.padding}
    colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"]; // alternatively colorbrewer.YlGnBu[9]

// Add the title of the whole map
var mapTitle = d3.select('body')
  .append("text")
  .text("Game of Thrones House-Wise Appearance")
  .attr('class', 'mapTitle')
  .style('text-align', 'center')
  .style('font-weight', 'bold')
  .style('font-size', "20px")

// Debugging
var data = ["Season 1", "Season 2", "Season 3", "Season 4", "Season 5", "Season 6"];

var select = d3.select('body')
  .append('select')
    .attr('class','select')
    .on('change',onchange)

var options = select
  .selectAll('option')
  .data(data).enter()
  .append('option')
    .text(function (d) { return d; });

function onchange() {
  selectValue = d3.select('select').property('value')
  seasonNum = Number( selectValue.substr(selectValue.length-1) )
  drawMap()
};

drawMap();

function drawMap() {
  // Update the svg
  d3.select("#chart").remove();

  d3.csv(dataFile, function(data) {
    // Set up data for graphs
    var filtered = [];
    data.forEach( function(d) {
      d.season = +d.season;
      if (d.season == seasonNum) {
        for (var key in names) {
          // Parse the data
          var parse = {'name':names[key], 'episode':+d.episode, 'count':+d[names[key]]};
          filtered.push(parse);
        }
      }
    });

    // Draw map using the filtered data
    // Create the svg
    var svg = d3.select("body").append("svg")
      .attr('id', 'chart')
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Define the xScale, yScale and colorScale for the grids
    var xScale = function(episode) { return grid.left+(episode-1)*grid.width; }
    var yScale = function(name) { return grid.top+(order[name]-1)*grid.height; }
    // var appers = [];  // Quantile Scale uses the frequencies of the data to determine the thresholds
    // filtered.forEach( function(d) { appers.push(d.count) } );
    // var colorScale = d3.scale.quantile()
    //   .domain(appers)
    //   .range(colors)
    var colorScale = d3.scale.quantize()
      .domain(d3.extent(filtered, function(d) { return d.count }))
      .range(colors)

    // Draw the rectangles
    var rects = svg.selectAll("rects")
      .data(filtered).enter()
      .append("rect")
      .attr('width', grid.width-2*grid.padding)
      .attr('height', grid.height-2*grid.padding)
      .attr('rx', grid.rx)
      .attr('ry', grid.ry)
      .attr('x', function(d) { return xScale(d.episode)+grid.dx-grid.width/2+3*grid.padding })
      .attr('y', function(d) { return yScale(d.name)-3*grid.dy+grid.padding })
      .attr('fill', function(d) { return colorScale(d.count)})

    // Draw the y labels
    var yLabels = svg.selectAll("Ytext")
      .data(names).enter()
      .append("text")
      .text(function(d,i) { return names[i]; })
      .attr('x', grid.left + 20)
      .attr('y', yScale)
      .attr('dx', -30)
      .style('text-anchor', 'right')
      .style('text-align', 'right')

    // Draw the y axis label
    var yAxisLabel = svg.append("text")
      .text("House")
      .attr('x', 0)
      .attr('y', grid.left)
      .attr('dx', -185)
      .attr('dy', -30)
      .attr('transform', 'rotate(-90)')
      .style('font-weight', 'bold')

    // Draw the x labels
    var xLabels = svg.selectAll("Xtext")
      .data(episodes).enter()
      .append("text")
      .text(function(d) { return d; })
      .attr('y', grid.bottom)
      .attr('x', xScale)
      .attr('dx', grid.dx-4*grid.padding)
      .attr('dy', -grid.dy)
      .style('text-align', 'center')

    // Draw the x axis label
    var xAxisLabel = svg.append("text")
      .text("Episode")
      .attr('y', 0)
      .attr('x', grid.left)
      .attr('dx', 285)
      .attr('dy', 370)
      .style('font-weight', 'bold')

    // Invert the function color to get the thresholds of the color scale
    var thresholds = colorScale.range().map(function(d) {
      d = colorScale.invertExtent(d);
      return d;
    })
    // console.log(thresholds)

    // Adding a color legend to the graph
    var legendSetting = {
      width: 35,
      height: 15,
      x: 200,
      y: 400,
      text_dy: 2
    }

    // Add the legend
    var legend = svg.selectAll("legend_rect")
      .data(thresholds)
      .enter().append("rect") // legend box
      .attr("height", legendSetting.height)
      .attr('width', legendSetting.width)
      .attr("x", function(d,i) { return legendSetting.x + legendSetting.width*i; })
      .attr('y', legendSetting.y)
      .attr("fill", function(d) { return colorScale(d[0]); })
      .style('stroke', 'black')
      .style('stroke-width', 1)

    // Add the text of legend
    var legnedText = svg.selectAll("legend_text")
      .data(thresholds)
      .enter().append("text")
      .text(function(d) { return d3.format('.0f')(d[0]) })
      .attr("x", function(d,i) { return legendSetting.x + legendSetting.width*i; })
      .attr('y', legendSetting.y - legendSetting.text_dy)
      .attr('dy', 27)
      .attr('stroke', 'black')
      .attr('opacity', 0.8)
      .attr('text-align', 'left')
      .style('font', "10px sans-serif")
      .style('font-weight', 'bold')
      .style("text-anchor", "start")

    // Add the legend title
    var legendTitle = svg.append("text")
      .text("Number of appearance")
      .attr('y', legendSetting.y)
      .attr('x', legendSetting.x)
      .attr('dx', 0)
      .attr('dy', -5)
      .style('font-weight', 'bold')
      .style('font-size', "10px")
  });
}
