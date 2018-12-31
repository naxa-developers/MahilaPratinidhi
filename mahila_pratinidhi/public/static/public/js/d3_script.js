//var base_url="http://localhost:8000";
console.log("dataupdated",data_content)
var base_url="https://mahilapratinidhi.naxa.com.np";

var chart_type ={
                  'age':['kernel','stacked','stacked','stacked'] ,
                  'ethnicity':['bar','stacked','stacked','stacked'] ,
                  'mother_tongue':['hbar','hstacked','hstacked','hstacked'] ,
                  'education':['bar','stacked','stacked','stacked'] ,
                  'election_type':['bar','stacked','stacked','stacked'] ,
                  'party':['hbar','hstacked','hstacked','hstacked'] ,
                  'political_engagement':['kernel','stacked','stacked','stacked'],
                  'political_commitment':['hbar','hstacked','hstacked','hstacked'] ,
                  'election_experience':['bar','stacked','stacked','stacked']

}
 age, ethnicity, mother tongue and education. Political variables include; political party, election type, years in political engagement and political commitment. When applicable, these variable have been cross sectioned int
for(let i =0 ; i<data_content.length;i++){
  if(data_content[i]["variable_name"] == "education"){
    $("#main_content_id")[0].innerText=data_content[i]["main_content"];
    var content_variable= data_content[i]["content_variable"];
    var content_province= data_content[i]["content_province"];
    var content_province_vs_federal_vs_national= data_content[i]["content_province_vs_federal_vs_national"];
    var content_party= data_content[i]["content_party"];

  }

}



$.get(base_url+'/api/education/',function(data){


    ReactDOM.render(
        <div>
        <ChartBox data_pass={[{'title':'education','content':content_variable,'data-type':chart_type['education'][0],'dataName':'total','data':(chart_type['education'][0]=="kernel")?data['all'] : data['total']}]} />
        <ChartBox data_pass={[{'title':'education' +" vs Province",'content':content_province,'data-type':chart_type['education'][2],'dataName':'provincial','data':data['provincial']}]} />
        <ChartBox data_pass={[{'title':'education' +" vs Province vs federal vs national",'content':content_province_vs_federal_vs_national,'data-type':chart_type['education'][3],'dataName':'vs','data':data['nationalvsfederalvsprovincial']}]} />
        <ChartBox data_pass={[{'title':'education' +" vs Party",'content':content_party,'data-type':chart_type['education'][1],'dataName':'party','data':data['party']}]} />

        </div>,
        document.getElementById("react-container")
      )



});


$(".dataVariable").on("click",function(){


  var variable = $(this).attr('data-value').toLowerCase().replace(" ","_");
  //insert static contents
$("#innervariable")[0].innerText=variable.replace("_"," ");
  console.log("data_content",data_content)
  for(let i =0 ; i<data_content.length;i++){
    if(data_content[i]["variable_name"].replace(" ","_")== variable){
      //$("#main_content_id")[0].innerText=data_content[i]["main_content"];
      var content_variable= data_content[i]["content_variable"];
      var content_province= data_content[i]["content_province"];
      var content_province_vs_federal_vs_national= data_content[i]["content_province_vs_federal_vs_national"];
      var content_party= data_content[i]["content_party"];

    }

  }



  $.get(base_url+'/api/'+ variable +'/',function(data){

    if (data['party']){
      var chart_party =   <ChartBox data_pass={[{'title':variable.replace("_"," ") +" vs Party",'content':content_party,'data-type':chart_type[variable][1],'dataName':'party','data':data['party']}]} />;
    }
    else{
      var chart_party = "";
    }


ReactDOM.unmountComponentAtNode(document.getElementById("react-container"));

  ReactDOM.render(
      <div>
      <ChartBox data_pass={[{'title':variable.replace("_"," "),'content':content_variable,'data-type':chart_type[variable][0],'dataName':'total','data': (chart_type[variable][0]=="kernel")?data['all'] : data['total']}]} />
      <ChartBox data_pass={[{'title':variable.replace("_"," ") +" vs Province",'content':content_province,'data-type':chart_type[variable][2],'dataName':'provincial','data':data['provincial']}]} />
      <ChartBox data_pass={[{'title':variable.replace("_"," ") + " vs Province vs federal vs national",'content':content_province_vs_federal_vs_national,'data-type':chart_type[variable][3],'dataName':'vs','data':data['nationalvsfederalvsprovincial']}]} />
      {chart_party}
      </div>,
      document.getElementById("react-container")
    )
 });


});



//       <ChartBox data_pass={[{'title':variable +" vs Province vs fed vs loc",'data-type':'1','dataName':'vs','data':data['nationalvsfederalvsprovincial']}]} />
