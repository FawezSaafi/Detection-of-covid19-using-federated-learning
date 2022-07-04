import React, {useState,useEffect} from 'react'
import {ToastContainer, toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
// import Card from "react-bootstrap/Card";
// import Navbar from 'src/components/Navbar';
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
// import * as AiIcons from 'react-icons/ai';
import './server.css'
// import Button from 'react-bootstrap/Button'
// import Modal from 'react-modal';
import { FaPlay } from "react-icons/fa";
// import { GlobalStyle } from '../globalStyles';
import swal from 'sweetalert';


import 'reactjs-popup/dist/index.css';
import Popup from '/home/fawaz/Desktop/projet_react/src/components/Popup';
import axios from 'axios';
import { render } from '@testing-library/react';


function Server() {
    const [isOpen, setIsOpen] = useState(false);
 
    const togglePopup = () => {
    setIsOpen(!isOpen);

  }
  const [round, setRound] = useState(0);
  const [client, setClient] = useState(1);
  async function launch (){
  
    let data = {num_rounds: round,ipaddress:'127.0.0.1', port:8080,resume:true,num_clients:client}
    const url = 'http://127.0.0.1:8000/launchFL';
    console.log(data);
   
    await axios.post(url,data).then((response) => {
        console.log(response.data);
        
      }).catch(err=>{
        console.log("error",err);
      });

      };
      const [hist, setHist] = useState([]);

      const getHist = async () => {
        // this.setState({notifs:[this.state.notifs,...[]]})
        let tab = []
        await axios.get("http://127.0.0.1:8000/selectHist").then(
            (res )=> {
                tab = res.data;
              console.log("tab hist",res)
              // setHist({hist:[hist,...tab]})
              setHist(tab)
            })
        .catch(error => {console.log(error)});
       
        console.log("hists",hist)
        return tab;
      }
      useEffect(() => {
        getHist();
      }, []); 
  return (
<div className='card-container'>
<table>
        <tr>
          <th><h3  className='text'>Training Sessions</h3></th>
          <th>
       
  <button onClick={togglePopup} className='but'><FaPlay color="#132c3d" className='launch' ></FaPlay></button>
    {isOpen && <Popup
      content={<>
        <b>Start New Session</b>
        <hr></hr>
        <h5 className='number'>Number of rounds</h5>
        <form className='form'>
          <div class="form-group">
            <input type="number" class="form-control" id='num' className='input' placeholder="0" onChange={(e)=>setRound(e.target.value)} />
            {/* <input type="number" class="form-control" className='input'  name="num_rounds" id='num' onChange={handleAddFormChange} placeholder="0" /> */}
            <h5 className='number' style={{marginBottom:"3%"}}>Number of clients</h5>
            <input type="number" class="form-control" id='num' className='input' placeholder="0" onChange={(e)=>setClient(e.target.value)} style={{marginTop:"-20%"}}/>

          </div>
        </form>
        <hr></hr>
        {/*<button className='but1' >Close</button>*/}
        <button className='but2' onClick={()=>{launch()}} >Submit</button>
          </>}
      handleClose={togglePopup}
    />}
    <ToastContainer />
 

</th>
         
        </tr>
</table>

 <hr className='line'>
 </hr>
 
 <div className='app'>
 <table className='table'>
   <thead>
 <tr>
 <th className='th1'>Session date </th>
 <th className='th1'>Nb. of rounds</th>
 <th className='th1'>Accuracy</th>
 </tr>
 </thead>
 <tbody>
   {
     hist.map((item, index)=>{ return <tr key={index}>
      <td>{item[1]}</td>
      <td>{item[2]}</td>
      <td>{item[3]}</td>
     </tr>})
   }
   
 </tbody>
 </table>
 </div>

 
 
 
</div>
  )
} 

export default Server;