//alert("pasyo");
var base_url="http://mahilapratinidhi.naxa.com.np";
// var base_url="http://localhost:8000";
var map =L.map('mapid',{minZoom: 7,maxZoom: 11,zoomSnap:0.3}).setView([27,85],7);

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



console.log("baseurlcheck",base_url+'/api/maps/');



function fetchapi(){

  $.ajax({
     url: base_url+'/api/maps/',
     type: 'get',
     dataType: 'json',
     async: false,
     success: handleData
  });

}

function handleData(data) {
  window["data_summary_all"]= data;
  window["marker_content"] = data["all"][0]
}

fetchapi();



var total_instance = 12004;


var customPopup = "National:<br/>Federal:<br/>Provincial:<br/>Local:<br/>";
var customOptions =
    {
    'maxWidth': '1000',
    'className' : 'custom-icon',
    'closeButton': false,
    'autoClose': false
    }

    function locateUser() {
        this.map.locate({setView : true});
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

function get_total_instance(e){


  var properties_object = e.target.feature.properties;

  if(Object.keys(properties_object).length=="1"){
    var xx = "Province "+ properties_object.Province;
  }

  else if (Object.keys(properties_object).length=="8"){
    var xx = properties_object['FIRST_DIST'].charAt(0).toUpperCase()+properties_object['FIRST_DIST'].slice(1).toLowerCase();
  }

//alert(marker_content[xx]);
return marker_content[xx];


}


function zoomToFeature(e){
 var properties_object = e.target.feature.properties;


  total_instance = get_total_instance(e);
  map.fitBounds(e.target.getBounds(),{padding:[25,25]});


if(Object.keys(properties_object).length=="1"){

  if(last_layer.length){
    last_layer.map(function(layer){
      map.removeLayer(layer);
    });
      last_layer=[];

  }

}

if(Object.keys(properties_object).length=="8"){


    if(last_layer[1]){
        map.removeLayer(last_layer[1]);
        last_layer.pop();

    }

}



 if(Object.keys(properties_object).length=="1"){
   var division = "province";
   var prodric= properties_object.Province;

 }

 else if (Object.keys(properties_object).length=="8"){
   var division = "municipality";
   var prodric= properties_object['FIRST_DIST'].charAt(0).toUpperCase() +  properties_object['FIRST_DIST'].slice(1).toLowerCase();

 }
else if (Object.keys(properties_object).length=="10"){
  return false

}

  for (var i=0;i<marker_array.length;i++){
    marker_array[i].removeFrom(map);
  }


  var layer_inside = L.geoJson.ajax(base_url+'/api/geojson/'+ division +'/'+ prodric,
            {onEachFeature:onEachFeature,
              style: { color: "white",
                       weight:2,
                       fillColor:"grey",

                       fillOpacity:1}}
            );




   layer_inside.addTo(map);
   last_layer.push(layer_inside);

}

var sum=0;
function returnSum(value){

  var sum =0;
  for(var i =0; i<array.length;i++){
    sum+= array[i];
  }
  return sum;

}

function BindFunction(feature,layer){

  layer.bindTooltip(get_name(feature));

}


function onEachFeature(feature,layer){

  BindFunction(feature,layer);
  Choropleth(feature,layer);
  circular_marker(get_center(feature,layer),get_number(feature),get_name(feature),feature);
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

function circular_marker(center,number,name,feature){
      if (number){ }
      else{
        number=4;
      }

      var name = name.replace(" ","_");


      var myIcon = L.divIcon({
          className:'my-div-icon'+ ' ' + name,
          iconSize: new L.Point(50, 50),
          html: '<p id='+ name +'>'+ number + '<p>',

      });


      // you can set .my-div-icon styles in CSS
      if (Object.keys(feature.properties).length=="10"){



                var marker_cluster = L.markerClusterGroup();
                for(let i=0;i<number;i++){
                  marker_cluster.addLayer(L.marker(center).bindPopup("Mahila Prathinidhi"));
                }

                map.addLayer(marker_cluster);
              marker_array.push(marker_cluster);

    }

      else{


      let marker= L.marker(center, {icon: myIcon}).addTo(map);
      marker_array.push(marker);

    }

                //.bindPopup('divIcon CSS3 popup. <br> Supposed to be easily stylable.');
}

function get_center(feature,layer){

  var center =(layer.getBounds().getCenter());
  return center;

}

function get_name(feature){

  var properties_object = feature.properties;
  if(Object.keys(properties_object).length=="1"){
    var xx = "Province "+ feature.properties.Province;

  }

  else if (Object.keys(properties_object).length=="8"){
    var xx = feature.properties['FIRST_DIST'].charAt(0).toUpperCase()+feature.properties['FIRST_DIST'].slice(1).toLowerCase();
  }

  else if (Object.keys(properties_object).length=="10"){
    var xx = feature.properties['FIRST_GaPa'].charAt(0).toUpperCase()+feature.properties['FIRST_GaPa'].slice(1).toLowerCase();
  }


  return xx;

}

function get_number(feature){

var xx = get_name(feature);

  var number = marker_content[xx];

  return number;
}


function getColor(d) {


//alert(d);

    return d > 20 ? '#031A3F' :
            d > 18 ? '#08204E' :
            d > 16 ? '#0F275E' :
           d > 14  ? '#22377E' :
           d > 12  ? '#3D4C9D' :
           d > 10  ? '#7276CD' :
           d > 5  ? '#8888DD' :

                      '#C1C1E6';

}


function Choropleth(feature,layer){

  var properties_object = feature.properties;

  if(Object.keys(properties_object).length=="1"){
    var xx = "Province "+ feature.properties.Province;
  }

  else if (Object.keys(properties_object).length=="8"){
    var xx = feature.properties['FIRST_DIST'].charAt(0).toUpperCase()+feature.properties['FIRST_DIST'].slice(1).toLowerCase();
  }

  else if (Object.keys(properties_object).length=="10"){
    var xx = feature.properties['FIRST_GaPa'].charAt(0).toUpperCase()+feature.properties['FIRST_GaPa'].slice(1).toLowerCase();
    return false;
  }


 var frequency = marker_content[xx];
 var percentage = (frequency*100)/total_instance;

  var color= getColor(percentage);
  layer.setStyle({fillColor :color});



}




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
    return total + num;
  });
  percentage_array =  array.map(function(i){
    return (i*100)/total;

  });
  return percentage_array;

}






