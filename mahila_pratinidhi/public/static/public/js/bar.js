class SimpleBar extends React.Component{
  constructor(props){
    super(props)
    this.simpleBar = this.simpleBar.bind(this);

  }

  componentDidMount(){
    //alert("component did mont")
    this.simpleBar(this.props.data[0].data);

  }


  componentWillReceiveProps(nextProps){
    d3.select('.simple-bar').selectAll("*").remove();
    this.simpleBar(nextProps.data[0].data);


  }

  simpleBar(sample){
console.log("sample",sample);

console.log("sampleafterdlt",sample);
    var value_value = sample.map((s)=> +s.total);
    console.log("value_value",value_value);

    alert(d3.max(value_value));
  var max_value=  Math.max.apply(null, value_value);


    const svg = d3.select('.simple-bar');


    var margin0 = {top: 20, right: 40, bottom: 10, left: 10};

    const width = 650 -margin0.left-margin0.right;
    const height = 350 -margin0.top- margin0.bottom;

    const chart = svg.append('g')
      .attr('transform', "translate(" + margin0.left + "," + margin0.top + ")");

      const xScale = d3.scale.ordinal()
      .rangeRoundBands([0, width],0.1)
      .domain(sample.map((s) => s.label))
      ;

        const yScale = d3.scale.linear()
          .domain([0, d3.max(value_value) ])
          .range([height, 0]);


          var yAxis0 = d3.svg.axis()
            .scale(yScale)
            .orient("left")
            .ticks(5)
            .tickSize(-width, 0, 0)
            .tickFormat( function(d) { return d } );

          var xAxis0 = d3.svg.axis()
            .scale(xScale)
            .orient("bottom")



    chart.append('g')
      .attr("class", "y axis")
      .call(yAxis0);

      chart.append('g')
        .attr("class", "x-axis")
        .attr('transform', "translate(0," + height + ")")
        .call(xAxis0);

        chart.selectAll(".x-axis text")
       .attr("transform", function(d) {
          return "translate(" + this.getBBox().height*-2 + "," + this.getBBox().height + ")rotate(-45)";
      });

    const barGroups = chart.selectAll()
      .data(sample)
      .enter()
      .append('g')

    barGroups
      .append('rect')
      .attr('class', 'simple-rect')
      .attr('x', (g) => xScale(g.label))
      .attr('y', (g) => yScale(g.total))
      .attr('height', (g) => height - yScale(g.total))
      .attr('width', xScale.rangeBand())
      .on('mouseenter', function (actual, i) {
        d3.selectAll('.value')
          .attr('opacity', 0)

        d3.select(this)
          .transition()
          .duration(300)
          .attr('opacity', 0.6)
          .attr('x', (a) => xScale(a.label) - 5)
          .attr('width', xScale.rangeBand() + 10)

        const y = yScale(actual.total)

        line = chart.append('line')
          .attr('id', 'limit')
          .attr('x1', 0)
          .attr('y1', y)
          .attr('x2', width)
          .attr('y2', y)

        barGroups.append('text')
          .attr('class', 'simple-divergence')
          .attr('x', (a) => xScale(a.label) + xScale.rangeBand() / 2)
          .attr('y', (a) => yScale(a.total) + 30)
          .attr('fill', 'white')
          .attr('text-anchor', 'middle')
          .text((a, idx) => {
            const divergence = (a.total - actual.total).toFixed(1)

            let text = ''
            if (divergence > 0) text += '+'
            text += `${divergence}`

            return idx !== i ? text : '';
          })

      })
      .on('mouseleave', function () {
        d3.selectAll('.value')
          .attr('opacity', 1)

        d3.select(this)
          .transition()
          .duration(300)
          .attr('opacity', 1)
          .attr('x', (a) => xScale(a.label))
          .attr('width', xScale.rangeBand())

        chart.selectAll('#limit').remove()
        chart.selectAll('.divergence').remove()
      })

    barGroups
      .append('text')
      .attr('class', 'simple-value')
      .attr('x', (a) => xScale(a.label) + xScale.rangeBand() / 2)
      .attr('y', (a) => yScale(a.total) - 5)
      .attr('text-anchor', 'middle')
      .text((a) => `${a.total}`)

    svg
      .append('text')
      .attr('class', 'simple-label')
      .attr('x', -(height / 2) - margin0.left)
      .attr('y', margin0.top / 2.4)
      .attr('transform', 'rotate(-90)')
      .attr('text-anchor', 'middle')
      .text('')

    svg.append('text')
      .attr('class', 'simple-label')
      .attr('x', width / 2 + margin0.left)
      .attr('y', height + margin0.top * 1.7+50)
      .attr('text-anchor', 'middle')
      .text('')

    svg.append('text')
      .attr('class', 'simple-title')
      .attr('x', width / 2 + margin0.left)
      .attr('y', 40)
      .attr('text-anchor', 'middle')
      .text('')




  } //end of function

  render(){

    return(<svg className="simple-bar" />);
  }



} //end of class
