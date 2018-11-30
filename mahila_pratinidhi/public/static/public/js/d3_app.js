class ChartBox extends React.Component {
  constructor(props){
    super(props);
    this.state ={
      checked : true
    };
    this.handleCheck = this.handleCheck.bind(this)
  }


  handleCheck= () => this.setState({checked : !this.state.checked});

  draw_d3 = function (data){
    }


    render (){
      var msg="checked";
       if (this.state.checked){
         msg= "yeschecked";
       }
       else{
        msg="unchecked";
       }

       if(this.props.data_pass[0].data){
         this.draw_d3(this.props.data_pass[0].data);
       }
  return (
        <div>
    <div className="graphItem"> <div className="row"> <div
    className="col-md-6"> <p className="gheader"> {this.props.data_pass[0].title}  </p> <p
    className="gtext"> Lorem ipsum dolor sit amet, consectetur adipiscing
    elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Consequat ac felis donec et odio. Natoque penatibus et magnis dis
    parturient montes nascetur </p> <div className="icons"> <a href=""> <i
    className="fa fa-facebook-f"></i> </a> <a href=""> <i className="fa
    fa-twitter"></i> </a> <a href=""> <i className="fa fa-linkedin-in"></i>
    </a> <a className="l5" href=""> <i className="fa fa-download"></i> </a>
    <a href=""> <i className="fa fa-share-alt"></i> </a> </div> </div> <div
    className="col-md-6 graphHolder">
    <StackedChart data={this.props.data_pass[0].data} />
    </div></div> </div>
    </div>
      )
    };

}
