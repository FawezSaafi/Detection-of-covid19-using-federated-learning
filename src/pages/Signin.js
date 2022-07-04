import './signin.css';
import React, {useState} from 'react';

import {BrowserRouter as Router, Route, Routes, Link, NavLink, Switch} from "react-router-dom";

import profile from "./../image/lung2.jpg";
import email from "./../image/email.jpg";
import pass from "./../image/pass.png";
// import Signup from 'src/pages/Signup';

import { MdMail } from "react-icons/md";
import { MdLock } from "react-icons/md";
import { MdPermIdentity } from "react-icons/md";
import res from '/home/fawaz/Desktop/projet_react/src/image/resize.jpeg';


export default function Signin() {
const [values, setValues] = useState({
  email: "",
  password: ""
});
const handleChange = (event)=>{
setValues({
...values,
[event.target.name]:event.target.value,
})
}
const handleFormSubmit = (event) => {
event.preventDefault();
}
  return (
  <div>
    {/* <div className="main"> */}
        <img src={res} className="img4"></img>

     <div className="sub-main">

       <div>
         <div className="imgs">
           <div className="container-image">
             {/* <img src={profile} alt="profile" className="profile"/> */}
             <MdPermIdentity className='profile'></MdPermIdentity>
           </div>
         </div>
         <div>
           <h3 className='title1'>Sign in</h3>
           <form>
           <div>
             {/* <img src={email} alt="email" className="email"/> */}
             <MdMail className='email'></MdMail>
             <input type="text" placeholder="email" className="name" name="email" value={values.email} onChange={handleChange}/>
           </div>
           
           <div className="second-input">
             {/* <img src={pass} alt="pass" className="email"/> */}
             <MdLock className='password'></MdLock>
             <input type="password" placeholder="password" className="name" name="password" value={values.password} onChange={handleChange}/>
           </div> 
           
          <div className="login-button">
          <button className='submit' ><a href="/newone" className='signin'>Sign in</a></button>
          </div>
          </form>
           
            <p className="link">
           <Router>
              <a href="#">Forgot password ?</a> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;  <a href="/signup">SignUp</a>
            </Router>
            </p>
           
 
         </div>
       </div>
       

     </div>
    </div>
  );
}
