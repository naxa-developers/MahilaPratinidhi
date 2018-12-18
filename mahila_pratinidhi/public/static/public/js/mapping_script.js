//alert("pasyo");
var base_url="http://mahilapratinidhi.naxa.com.np";
//  var base_url="http://localhost:8000";
var map =L.map('mapid',{minZoom: 7,maxZoom: 13,zoomSnap:0.1, zoomControl:false}).setView([28.5,84],7.4);

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

var baseMaps = {
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



var total_instance = 300;




    function locateUser() {
        this.map.locate({setView : true});
    }



function highlightFeature(e){
  console.log("xtty");
  var layer= e.target;
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
  for (var i=0;i<marker_array.length;i++){
    marker_array[i].removeFrom(map);
  }


}

if(Object.keys(properties_object).length=="8"){

    if(last_layer[1]){
        map.removeLayer(last_layer[1]);
        last_layer.pop();


    }

    for (var i=0;i<marker_array.length;i++){
      marker_array[i].removeFrom(map);
    }


}



 if(Object.keys(properties_object).length=="1"){
   var division = "province";
   var prodric= properties_object.Province;
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

 else if (Object.keys(properties_object).length=="8"){
   console.log("markers",marker_array)
   var division = "municipality";
   var dric= properties_object['FIRST_DIST'].toLowerCase();
   var muni_layers = L.layerGroup().addTo(map);


   $.each(muni._layers,function(key,value){


     if(value.feature.properties.DISTRICT.toLowerCase()=== dric){
       var geo = value.feature;
       var hlcit = value.feature.properties['HLCIT_CODE'];
       var profile_link ="http://localhost:8000/detail/national/172/";
       var popup_content ="<div style='overflow-y:scroll;height:150px;'><strong>"+ value.feature.properties['LU_Name']+" "+ value.feature.properties['LU_Type'] + "</strong><br><br>";


       $.get(base_url+"/api/hlcit/"+ hlcit ,function(data){
         var females = data;
         for(let i =0;i<females.length;i++){
           var model = (females[i]['model']=="province") ? females[i]['model'] +"/" + hlcit.slice(7,8)  : females[i]['model'];
           var detail = (females[i]['model']=="province") ? "explore" : "detail";
           popup_content += "<h6><a href='"+ base_url+ "/"+ detail + "/" + model + "/" + females[i]['id']  +  "'>"+ females[i]['name'] + "</a></h6>";
           popup_content += "<div>"+ (females[i]['model'] != 'pratinidhi')? females[i]['model']:'federal'  +"</div><br>"
           if(i==females.length-1){
             popup_content +="</div>"

           }

         }

                var muni_layer= L.geoJson(geo,{onEachFeature:onEachFeature_second,
                  style: { color: "white",
                           weight:2,
                           fillColor:"grey",
                           fillOpacity:"0.6"
                           }
                         }).bindPopup(popup_content);

                muni_layers.addLayer(muni_layer);

       });

      }



   });
   last_layer.push(muni_layers);



 }

else if (Object.keys(properties_object).length=="10"){

  return false

}
else if (Object.keys(properties_object).length=="11"){

  return false

}



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

  layer.bindTooltip(get_name(feature),{sticky:true});

}

function onEachFeature_second(feature,layer){
  BindFunction(feature,layer);
  circular_marker(get_center(feature,layer),get_number(feature),get_code(feature),feature);
  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click:zoomToFeature
  })


}


function onEachFeature(feature,layer){

  BindFunction(feature,layer);

  Choropleth(feature,layer);
  circular_marker(get_center(feature,layer),get_number(feature),get_name(feature),feature);
  //layer.bindPopup(customPopup,customOptions);

  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click:zoomToFeature
  })
}

function ward_leader(number,center,females,hlcit){

if(number){
  var marker_cluster = L.markerClusterGroup();

  for(let i=0;i<number;i++){
    var popup_content = "";
    var model = (females[i]['model']=="province") ? females[i]['model'] +"/" + hlcit.slice(7,8)  : females[i]['model'];
    var detail = (females[i]['model']=="province") ? "explore" : "detail";
    popup_content += "<a href='"+ base_url+"/"+ detail+ "/" + model + "/" + females[i]['id'] +  "'>" + females[i]['name'] + "</a>"
    marker_cluster.addLayer(L.marker(center).bindPopup(popup_content));
  }

map.addLayer(marker_cluster);
marker_array.push(marker_cluster);

}
}

