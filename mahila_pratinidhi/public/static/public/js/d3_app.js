class ChartBox extends React.Component {
  constructor(props){
    super(props);
    this.state ={
      checked : true
    };
    this.handleClick = this.handleClick.bind(this)
  }



handleClick= function(e){

var needed = e.target;
console.log(needed);
$("#d3modal").show();
var d3png = document.getElementById("d3png");
var d3csv = document.getElementById("d3csv");
d3csv.onclick = ()=>{
 var items = (this.props.data_pass[0]['data']);
 const replacer = (key, value) => value === null ? '' : value // specify how you want to handle null values here
 const header = Object.keys(items[4])
 var csv = items.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','))
 csv.unshift(header.join(','))
 csv = csv.join('\r\n')
 console.log("csv",csv);
 var filename =  'export.csv';
if (!csv.match(/^data:text\/csv/i)) {
             csv = 'data:text/csv;charset=utf-8,' + csv;
         }
         var datacsv = encodeURI(csv);
         var d3link = document.createElement('a');
         d3link.setAttribute('href', datacsv);
         d3link.setAttribute('download', filename);
        document.body.appendChild(d3link);
         d3link.click();
        document.body.removeChild(d3link);




}

d3png.onclick = function(){
  var s = new XMLSerializer().serializeToString($("svg")[0]);
  var encodedData = window.btoa(s);
  console.log(encodedData);
  saveSvgAsPng($(needed).closest(".row").find("svg")[0], "diagram.png",{backgroundColor:"hsl(50, 33%, 25%)",scale:"1"});

}

};



render (){
      let bar;
      var base_url="https://mahilapratinidhi.naxa.com.np";
      //var base_url="http://localhost:8000";
      switch (this.props.data_pass[0]['dataName']){

        case "total":
        var key_no= 0;
          break;

        case "provincial":
        var key_no= 1;

        break;

        case "vs":
        var key_no= 2;
        break;

        case "party":
        var key_no= 3;
        break;


      }






      const fb_link = base_url+"/visualize/" + this.props.data_pass[0].title.replace(" ","_") + "/"+ key_no
      const fb_href = "https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fmahilapratinidhi.naxa.com.np%2Fvisualize%2F"+ this.props.data_pass[0].title.replace(" ","_") + "%2F"+key_no+"&amp;src=sdkpreparse"
      const twitter_href= "https://twitter.com/intent/tweet?url=https://mahilapratinidhi.naxa.com.np/visualize/" + this.props.data_pass[0].title.replace(" ","_") + "/"+key_no ;


      if(this.props.data_pass[0]['data-type']=="stacked"){
        bar = <StackedChart data={[{'data':this.props.data_pass[0]['data'],'ind':this.props.data_pass[0]['ind'],'dataName':this.props.data_pass[0]['dataName']}]}  />;
      }

      else if(this.props.data_pass[0]['data-type']=="bar"){
        bar = <SimpleBar data={[{'data':this.props.data_pass[0]['data'],'dataName':this.props.data_pass[0]['dataName']}]}  />;
      }


      else if(this.props.data_pass[0]['data-type']=="hbar"){
              bar = <HBar data={[{'data':this.props.data_pass[0]['data'],'dataName':this.props.data_pass[0]['dataName']}]}  />;
            }

    else if(this.props.data_pass[0]['data-type']=="kernel"){
                    bar = <Kernel data={[{'data':this.props.data_pass[0]['data'],'dataName':this.props.data_pass[0]['dataName']}]}  />;
                  }

    else if(this.props.data_pass[0]['data-type']=="hstacked"){

                                  bar = <HStackedChart data={[{'data':this.props.data_pass[0]['data'],'dataName':this.props.data_pass[0]['dataName']}]}  />;
                                }

        else{

          bar ="No Visualization"

          }


          var {content}=this.props.data_pass[0];

  return (
        <div>
    <div className="graphItem" > <div className="row">

    <div className="col-md-4">  <p className="gheader"> {this.props.data_pass[0].title} - {this.props.data_pass[0]['dataName']} </p> <p
    className="gtext"> {content} </p> <div className="icons">

<div style={{display:'inline'}} class="fb-share-button"
  data-href={fb_link}
  data-layout="button_count" data-size="small" data-mobile-iframe="true">
  <a target="_blank"
   href={fb_href}
  class="fb-xfbml-parse-ignore"><i className="fa fa-facebook-f"></i>
  </a>
</div>

<a class="twitter-share-button"
  href={twitter_href}
  data-text= "Mahila pratinidhi in data">
  <i className="fa
  fa-twitter"></i></a>


    <span className="buttons" onClick={(e)=>this.handleClick(e)}> <i className="fa fa-download"></i> </span>
    <a href="#"> <i className="fa fa-share-alt" style={{display:"none"}}></i> </a> </div> </div>

    <div className="col-md-8 graphHolder">{bar}</div>

    </div> </div>
    </div>
      )
    };

}
