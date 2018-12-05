//alert("pasyo");
//var base_url="http://mahilapratinidhi.naxa.com.np";
var base_url="http://localhost:8000";

//according to the tab pressed, call api , accordingly determine the no of checkbox app that needs to be called
$(".dataVariable").on("click",function(){

  var variable = $(this).text().toLowerCase().replace(" ","_");
  alert(variable)

  $.get(base_url+'/api/'+ variable +'/',function(data){

    ReactDOM.render(
      <div>
      <ChartBox data_pass={[{'title':variable,'data-type':'0','data':data['total']}]} />

      </div>,
      document.getElementById("react-container")
    )
 });


});

//

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


//format the data from api according to need