function circular_marker(center,number,name,feature){
      if (number){  }
      else{
        number=0;
      }

      var name = name.replace(" ","_");


      var myIcon = L.divIcon({
          className:'my-div-icon'+ ' ' + name,
          iconSize: new L.Point(40, 40),
          html: '<p id='+ name +'>'+ number + '<p>',

      });

      // you can set .my-div-icon styles in CSS
      if (Object.keys(feature.properties).length=="11"){


        $.get(base_url+'/api/hlcit/'+name.replace("_"," "), function(data){
                var females =data;
                ward_leader(number,center,females,name.replace("_"," "))

    });
}
      else{


      let marker= L.marker(center, {icon: myIcon}).addTo(map);
      marker_array.push(marker);

    }

  }
                //.bindPopup('divIcon CSS3 popup. <br> Supposed to be easily stylable.');

function get_center(feature,layer){

  var center =(layer.getBounds().getCenter());
  return center;

}

function get_code(feature){
  var properties_object = feature.properties;
  if (Object.keys(properties_object).length=="11"){
   var xx = feature.properties['HLCIT_CODE'];
 }

return xx;

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

    else if (Object.keys(properties_object).length=="11"){
      var xx = feature.properties['LU_Name'].charAt(0).toUpperCase()+feature.properties['LU_Name'].slice(1).toLowerCase();
    }

  return xx;

}

function get_number(feature){

  var properties_object = feature.properties;
  if (Object.keys(properties_object).length=="11"){
    var xx = get_code(feature)
    if(xx== "524 1 02 4 003"){
      console.log(marker_content);
    }

  }
else{
  var xx = get_name(feature);
}

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


var muni =L.geoJson.ajax('https://dfid.naxa.com.np/core/geojson/municipalities/',
                              {
                               style: { color: "white",
                                        weight:2,
                                        fillColor:"grey",
                                        fillOpacity:"0.6"

                                        }
                              });


console.log("muni",muni);
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

function getLocation(){
  navigator.geolocation.getCurrentPosition(function(location) {
  var latlng = new L.LatLng(location.coords.latitude, location.coords.longitude);
  console.log("country",country);
  $.each(muni._layers, function(key,value){
      if(value._bounds.contains(latlng)== true){
        var geo = value.feature;
        var muni_layer =L.geoJson(geo,{}).addTo(map);
        last_layer.push(muni_layer);
        map.setView([location.coords.latitude, location.coords.longitude], 13);
        for (var i=0;i<marker_array.length;i++){
          marker_array[i].removeFrom(map);
        }
        var hlcit =(value.feature.properties['HLCIT_CODE']);
        $.get(base_url+'/api/hlcit/'+hlcit, function(data){

          var females=data;
          ward_leader(get_number(value.feature),get_center(value,value),females,hlcit);

        })




    }
});


//
//   $.each(country._layers, function(key,value){
//     if(value._bounds.contains(latlng)== true){
//       alert("true");
//       var state =(value.feature.properties.Province);
//       alert(state);
//       var districts = L.geoJson.ajax(base_url+'/api/geojson/province/'+ state);
//       console.log("districts",districts)
//       districts.on("data:loaded",function(){
//         $.each(districts._layers, function(key,value){
//
//           if(value._bounds.contains(latlng)== true){
//             alert("district vetayo");
//             var district =value.feature.properties["FIRST_DIST"];
//             console.log("muni",muni);
//             $.each(muni._layers, function(key,value){
//                     if(value.feature.properties["DISTRICT"]== district){
//                       alert("vitrai pasyo")
//                       alert(value.feature.properties["LU_Name"]);
//                     }
//                   });
//         }
//     });
//
//   });
//
//   }
// });



});
}
$("#local_leader").on('click',function(){

  var latlng = getLocation();


})


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
// }last_layer
