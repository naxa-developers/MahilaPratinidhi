//alert("pasyo");
var base_url="http://mahilapratinidhi.naxa.com.np";
//var base_url="http://localhost:8000";

//according to the tab pressed, call api , accordingly determine the no of checkbox app that needs to be called
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


const sample = [ { language: 'Rust', value: 78.9, color: '#000000' }, {
language: 'Kotlin', value: 75.1, color: '#00a2ee' }, { language: 'Python',
value: 68.0, color: '#fbcb39' }, { language: 'TypeScript', value: 67.0, color:
'#007bc8' }, { language: 'Go', value: 65.6, color: '#65cedb' }, { language:
'Swift', value: 65.1, color: '#ff6e52' }, { language: 'JavaScript', value: 61.9,
color: '#f9de3f' }, { language: 'C#', value: 60.4, color: '#5d2f8e' }, {
language: 'F#', value: 59.6, color: '#008fc9' }, { language: 'Clojure', value:
59.6, color: '#507dca' } ];

//
// $.get(base_url+'/api/ethnicity/',function(data){
// });

var datause= {"total_ethnicity":
                        [ { "caste": "", "total": "1" }, { "caste": "Dalit", "total":
                        "35" }, { "caste": "Indigenous", "total": "97" }, { "caste": "Khas Arya",
                        "total": "74" }, { "caste": "Madhesi", "total": "45" }, { "caste": "Muslim",
                        "total": "9" }, { "caste": "Others", "total": "7" }, { "caste": "Tharu",
                        "total": "11" } ],
    "party_ethnicity": [
        {
            "caste": "",
            "": 2,
            "Bebeksheel Sajha Party": 1,
            "Federal Socialist Forum, Nepal": 18,
            "Naya Shakti Party, Nepal": 1,
            "Nepal Communist Party": 170,
            "Nepali Congress": 59,
            "Nepal Workers Peasants Party": 1,
            "Om Sangrami": 1,
            "Others": 1,
            "Rastriya Janamorcha, Nepal": 2,
            "Rastriya Janata Party": 1,
            "Rastriya Janata Party Nepal": 17,
            "Rastriya Prajatantra Party": 3,
            "Rastriya Prajatantra Party(Prajatantrik)": 1,
            "Rastriya Janamorcha": 1
        },
        {
            "caste": "Indigenous",
            "": 2,
            "Bebeksheel Sajha Party": 1,
            "Federal Socialist Forum, Nepal": 3,
            "Naya Shakti Party, Nepal": 1,
            "Nepal Communist Party": 63,
            "Nepali Congress": 20,
            "Nepal Workers Peasants Party": 1,
            "Om Sangrami": 1,
            "Others": 1,
            "Rastriya Janamorcha, Nepal": 1,
            "Rastriya Prajatantra Party": 1,
            "Rastriya Prajatantra Party(Prajatantrik)": 1,
            "Rastriya Janata Party Nepal": 1
        },
        {
            "caste": "Others",
            "Nepali Congress": 2,
            "Rastriya Janata Party Nepal": 1,
            "Rastriya Prajatantra Party": 1,
            "Federal Socialist Forum, Nepal": 1,
            "Nepal Communist Party": 2
        },
        {
            "caste": "Muslim",
            "Federal Socialist Forum, Nepal": 2,
            "Nepal Communist Party": 6,
            "Nepali Congress": 1
        },
        {
            "caste": "Dalit",
            "Federal Socialist Forum, Nepal": 2,
            "Nepal Communist Party": 22,
            "Nepali Congress": 11
        },
        {
            "caste": "Madhesi",
            "Federal Socialist Forum, Nepal": 8,
            "Nepal Communist Party": 16,
            "Nepali Congress": 8,
            "Rastriya Janata Party Nepal": 13
        },
        {
            "caste": "Tharu",
            "Nepal Communist Party": 9,
            "Nepali Congress": 2
        },
        {
            "caste": "Khas Arya",
            "Federal Socialist Forum, Nepal": 2,
            "Nepal Communist Party": 51,
            "Nepali Congress": 15,
            "Rastriya Janamorcha, Nepal": 1,
            "Rastriya Janata Party": 1,
            "Rastriya Prajatantra Party": 1,
            "Rastriya Janamorcha": 1,
            "Rastriya Janata Party Nepal": 2
        }
    ]}

  ReactDOM.render(
    <div>
    <ChartBox data_pass={[{'title':"Ethnictiy",'data-type':'0','data':datause['total_ethnicity']}]} />
    <ChartBox data_pass={[{'title':"Ethnictiy vs party",'data-type':'1','data':datause['party_ethnicity']}]} />
    </div>,
    document.getElementById("react-container")
  )

//format the data from api according to need
