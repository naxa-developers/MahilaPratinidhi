class HBar extends React.Component{
  constructor(props){
    super(props)
    this.hBar = this.hBar.bind(this);

  }

  componentDidMount(){
    //alert("component did mont")
    this.hBar(this.props.data[0].data);

  }


  componentWillReceiveProps(nextProps){
    d3.select('.hbar').selectAll("*").remove();
    this.hBar(nextProps.data[0].data);


  }

  hBar(sample){

    var data = sample;
        //sort bars based on value
        data = data.sort(function (a, b) {
            return d3.ascending(+a.total, +b.total);
        })


        //set up svg using margin conventions - we'll need plenty of room on the left for labels


        var margin = {
            top: 20,
            right: 40,
            bottom: 10,
            left: 130
        };

        var width = 650 - margin.left - margin.right,
            height = 350 - margin.top - margin.bottom;



        var svg = d3.select(".hbar")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scale.linear()
            .range([0, width])
            .domain([0, d3.max(data, function (d) {

                return +d.total;
            })]);

        var y = d3.scale.ordinal()
            .rangeRoundBands([height, 0], .1)
            .domain(data.map(function (d) {
                return d.label;
            }));


        //make y axis to show bar names
        var yAxis = d3.svg.axis()
            .scale(y)
            //no tick marks
            .tickSize(0)
            .orient("left");

        var gy = svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)


        var bars = svg.selectAll(".hbarrect")
                        .data(data)
                        .enter()
                        .append("g")

                    //append rects
                    bars.append("rect")
                        .attr("class", "hbarrect")
                        .attr("y", function (d) {
                            return y(d.label);
                        })
                        .attr("height", y.rangeBand())
                        .attr("x", 0)
                        .attr("width", function (d) {
                            return x(d.total);
                        });

                    //add a value label to the right of each bar
                    bars.append("text")
                        .attr("class", "labeltop")
                        //y position of the label is halfway down the bar
                        .attr("y", function (d) {
                            return y(d.label) + y.rangeBand() / 2 + 4;
                        })
                        //x position is 3 pixels to the right of the bar
                        .attr("x", function (d) {
                            return x(d.total) + 3;
                        })
                        .text(function (d) {
                            return d.total;
                        });














  } //end of function


  render(){

    return(<svg className="hbar" />);
  }



} //end of class
