class StackedChart extends React.Component{
  constructor(props){
    super(props)
    this.stackedChart = this.stackedChart.bind(this);

  }

  componentDidMount(){
    //alert("component did mont")
    this.stackedChart(this.props.data);

  }

  stackedChart(data){


  var margin = {top: 20, right: 170, bottom: 20, left: 30};

  var width = 700 - margin.left - margin.right,
      height = 350 - margin.top - margin.bottom;

  var svg = d3.select(".stacked-bar")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    //var parse = d3.time.format("%Y").parse;

    var party_array =["Nepal Communist Party","Nepali Congress","Federal Socialist Forum, Nepal",
    "Rastriya Janata Party Nepal"]

//["redDelicious", "mcintosh", "oranges", "pears"]
    // Transpose the data into layers
    var dataset = d3.layout.stack()(party_array.map(function(fruit) {
      return data.map(function(d) {
        return {x: d.caste, y: +d[fruit]};
      });
    }));

    console.log("dataset",dataset);


    // Set x, y and colors
    var x = d3.scale.ordinal()
      .domain(dataset[0].map(function(d) { return d.x; }))
      .rangeRoundBands([10, width-10], 0.02);

    var y = d3.scale.linear()
      .domain([0, d3.max(dataset, function(d) {  return d3.max(d, function(d) { return d.y0 + d.y; });  })])
      .range([height, 0]);

    var colors = ["#d25c4d", "#f2b447", "#d9d574","#9b42f4"];


    // Define and draw axes
    var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(5)
      .tickSize(-width, 0, 0)
      .tickFormat( function(d) { return d } );

    var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickPadding([0.4])
      //.tickFormat(d3.time.format("%Y"));

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);


    // Create groups for each series, rects for each segment
    var groups = svg.selectAll("g.cost")
      .data(dataset)
      .enter().append("g")
      .attr("class", "cost")
      .style("fill", function(d, i) { return colors[i]; });

    var rect = groups.selectAll("rect")
      .data(function(d) { return d; })
      .enter()
      .append("rect")
      .attr("x", function(d) { return x(d.x); })
      .attr("y", function(d) { return y(d.y0 + d.y); })
      .attr("height", function(d) { return y(d.y0) - y(d.y0 + d.y); })
      .attr("width", x.rangeBand())
      .on("mouseover", function() { tooltip.style("display", "none"); })
      .on("mouseout", function() { tooltip.style("display", "none"); })
      .on("mousemove", function(d) {
        tooltip.style("display", "block");
        var xPosition = d3.mouse(this)[0] - 15;
        var yPosition = d3.mouse(this)[1] - 25;
        tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
        tooltip.select("text").text(d.y);
      });


      var tooltip = svg.append("g")
        .style("display", "none");

      tooltip.append("rect")

        .attr("width", 30)
        .attr("height", 20)
        .attr("fill", "white")
        .style("opacity", 0.5);

      tooltip.append("text")
        .attr("x", 15)
        .attr("dy", "1.2em")
        .style("text-anchor", "middle")
        .attr("font-size", "12px")
        .attr("font-weight", "bold");


    // Draw legend
    var legend = svg.selectAll(".legend")
      .data(colors)
      .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });

    legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", function(d, i) {return colors.slice()[i];});

    legend.append("text")
      .attr("x", width + 5)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "start")
      .style("fill","white")
      .style("font-size","small")
      .text(function(d, i) {
        switch (i) {
          case 0: return party_array[0];
          case 1: return party_array[1];
          case 2: return party_array[2];
          case 3: return party_array[3];

        }
      });


    // Prep the tooltip bits, initial display is hidden

  } //end of function

  render(){

    return(<svg className="stacked-bar" />);
  }



} //end of class
