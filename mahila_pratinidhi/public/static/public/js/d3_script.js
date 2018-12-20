//var base_url="http://localhost:8000";
var base_url="http://mahilapratinidhi.naxa.com.np";







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



$.get(base_url+'/api/education/',function(data){


    ReactDOM.render(
        <div>
        <ChartBox data_pass={[{'title':'education','data-type':chart_type['education'][0],'dataName':'total','data':(chart_type['education'][0]=="kernel")?data['all'] : data['total']}]} />
        <ChartBox data_pass={[{'title':'education' +" vs Province",'data-type':chart_type['education'][2],'dataName':'provincial','data':data['provincial']}]} />
        <ChartBox data_pass={[{'title':'education' +" vs Province vs federal vs national",'data-type':chart_type['education'][3],'dataName':'vs','data':data['nationalvsfederalvsprovincial']}]} />
        <ChartBox data_pass={[{'title':'education' +" vs Party",'data-type':chart_type['education'][1],'dataName':'party','data':data['party']}]} />

        </div>,
        document.getElementById("react-container")
      )



});



$(".dataVariable").on("click",function(){


  var variable = $(this).attr('data-value').toLowerCase().replace(" ","_");
  $("#innervariable")[0].innerText=variable.replace("_"," ");

  $.get(base_url+'/api/'+ variable +'/',function(data){

    if (data['party']){
      var chart_party =   <ChartBox data_pass={[{'title':variable.replace("_"," ") +" vs Party",'data-type':chart_type[variable][1],'dataName':'party','data':data['party']}]} />;
    }
    else{
      var chart_party = "";
    }


ReactDOM.unmountComponentAtNode(document.getElementById("react-container"));

  ReactDOM.render(
      <div>
      <ChartBox data_pass={[{'title':variable.replace("_"," "),'data-type':chart_type[variable][0],'dataName':'total','data': (chart_type[variable][0]=="kernel")?data['all'] : data['total']}]} />
      <ChartBox data_pass={[{'title':variable.replace("_"," ") +" vs Province",'data-type':chart_type[variable][2],'dataName':'provincial','data':data['provincial']}]} />
      <ChartBox data_pass={[{'title':variable.replace("_"," ") + " vs Province vs federal vs national",'data-type':chart_type[variable][3],'dataName':'vs','data':data['nationalvsfederalvsprovincial']}]} />
      {chart_party}
      </div>,
      document.getElementById("react-container")
    )
 });


});



//       <ChartBox data_pass={[{'title':variable +" vs Province vs fed vs loc",'data-type':'1','dataName':'vs','data':data['nationalvsfederalvsprovincial']}]} />
