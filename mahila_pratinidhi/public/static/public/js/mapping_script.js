//alert("pasyo");
var base_url="http://mahilapratinidhi.naxa.com.np";
//var base_url="http://localhost:8000";
var map =L.map('mapid',{minZoom: 7,maxZoom: 10}).setView([27,85],7);

var OSM = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
});

var OpenStreetMap_BlackAndWhite = L.tileLayer('http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var Thunderforest_TransportDark = L.tileLayer('https://{s}.tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey={apikey}', {
	attribution: '&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
	apikey: 'ddb2f354bd68480ebfa4ce3a9726c511',
	maxZoom: 22
});

baseMaps = {
    //"Street View": street_view,
    "OSM": OSM,
    "blackwhite":OpenStreetMap_BlackAndWhite,
    "dark":Thunderforest_TransportDark,
    "Empty" : L.tileLayer(''),
};
L.control.layers(baseMaps).addTo(map);



var customPopup = "National:<br/>Federal:<br/>Provincial:<br/>Local:<br/>";
var customOptions =
    {
    'maxWidth': '1000',
    'className' : 'custom-icon',
    'closeButton': false,
    'autoClose': false
    }

function update_popup(data){
  customPopup = "National:"+data[0]+"<br/>Federal:"+data[1]+"<br/>Provincial:"+data[2]+"<br/>Local:"+data[3]+"<br/>";

}

function highlightFeature(e){
  layer= e.target;
  var province=layer.feature.properties.Province;
  layer.setStyle({
    weight:3,
    color: '#666',
    dashArray :'',
    fillOpacity:0.7
  });
}

function resetHighlight(e){
  country.resetStyle(e.target);
}


var last_layer =[];
var marker_array=[];
function zoomToFeature(e){
  map.fitBounds(e.target.getBounds());
  if(last_layer[0]){
      map.removeLayer(last_layer[0]);
      last_layer.pop();
    }
  var province= e.target.feature.properties.Province;
  for (var i=0;i<marker_array.length;i++){
    marker_array[i].removeFrom(map);
  }
  console.log("baseurlcheck",base_url+'/api/geojson/province/'+ province);
  var layer = L.geoJson.ajax(base_url+'/api/geojson/province/'+ province,
            {onEachFeature:onEachFeature,
              style: { color: "black",
                       weight:1.5,

                       fillOpacity:0}}
            );

   layer.addTo(map);
   last_layer.push(layer);

}

function onEachFeature(feature,layer){


  circular_marker(get_center(feature,layer),data_summary_all['total'][feature.properties.Province-1]);
  //layer.bindPopup(customPopup,customOptions);
  layer.on('mouseover', function (e) {
              this.openPopup();
          });
  layer.on('mouseout', function (e) {
              this.closePopup();
          });
  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click:zoomToFeature
  })
}

function circular_marker(center,number){

      if (number){ }
      else{
        number="xx";
      }


      var myIcon = L.divIcon({
          className:'my-div-icon',
          iconSize: new L.Point(40, 40),
          html: number
      });
      // you can set .my-div-icon styles in CSS
      var marker= L.marker(center, {icon: myIcon}).addTo(map);
      marker_array.push(marker);
          //.bindPopup('divIcon CSS3 popup. <br> Supposed to be easily stylable.');
}

function get_center(feature,layer){

  var center =(layer.getBounds().getCenter());
  return center;

}
console.log("baseurlcheck",base_url+'/api/geojson/country');

var country =L.geoJson.ajax(base_url+'/api/geojson/country',
          {onEachFeature:onEachFeature,
           style: { color: "black",
                    weight:1.5,

                    fillOpacity:0}
          }).addTo(map);



  //
  // var center_for_markers = [ [27.244862521497282,87.2314453125],
  // [26.941659545381516,85.67138671875], [27.751607687549384,85.352783203125],
  // [28.294707428421205,84.166259765625], [28,83], [29.,82.5],
  // [29.49698759653577,80.980224609375] ]

//api call_

  var data_summary_all ={
    'total':[32, 37, 37, 20, 32, 13, 18],
    'national': [1,2,2,5,3,30,7],
    'provincial':[32, 37, 37, 20, 32, 13, 0]
    }
  frequency_array=[1187,1000,800,1730,2000,3212,3212];
console.log("baseurlcheck",base_url+'/api/maps/');
  $.get(base_url+'/api/maps/',function(data){

    data_summary_all['provincial']= data['provincial'];
    data_summary_all['national']= data['national'];

});
//interaction with sidebar

$("#national-all").on('click',function(){



});

$("#federal-all").on('click',function(){


});

$("#provincial-all").on('click',function(){


});

$("#local-all").on('click',function(){

});
