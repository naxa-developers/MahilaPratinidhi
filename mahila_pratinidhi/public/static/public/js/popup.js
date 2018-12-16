
class Popup extends React.Component {
  constructor( props){
    super(props);
    this.state={

    }

  }


render(){
  return(
<div>
    <div className="">
     <ul className="" style={{listStyleType:"none"}}>
     <li id="national-all"> <img src="public/image/city-hall.svg" alt="" /> <div className="">NATIONAL
    ASSEMBLY </div>
    <ul style={{listStyleType:"none"}}>
    <li>mahila pratinidhi 1 </li>
    <li> mahila pratinidhi 1</li>
    <li> mahila pratinidhi 1</li>
    </ul>
    </li>
    <li id="federal-all"> <img src="public/image/elementary-school.svg" alt="" /> <div className="">FEDERAL
    PARLIAMENT </div><ul style={{listStyleType:"none"}}>
    <li>mahila pratinidhi 1 </li>
    <li> mahila pratinidhi 1</li>
    <li> mahila pratinidhi 1</li>
    </ul> </li>
    <li id="provincial-all"> <img src="public/image/parliament.svg" alt="" /> <div className="">PROVINCIAL ASSEMBLY
    </div><ul style={{listStyleType:"none"}}>
    <li>mahila pratinidhi 1 </li>
    <li> mahila pratinidhi 1</li>
    <li> mahila pratinidhi 1</li>
    </ul> </li>
     </ul>
     </div>

    </div>

  )
}

}
