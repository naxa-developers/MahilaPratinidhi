class ChartBox extends React.Component {
  constructor(props){
    super(props);
    this.state ={
      checked : true
    };
    this.handleCheck = this.handleCheck.bind(this)
  }


  handleCheck= () => this.setState({checked : !this.state.checked});




    render (){
      var msg="checked";
      let bar;
      if(this.props.data_pass[0]['data-type']=="1"){
        bar = <StackedChart data={this.props.data_pass[0]['data']} />;
      }

      else if(this.props.data_pass[0]['data-type']=="0"){
        bar = <SimpleBar data={this.props.data_pass[0]['data']} />;
      }

      console.log("render",this.props.data_pass[0]['data'])



  return (
        <div>
    <div className="graphItem" > <div className="row"> <div
    className="col-md-5"> <p className="gheader"> {this.props.data_pass[0].title}  </p> <p
    className="gtext"> Lorem ipsum dolor sit amet, consectetur adipiscing
    elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Consequat ac felis donec et odio. Natoque penatibus et magnis dis
    parturient montes nascetur </p> <div className="icons"> <a href=""> <i
    className="fa fa-facebook-f"></i> </a> <a href=""> <i className="fa
    fa-twitter"></i> </a> <a href=""> <i className="fa fa-linkedin-in"></i>
    </a> <a className="l5" href=""> <i className="fa fa-download"></i> </a>
    <a href=""> <i className="fa fa-share-alt"></i> </a> </div> </div> <div
    className="col-md-7 graphHolder">

      {bar}

    </div></div> </div>
    </div>
      )
    };

}
