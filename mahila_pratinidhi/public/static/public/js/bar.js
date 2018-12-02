class SimpleBar extends React.Component{
  constructor(props){
    super(props)
    this.simpleBar = this.simpleBar.bind(this);

  }

  componentDidMount(){
    //alert("component did mont")
    this.simpleBar(this.props.data);

  }

  simpleBar(sample){

    console.log("sample",sample.map((s) => s.caste));
    const svg = d3.select('.simple-bar');
    const svgContainer = d3.select('#container');

    const margin = 20;
    const width = 550 - 2 * margin;
    const height = 300 - 2 * margin;

    const chart = svg.append('g')
      .attr('transform', "translate(" + margin + "," + margin + ")");

      const xScale = d3.scale.ordinal()
      .rangeRoundBands([0, width])
      .domain(sample.map((s) => s.caste))
      ;

        const yScale = d3.scale.linear()
          .range([height, 0])
          .domain([0, 100 ]);


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
        .attr("class", "x axis")
        .attr('transform', "translate(0," + height + ")")
        .call(xAxis0);

    const barGroups = chart.selectAll()
      .data(sample)
      .enter()
      .append('g')

    barGroups
      .append('rect')
      .attr('class', 'simple-rect')
      .attr('x', (g) => xScale(g.caste))
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
          .attr('x', (a) => xScale(a.caste) - 5)
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
          .attr('x', (a) => xScale(a.caste) + xScale.rangeBand() / 2)
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
          .attr('x', (a) => xScale(a.caste))
          .attr('width', xScale.rangeBand())

        chart.selectAll('#limit').remove()
        chart.selectAll('.divergence').remove()
      })

    barGroups
      .append('text')
      .attr('class', 'simple-value')
      .attr('x', (a) => xScale(a.caste) + xScale.rangeBand() / 2)
      .attr('y', (a) => yScale(a.total) - 5)
      .attr('text-anchor', 'middle')
      .text((a) => `${a.total}`)

    svg
      .append('text')
      .attr('class', 'simple-label')
      .attr('x', -(height / 2) - margin)
      .attr('y', margin / 2.4)
      .attr('transform', 'rotate(-90)')
      .attr('text-anchor', 'middle')
      .text('')

    svg.append('text')
      .attr('class', 'simple-label')
      .attr('x', width / 2 + margin)
      .attr('y', height + margin * 1.7+25)
      .attr('text-anchor', 'middle')
      .text('Ethnictiy')

    svg.append('text')
      .attr('class', 'simple-title')
      .attr('x', width / 2 + margin)
      .attr('y', 40)
      .attr('text-anchor', 'middle')
      .text('')




  } //end of function

  render(){

    return(<svg className="simple-bar" />);
  }



} //end of class
