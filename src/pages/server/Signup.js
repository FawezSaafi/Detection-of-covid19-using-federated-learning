import './signup.css';
import React, { Component }  from 'react';
/*import {BrowserRouter as Router, Route, Link, NavLink, Switch} from "react-router-dom";*/


// import profile from "./../image/lung2.jpg";
import institution from "./../image/institution.png";
import email from "./../image/mail.png";
import pass from "./../image/pass.png";
import { MdPermIdentity } from "react-icons/md";
import res from '/Users/macbookair/front_v2/src/image/resize.jpeg';
import { MdEmail } from "react-icons/md";
import { MdOutlineLock } from "react-icons/md";
import { MdOutlineDomain } from "react-icons/md";


function SignUp() {
  return (
    <div>
    {/* // <div className="main1"> */}
    <img src={res} className="img5"></img>
     <div className="sub-main1">
     {/* <MdPermIdentity className='profile'></MdPermIdentity> */}
       <div>
         <div className="imgs1">
           <div className="container-image1">
             {/* <img src={profile} alt="profile" className="profile1"/> */}
             <MdPermIdentity className='profile'></MdPermIdentity>

           </div>


         </div>
         <div>
           <h3 className='title'>Sign Up</h3>
           <div>
             {/* <img src={institution} alt="email" className="email1"/> */}
             <MdOutlineDomain className='email1'></MdOutlineDomain>
             <input type="text" placeholder="institution name" className="name1"/>
           </div>
           
           <div className="second">
             {/* <img src={email} alt="pass" className="email1"/> */}
             <MdEmail className='email1'></MdEmail>
             <input type="text" placeholder="email" className="name1"/>
           </div>
           
           <div className="second">
             {/* <img src={pass} alt="pass" className="pass1"/> */}
             <MdOutlineLock className='pass1'></MdOutlineLock>
             <input type="text" placeholder="password" className="name1"/>
           </div>
           
           <div className="second">
             {/* <img src={pass} alt="pass" className="pass1"/> */}
             <MdOutlineLock className='pass1'></MdOutlineLock>
             <input type="text" placeholder="verify password" className="name1"/>
           </div>
           
          <div className="login-button1">
          <button className='button1'><a href='/client' className='signup'>Sign up</a></button>
          </div>
          
          <p className='link'>
          <a href="/" style={{marginLeft:"45%"}}>Back</a>
          </p>
           
           
           
 
         </div>
       </div>
       

     </div>
    </div>
  );
}

export default SignUp;