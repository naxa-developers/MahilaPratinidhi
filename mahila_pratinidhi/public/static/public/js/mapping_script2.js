//var base_url="https://mahilapratinidhi.naxa.com.np";
var base_url="http://localhost:8000";
var layers_array=[];
var markers_array=[];
var markers_pie_array=[];
var markers_pie_all_array=[];
var count1_visualize =0;
var count2_visualize =0;
var compare_variable ="all";
var name1_visualize ="524 5 54 4 003";
var name2_visualize="524 1 04 3 007";


var map =L.map('mapd',{minZoom: 7,maxZoom: 13,zoomSnap:0.7, zoomControl:false,scrollWheelZoom: false}).setView([28.5,84],8);

L.control.zoom({
     position:'topright'
}).addTo(map);

var CartoDB_DarkMatterNoLabels = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
	subdomains: 'abcd',
	maxZoom: 19
}).addTo(map);
 
map.on('zoomend', function() {
/* 	if(map.getZoom() <10.2 && !map.hasLayer(markers_pie_all_array[0])){
		
		markers_pie_all_array.map(marker => marker.addTo(map))
		}
 */
 	if (map.getZoom() <10 && markers_pie_array.length){
		 
					map.removeLayer(markers_pie_array[0]);
					
	}
 
/* 	if (map.getZoom() >10.2){
 		 markers_pie_all_array.map(marker => map.removeLayer(marker))  
 }
 */	
});
 

function fetchapi(){

  $.ajax({
     url: base_url+'/api/maps/',
     type: 'get',
     dataType: 'json',
     async: false,
     success: handleData
	});

	$.ajax({
		url: base_url+'/api/pie/',
		type: 'get',
		dataType: 'json',
		async: false,
		success: handlePie
 });

}

function handleData(data) {
  window["data_summary_all"]= data;
  window["marker_content"] = data["all"][0]
}

function handlePie(data) {
  window["data_pie_all"]= data;
  window["pie_content"] = data["all"]
}

fetchapi();


var muni =L.geoJson.ajax(base_url+'/api/geojson/municipality/',
                              {onEachFeature:onEachFeature_discover,
                               style: { color: "white",
                                        weight:0.5,
                                        fillOpacity:"0.1"

                                        }
                              }).addTo(map);




