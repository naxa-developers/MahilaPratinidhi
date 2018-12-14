//var base_url="http://mahilapratinidhi.naxa.com.np";
 var base_url="http://localhost:8000";

$.get(base_url+'/api/age/',function(data){


    ReactDOM.render(
        <div>
        <ChartBox data_pass={[{'title':'age','data-type':'0','dataName':'total','data':data['total']}]} />
        <ChartBox data_pass={[{'title':'age' +" vs Party",'data-type':'1','dataName':'party','data':data['party']}]} />
        <ChartBox data_pass={[{'title':'age' +" vs Province",'data-type':'1','dataName':'provincial','data':data['provincial']}]} />

        </div>,
        document.getElementById("react-container")
      )



});



$(".dataVariable").on("click",function(){

  var variable = $(this).attr('data-value').toLowerCase().replace(" ","_");

  $.get(base_url+'/api/'+ variable +'/',function(data){



ReactDOM.unmountComponentAtNode(document.getElementById("react-container"));

  ReactDOM.render(
      <div>
      <ChartBox data_pass={[{'title':variable,'data-type':'0','dataName':'total','data':data['total']}]} />
      <ChartBox data_pass={[{'title':variable +" vs Party",'data-type':'1','dataName':'party','data':data['party']}]} />
      <ChartBox data_pass={[{'title':variable +" vs Province",'data-type':'1','dataName':'provincial','data':data['provincial']}]} />
      <ChartBox data_pass={[{'title':variable +" vsProvvsfedvsnat",'data-type':'1','dataName':'vs','data':data['nationalvsfederalvsprovincial']}]} />

      </div>,
      document.getElementById("react-container")
    )
 });


});



//       <ChartBox data_pass={[{'title':variable +" vs Province vs fed vs loc",'data-type':'1','dataName':'vs','data':data['nationalvsfederalvsprovincial']}]} />
