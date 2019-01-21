//alert("pasyo");
var base_url="https://mahilapratinidhi.naxa.com.np";
//var base_url="http://localhost:8000";

var map_height = window.innerHeight - parseInt($("#find").css('height'));
//map_height =map_height -126;
$("#mapid").css("height",map_height+"px");

var map =L.map('mapid',{minZoom: 7,maxZoom: 13,zoomSnap:0.1, zoomControl:false,scrollWheelZoom: false}).setView([28.5,84],7.2);

map.on('click', function() {
  //map.scrollWheelZoom.enable();
  });

var info = L.control();
//info.options ={ positon: 'topleft'};
info.onAdd = function (map) {
				this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
				info._div.innerHTML="<button id='refresh-button' class='btn btn-default'>refresh </button> ";
				return this._div;
			};

			// method that we will use to update the control based on feature properties passed
//
// info.onClick = function (e) {
//       e.preventDefault();
// e.stopPropagation()
//   		alert(x);
//       };

$(".button-action").on('click',function(){
  alert("x");
})



var OSM = L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',



});

var empty = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
  opacity:0

});

var Wikimedia = L.tileLayer('https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}{r}.png', {
	attribution: '<a href="https://wikimediafoundation.org/wiki/Maps_Terms_of_Use">Wikimedia</a>',
	minZoom: 1,
	maxZoom: 19
});


var OpenStreetMap_BlackAndWhite = L.tileLayer('//{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  opacity:1


});

var Thunderforest_TransportDark = L.tileLayer('https://{s}.tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey={apikey}', {
	attribution: '&copy; <a href="https://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
	apikey: 'ddb2f354bd68480ebfa4ce3a9726c511',
	maxZoom: 22
});





var gl = L.mapboxGL({
       attribution: '<a href="https://www.maptiler.com/license/maps/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
       accessToken: 'not-needed',
       style: 'https://maps.tilehosting.com/c/163bd208-a4f1-4885-8b97-416ac0b47d00/styles/darkmatter_upen/style.json?key=SWfpfQVfURyYQrAEj6J3'
     });


     var NASAGIBS_ViirsEarthAtNight2012 = L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/VIIRS_CityLights_2012/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
     	attribution: 'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
     	bounds: [[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
     	minZoom: 1,
     	maxZoom: 8,
     	format: 'jpg',
     	time: '',
     	tilematrixset: 'GoogleMapsCompatible_Level'
     });

     var CartoDB_DarkMatter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
	subdomains: 'abcd',
	maxZoom: 19
});

var CartoDB_DarkMatterNoLabels = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
	subdomains: 'abcd',
	maxZoom: 19
}).addTo(map);

var baseMaps = {
    //"Street View": street_view,
    "OSM": OSM,
    "Black&White":OpenStreetMap_BlackAndWhite,
    // "dark":Thunderforest_TransportDark,
    "none":empty,
    "Wikimedia":Wikimedia,
    // "NASAGIBS_ViirsEarthAtNight2012":NASAGIBS_ViirsEarthAtNight2012,
    "CartoDB_DarkMatter":CartoDB_DarkMatter,
    "CartoDB_DarkMatterNoLabels":CartoDB_DarkMatterNoLabels

    //"Empty" : L.tileLayer(''),
    //"gl":gl
};

L.control.layers(baseMaps).addTo(map);
L.control.zoom({
     position:'topright'
}).addTo(map);



var ourCustomControl = L.Control.extend({

  options: {
    position: 'topright'
    //control position - allowed: 'topleft', 'topright', 'bottomleft', 'bottomright'
  },

  onAdd: function (map) {
    var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
    container.style.backgroundColor = 'white';
    container.style.width = '30px';
    container.style.height = '30px';
    container.style.padding = '0px';
    container.style.backgroundColor = 'white';

    container.style.backgroundSize = "30px 30px";
    var imgnode = document.createElement("img");
    imgnode.src = refresh_url;
    imgnode.style.height ='25px';
    imgnode.style.width ='25px';


    container.appendChild(imgnode);

    container.onclick = function(){

      for(var i =0; i<marker_array.length;i++){
        marker_array[i].removeFrom(map);
      }

      for(var i =0; i<last_layer.length;i++){
        last_layer[i].removeFrom(map);

      }
      last_layer =[];


      map.setView([28.5,84],7.2);
      console.log("country",country);
      marker_content = data_summary_all["all"][0]

      country.setStyle({fillOpacity:"0.1"})

 $.each(country._layers,function(key,value){

   circular_marker(get_center(value.feature,value),get_number(value.feature),get_name(value.feature),value.feature);


 })
    }


    return container;
  },

});

