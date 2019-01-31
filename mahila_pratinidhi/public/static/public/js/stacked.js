class StackedChart extends React.Component{
  constructor(props){
    super(props)
    this.stackedChart = this.stackedChart.bind(this);

  }

  componentDidMount(){
    //alert("component did mont" +this.props.data[0].data)
    this.stackedChart(this.props.data[0].data, this.props.data[0].dataName,this.props.data[0].ind);

  }

  componentWillReceiveProps(nextProps){
    //alert("component did receive");
    d3.selectAll('.stacked-bar').selectAll("*").remove();
    this.stackedChart(nextProps.data[0].data,nextProps.data[0].dataName);
  }

  stackedChart(data,dataName,ind,variable_colors){


    if (dataName== "party"){

        var legend_array =["Communist Party of Nepal","Nepali Congress","Federal Socialist Forum",
        "Rastriya Janata Party Nepal"];
        var count = 2;
    }

    else if(dataName== "provincial") {


        var legend_array= ["1","2","3","4","5","6","7"];
        count =0;
    }

    else if (dataName== "vs") {

        var legend_array= ["province", "federal", "national"];
        count =1;

    }




  var margin = {top: 20, right: 70, bottom: 20, left: 30};



  var width = 650 - margin.left - margin.right,
      height = 350 - margin.top - margin.bottom;

if(ind=='true'){

  var svg = d3.selectAll(".stacked-bar")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


}

else {
  var svg = d3.selectAll(".stacked-bar").filter(function(d,i){


    return i === count;
  })
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
}
    //var parse = d3.time.format("%Y").parse;

//["redDelicious", "mcintosh", "oranges", "pears"]
    // Transpose the data into layers


    var dataset = d3.layout.stack()(legend_array.map(function(fruit) {
      return data.map(function(d) {
        return {x: d.label, y: +d[fruit]};
      });
    }));

    // Set x, y and colors
    var x = d3.scale.ordinal()
      .rangeRoundBands([10, width-10], 0.02)
      .domain(dataset[0].map(function(d) { return d.x; }));

    var y = d3.scale.linear()
      .domain([0, d3.max(dataset, function(d) {  return d3.max(d, function(d) { return d.y0 + d.y; });  })])
      .range([height, 0]);


      var default_colors = [ "#00CA64","#E238C2","#FAFF37",  "#00C1FF" ,"#5244B8" ,"#E9807B","#f44141" ];

    var colors0 = [	 "#69131a","#e86c75","#faa2ad","#ac779d","#4b1b31" ,"#f441a6","#f44141"];
    var default_colors0 =["#ff6367","#98b000","#00cc7a","#00a5f9","#fb00f6","#f441a6","#f44141"];

    var colors = variable_colors || default_colors;


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
      //.tickPadding([0.4])
      //.tickFormat(d3.time.format("%Y"));

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    svg.append("g")
      .attr("class", "x-axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);


      svg.selectAll(".x-axis text")
     .attr("transform", function(d) {
        return "translate(" + this.getBBox().height*-2 + "," + this.getBBox().height*1.7 + ")rotate(-25)";
    });

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
      .data(colors.slice(0,legend_array.length))
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
      .style("font-size","xx-small")
      .text(function(d, i) {
        switch (i) {
          case 0: return legend_array[0];
          case 1: return legend_array[1];
          case 2: return legend_array[2];
          case 3: return legend_array[3];
          case 4: return legend_array[4];
          case 5: return legend_array[5];
          case 6: return legend_array[6];
          case 7: return legend_array[7];

        }
      });


    // Prep the tooltip bits, initial display is hidden

  } //end of function

  render(){

    return(<svg className="stacked-bar" />);
  }



} //end of class
