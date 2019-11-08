import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router } from 'react-router-dom'
import Home from './Home';
import Browse from './Browse';
import Book from './Book';
import Log from './Log';


const routing = (
    <Router>
        <div>
            <Route exact path="/" component={Home} />
            {/* <Route path="/register" component={Register} />
            <Route path="/login" component={Login} />
            <Route path="/logout" component={Logout} />
            <Route path="/scrape" component={Scrape} />*/}
            <Route path="/browse" component={Browse} />
            {/* <Route path="/searchbyasin" component={Search} /> */}
            <Route path='/books/:bookid' component={Book} />
            <Route path='/log' component={Log} />
        </div>
    </Router>
)

ReactDOM.render(routing, document.getElementById('root'));