function onEachFeature(feature,layer){


	BindFunction(feature,layer);

	  //circular_marker(get_center(feature,layer),get_number(feature),get_code(feature));
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

  if(number){ }
  else{ number =1}


      if (number){



				var myIcon = L.divIcon({
	          className:'my-div-icon',
	          iconSize: new L.Point(2.5, 2.5),
	          html: `<div id='mun${code.replace(/\s/g,"_")}'></div>`,
				});
				

	      // you can set .my-div-icon styles in CSS
				console.log("center",center)
				let marker= L.marker([center[1],center[0]], {icon: myIcon});
				marker.addTo(map);
				markers_pie_all_array.push(marker);
				
				var data_for_pie = [] 
				
				for(let i=0;i<pie_content.length;i++){
					if(pie_content[i]['hlcit_code'] == code){
						let temp_dict = {}
						temp_dict["label"]=pie_content[i]['party_name'] || 'not found'
						temp_dict["value"]=pie_content[i]['total'] || 2
						data_for_pie.push(temp_dict)
					
					}
						
				}
				
				

				piechart(data_for_pie,'mun'+code.replace(/\s/g,"_",10),10) 
 

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

		if(markers_pie_array.length){
			map.removeLayer(markers_pie_array[0])
			markers_pie_array=[]
		}
		map.fitBounds(e.target.getBounds(),{padding:[25,25]});
 		
		/* map.setView(e.target.getBounds().getCenter(), 12); */
		var myIcon = L.divIcon({
			className:'my-pie-icon',
			iconSize: new L.Point(200, 200),
			html: `<div id='my-pie-icon-chart'></div>`,
	});
	
	let center = e.target.getBounds().getCenter()
	// you can set .my-div-icon styles in CSS
	let marker= L.marker(center, {icon: myIcon}).addTo(map);
	markers_pie_array.push(marker);
	var hlcit_discover= e.target.feature.properties["HLCIT_CODE"]

	let data_for_pie = [] 
	for(let i=0;i<pie_content.length;i++){
					if(pie_content[i]['hlcit_code']== hlcit_discover){
						data_for_pie.push({"label":pie_content[i]['party_name'],"value":pie_content[i]['total']})
					}
			}


	//var pie_data= pie_content[hlcit_discover]
	piechart(data_for_pie,"my-pie-icon-chart") 


    $("#sideinfoid").addClass("sideinfo");
    $.get(base_url+"/api/hlcit/"+hlcit_discover,function(data){

			$("#sideinfoid ul").html("");
			$("#sideinfoid ul").append(`<h5>${e.target.feature.properties["LU_Name"]} ${e.target.feature.properties["LU_Type"]}</h5>`)


      data.map((dict)=>{
				console.log(dict['model'])

				var model = (dict['model']=="province") ? dict['model'] +"/" + hlcit_discover.slice(7,8)  :
										(dict['model']=='district') ? dict['model'] +"/" + dict['district_id']:  
										dict['model'];
				
				var detail = (dict['model']=="pratinidhi") ? "detail" : 
										 "explore";	

        // &nbsp &nbsp<div class="d-inline bg-secondary" style="font-size:x-small;">${dict['model']}</div>

        $("#sideinfoid ul").append(`<li><a href="${base_url}/${detail}/${model}/${dict['id']}">${dict.name}</a></li>`)
      }
    )


    });


  }


  function zoomToFeature(e){
  	
	var properties_object = e.target.feature.properties;
	
	switch (Object.keys(properties_object).length){
		case 1:
			var properties_name = properties_object.Province;
			break;
									
		case 13:
			var properties_name = properties_object.HLCIT_CODE;
			break;

		case 147:
		var properties_name = properties_object.DISTRICT;
		break;

		default:
			break;
	}

				
	
	if(e.target._map._container.id=='mapd1'){

					layers_array[0].setStyle({"color":"white"})
					e.target.setStyle({"color":"blue"})
          count1_visualize =1;
					map1.fitBounds(e.target.getBounds(),{padding:[25,25]});
					name1_visualize= properties_name;

        }

  else if(e.target._map._container.id=='mapd2'){
					layers_array[1].setStyle({"color":"white"})
					e.target.setStyle({"color":"green"})

          count2_visualize =1;
					map2.fitBounds(e.target.getBounds(),{padding:[25,25]});
					name2_visualize= properties_name;
        }

    
    if(count1_visualize && count2_visualize){
			$("#data-viz-map").addClass("showviz");
			$("#data-viz-map").removeClass("hidemap");
/* 			let base_url="http://localhost:8000"; */
			$("#c3chart-1").html("")
			$("#c3chart-2").html("")
			$("#c3chart-3").html("")
			$("#c3chart-4").html("")
			$("#c3chart-5").html("")

			if(!compare_variable){compare_variable = "all"}
			alert(base_url+"/api/"+compare_variable +"/"+name1_visualize+"/"+name2_visualize)
			
			$.get(base_url+"/api/"+compare_variable +"/"+name1_visualize+"/"+name2_visualize, function(data){
				stackedChart(data["education"],[name1_visualize,name2_visualize],"c3chart-1",["blue","green"]);
				stackedChart(data["Ethnicity"],[name1_visualize,name2_visualize],"c3chart-2",["blue","green"]);
				stackedChart(data["Party Name"],[name1_visualize,name2_visualize],"c3chart-3",["blue","green"]);
				kernel(data["age"],[name1_visualize,name2_visualize],"c3chart-4");
				kernel(data["Years in Politics"],[name1_visualize,name2_visualize],"c3chart-5");

			})
			           
	
      $('html, body').animate({
             scrollTop: $("#data-viz-map").offset().top
				 }, 2000); 

				 count1_visualize= 0;
				 count2_visualize=0;
			
			
				 
		
    }



}



  function get_name(feature){


    var properties_object = feature.properties;

    if(Object.keys(properties_object).length=="13"){
      var xx = feature.properties.LU_Name;

    }

    else if (Object.keys(properties_object).length=="8"){
      var xx = feature.properties['FIRST_DIST'].charAt(0).toUpperCase()+feature.properties['FIRST_DIST'].slice(1).toLowerCase();
    }


    return xx;

  }

	function get_center(feature,layer){
		if (Object.keys(feature.properties).length=="13"){
			
			var center =[feature.properties.centroid_X,feature.properties.cenroid_Y];

		}
		else{
			var center =(layer.getBounds().getCenter());
		}
	  
	  return center;

	}

	function get_number(feature){

	  var properties_object = feature.properties;
	  if (Object.keys(properties_object).length=="13"){
			var xx = get_code(feature)


	  }

		//var number = marker_content[xx];
		number = 10


	  return number;
	}


	function get_code(feature){
	  var properties_object = feature.properties;
	  if (Object.keys(properties_object).length=="13"){
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


	$(".discover").addClass("hidemap")

	$("#mapd").addClass("hidemap");
	$("#mapd").removeClass("showmap");
	$("#map-compare-div").addClass("showmap");
	$("#map-compare-div").removeClass("hidemap");

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
					compare_variable= "province";
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


		compare_variable= "district";
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

		compare_variable= "all";						
		layers_array.map((e)=> {map1.removeLayer(e);
			map2.removeLayer(e);

		});

		layers_array =[];
				layers_array.push(
				L.geoJson.ajax(base_url+'/api/geojson/municipality/',
																	{onEachFeature:onEachFeature,
																	 style: { color: "white",
																						weight:0.5,
																						fillOpacity:"0.1"

																						}
																	}).addTo(map1),

			L.geoJson.ajax(base_url+'/api/geojson/municipality/',
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
	$("#data-viz-map").removeClass("showviz");
	$(".discover").removeClass("hidemap");
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