map.addControl(new ourCustomControl());


$("#mapid").on("change","input.leaflet-control-layers-selector", function(){


  if(map.hasLayer(empty)){
    $("#mapid").css("background-color","#0f2842");


  }

  else{
    $("#mapid").css("background-color","#dddddd");


  }

})

console.log("baseurlcheck",base_url+'/api/maps/');
//
// var marker_content = {"Province 1": 46,
//             "Province 2": 59,
//             "Province 3": 74,
//             "Province 4": 30,
//             "Province 5": 49,
//             "Province 6": 17,
//             "Province 7": 25,
// }




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


var country =L.geoJson.ajax(base_url+'/api/geojson/country',
          {onEachFeature:onEachFeature,
           style: { color: "white",
                    weight:1,



                    }
          }).addTo(map);

country.on('data:loaded', function () {
                $("#loading-id").find("h3").css("display","none");
             });


var total_instance = 300;




    function locateUser() {
        this.map.locate({setView : true});
    }



function highlightFeature(e){
  console.log("xtty");
  var layer= e.target;
  layer.setStyle({
    weight:3,


  });
}

function resetHighlight(e){
  e.target.setStyle({
    weight:1,

  });
}


var last_layer =[];
var marker_array=[];

function get_total_instance(feature){


  var properties_object = feature.properties;

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



  console.log("eventorfeature",e);


  if(e.target){

     var properties_object = e.target.feature.properties;
     total_instance = get_total_instance(e.target.feature);
     map.fitBounds(e.target.getBounds(),{padding:[25,25]});


}
else{
  var properties_object = e.properties;
  total_instance = get_total_instance(e);
  console.log("egfit",e)
  map.fitBounds(layer.getBounds(),{padding:[25,25]});


}

if(last_layer[0]){
  last_layer[0].setStyle({fillOpacity:"0.08"})

}

if(last_layer[1]){
  last_layer[1].setStyle({fillOpacity:"0.08"})


}

if(Object.keys(properties_object).length=="1"){
  $("#loading-id").find("h3").css("display","block");


  if(last_layer.length){
    last_layer.map(function(layer){
      map.removeLayer(layer);
    });
      last_layer=[];

  }
  for (var i=0;i<marker_array.length;i++){
    marker_array[i].removeFrom(map);
  }

  country.setStyle({fillOpacity:"0.08"})


}

if(Object.keys(properties_object).length=="8"){
  $("#loading-id").find("h3").css("display","block");


    if(last_layer[1]){
      console.log("districts",last_layer[0])


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
   let layer_inside = L.geoJson.ajax(base_url+'/api/geojson/'+ division +'/'+ prodric,
             {onEachFeature:onEachFeature,
               style: { color: "white",
                        weight:2,


                        }}
             );

layer_inside.on('data:loaded',function(){
  $("#loading-id").find("h3").css("display","none");


})

                layer_inside.addTo(map);
                last_layer.push(layer_inside);



 }

 else if (Object.keys(properties_object).length=="8"){

   var division = "municipality";
   var dric= properties_object['FIRST_DIST'].toLowerCase();

   let layer_inside = L.geoJson.ajax(base_url+'/api/geojson/'+ division +'/'+ dric,
             {
               onEachFeature:onEachFeature_second,
               style: { color: "white",
                        weight:2,


                        }}
             );
      layer_inside.on('data:loaded',function(){
               $("#loading-id").find("h3").css("display","none");


             })

                layer_inside.addTo(map);
                last_layer.push(layer_inside);







   var muni_layers = L.layerGroup()
   // .addTo(map);
   $.each(muni._layers,function(key,value){


     if(value.feature.properties.DISTRICT.toLowerCase()=== dric){
       var geo = value.feature;
       var hlcit = value.feature.properties['HLCIT_CODE'];
       var profile_link =base_url+"/detail/national/172/";
       var popup_content ="<div style='overflow-y:scroll;height:150px;'><h7><strong>"+ value.feature.properties['LU_Name']+" "+ value.feature.properties['LU_Type'] + "</strong></h7><br><br>";


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

                // var muni_layer= L.geoJson(geo,{onEachFeature:onEachFeature_second,
                //   style: { color: "white",
                //            weight:2,
                //            fillColor:"grey",
                //            fillOpacity:"0.6"
                //            }
                //          }).bindPopup(popup_content);
                //
                // muni_layers.addLayer(muni_layer);

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

function BindPopupFunction(feature,layer){


    var hlcit = feature.properties['hlcit_code'] || feature.properties['HLCIT_CODE'] ;
    var profile_link =base_url+"/detail/national/172/";
    var popup_content ="<div style='overflow-y:scroll;height:150px;'><h7><strong>"+ feature.properties['FIRST_GaPa']+" "+ feature.properties['FIRST_Type'] + "</strong></h7><br><br>";


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

           layer.bindPopup(popup_content)


                });


}


function onEachFeature_second(feature,layer){
  BindFunction(feature,layer);
  circular_marker(get_center(feature,layer),get_number(feature),get_code(feature),feature);
  BindPopupFunction(feature,layer);
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


      let marker= L.marker(center, {icon: myIcon}).addTo(map).on('click',function(e){
        zoomToFeature(feature)
      });
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
   var xx = feature.properties['hlcit_code'] || feature.properties['HLCIT_CODE'];
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

  else if (Object.keys(properties_object).length=="11"){
    var xx = feature.properties['FIRST_GaPa'].charAt(0).toUpperCase()+feature.properties['FIRST_GaPa'].slice(1).toLowerCase();
  }

    else if (Object.keys(properties_object).length=="12"){
      var xx = feature.properties['LU_Name'].charAt(0).toUpperCase()+feature.properties['LU_Name'].slice(1).toLowerCase();
    }

  return xx;

}

function get_number(feature){

  var properties_object = feature.properties;

  if (Object.keys(properties_object).length=="11"){
    var xx = get_code(feature)


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
  layer.setStyle({fillColor :color,fillOpacity:1});



}






var muni =L.geoJson.ajax('https://dfid.naxa.com.np/core/geojson/municipalities/',
                              {
                               style: { color: "white",
                                        weight:2,
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






//interaction with sidebar{% block upper_content %}

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
      marker_value = "0";
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
          BindPopupFunction(value.feature,muni_layer);

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

function filter_options(options,idname){



					var selectBox = document.getElementById(idname);
					selectBox.innerHTML= "<option>"+ "Select" + "</option>" ;
					for(var i = 0, l = options.length; i < l; i++){
						  var option = options[i];
						  selectBox.options.add( new Option(option.name, option.id) );

					}
}

$("#leader-province").on('change',function(){
    var myvalue = (this.value).toString();
    $.get(base_url + '/api/districts/?province_id='+ myvalue, function(data){
      filter_options(data,"leader-district");
    })

})

$("#leader-district").on('change',function(){

  //needs to change
    var myvalue = (this.value).toString();
    $.get(base_url + '/api/districts/?province_id='+ myvalue, function(data){
      filter_options(data,"leader-district");
    })

});


$('#apply-filter').on('click', function(){


});


$('#clear-filter').on('click', function(){

  for(var i =0; i<marker_array.length;i++){
    marker_array[i].removeFrom(map);
  }

  for(var i =0; i<last_layer.length;i++){
    last_layer[i].removeFrom(map);

  }
  last_layer =[];


  map.setView([28.5,84],7.2);
  console.log("country",country);
  marker_content = data_summary_all["all"][0]


$.each(country._layers,function(key,value){

circular_marker(get_center(value.feature,value),get_number(value.feature),get_name(value.feature),value.feature);


});

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
