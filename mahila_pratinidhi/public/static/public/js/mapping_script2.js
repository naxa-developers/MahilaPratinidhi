//var base_url="https://mahilapratinidhi.naxa.com.np";
var base_url="http://localhost:8000";

var map =L.map('mapd',{minZoom: 7,maxZoom: 13,zoomSnap:0.7, zoomControl:false,scrollWheelZoom: false}).setView([28.5,84],8);

L.control.zoom({
     position:'topright'
}).addTo(map);

var CartoDB_DarkMatterNoLabels = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
	subdomains: 'abcd',
	maxZoom: 19
}).addTo(map);

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



var muni =L.geoJson.ajax('https://dfid.naxa.com.np/core/geojson/municipalities/',
                              {onEachFeature:onEachFeature,
                               style: { color: "white",
                                        weight:0.5,
                                        fillOpacity:"0.1"

                                        }
                              }).addTo(map);


var layers_array=[];




function onEachFeature(feature,layer){

  BindFunction(feature,layer);

	  circular_marker(get_center(feature,layer),get_number(feature));
	  //layer.bindPopup(customPopup,customOptions);


  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click:zoomToFeature
  })

}


function BindFunction(feature,layer){

  layer.bindTooltip(get_name(feature),{sticky:true});

}


function circular_marker(center,number){


      if (number){

				var myIcon = L.divIcon({
	          className:'my-div-icon',
	          iconSize: new L.Point(number, number),
	          html: '',

	      });

	      // you can set .my-div-icon styles in CSS
	      let marker= L.marker(center, {icon: myIcon}).addTo(map);


			  }
      else{
        number=0;
      }




  }



  function highlightFeature(e){
    var layer= e.target;
    layer.setStyle({
      weight:2,


    });
  }

  function resetHighlight(e){
    e.target.setStyle({
      weight:1,

    });
  }
  function zoomToFeature(e){ }



  function get_name(feature){


    var properties_object = feature.properties;

    if(Object.keys(properties_object).length=="11"){
      var xx = feature.properties.LU_Name;

    }

    else if (Object.keys(properties_object).length=="8"){
      var xx = feature.properties['FIRST_DIST'].charAt(0).toUpperCase()+feature.properties['FIRST_DIST'].slice(1).toLowerCase();
    }


    return xx;

  }

	function get_center(feature,layer){
	  var center =(layer.getBounds().getCenter());
	  return center;

	}

	function get_number(feature){

	  var properties_object = feature.properties;

	  if (Object.keys(properties_object).length=="11"){
	    var xx = get_code(feature)


	  }

	  var number = marker_content[xx];


	  return number;
	}


	function get_code(feature){
	  var properties_object = feature.properties;
	  if (Object.keys(properties_object).length=="11"){
	   var xx = feature.properties['HLCIT_CODE'];
	 }

	return xx;

	}



////Compare

$(".compare-area-select").on('change',function(){
	$(this).removeClass("btn-dark");
	$(this).addClass("btn-primary");
	$(this).siblings().removeClass("btn-primary");
	$(this).siblings().addClass("btn-dark");


	$("#mapd").addClass("hidemap");
	$("#mapd").removeClass("showmap");
	$("#map-compare-div").addClass("showmap");
	$(".sidebar").addClass("hidemap");

if($("#mapd1").children().length){



}

else{


		window.map1 =L.map('mapd1',{minZoom: 7,maxZoom: 13,zoomSnap:0.7, zoomControl:false,scrollWheelZoom: false}).setView([28.5,84],6);
		window.map2 =L.map('mapd2',{minZoom: 7,maxZoom: 13,zoomSnap:0.7, zoomControl:false,scrollWheelZoom: false}).setView([28.5,84],6);
		L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
			attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
			subdomains: 'abcd',
			maxZoom: 19
		}).addTo(map1);
		L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
			attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
			subdomains: 'abcd',
			maxZoom: 19
		}).addTo(map2);




}




	switch($(this).find(":selected").text()){
		case "Provinces":

					layers_array.map((e)=> {map1.removeLayer(e);
						map2.removeLayer(e);

					});

					layers_array =[];

					layers_array.push(	L.geoJson.ajax(base_url+'/api/geojson/country',
																					{onEachFeature:onEachFeature,
																					 style: { color: "white",
																										weight:0.5,
																										fillOpacity:"0.1"

																										}
																					}).addTo(map1),
																											L.geoJson.ajax(base_url+'/api/geojson/country',
																											{onEachFeature:onEachFeature,
																											 style: { color: "white",
																																weight:0.5,
																																fillOpacity:"0.1"

																																}
																											}).addTo(map2))

							break;


		case "Districts":

		layers_array.map((e)=> {map1.removeLayer(e);
			map2.removeLayer(e);

		});

		layers_array =[];
					layers_array.push(L.geoJson.ajax(base_url+'/api/geojson/districts',
																							{onEachFeature:onEachFeature,
																							 style: { color: "white",
																												weight:0.5,
																												fillOpacity:"0.1"

																												}
																							}).addTo(map1),
								L.geoJson.ajax(base_url+'/api/geojson/districts',
								{onEachFeature:onEachFeature,
								 style: { color: "white",
													weight:0.5,
													fillOpacity:"0.1"

													}
								}).addTo(map2)

					)



									break;

		case "Municipalities":


		layers_array.map((e)=> {map1.removeLayer(e);
			map2.removeLayer(e);

		});

		layers_array =[];
				layers_array.push(
				L.geoJson.ajax('https://dfid.naxa.com.np/core/geojson/municipalities/',
																	{onEachFeature:onEachFeature,
																	 style: { color: "white",
																						weight:0.5,
																						fillOpacity:"0.1"

																						}
																	}).addTo(map1),

			L.geoJson.ajax('https://dfid.naxa.com.np/core/geojson/municipalities/',
																	                              {onEachFeature:onEachFeature,
																	                               style: { color: "white",
																	                                        weight:0.5,
																	                                        fillOpacity:"0.1"

																	                                        }
																	                              }).addTo(map2)

 )




									break;

		default:
				break;


	}


//

// muni.addTo(map2);




});

$("#discover-map").on('click',function(){
	$(this).removeClass("btn-dark");
	$(this).addClass("btn-primary");
	$(this).siblings().removeClass("btn-primary");
	$(this).siblings().addClass("btn-dark");
	$(this).siblings().val("COMPARE");

	$("#mapd").addClass("showmap");
	$("#mapd").removeClass("hidemap");
	$("#map-compare-div").addClass("hidemap");
	$("#map-compare-div").removeClass("showmap");


});
