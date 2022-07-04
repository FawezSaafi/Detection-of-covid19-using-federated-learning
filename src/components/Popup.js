import React from "react";
import './Popup.css'
const Popup = props => {
  return (
    <div className="popup-box">
      <div className="box">
        {/*<span className="close-icon" onClick={props.handleClose}>x</span>*/}
        {props.content}
        <button onClick={props.handleClose} className='but1'>close</button>
      </div>
    </div>
  );
};
 
export default Popup;