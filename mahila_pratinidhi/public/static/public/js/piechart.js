class PieChart extends React.Component{

  constructor(props){
    super(props)
    this.piechart= this.piechart.bind(this);
  }

  componentDidMount(){

    console.log("dataaa",this.props.data[0].data);

    this.piechart(this.props.data[0].data);

  }

  piechart(data){

    var margin = {top: 20, right: 170, bottom: 50, left: 30};
var color =["#69131a","#e86c75","#faa2ad","#ac779d","#4b1b31" ,"#f441a6","#f44141"];
    var width = 700 - margin.left - margin.right,
        height = 350 - margin.top - margin.bottom;


    var pieGenerator = d3.layout.pie();
  var arcs = pieGenerator([1,2,3]);

  const svg = d3.selectAll(".pie-chart")
      .attr("text-anchor", "middle")
      .style("font", "12px sans-serif");

  const g = svg.append("g")
      .attr("transform", `translate(${width / 2},${height / 2})`);

  g.selectAll("path")
    .data(arcs)
    .enter().append("path")
      .attr("fill", (d,k) => color[k])
      .attr("stroke", "white")
      .attr("d", arc)
    .append("title")
      .text(d => `${d.data.name}: ${d.data.value.toLocaleString()}`);

  const text = g.selectAll("text")
    .data(arcs)
    .enter().append("text")
      .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
      .attr("dy", "0.35em");

  text.append("tspan")
      .attr("x", 0)
      .attr("y", "-0.7em")
      .style("font-weight", "bold")
      .text(d => d.data.name);

  text.filter(d => (d.endAngle - d.startAngle) > 0.25).append("tspan")
      .attr("x", 0)
      .attr("y", "0.7em")
      .attr("fill-opacity", 0.7)
      .text(d => d.data.value.toLocaleString());

}




  render(){

    return(<svg className="pie-chart" />)
  }

}
