var width = 500,
    height = 500;

var graticule = d3.geo.graticule();

var backGrid = graticule();
var grid = graticule();

var globe = {type: "Sphere"};

var projection = d3.geo.orthographic()
    .scale(height / 2.1)
    .translate([width / 2, height / 2])
    .precision(0.6);

var canvas = d3.select("body").append("canvas")
    .attr("width", width)
    .attr("height", height);

var c = canvas.node().getContext("2d");

var path = d3.geo.path()
    .projection(projection)
    .context(c);

var title = d3.select("h1");

d3.queue()
    .defer(d3.json, "https://s3-us-west-2.amazonaws.com/s.cdpn.io/95802/world-110m.json")
    .await(ready);

function ready(error, world) {
  if (error) throw error;

  var land = topojson.feature(world, world.objects.land),
      countries = topojson.feature(world, world.objects.countries).features,
      borders = topojson.mesh(world, world.objects.countries, function(a, b) { return a !== b; }),
      i = -1,
      n = countries.length;

  (function transition() {
    d3.transition()
        .duration(1250)
        .each("start", function() {
          title.text(countries[i = (i + 1) % n].name);
        })
        .tween("rotate", function() {
          var p = d3.geo.centroid(countries[i]),
              r = d3.interpolate(projection.rotate(), [-p[0], -p[1]]);
          return function(t) {
            c.clearRect(0, 0, width, height);

            projection.rotate(r(t)).clipAngle(180);
            c.fillStyle = "#dadac4", c.beginPath(), path(land), c.fill();
            // c.fillStyle = "#f00", c.beginPath(), path(countries[i]), c.fill();
            c.strokeStyle = "#fff", c.lineWidth = .5, c.beginPath(), path(borders), c.stroke();
            c.strokeStyle = "#000", c.lineWidth = 1, c.beginPath(), path(globe), c.stroke();
            c.strokeStyle = "rgba(0, 0, 0, 0.05)", c.lineWidth = .5, c.beginPath(), path(backGrid), c.stroke();

            projection.rotate(r(t)).clipAngle(90);
            c.fillStyle = "#737368", c.beginPath(), path(land), c.fill();
            c.fillStyle = "#f00", c.beginPath(), path(countries[i]), c.fill();
            c.strokeStyle = "#fff", c.lineWidth = .5, c.beginPath(), path(borders), c.stroke();
            c.strokeStyle = "rgba(0, 0, 0, 0.1)", c.lineWidth = 1, c.beginPath(), path(globe), c.stroke();
            c.strokeStyle = "rgba(0, 0, 0, 0.1)", c.lineWidth = .5, c.beginPath(), path(grid), c.stroke();
          };
        })
      .transition()
        .each("end", transition);
  })();
};

d3.select(self.frameElement).style("height", height + "px");