//alert("pasyo");
//var base_url="http://mahilapratinidhi.naxa.com.np";
var base_url="http://localhost:8000";
$(".dataVariable").on("click",function(){

  var variable = $(this).text().toLowerCase().replace(" ","_");
  $.get(base_url+'/api/'+ variable +'/',function(data){



ReactDOM.unmountComponentAtNode(document.getElementById("react-container"));

  ReactDOM.render(
      <div>
      <ChartBox data_pass={[{'title':variable,'data-type':'0','dataName':'total','data':data['total']}]} />
      <ChartBox data_pass={[{'title':variable +" vs Party",'data-type':'1','dataName':'party','data':data['party']}]} />
      <ChartBox data_pass={[{'title':variable +" vs Province",'data-type':'1','dataName':'provincial','data':data['provincial']}]} />
      </div>,
      document.getElementById("react-container")
    )
 });


});
