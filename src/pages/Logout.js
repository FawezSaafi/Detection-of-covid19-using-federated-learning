import './logout.css';
import React, {useState} from 'react';

import {BrowserRouter as Router, Route, Routes, Link, NavLink, Switch} from "react-router-dom";

import profile from "./../image/lung2.jpg";
import email from "./../image/email.jpg";
import pass from "./../image/pass.png";
// import Signup from 'src/pages/Signup';

function Logout() {
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
    <div className="main">
     <div className="sub-main">
       <div>
         <div className="imgs">
           <div className="container-image">
             <img src={profile} alt="profile" className="profile"/>
           </div>
         </div>
         <div>
           <h3 className='title2'>Sign in</h3>
           <form>
           <div>
             <img src={email} alt="email" className="email"/>
             <input type="text" placeholder="email" className="name" name="email" value={values.email} onChange={handleChange}/>
           </div>
           
           <div className="second-input">
             <img src={pass} alt="pass" className="email"/>
             <input type="password" placeholder="password" className="name" name="password" value={values.password} onChange={handleChange}/>
           </div> 
           
          <div className="login-button">
          <button className='submit' ><a href="/newone">Sign in</a></button>
          </div>
          </form>
           
            <p className="link">
           <Router>
              <a href="#">Forgot password ?</a> Or <a href="/signup">SignUp</a>
            </Router>
            </p>
           
 
         </div>
       </div>
       

     </div>
    </div>
  )
}

export default Logout;