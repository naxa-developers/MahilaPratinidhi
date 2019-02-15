
var colors=['red','green','pink','yellow']
var legend_array =["Communist Party of Nepal","Nepali Congress","Federal Socialist Forum",
        "Rastriya Janata Party Nepal"];
var legend = d3.select(".discover-legend")
        .append('svg')
        .attr('class','stacked-legend')
        .attr('width',"100")
        .attr('height',"10")
        .selectAll('g')
        .data(colors)
      .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate("+ 130*i + "," + 19 + ")"; });

    legend.append("rect")
      .attr("x", 100)
      .attr("width", 10)
      .attr("height", 10)
      .style("fill", function(d, i) {return colors.slice()[i];});

    legend.append("text")
      .attr("x", 100 + 20)
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