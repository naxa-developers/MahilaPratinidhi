function piechart(data,elementid,size){

elementid = elementid || "my-pie-icon-chart";


var w = size || 100;
  var h = size || 100;
  var r = h/2;
  var aColor = {
      'Communist Party of Nepal':'red',
      'Nepali Congress':'green',
      'Federal Socialist Forum':'blue',
      'Rastriya Janata Party Nepal':'yellow',
      'Bebeksheel Sajha Party':'brown'
  }
  
  var data = data || [
      {"label":"Colorectale levermetastase", "value":74}, 
      {"label": "Primaire maligne levertumor", "value":12},
      {"label":"Levensmetatase van andere origine", "value":7}, 
      {"label":"Beningne levertumor", "value":7}
  ];

  var vis = d3.select('#'+elementid)
  .append('svg')
  .attr("class","pie-svg")
  .data([data]).attr("width", w).attr("height", h).attr("transform", "translate(" + r + "," + r*1.5 + ")");
  var pie = d3.layout.pie().value(function(d){return d.value;});
  // Declare an arc generator function
  var arc = d3.svg.arc().outerRadius(r);
  
  // Select paths, use arc generator to draw
  var arcs = vis.selectAll("g.slice").data(pie).enter().append("svg:g").attr("class", "slice");
  arcs.append("svg:path")
      .attr("fill", function(d, i){
                                    return aColor[d.data.label]?aColor[d.data.label]:'purple';})
      .attr("d", function (d) {return arc(d);})
  ;
  
  // Add the text
 /*  arcs.append("svg:text")
      .attr("transform", function(d){
          d.innerRadius = r/2;
          d.outerRadius = r;
          return "translate(" + arc.centroid(d) + ")";}
      )
      .attr("text-anchor", "middle")
      .text( function(d, i) {return data[i].value + '%';}); */
}




