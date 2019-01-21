var base_url="https://mahilapratinidhi.naxa.com.np";
//var base_url="http://localhost:8000";

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
                              {onEachFeature:onEachFeature_discover,
                               style: { color: "white",
                                        weight:0.5,
                                        fillOpacity:"0.1"

                                        }
                              }).addTo(map);


var layers_array=[];
var markers_array=[];
var count1_visualize =0;
var count2_visualize =0;
var name1_visualize ="";
var name2_visualize="";


function onEachFeature(feature,layer){

  BindFunction(feature,layer);

	  circular_marker(get_center(feature,layer),get_number(feature),get_code(feature));
	  //layer.bindPopup(customPopup,customOptions);


  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click:zoomToFeature
  })

}

function onEachFeature_discover(feature,layer){

  BindFunction(feature,layer);
  circular_marker(get_center(feature,layer),get_number(feature),get_code(feature));
	  //layer.bindPopup(customPopup,customOptions);


  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click:discoverOnClick,
  })

}

function BindFunction(feature,layer){

  layer.bindTooltip(get_name(feature),{sticky:true,permanent: false});

}


function circular_marker(center,number,code){

  if(number){}
  else{ number =1}


      if (number){

				var myIcon = L.divIcon({
	          className:'my-div-icon',
	          iconSize: new L.Point(number*2.5, number*2.5),
	          html: `<div id=$(code)></div>`,

	      });

	      // you can set .my-div-icon styles in CSS
	      let marker= L.marker(center, {icon: myIcon}).addTo(map);
				markers_array.push(marker);


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
      weight:0.5,

    });
  }


  function discoverOnClick(e){

    map.fitBounds(e.target.getBounds(),{padding:[25,25]});


    $("#sideinfoid").addClass("sideinfo");
    console.log("ee",e.target.feature.properties["HLCIT_CODE"])
var hlcit_discover= e.target.feature.properties["HLCIT_CODE"]




    $.get(base_url+"/api/hlcit/"+hlcit_discover,function(data){

      console.log(data)
      $("#sideinfoid ul").html("")


      data.map((dict)=>{


        var model = (dict['model']=="province") ? dict['model'] +"/" + hlcit_discover.slice(7,8)  : dict['model'];
        var detail = (dict['model']=="province") ? "explore" : "detail";

        // &nbsp &nbsp<div class="d-inline bg-secondary" style="font-size:x-small;">${dict['model']}</div>

        $("#sideinfoid ul").append(`<li><a href="${base_url}/${detail}/${model}/${dict['id']}">${dict.name}</a></li>`)
      }
    )


    });


  }


  function zoomToFeature(e){
  //
  //   layers_array.map((f)=>
  //   {
  //
  //     f.setStyle({"color":"white"})
  //   }
  // )
  //   e.target.setStyle({"color":"blue"})

        if(e.target._map._container.id=='mapd1'){
          count1_visualize =1;
          map1.fitBounds(e.target.getBounds(),{padding:[25,25]});

        }

        else if(e.target._map._container.id=='mapd2'){
          count2_visualize =1;
          map2.fitBounds(e.target.getBounds(),{padding:[25,25]});
        }

    var properties_object = e.target.feature.properties;
    if(Object.keys(properties_object).length=="1"){
      var properties_name = properties_object.Province;

    }
    else if(Object.keys(properties_object).length=="11"){
      var properties_name = properties_object.LU_Name;

    }

    else if(Object.keys(properties_object).length >11){
      var properties_name = properties_object.DISTRICT;
    }
    if(count1_visualize && count2_visualize){
      $("#data-viz-map").addClass("showmap");
      $('html, body').animate({
             scrollTop: $("#data-viz-map").offset().top
         }, 4000);
    }



}



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

  $("#sideinfoid").addClass("sideinfo_hide");
  $("#sideinfoid").removeClass("sideinfo");


	$("#mapd").addClass("hidemap");
	$("#mapd").removeClass("showmap");
	$("#map-compare-div").addClass("showmap");

if($("#mapd1").children().length){



}

else{


		window.map1 =L.map('mapd1',{minZoom: 7,maxZoom: 13,zoomSnap:0.7, zoomControl:false,scrollWheelZoom: false}).setView([28.5,84],6);
		window.map2 =L.map('mapd2',{minZoom: 7,maxZoom: 13,zoomSnap:0.7, zoomControl:false,scrollWheelZoom: false}).setView([28.5,84],6);
    L.control.zoom({
      position:'topright'
    }).addTo(map1);


    L.control.zoom({
      position:'topright'
    }).addTo(map2);


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
  $("#data-viz-map").addClass("hidemap");
  $("#data-viz-map").removeClass("showmap");
  count1_visualize=0;
  count2_visualize=0;
});


$("#filter-all").on('click',function(){

	marker_content=data_summary_all['all'][0];
});



$("#filter-local").on('click',function(){
	marker_content=data_summary_all['local'][0];

});


$("#filter-national").on('click',function(){

	marker_content=data_summary_all['national'][0];

});


$("#filter-federal").on('click',function(){

	marker_content=data_summary_all['federal'][0];

});


$("#filter-provincial").on('click',function(){

	marker_content=data_summary_all['provincial'][0];

});
