//alert("pasyo");
var base_url="http://mahilapratinidhi.naxa.com.np";
//var base_url="http://localhost:8000";

//according to the tab pressed, call api , accordingly determine the no of checkbox app that needs to be called

    const sample = [ { language: 'Rust', value: 78.9, color: '#000000' }, {
language: 'Kotlin', value: 75.1, color: '#00a2ee' }, { language: 'Python',
value: 68.0, color: '#fbcb39' }, { language: 'TypeScript', value: 67.0, color:
'#007bc8' }, { language: 'Go', value: 65.6, color: '#65cedb' }, { language:
'Swift', value: 65.1, color: '#ff6e52' }, { language: 'JavaScript', value: 61.9,
color: '#f9de3f' }, { language: 'C#', value: 60.4, color: '#5d2f8e' }, {
language: 'F#', value: 59.6, color: '#008fc9' }, { language: 'Clojure', value:
59.6, color: '#507dca' } ];


var data_to_use=[];
$.get(base_url+'/api/ethnicity/',function(data){



  ReactDOM.render(
    <div>
    <ChartBox data_pass={[{'title':"Ethnictiy",'data-type':'0','data':data['total_ethnicity']}]} />
    <ChartBox data_pass={[{'title':"Ethnictiy vs party",'data-type':'1','data':data['party_ethnicity']}]} />
    </div>,
    document.getElementById("react-container")
  )

});



//format the data from api according to need
var data_fruit = [
  { year: "2006", redDelicious: "10", mcintosh: "15", oranges: "9", pears: "6" },
  { year: "2007", redDelicious: "12", mcintosh: "18", oranges: "9", pears: "4" },
  { year: "2008", redDelicious: "05", mcintosh: "20", oranges: "8", pears: "2" },
  { year: "2009", redDelicious: "01", mcintosh: "15", oranges: "5", pears: "4" },
  { year: "2010", redDelicious: "02", mcintosh: "10", oranges: "4", pears: "2" },
  { year: "2011", redDelicious: "03", mcintosh: "12", oranges: "6", pears: "3" },
  { year: "2012", redDelicious: "04", mcintosh: "15", oranges: "8", pears: "1" },
  { year: "2013", redDelicious: "06", mcintosh: "11", oranges: "9", pears: "4" },
  { year: "2014", redDelicious: "10", mcintosh: "13", oranges: "9", pears: "5" },
  { year: "2015", redDelicious: "16", mcintosh: "19", oranges: "6", pears: "9" },
  { year: "2016", redDelicious: "19", mcintosh: "17", oranges: "5", pears: "7" },
];
