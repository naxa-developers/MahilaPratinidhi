//alert("pasyo");
//var base_url="http://mahilapratinidhi.naxa.com.np";
var base_url="http://localhost:8000";
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


var gl = L.mapboxGL({
       attribution: '<a href="https://www.maptiler.com/license/maps/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
       accessToken: 'not-needed',
       style: 'https://maps.tilehosting.com/c/163bd208-a4f1-4885-8b97-416ac0b47d00/styles/darkmatter_upen/style.json?key=SWfpfQVfURyYQrAEj6J3'
     });

baseMaps = {
    //"Street View": street_view,
    "OSM": OSM,
    "blackwhite":OpenStreetMap_BlackAndWhite,
    "dark":Thunderforest_TransportDark,
    "Empty" : L.tileLayer(''),
    "gl":gl
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
    weight:4,

  });
}

function resetHighlight(e){
  e.target.setStyle({
    weight:2,

  });
}


var last_layer =[];
var marker_array=[];


function zoomToFeature(e){
  map.fitBounds(e.target.getBounds());
  if(last_layer[0]){
      map.removeLayer(last_layer[0]);
      last_layer.pop();

  }


 var properties_object = e.target.feature.properties;


 if(Object.keys(properties_object).length=="1"){
   var division = "province";
   var prodric= properties_object.Province;

 }

 else if (Object.keys(properties_object).length=="8"){
   var division = "municipality";
   var prodric= properties_object['FIRST_DIST'].charAt(0).toUpperCase() +  properties_object['FIRST_DIST'].slice(1).toLowerCase();

 }


  for (var i=0;i<marker_array.length;i++){
    marker_array[i].removeFrom(map);
  }


  var layer = L.geoJson.ajax(base_url+'/api/geojson/'+ division +'/'+ prodric,
            {onEachFeature:onEachFeature,
              style: { color: "white",
                       weight:2,
                       fillColor:"grey",

                       fillOpacity:1}}
            );

   layer.addTo(map);
   last_layer.push(layer);

}

var sum=0;
function returnSum(value){

  var sum =0;
  for(var i =0; i<array.length;i++){
    sum+= array[i];
  }
  return sum;

}

function onEachFeature(feature,layer){

  console.log("props",feature.properties);

  Choropleth(layer,data_summary_all_percentage['total'][feature.properties.Province-1]);
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

function getColor(d) {


//alert(d);

    return d > 25 ? '#031A3F' :
            d > 18 ? '#08204E' :
            d > 16 ? '#0F275E' :
           d > 14  ? '#22377E' :
           d > 12  ? '#3D4C9D' :
           d > 10  ? '#7276CD' :
           d > 5  ? '#8888DD' :

                      '#C1C1E6';
}


function Choropleth(layer,frequency){

  var color= getColor(frequency);
  layer.setStyle({fillColor :color}) ;

}




console.log("baseurlcheck",base_url+'/api/geojson/country');

var country =L.geoJson.ajax(base_url+'/api/geojson/country',
          {onEachFeature:onEachFeature,
           style: { color: "white",
                    weight:2,
                    fillColor:"grey",
                    fillOpacity:"0.6"

                    }
          }).addTo(map);



  //
  // var center_for_markers = [ [27.244862521497282,87.2314453125],
  // [26.941659545381516,85.67138671875], [27.751607687549384,85.352783203125],
  // [28.294707428421205,84.166259765625], [28,83], [29.,82.5],
  // [29.49698759653577,80.980224609375] ]

//api call_

function percentage(array){
  var total = array.reduce(function(total,num){
    return total +num;
  });
  percentage_array =  array.map(function(i){
    return (i*100)/total;

  });
  return percentage_array;

}

  var data_summary_all ={
    'total':[32, 37, 37, 20, 32, 13, 18],
    'national': [1,2,2,5,3,30,7],
    'provincial':[32, 37, 37, 20, 32, 13, 0]
    }






console.log("baseurlcheck",base_url+'/api/maps/');
  $.get(base_url+'/api/maps/',function(data){

    data_summary_all['provincial']= data['provincial'];
    data_summary_all['national']= data['national'];

});

var data_summary_all_percentage ={
  'total':percentage(data_summary_all['total']),
  'national': percentage(data_summary_all['national']),
  'provincial':percentage(data_summary_all['provincial'])

  }

  console.log("percentage",data_summary_all_percentage);


//interaction with sidebar

$("#national-all").on('click',function(){



});

$("#federal-all").on('click',function(){


});

$("#provincial-all").on('click',function(){


});

$("#local-all").on('click',function(){

});
