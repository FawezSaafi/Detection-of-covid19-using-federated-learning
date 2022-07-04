import React, { Component }  from 'react';
import './newone.css';
import {BrowserRouter as Router, Route, Routes, Link, NavLink, Switch} from "react-router-dom";

import Navbar from '/home/fawaz/Desktop/projet_react/src/components/Navbar';
import Server from '/home/fawaz/Desktop/projet_react/src/pages/server/Server';
// import Contributions from '../pages/Contributions';
// import Logout from '/home/fawaz/Desktop/projet_react/src/pages/Logout.js';
import Signin from '../Signin';
// import page from './page';



function newone() {
  return (
   
    <Router>
      <Switch>
            <Route exact path="/" component={Signin}/>
        <div>
          <Navbar />
          <Route exact path="/newone" component={Server}/>
          {/*<Route exact path="/contributions" component={Contributions}/> */}
            <Route exact path="/server" component={Server}/>
        </div>
      </Switch>
    </Router>
  
   
  )
}

export default newone;