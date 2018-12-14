class PieChart extends React.Component{

  constructor(props){
    super(props)
    this.piechart= this.piechart.bind(this);
  }

  componentDidMount(){
    alert("x")
    console.log(this.props.data[0].data);

    this.piechart(this.props.data[0].data);

  }

  piechart(data){

    const pie =d3.pie()
      .sort(null)
      .value(d => d.value)

  const arcs = pie(data);

  const svg = d3.selectAll(".pie-chart")
      .attr("text-anchor", "middle")
      .style("font", "12px sans-serif");

  const g = svg.append("g")
      .attr("transform", `translate(${width / 2},${height / 2})`);

  g.selectAll("path")
    .data(arcs)
    .enter().append("path")
      .attr("fill", d => color(d.data.name))
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
