import React, { Component } from 'react';
import './client.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';
// import bgImage from '/Users/macbookair/front_v2/src/video/background.mp4';
import res from '/home/fawaz/Desktop/projet_react/src/image/resize.jpeg';
import { FaFileImage } from "react-icons/fa"
import { BsFillFileEarmarkZipFill } from "react-icons/bs";
import talan from "/home/fawaz/Desktop/projet_react/src/image/logo-talan.png";
import Signin from '../Signin';
import Popup2 from '../../components/Popup2.js';
// import { useHistory } from "react-router-dom";
import { FaBell } from "react-icons/fa";
//import Notif from '../../components/notif';

import 'reactjs-popup/dist/index.css';
//import Popup from '//home/fawaz/Desktop/projet_react/src/components/Popup2';


class Client extends Component {

  state = {
    notifs: [],
    selectedFile: null,
    test: "",
    isOpen: false,



  };



  onFileChange = event => {
    this.setState({ selectedFile: event.target.files[0] });
  };

  onFileUpload = async () => {
    document.getElementById("selectedFile").click()
    const url = 'http://127.0.0.1:8001/predictCovid';
    const formData = new FormData();
    formData.append('file', this.state.selectedFile);
    // formData.append('fileName', file.name);
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    };
    let x
    await axios.post(url, formData, config).then((response) => {
      console.log(response.data);

      // this.setState({ test : response.data});
      x = response.data
    });
    this.setState({ test: x });
    console.log(this.state.test);
  };

  onAccept = async (datenotif, idclient) => {
    console.log("client", datenotif)
    let data = { client_id: idclient, notif_date: datenotif }
    const url = 'http://127.0.0.1:8001/clientAccept';
    console.log(data)
    await axios.put(url, data).then((response) => {
      console.log("response put ", response.data);

    }).catch(err => {
      console.log("error", err);
    });
    toast('Your participation is confirmed !');
  }
  onDecline = async (datenotif, idclient) => {
    console.log("client", datenotif)
    let data = { client_id: idclient, notif_date: datenotif }
    const url = 'http://127.0.0.1:8001/clientDecline';
    console.log(data)
    await axios.put(url, data).then((response) => {
      console.log("response put ", response.data);

    }).catch(err => {
      console.log("error", err);
    });
    toast('Your are not going to participate in this session !');
  }


  getNotif = async () => {
    // this.setState({notifs:[this.state.notifs,...[]]})
    let tab = []
    await axios.get("http://127.0.0.1:8001/selectNotif").then(
      (res) => {
        tab = res.data;
        console.log("tab notif", res)
        this.setState({ notifs: [this.state.notifs, ...tab] })
      })
      .catch(error => { console.log(error) });

    console.log("notifs", this.state.notifs)
    return tab;
  }


  togglePopup = () => {
    this.setState({ isOpen: !this.state.isOpen });
    // this.setState({notifs: []}) 
  }

  openPopUp = () => {
    this.togglePopup();
    this.getNotif();
  }


  onFileUploadzip = () => {
    document.getElementById("selectedFileZip").click()
    const url = 'http://127.0.0.1:8001/Contribute';
    const formData = new FormData();
    formData.append('file', this.state.selectedFile);
    // formData.append('fileName', file.name);
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    };
    axios.post(url, formData, config).then((response) => {
      console.log(response.data);
    });

  };


  render() {
    return (
      <div>
        {/* <video autoPlay loop muted >
   <source src={bgImage} type='video/mp4' />
   </video> */}

        <img src={res} className="img1"></img>
        <img src={talan} className="img2"></img>
        <button className='but5' onClick={this.openPopUp.bind(this)}>

          <FaBell style={{ marginRight: "6px", marginBottom: "-2px" }}></FaBell>
          Notifications
        </button>

        {this.state.isOpen &&
          <Popup2
            content={<table className='table'>
              {/* {console.log("otside",this.state.notifs[1])} */}
              <tr>
                <th className='th1'>Centeral organization</th>
                {/* <th className='th1'>State</th> */}
                <th className='th1'>Start date</th>
                <th className='th1'>Participate</th>
              </tr>
              {this.state.notifs.slice(1,).map((item, index) => {
                return <tr key={index}>
                  <td>{item[0]}</td>
                  <td>{item[2]}</td>
                  <td>
                    {/* onClick={this.onAccept(item[2],item[3])} */}
                    <button style={{ background: "green", color: "white", height: "40px", width: "40px", fontSize: "15px" }} onClick={() => { this.onAccept(item[2], item[3]) }}>Yes</button>
                    <button style={{ background: "#d7363c", color: "white", height: "40px", width: "40px", marginLeft: "6px", fontSize: "15px" }}onClick={() => { this.onDecline(item[2], item[3]) }}>No</button>
                  </td>
                </tr>
              })
              }
               <ToastContainer />
            </table>}
            handleClose={this.togglePopup.bind(this)}
          />}





        <div className='card-container1'>

          <center className='textt' style={{ color: "white", marginTop: "60px" }}>Covid-19 Detection</center>
          {/* <hr className='hr'></hr> */}
          {/* #D7DBDD" */}
          <center className='textt1' style={{ color: "white", marginBottom: "25px" }}>Welcome to our application</center>
          {/* <button className='but3' onClick={this.onFileUploadzip.bind(this)}><BsFillFileEarmarkZipFill color="#CD6155" style={{ marginRight: "20px", marginLeft: "-100px", width: "30px", height: "30px", fontSize: "x-large" }}> </BsFillFileEarmarkZipFill>Contribute with Data</button>*/}
          <button className='but3' onClick={this.onFileUploadzip.bind(this)}><BsFillFileEarmarkZipFill color="#CD6155" style={{ marginRight: "5px" }}> </BsFillFileEarmarkZipFill>Contribute with Data</button>

          <input className='input1' id="selectedFileZip" type="file" style={{ display: "none" }} onChange={this.onFileChange} accept='.zip, .rar' />
          <button className='but3' onClick={this.onFileUpload.bind(this)}><FaFileImage color="#CD6155" style={{ marginRight: "5px" }}> </FaFileImage>Covid-19 prediction</button>
          <input className='input2' id="selectedFile" type="file" style={{ display: "none" }} onChange={this.onFileChange} />

          <p style={{ marginLeft: "40%", color: "white" }}>{this.state.test}</p>



          <button className='but4'>
            <a href="/" style={{ marginLeft: "10%" }}>
              Logout
            </a>
          </button>
          {/* <button className='but3' onClick={this.uploadfiles.bind(this)}>upload</button>
        <input id="selectedFile" type="file" style={{display:"none"}} onChange={this.onFileChange}/> */}


        </div>
      </div>

    )
  }
}
export default Client;