//interaction with sidebar

$("#national-all").on('click',function(){

//console.log(marker_array);
marker_content =data_summary_all['national'][0];
for( var i=0; i< marker_array.length;i++){
  if(marker_array[i]._icon == null){

  }
  else {
    var key = marker_array[i]._icon.firstChild.id;
    var marker_value = marker_content[key.replace("_"," ")];
    if(marker_value == null){
      marker_value = "xxx";
    }



    marker_array[i]._icon.innerHTML =   '<p id='+ key +'>'+ marker_value + '<p>'
}
}

});

$("#federal-all").on('click',function(){
//console.log(marker_array);
marker_content =data_summary_all['federal'][0];

for( var i=0; i< marker_array.length;i++){
  if(marker_array[i]._icon == null){

  }
else{
    var key = marker_array[i]._icon.firstChild.id;
    var marker_value = marker_content[key.replace("_"," ")];
    if(marker_value == null){
      marker_value = "xxx";
    }

    marker_array[i]._icon.innerHTML =   '<p id='+ key +'>'+ marker_value + '<p>'
  }
}


});

$("#provincial-all").on('click',function(){
//console.log(marker_array);
marker_content =data_summary_all['provincial'][0];
for( var i=0; i< marker_array.length;i++){
  if(marker_array[i]._icon == null){
  }
  else{
    //console.log(marker_array[i]._icon);
    var key = marker_array[i]._icon.firstChild.id;
    var marker_value = marker_content[key.replace("_"," ")]
    if(marker_value == null){
      marker_value = "xxx";
    }

    marker_array[i]._icon.innerHTML =   '<p id='+ key +'>'+ marker_value + '<p>'
}

}

});

$("#local-all").on('click',function(){
//console.log(marker_array);
marker_content =data_summary_all['local'][0];
for( var i=0; i< marker_array.length;i++){
  if(marker_array[i]._icon == null){
  }
  else {
    //console.log(marker_array[i]._icon);

    var key = marker_array[i]._icon.firstChild.id;
    var marker_value = marker_content[key.replace("_"," ")];
    if(marker_value == null){
      marker_value = "xxx";
    }
    marker_array[i]._icon.innerHTML =   '<p id='+ key +'>'+ marker_value  + '<p>'
}
}


});


// var myRenderer = L.canvas({ padding: 0.5 });
//
//
// for (var i = 0; i < 100000; i += 1) { // 100k points
// 	L.circleMarker(getRandomLatLng(), {
//   	renderer: myRenderer
//   }).addTo(map).bindPopup('marker ' + i);
// }
//
// function getRandomLatLng() {
// 	return [
//     -90 + 180 * Math.random(),
//     -180 + 360 * Math.random()
//   ];
// }
