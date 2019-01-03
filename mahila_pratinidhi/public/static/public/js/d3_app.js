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
  saveSvgAsPng($(needed).closest(".row").find("svg")[0], "diagram.png",{backgroundColor:"hsl(50, 33%, 25%)",scale:1});

}

};



render (){
      let bar;


      if(this.props.data_pass[0]['data-type']=="stacked"){
        bar = <StackedChart data={[{'data':this.props.data_pass[0]['data'],'dataName':this.props.data_pass[0]['dataName']}]}  />;
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

    <div className="col-md-4">  <p className="gheader"> {this.props.data_pass[0].title}  </p> <p
    className="gtext"> {content} </p> <div className="icons">
    <a target="_blank"
    href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fmahilapratinidhi.naxa.com.np%2Fvisualize%2F&amp;src=sdkpreparse" class="fb-xfbml-parse-ignore">
    <div style={{display:'inline'}} className="fb-share-button"
    data-href="https://mahilapratinidhi.naxa.com.np/visualize/"
    data-layout="button_count" data-size="small"
    data-mobile-iframe="true">
    <i className="fa fa-facebook-f"></i>
    </div></a>
    <a href="#"> <i className="fa
    fa-twitter"></i> </a> <a href="#"> <i className="fa fa-linkedin-in"></i>
    </a> <span className="buttons" onClick={(e)=>this.handleClick(e)}> <i className="fa fa-download"></i> </span>
    <a href="#"> <i className="fa fa-share-alt"></i> </a> </div> </div>
    <div className="col-md-8 graphHolder">{bar}</div>

    </div> </div>
    </div>
      )
    };

}
