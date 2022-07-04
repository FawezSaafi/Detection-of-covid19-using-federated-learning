// import logo from './logo.svg';
import React, { Component }  from 'react';
import './App.css';
import {BrowserRouter as Router, Route, Routes, Link, NavLink, Switch} from "react-router-dom";
// import Signin from './pages/Signin';
import Signup from './pages/Signup'
import Navbar from './components/Navbar';
import Server from './pages/server/Server';
// import Contributions from './pages/Contributions';
import Logout from './pages/Logout';
import newone from './pages/server/newone';
import Client from './pages/client/Client';

// import { RequireToken } from "./Auth";
import Signin from './pages/Signin';
// import Profile from "./Profile.js";
// import login from './login';

function App() {
  return (
    <Router>
    <div>
        
        <Switch> 
            <Route exact path="/signup" component={Signup}/> 
            <Route exact path="/" component={Signin}/>
            <Route exact path="/newone" component={newone}/>
            <Route exact path="/client" component={Client}/>
            {/*<Route exact path="/logout" component={Logout} /> */}
            {/* <Route exact path="/server" component={Server} /> */}

            {/* <Route path="/login" component = {login}/>
            <Route path="/profile" component = {Profile}/> */}
            
        </Switch>     
    </div>
</Router>
  

  );
}

export default App;