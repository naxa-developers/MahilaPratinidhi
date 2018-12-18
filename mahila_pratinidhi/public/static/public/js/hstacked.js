class HStackedChart extends React.Component{
  constructor(props){
    super(props)
    this.hstackedChart = this.hstackedChart.bind(this);
  }

  componentDidMount(){
    //alert("component did mont" +this.props.data[0].dataName)

    this.hstackedChart(this.props.data[0].data, this.props.data[0].dataName);

  }

  componentWillReceiveProps(nextProps){
    alert("component did receive");
    d3.selectAll('.stacked-bar').selectAll("*").remove();
    this.hstackedChart(nextProps.data[0].data,nextProps.data[0].dataName);
  }

  hstackedChart(data,dataName,variable_colors){


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



  var margin = {top: 20, right: 170, bottom: 50, left: 30};

  var width = 700 - margin.left - margin.right,
      height = 350 - margin.top - margin.bottom;

  var svg = d3.select(".hstacked-bar")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    //var parse = d3.time.format("%Y").parse;

//["redDelicious", "mcintosh", "oranges", "pears"]
    // Transpose the data into layers


    var dataset = d3.layout.stack()(legend_array.map(function(fruit) {
      return data.map(function(d) {
        return {x: d.label, y: +d[fruit]};
      });
    }));

    var y = d3.scale.ordinal()
      .domain(dataset[0].map(function(d) { return d.x; }))
      .rangeRoundBands([10, height-10], 0.02);

      var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")

        svg.append("g")
          .attr("class", "y axis")
          .call(yAxis);

    var x = d3.scale.linear()
      .domain([0, d3.max(dataset, function(d) {  return d3.max(d, function(d) { return d.y0 + d.y; });  })])
      .range([width, 0]);

      var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .tickPadding([0.4])


    var colors = [	 "#69131a","#e86c75","#faa2ad","#ac779d","#4b1b31" ,"#f441a6","#f44141"];
    var default_colors =["#ff6367","#98b000","#00cc7a","#00a5f9","#fb00f6","#f441a6","#f44141"];

    var colors = variable_colors || default_colors;


    // Define and draw axes

      //.tickFormat(d3.time.format("%Y"));



    // Prep the tooltip bits, initial display is hidden

  } //end of function

  render(){

    return(<svg className="hstacked-bar" />);
  }



} //end of class
