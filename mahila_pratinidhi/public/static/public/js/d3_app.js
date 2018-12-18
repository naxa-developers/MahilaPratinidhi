class ChartBox extends React.Component {
  constructor(props){
    super(props);
    this.state ={
      checked : true
    };
    this.handleClick = this.handleClick.bind(this)
  }



handleClick= function(e){

  saveSvgAsPng($(e.target).closest(".row").find("svg")[0], "diagram.png",{backgroundColor:"hsl(50, 33%, 25%)",scale:1});
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

        else{

          bar ="No Visualization"

          }






  return (
        <div>
    <div className="graphItem" > <div className="row">

    <div className="col-md-4">  <p className="gheader"> {this.props.data_pass[0].title}  </p> <p
    className="gtext"> Lorem ipsum dolor sit amet, consectetur adipiscing
    elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Consequat ac felis donec et odio. Natoque penatibus et magnis dis
    parturient montes nascetur </p> <div className="icons"> <a href="#"> <i
    className="fa fa-facebook-f"></i> </a> <a href="#"> <i className="fa
    fa-twitter"></i> </a> <a href="#"> <i className="fa fa-linkedin-in"></i>
    </a> <span className="buttons" onClick={(e)=>this.handleClick(e)}> <i className="fa fa-download"></i> </span>
    <a href="#"> <i className="fa fa-share-alt"></i> </a> </div> </div>
    <div className="col-md-8 graphHolder">{bar}</div>

    </div> </div>
    </div>
      )
    };

}
